#!/usr/bin/env node
/**
 * mcp_cli.mjs — a generic one-shot MCP (Model Context Protocol) stdio client.
 *
 * The real omnicinema-mcp server is a normal MCP server (JSON-RPC 2.0 over
 * newline-delimited stdio, via @modelcontextprotocol/sdk). Normally you'd
 * need to register it in an MCP-capable client (Claude Desktop config,
 * Cursor's mcp.json, etc.) and keep a long-lived server process running.
 *
 * This script removes that step entirely: it spawns the server fresh, does
 * the minimal MCP handshake, calls exactly one tool, prints the result as
 * JSON to stdout, and exits. Any agent that can run a shell command — with
 * or without native MCP support — can use the server's full, real,
 * unmodified functionality this way. There is zero duplicated logic: this
 * file talks nothing but the protocol, so it can never drift from the
 * server's real behavior.
 *
 * Usage:
 *   node mcp_cli.mjs <run-command...> -- <tool_name> '<json-args>'
 *
 * Example:
 *   node mcp_cli.mjs node /path/to/dist/index.js -- list_providers '{}'
 *
 * Exit code: 0 on success (tool returned isError:false or omitted),
 *            1 on a tool-level error, 2 on a transport/handshake error.
 */

import { spawn } from "node:child_process";
import readline from "node:readline";

function usageError(msg) {
  console.error(`mcp_cli.mjs: ${msg}`);
  console.error("Usage: node mcp_cli.mjs <run-command...> -- <tool_name> '<json-args>'");
  process.exit(2);
}

const args = process.argv.slice(2);
const sep = args.indexOf("--");
if (sep === -1 || sep === 0 || sep === args.length - 1) {
  usageError("expected: <run-command...> -- <tool_name> ['<json-args>']");
}
const runCommand = args.slice(0, sep);
const toolName = args[sep + 1];
const jsonArgsRaw = args[sep + 2] ?? "{}";

let toolArgs;
try {
  toolArgs = JSON.parse(jsonArgsRaw);
} catch (e) {
  usageError(`the json-args argument is not valid JSON: ${e.message}`);
}

const TIMEOUT_MS = Number(process.env.MCP_CLI_TIMEOUT_MS || 600000); // 10 min default

const child = spawn(runCommand[0], runCommand.slice(1), {
  stdio: ["pipe", "pipe", "pipe"],
});

let stderrBuf = "";
child.stderr.on("data", (d) => {
  stderrBuf += d.toString();
});

const rl = readline.createInterface({ input: child.stdout, crlfDelay: Infinity });

let nextId = 1;
const pending = new Map();

function send(obj) {
  child.stdin.write(JSON.stringify(obj) + "\n");
}

function request(method, params) {
  return new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, { resolve, reject });
    send({ jsonrpc: "2.0", id, method, params });
  });
}

function notify(method, params) {
  send({ jsonrpc: "2.0", method, params });
}

rl.on("line", (line) => {
  line = line.trim();
  if (!line) return;
  let msg;
  try {
    msg = JSON.parse(line);
  } catch {
    return; // ignore non-JSON stdout noise
  }
  if (msg.id !== undefined && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(`${msg.error.message} (code ${msg.error.code})`));
    else resolve(msg.result);
  }
});

const timer = setTimeout(() => {
  console.error(`mcp_cli.mjs: timed out after ${TIMEOUT_MS}ms waiting on the server.`);
  child.kill("SIGKILL");
  process.exit(2);
}, TIMEOUT_MS);
timer.unref?.();

child.on("error", (err) => {
  console.error(`mcp_cli.mjs: failed to start server (${runCommand.join(" ")}): ${err.message}`);
  process.exit(2);
});

child.on("exit", (code, signal) => {
  if (pending.size > 0) {
    console.error(
      `mcp_cli.mjs: server exited (code=${code} signal=${signal}) before responding.` +
        (stderrBuf ? `\n--- server stderr ---\n${stderrBuf}` : ""),
    );
    process.exit(2);
  }
});

try {
  await request("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "ai-skills-mcp-cli", version: "1.0.0" },
  });
  notify("notifications/initialized", {});

  const result = await request("tools/call", { name: toolName, arguments: toolArgs });

  clearTimeout(timer);
  child.stdin.end();
  child.kill();

  // MCP tool results carry content: [{type:"text", text}, ...] plus optional
  // structured fields and isError. Print the raw JSON result so a caller can
  // pull out .content[].text (human-readable) or any structured data.
  console.log(JSON.stringify(result, null, 2));
  process.exit(result?.isError ? 1 : 0);
} catch (err) {
  clearTimeout(timer);
  console.error(`mcp_cli.mjs: ${err.message}` + (stderrBuf ? `\n--- server stderr ---\n${stderrBuf}` : ""));
  child.kill("SIGKILL");
  process.exit(2);
}
