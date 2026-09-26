#!/usr/bin/env node
/**
 * mcp_cli.mjs — generic one-shot MCP stdio client (shared by the devuniverse
 * and omnicinema skills; identical copy in each).
 *
 * Spawns an MCP stdio server, does the handshake, runs ONE request, prints
 * the result and exits. No MCP client registration, no long-lived process,
 * no duplicated logic — it only speaks the protocol to the real server.
 *
 * Usage:
 *   node mcp_cli.mjs [--json] <run-command...> -- <tool_name> ['<json-args>' | @args.json]
 *   node mcp_cli.mjs [--json] <run-command...> -- --list
 *
 *   --json   print the raw MCP result (content + structuredContent + isError).
 *            Default prints the human-readable text content only.
 *   @file    read the JSON arguments from a file (avoids shell-quoting trouble
 *            with long briefs, quotes, Arabic text …).
 *   --list   print every tool with its description and argument names.
 *
 * Exit: 0 ok · 1 tool returned isError · 2 usage/transport/handshake error.
 * Env:  MCP_CLI_TIMEOUT_MS (default 900000 = 15 min — renders can be slow).
 */
import { spawn } from "node:child_process";
import fs from "node:fs";
import readline from "node:readline";

function usageError(msg) {
  console.error(`mcp_cli.mjs: ${msg}`);
  console.error("Usage: node mcp_cli.mjs [--json] <run-command...> -- <tool_name> ['<json-args>'|@file] | --list");
  process.exit(2);
}

let args = process.argv.slice(2);
let raw = false;
if (args[0] === "--json") { raw = true; args = args.slice(1); }
const sep = args.indexOf("--");
if (sep <= 0 || sep === args.length - 1) usageError("expected: <run-command...> -- <tool_name> ['<json-args>']");
const runCommand = args.slice(0, sep);
const toolName = args[sep + 1];
const listMode = toolName === "--list";
let jsonArgsRaw = args[sep + 2] ?? "{}";
if (jsonArgsRaw.startsWith("@")) {
  try { jsonArgsRaw = fs.readFileSync(jsonArgsRaw.slice(1), "utf8"); }
  catch (e) { usageError(`cannot read args file ${jsonArgsRaw.slice(1)}: ${e.message}`); }
}
let toolArgs = {};
if (!listMode) {
  try { toolArgs = JSON.parse(jsonArgsRaw.trim() || "{}"); }
  catch (e) { usageError(`the json-args argument is not valid JSON: ${e.message}`); }
}

const TIMEOUT_MS = Number(process.env.MCP_CLI_TIMEOUT_MS || 900000);
const child = spawn(runCommand[0], runCommand.slice(1), { stdio: ["pipe", "pipe", "pipe"], env: process.env });
let stderrBuf = "";
child.stderr.on("data", (d) => { stderrBuf += d.toString(); if (stderrBuf.length > 200000) stderrBuf = stderrBuf.slice(-100000); });
const rl = readline.createInterface({ input: child.stdout, crlfDelay: Infinity });
let nextId = 1;
const pending = new Map();
const send = (o) => child.stdin.write(JSON.stringify(o) + "\n");
const request = (method, params) => new Promise((resolve, reject) => {
  const id = nextId++; pending.set(id, { resolve, reject }); send({ jsonrpc: "2.0", id, method, params });
});
rl.on("line", (line) => {
  line = line.trim(); if (!line) return;
  let msg; try { msg = JSON.parse(line); } catch { return; }
  if (msg.id !== undefined && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id); pending.delete(msg.id);
    msg.error ? reject(new Error(`${msg.error.message} (code ${msg.error.code})`)) : resolve(msg.result);
  }
});
const timer = setTimeout(() => {
  console.error(`mcp_cli.mjs: timed out after ${TIMEOUT_MS}ms (raise MCP_CLI_TIMEOUT_MS for long renders).`);
  child.kill("SIGKILL"); process.exit(2);
}, TIMEOUT_MS);
child.on("error", (err) => { console.error(`mcp_cli.mjs: failed to start server (${runCommand.join(" ")}): ${err.message}`); process.exit(2); });
child.on("exit", (code, signal) => {
  if (pending.size > 0) {
    console.error(`mcp_cli.mjs: server exited (code=${code} signal=${signal}) before responding.` + (stderrBuf ? `\n--- server stderr ---\n${stderrBuf}` : ""));
    process.exit(2);
  }
});

function finish(code) { clearTimeout(timer); child.stdin.end(); child.kill(); process.exit(code); }

try {
  await request("initialize", { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "ai-skills-mcp-cli", version: "2.0.0" } });
  send({ jsonrpc: "2.0", method: "notifications/initialized", params: {} });
  if (listMode) {
    const r = await request("tools/list", {});
    if (raw) console.log(JSON.stringify(r, null, 2));
    else for (const t of r.tools) {
      const props = Object.keys(t.inputSchema?.properties || {});
      const req = new Set(t.inputSchema?.required || []);
      console.log(`${t.name}(${props.map((p) => (req.has(p) ? p : p + "?")).join(", ")})\n  ${(t.description || "").split("\n")[0]}\n`);
    }
    finish(0);
  }
  const result = await request("tools/call", { name: toolName, arguments: toolArgs });
  if (raw) console.log(JSON.stringify(result, null, 2));
  else {
    const text = (result?.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n");
    console.log(text || JSON.stringify(result, null, 2));
  }
  finish(result?.isError ? 1 : 0);
} catch (err) {
  clearTimeout(timer);
  console.error(`mcp_cli.mjs: ${err.message}` + (stderrBuf ? `\n--- server stderr ---\n${stderrBuf.slice(-4000)}` : ""));
  child.kill("SIGKILL"); process.exit(2);
}
