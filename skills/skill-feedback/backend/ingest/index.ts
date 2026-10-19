// Edge Function `ingest` — public endpoint for anonymous, non-personal skill feedback.
// Accepts POST JSON or GET query params (for agents that can only fetch a URL).
// Validates strictly, rejects anything that looks personal, rate-limits per install and globally,
// stores only the whitelisted fields. The caller's IP is never stored by this function.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const AGENTS = ["claude","cursor","gemini","antigravity","windsurf","chatgpt","codex","copilot","other"];
const SURFACES = ["cli","desktop","web","mobile","ide","api","other"];
const OSES = ["macos","windows","linux","ios","android","other","unknown"];
const EVENTS = ["gap","failure","wrong_info","suggestion","new_skill_request","success_note"];
const OUTCOMES = ["success","partial","failure"];
const TAGS = ["platform-rule-outdated","missing-platform","missing-case","script-bug","unclear-instructions",
  "automation-gap","language-dialect","too-long","tool-unavailable","wrong-output","missing-reference","other"];
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const SKILL = /^[a-z0-9][a-z0-9-]{1,63}$/;
const VERSION = /^[A-Za-z0-9._-]{1,40}$/;

// Anything matching these is rejected, not stored.
const PII: [string, RegExp][] = [
  ["email", /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/],
  ["handle", /(^|\s)@[A-Za-z0-9_.]{2,}/],
  ["url", /(https?:\/\/|www\.)\S+/i],
  ["domain", /\b[a-z0-9-]+\.(com|net|org|io|co|app|dev|ai|me|eg|sa|ae|info|xyz)\b/i],
  ["phone", /(\+?\d[\d\s().-]{7,}\d)/],
  ["path", /([A-Za-z]:\\|\/Users\/|\/home\/|\/Volumes\/|~\/|\\\\)/],
  ["ip", /\b\d{1,3}(\.\d{1,3}){3}\b/],
  ["token", /\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{24,}\b/],
  ["long-digits", /\d{6,}/],
];

function cors(): HeadersInit {
  return { "content-type": "application/json", "access-control-allow-origin": "*",
    "access-control-allow-headers": "content-type, authorization, apikey", "access-control-allow-methods": "GET, POST, OPTIONS" };
}
function reply(status: number, body: unknown) { return new Response(JSON.stringify(body), { status, headers: cors() }); }

function textField(name: string, v: unknown, max: number): string | null {
  if (v === undefined || v === null || v === "") return null;
  if (typeof v !== "string") throw new Error(`${name} must be text`);
  const s = v.replace(/\s+/g, " ").trim();
  if (s.length > max) throw new Error(`${name} longer than ${max} characters`);
  for (const [label, re] of PII) if (re.test(s)) throw new Error(`${name} looks like it contains ${label}; describe the gap generically`);
  return s || null;
}
function pick(name: string, v: unknown, allowed: string[], fallback?: string): string {
  const s = typeof v === "string" ? v.toLowerCase() : fallback;
  if (!s || !allowed.includes(s)) throw new Error(`${name} must be one of: ${allowed.join(", ")}`);
  return s;
}
async function sha(s: string) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(d)).map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, 32);
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors() });
  let input: Record<string, unknown> = {};
  try {
    if (req.method === "GET") {
      const u = new URL(req.url);
      for (const [k, v] of u.searchParams) input[k] = v;
      if (typeof input.tags === "string") input.tags = (input.tags as string).split(",").map((t) => t.trim()).filter(Boolean);
    } else if (req.method === "POST") {
      const raw = await req.text();
      if (raw.length > 4000) return reply(413, { ok: false, error: "payload too large" });
      input = JSON.parse(raw);
    } else return reply(405, { ok: false, error: "method not allowed" });
  } catch { return reply(400, { ok: false, error: "invalid input" }); }

  try {
    const install_id = String(input.install_id ?? "");
    if (!UUID.test(install_id)) throw new Error("install_id must be a random UUID");
    const skill = String(input.skill ?? "");
    if (!SKILL.test(skill)) throw new Error("skill must be a skill folder name");
    const event = pick("event", input.event, EVENTS);
    const outcome = input.outcome ? pick("outcome", input.outcome, OUTCOMES) : null;
    const agent = pick("agent", input.agent, AGENTS, "other");
    const surface = pick("surface", input.surface, SURFACES, "other");
    const os = pick("os", input.os, OSES, "unknown");
    const version = input.skill_version ? String(input.skill_version) : null;
    if (version && !VERSION.test(version)) throw new Error("skill_version malformed");
    const tagsIn = Array.isArray(input.tags) ? input.tags.map(String) : [];
    if (tagsIn.length > 5) throw new Error("at most 5 tags");
    for (const t of tagsIn) if (!TAGS.includes(t)) throw new Error(`unknown tag ${t}; allowed: ${TAGS.join(", ")}`);
    const gap = textField("gap", input.gap, 300);
    const suggestion = textField("suggestion", input.suggestion, 500);
    if (!gap && !suggestion && event !== "success_note") throw new Error("gap or suggestion required");

    const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
    const dayAgo = new Date(Date.now() - 86400_000).toISOString();
    const hourAgo = new Date(Date.now() - 3600_000).toISOString();
    const mine = await db.from("skill_feedback").select("id", { count: "exact", head: true }).eq("install_id", install_id).gte("received_at", dayAgo);
    if ((mine.count ?? 0) >= 20) return reply(429, { ok: false, error: "daily limit for this installation reached" });
    const all = await db.from("skill_feedback").select("id", { count: "exact", head: true }).gte("received_at", hourAgo);
    if ((all.count ?? 0) >= 1000) return reply(429, { ok: false, error: "service busy, try later" });

    const gap_hash = await sha(`${skill}|${event}|${(gap ?? "").toLowerCase()}|${(suggestion ?? "").toLowerCase()}`);
    const { error } = await db.from("skill_feedback").insert({ install_id, skill, event, outcome, agent, surface, os,
      skill_version: version, tags: tagsIn, gap, suggestion, gap_hash });
    if (error) {
      if (error.code === "23505") return reply(200, { ok: true, duplicate: true });
      return reply(500, { ok: false, error: "storage error" });
    }
    return reply(200, { ok: true });
  } catch (e) {
    return reply(422, { ok: false, error: (e as Error).message });
  }
});
