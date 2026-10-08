"""Credentials: which ones a workflow needs, how to get each one, and (optionally) create them on an
instance from the user's secrets file and wire them into the workflow.

autokit creds flow.json                       → table: node · credential types · where to get it
autokit creds flow.json --target local --apply   → create missing credentials listed in the secrets file
                                                (credentials.<name> = {"type": "...", "data": {...}}) and put
                                                their ids into the workflow nodes (flow.json is updated)
The USER creates accounts, apps and keys (references/credentials.md has the click-by-click steps);
the AI never types passwords or keys into websites, and never prints secret values.
"""
from __future__ import annotations

import json
from pathlib import Path

DOCS = "https://docs.n8n.io/integrations/builtin/credentials/"
HINTS = {
    "googleSheetsOAuth2Api": "google/oauth-single-service/", "gmailOAuth2": "google/oauth-single-service/", "googleApi": "google/service-account/",
    "googleDriveOAuth2Api": "google/oauth-single-service/", "googleCalendarOAuth2Api": "google/oauth-single-service/",
    "slackApi": "slack/", "slackOAuth2Api": "slack/", "telegramApi": "telegram/", "openAiApi": "openai/", "anthropicApi": "anthropic/",
    "googlePalmApi": "googleai/", "notionApi": "notion/", "airtableTokenApi": "airtable/", "hubspotAppToken": "hubspot/",
    "whatsAppApi": "whatsapp/", "discordBotApi": "discord/", "postgres": "postgres/", "mySql": "mysql/", "smtp": "send-email/",
    "httpHeaderAuth": "httpRequest/", "httpBearerAuth": "httpRequest/", "httpBasicAuth": "httpRequest/",
    "microsoftOutlookOAuth2Api": "microsoft/", "microsoftExcelOAuth2Api": "microsoft/", "stripeApi": "stripe/",
    "twilioApi": "twilio/", "trelloApi": "trello/", "githubApi": "github/", "jiraSoftwareCloudApi": "jira/",
}


def report(wf: dict, cat: dict, env, apply_target: str | None = None) -> int:
    from wfcheck import check
    res = check(wf, cat, env, sdk=False)
    need = res["credentials"]
    have = {n["name"]: n.get("credentials") for n in wf.get("nodes", []) if n.get("credentials")}
    if not need and not have:
        print("this workflow needs no credentials ✓")
        return 0
    print("Node → credential (choose ONE type per node) · how to get it")
    for nm, types in need.items():
        guide = next((DOCS + HINTS[t] for t in types if t in HINTS), DOCS)
        print(f"  ✗ {nm}: {' | '.join(types)}\n      steps: references/credentials.md · docs: {guide}")
    for nm, c in have.items():
        ok = all(isinstance(v, dict) and v.get("id") for v in c.values())
        print(f"  {'✓' if ok else '…'} {nm}: {', '.join(c.keys())}{'' if ok else ' (no id yet — create/select in n8n)'}")
    return 0


def apply(wf_path: Path, cat: dict, env, target: str) -> int:
    import n8napi
    wf = json.loads(wf_path.read_text())
    secrets = env.secrets().get("credentials") or {}
    if not secrets:
        p = env.ensure_secrets_template()
        print(f"no credentials in {p}. Add entries like  \"My OpenAI\": {{\"type\": \"openAiApi\", \"data\": {{\"apiKey\": \"…\"}}}}  "
              f"(the field names for a type: autokit creds-schema <type> --target {target})")
        return 1
    api = n8napi.Api(env.target(target))
    existing = {}
    try:
        for c in api.all("/credentials"):
            existing[(c.get("type"), c.get("name"))] = c.get("id")
    except SystemExit:
        pass
    by_type = {}
    for name, spec in secrets.items():
        key = (spec["type"], name)
        cid = existing.get(key)
        if not cid:
            r = api.req("POST", "/credentials", {"name": name, "type": spec["type"], "data": spec.get("data", {})})
            cid = r.get("id")
            print(f"created credential “{name}” ({spec['type']}) → {cid}")
        else:
            print(f"credential “{name}” ({spec['type']}) already on {target} → {cid}")
        by_type.setdefault(spec["type"], (cid, name))
    from wfcheck import check
    needs = check(wf, cat, env, sdk=False)["credentials"]      # only nodes that really need one
    changed = 0
    for n in wf.get("nodes", []):
        if n["name"] not in needs:
            continue
        for t in needs[n["name"]]:
            if t in by_type and not (n.get("credentials") or {}).get(t, {}).get("id"):
                cid, name = by_type[t]
                n.setdefault("credentials", {})[t] = {"id": cid, "name": name}
                changed += 1
                break
    wf_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"wired {changed} node credential(s) into {wf_path.name} — redeploy: autokit deploy {wf_path.name} --target {target}")
    return 0


def schema(env, target: str, ctype: str) -> int:
    import n8napi
    s = n8napi.credential_schema(env, target, ctype)
    print(json.dumps(s, indent=1)[:4000])
    return 0
