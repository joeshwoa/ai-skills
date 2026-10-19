"""Locate the n8n installation the toolkit drives (local CLI for building/validating/testing) and the
deployment targets (n8n instances reached through the public REST API).

Config: ~/.config/ai-skills/automation.json
{
  "n8n_dir": "~/.local/share/ai-skills/n8n",        # folder with node_modules/n8n (setup_n8n.sh makes it)
  "node": "~/.local/share/ai-skills/n8n/node/bin/node",
  "targets": {
    "local": {"url": "http://localhost:5678"},
    "cloud": {"url": "https://YOURNAME.app.n8n.cloud"}
  },
  "secrets_file": "~/.config/ai-skills/automation-secrets.json"
}
Secrets (the USER writes them; chmod 600; never printed): {"n8n_api_keys": {"local": "…", "cloud": "…"},
"credentials": {"<name>": {"type": "openAiApi", "data": {...}}}}
Environment overrides: AUTOKIT_N8N_DIR, AUTOKIT_NODE, N8N_API_KEY_<TARGET>.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

def _real_home() -> Path:
    h = Path.home()
    parts = h.parts
    if ".gemini" in parts and "users" in parts:
        idx = parts.index(".gemini")
        return Path(*parts[:idx])
    return h


REAL_HOME = _real_home()
CFG_PATH = REAL_HOME / ".config" / "ai-skills" / "automation.json"
DEFAULT_SECRETS = REAL_HOME / ".config" / "ai-skills" / "automation-secrets.json"
DEFAULT_DIR = REAL_HOME / ".local" / "share" / "ai-skills" / "n8n"
HERE = Path(__file__).resolve().parent


def _x(p) -> Path:
    s = str(p)
    if s.startswith("~/"):
        return REAL_HOME / s[2:]
    return Path(os.path.expanduser(s))


def load_cfg() -> dict:
    try:
        return json.loads(CFG_PATH.read_text())
    except Exception:
        return {}


def save_cfg(cfg: dict):
    CFG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CFG_PATH.write_text(json.dumps(cfg, indent=2))


class Env:
    def __init__(self):
        cfg = load_cfg()
        self.cfg = cfg
        cands = [os.environ.get("AUTOKIT_N8N_DIR"), cfg.get("n8n_dir"), str(DEFAULT_DIR), "/opt/n8n"]
        self.dir = None
        for c in cands:
            if c and (_x(c) / "node_modules" / "n8n" / "package.json").exists():
                self.dir = _x(c)
                break
        node_cands = [os.environ.get("AUTOKIT_NODE"), cfg.get("node"),
                      str(self.dir / "node" / "bin" / "node") if self.dir else None, "/opt/node24/bin/node", shutil.which("node")]
        self.node = next((str(_x(c)) for c in node_cands if c and _x(c).exists()), None)
        self.secrets_path = _x(cfg.get("secrets_file", DEFAULT_SECRETS))

    # ------------------------------------------------------------------ status
    @property
    def ok(self) -> bool:
        return bool(self.dir and self.node)

    def require(self):
        if not self.ok:
            raise SystemExit("n8n is not installed for the toolkit. Run:  bash scripts/setup_n8n.sh   "
                             "(installs n8n + Node 24 into ~/.local/share/ai-skills/n8n — asks first).")
        v = self.node_version()
        if v and v < 20:
            raise SystemExit(f"Node {v} is too old for n8n — run scripts/setup_n8n.sh (it adds a private Node 24).")

    def node_version(self) -> int | None:
        try:
            out = subprocess.run([self.node, "-v"], capture_output=True, text=True).stdout
            return int(re.match(r"v(\d+)", out).group(1))
        except Exception:
            return None

    @property
    def version(self) -> str:
        try:
            return json.loads((self.dir / "node_modules" / "n8n" / "package.json").read_text())["version"]
        except Exception:
            return "?"

    def js(self, script: str, *args, timeout=300, env=None) -> subprocess.CompletedProcess:
        e = dict(os.environ)
        e["NODE_PATH"] = str(self.dir / "node_modules")
        if env:
            e.update(env)
        return subprocess.run([self.node, str(HERE / "js" / script), str(self.dir), *map(str, args)],
                              capture_output=True, text=True, timeout=timeout, env=e)

    def n8n_cli(self, *args, user_folder: Path, timeout=300, extra_env=None) -> subprocess.CompletedProcess:
        e = dict(os.environ)
        e.update({"N8N_USER_FOLDER": str(user_folder), "N8N_DIAGNOSTICS_ENABLED": "false",
                  "N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS": "false", "N8N_LOG_LEVEL": "info", "N8N_LOG_OUTPUT": "console",
                  "N8N_VERSION_NOTIFICATIONS_ENABLED": "false", "N8N_PERSONALIZATION_ENABLED": "false",
                  "N8N_BLOCK_ENV_ACCESS_IN_NODE": "false", "NODE_PATH": str(self.dir / "node_modules"),
                  "PATH": str(Path(self.node).parent) + os.pathsep + e.get("PATH", "")})
        # a running n8n server (e.g. the local instance on 5678) owns the task-broker port 5679 —
        # give every CLI run its own free port so tests work next to it
        import socket
        with socket.socket() as sk:
            sk.bind(("127.0.0.1", 0))
            e["N8N_RUNNERS_BROKER_PORT"] = str(sk.getsockname()[1])
        if extra_env:
            e.update(extra_env)
        return subprocess.run([self.node, str(self.dir / "node_modules" / "n8n" / "bin" / "n8n"), *args],
                              capture_output=True, text=True, timeout=timeout, env=e)

    # ------------------------------------------------------------------ node definitions + catalog
    def ensure_defs(self) -> Path:
        self.require()
        stamp = self.dir / "node-defs" / ".autokit-version"
        if not stamp.exists() or stamp.read_text().strip() != self.version:
            r = self.js("gen_defs.js", timeout=600)
            if r.returncode:
                raise SystemExit("could not generate node definitions:\n" + r.stderr[-2000:])
            stamp.parent.mkdir(parents=True, exist_ok=True)
            stamp.write_text(self.version)
        return self.dir / "node-defs"

    def catalog(self) -> dict:
        self.require()
        cache = self.dir / "autokit-catalog.json"
        if cache.exists():
            try:
                c = json.loads(cache.read_text())
                if c.get("_version") == self.version:
                    return c["nodes"]
            except Exception:
                pass
        nodes = {}
        for pkg, prefix in (("n8n-nodes-base", "n8n-nodes-base"), ("@n8n/n8n-nodes-langchain", "@n8n/n8n-nodes-langchain")):
            f = self.dir / "node_modules" / pkg / "dist" / "types" / "nodes.json"
            if not f.exists():
                continue
            for d in json.loads(f.read_text()):
                name = d["name"] if "." in d["name"] else f"{prefix}.{d['name']}"
                vs = d["version"] if isinstance(d["version"], list) else [d["version"]]
                e = nodes.setdefault(name, {"displayName": d.get("displayName"), "versions": [], "defaultVersion": d.get("defaultVersion"),
                                            "group": d.get("group", []), "description": d.get("description", ""),
                                            "credentials": [], "categories": [], "props": {}, "inputs": d.get("inputs"),
                                            "outputs": d.get("outputs"), "webhook": False, "polling": False})
                e["versions"] = sorted(set(e["versions"] + vs))
                if d.get("defaultVersion"):
                    e["defaultVersion"] = d["defaultVersion"]
                for c in d.get("credentials") or []:
                    if c["name"] not in e["credentials"]:
                        e["credentials"].append(c["name"])
                cod = d.get("codex") or {}
                for c in cod.get("categories") or []:
                    if c not in e["categories"]:
                        e["categories"].append(c)
                if d.get("webhooks"):
                    e["webhook"] = True
                if d.get("polling"):
                    e["polling"] = True
                for v in vs:
                    e["props"][str(v)] = sorted({p["name"] for p in d.get("properties", [])})
        for e in nodes.values():
            if not e["defaultVersion"]:
                e["defaultVersion"] = e["versions"][-1]
        cache.write_text(json.dumps({"_version": self.version, "nodes": nodes}))
        return nodes

    # ------------------------------------------------------------------ targets & secrets
    def secrets(self) -> dict:
        try:
            return json.loads(self.secrets_path.read_text())
        except FileNotFoundError:
            return {}
        except Exception as e:
            raise SystemExit(f"secrets file {self.secrets_path} is not valid JSON: {e}")

    def ensure_secrets_template(self):
        p = self.secrets_path
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({"n8n_api_keys": {"local": "", "cloud": ""}, "credentials": {}}, indent=2))
            os.chmod(p, 0o600)
        return p

    def target(self, name: str) -> dict:
        t = (self.cfg.get("targets") or {}).get(name)
        if not t:
            if name == "local":
                t = {"url": "http://localhost:5678"}
            else:
                raise SystemExit(f"target '{name}' is not configured. Add it to {CFG_PATH} under \"targets\" "
                                 f"(e.g. {{\"{name}\": {{\"url\": \"https://you.app.n8n.cloud\"}}}}).")
        key = os.environ.get(f"N8N_API_KEY_{name.upper()}") or (self.secrets().get("n8n_api_keys") or {}).get(name)
        return {"name": name, "url": t["url"].rstrip("/"), "key": key or ""}
