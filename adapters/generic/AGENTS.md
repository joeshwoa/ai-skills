# Agent instructions — this repo

This repo stores reusable "skills" (agent playbooks) under `skills/<name>/`.
Any coding agent working in a project that includes this repo (or has this
file copied into it) should, before doing work that matches a skill's
purpose, read that skill's `SKILL.md` in full and follow it.

## Read this first, every time

**skill-router** (`skills/skill-router/SKILL.md`) — read this one FIRST,
before any other skill, for any non-trivial request. It checks
`skills/manifest.json` and auto-selects a matching installed skill (no
need to be told which one to use), and — if nothing installed matches —
searches for or builds a new skill and installs it into this repo
automatically, following the same procedure used to build every skill
below. This is the dispatcher; the rest of this list is what it
dispatches to. It also logs a short usage report after every skill use
(`skills/skill-enhancer/scripts/log_report.py`) — see **skill-enhancer**
below for what that feeds.

## Available skills

- **premium-presentations** (`skills/premium-presentations/SKILL.md`) —
  agency-quality editable decks (.pptx + animated HTML) in English or Arabic
  (RTL): 33 slide types incl. native charts, diagrams, KPI, image and teaching
  slides, speaker notes, stock photos/icons, brand kits. Trigger: any request
  for a deck, slides, pitch deck, PowerPoint, lecture or lesson slides.
- **premium-documents** (`skills/premium-documents/SKILL.md`) — any document
  as editable Word + designed PDF from one spec (reports, proposals, e-books,
  contracts, letters, invoices, CVs, certificates, newsletters, worksheets,
  exams…), English or Arabic. Trigger: write/design/format a document or PDF.
- **premium-spreadsheets** (`skills/premium-spreadsheets/SKILL.md`) —
  formula-driven Excel workbooks (budgets, P&L, dashboards, trackers,
  gradebooks, question banks) with tables, validation, charts and an
  automatic recalculation error check. Trigger: any spreadsheet/Excel request.
- **course-studio** (`skills/course-studio/SKILL.md`) — designs and writes
  complete courses (plans, outcomes, timed lessons, full content, slides,
  handouts, labs, quizzes + keys, rubrics, instructor guides, gradebooks);
  always asks the context first. Trigger: course, curriculum, programme,
  training, lesson series, course materials.
- **premium-design-kit** (`skills/premium-design-kit/SKILL.md`) — the shared
  design engine of the four skills above (themes, brands, Arabic, assets,
  charts, previews). Trigger: choosing a look, sourcing images/icons for a
  design, previewing/QA-ing an Office/PDF file, setting the skills up.
- **automation-studio** (`skills/automation-studio/SKILL.md`) — an automation
  agency: brief → process map + diagram → build n8n workflows with n8n's own SDK
  and schemas → validate → test every case in a real local n8n (mocked apps,
  live key-less APIs, idempotency over repeated runs) → credentials walkthrough
  → deploy/activate/monitor via the API (local Mac, self-hosted, n8n Cloud);
  12 tested patterns from simple to orchestrated (error alerts, idempotency, AI
  agent, document AI, human approval, sub-workflows); converters to Node-RED
  (runs), Make (blueprint) and build guides for Zapier, Power Automate,
  Pipedream, Activepieces. Never creates accounts or handles keys itself.
  Trigger: automate a task/process, n8n/Make/Zapier/flow, webhook, schedule,
  connect apps, AI agent workflow, automation diagram.
- **n8n-agent-studio** (`skills/n8n-agent-studio/SKILL.md`) — n8n + browser
  agents for anything with NO API: probes the site, ranks the access routes
  (official node/API → hidden JSON → recipe → attach to the user's Chrome →
  LLM agent → human-in-the-loop), builds and tests the n8n flow, deploys local
  or published; browserd recipe worker, AI-agent and MCP-bridge patterns.
  Trigger: automate a site/app without an API, control a website from n8n,
  browser/scraping/RPA in n8n, a web-UI agent, n8n as an MCP server.
- **premium-3d-models** (`skills/premium-3d-models/SKILL.md`) — build
  real parametric 3D models (.glb/.stl/.obj) for Flutter, web/React,
  Blender, or 3D printing. Trigger: any request to "model," "3D model,"
  or make a 3D object/part/asset/prop.
- **premium-subtitle-localization**
  (`skills/premium-subtitle-localization/SKILL.md`) — find/transcribe
  source subtitles, verify the transcript against the actual audio,
  translate with real cultural/comedic adaptation (never
  literal/mechanical translation), validate, and mux into a video
  without re-encoding. Trigger: any request to subtitle, translate, or
  localize a video/movie into another language. Note its hard rule: a
  garbled ASR cue may only be re-transcribed from audio, marked
  unclear, or asked about — never guessed from context, however obvious
  it looks.
- **reels-studio** (`skills/reels-studio/SKILL.md`) — a full video content
  team (strategist, audience analyst, trend researcher, idea lead, hook
  writer, scriptwriter + dialect specialist, director, editor, copywriter,
  media buyer, researcher, growth analyst, brand/legal reviewer) for three
  content types: reels/TikTok/Shorts, ads (master + cutdowns per placement —
  Meta, TikTok, YouTube skippable/bumper, TV — ratios, ad copy, ad-policy
  checks) and long-form (YouTube explainers, course lessons, webinars,
  podcasts, brand films — chapters, timecodes, titles/thumbnails). Locks
  scope and audience first, researches live dated trends, scores ideas and
  hooks, writes in any language or dialect (Egyptian Arabic as people speak
  it, Gulf, Levantine, MSA, English…), validates, and renders PDF + DOCX in
  the house script style (Neo AI built in) plus teleprompter, draft SRT and a
  production file flow-studio-director reads. Trigger: write/plan/fix a reel,
  ad/commercial, YouTube video, lesson or podcast script, hooks, trends, or a
  content calendar — before any production skill.
- **video-post-studio** (`skills/video-post-studio/SKILL.md`) — the full
  post-production team on the user's studio-mcp: edit footage (scene detection,
  take selection, transcript edits with Arabic/English filler removal, cut to
  the beat, colour match, sound, captions, QC, exports, Kdenlive + FCPXML/OTIO
  for Resolve/Premiere) or make new videos from a brief with free stock b-roll.
  Trigger: edit/cut/montage/colour/mix/caption/deliver a video, make a reel/ad/
  promo/YouTube video from footage, a script or a voiceover.
- **motion-design-studio** (`skills/motion-design-studio/SKILL.md`) — the motion
  graphics team with an engine router (GSAP compositions, Lottie, three.js 3D,
  Blender, Remotion when licensed): kinetic type, logo stings, titles, lower
  thirds, promos, explainers, charts, 3D titles. Trigger: animate, motion
  graphics, intro/outro, logo animation, animated post/ad.
- **stock-library** (`skills/stock-library/SKILL.md`) — free stock footage,
  photos, illustrations, vectors, music, SFX and icons from every free stock
  site with an official API, with licence sidecars, clearance and credits.
  Trigger: b-roll, stock, royalty-free, music/SFX for a video, credits.
- **creative-studio** (`skills/creative-studio/SKILL.md`) — a whole
  content-creation team on free/open-source tools via the user's studio-mcp
  (110 tools): brand kits (logo concepts, palette, Arabic+Latin type,
  guidelines), social/print design, Photoshop-style photo work (layered
  PSD/XCF), Illustrator-style vector, Premiere-style editing (JSON timeline →
  MP4 + editable Kdenlive project, captions, reframing), After-Effects-style
  motion graphics, Egyptian-Arabic voiceover/transcription/mastering, and AI
  images/video (local ComfyUI/mflux or free services). Every tool returns
  previews to LOOK at. Trigger: design, brand, edit, animate, caption, voice,
  retouch or "make content" for a business or social media.
- **omnicinema** (`skills/omnicinema/SKILL.md`) — logos (+ reversed/icon),
  vector illustrations, UI mockups, genre music (WAV + MIDI), sound effects,
  voiceover and short promo/animatic videos from the user's omnicinema-mcp
  engine; offline and free by default, stock/AI with the user's keys; every
  output checked with `scripts/check_media.sh`. Runs the real server as a
  one-shot local command. Trigger: logo, mockup, illustration, music, beat,
  SFX, voiceover, quick promo/storyboard video.
- **devuniverse** (`skills/devuniverse/SKILL.md`) — scaffold a Flutter app
  (+ Supabase/Firebase, optional Fastify service, optional 3D journey) from
  a brief via the user's devuniverse-mcp persona agency: dry-run plan →
  generate → `scripts/verify_project.sh` (flutter analyze/test, service
  tests, RLS, audit). Trigger: start/scaffold a new app, add a 3D journey,
  re-theme from images, release audit, privacy/terms drafts.
- **flow-studio-director** (`skills/flow-studio-director/SKILL.md`) — a
  full AI film crew for Google Flow (Veo 3.1 + Omni Flash + Nano Banana)
  that takes a client's script to the finished video: script breakdown
  and analysis, characters and voices built and approved before any shot,
  storyboard animatic, per-shot routing and credit pricing, dense
  cinematic prompts, native in-clip dialogue, QC of every take, editing
  (fix in post first), transitions, captions from the script, montage and
  delivery — order enforced by five gates the user signs; can drive Flow in
  Chrome (Kapture) in four autonomy modes. Trigger: any request to make, plan, prompt, fix, check,
  extend or finish an AI video/reel/ad/short/animated series, or which Flow
  model to use / what it will cost.
- **skill-router** (`skills/skill-router/SKILL.md`) — see "Read this
  first, every time" above; also documents how to keep
  `skills/manifest.json` in sync and the full search/build/install
  procedure for adding a new skill.
- **skill-enhancer** (`skills/skill-enhancer/SKILL.md`) — audits and
  improves any skill using the usage reports skill-router logs (or a
  direct read-through when none exist yet): finds recurring issues and
  missing coverage, fixes them, re-validates, ships the update. Trigger:
  a skill produced a bad/incomplete result, or any request to
  enhance/improve/audit/review a skill's quality.
- **packet-tracer-studio** (`skills/packet-tracer-studio/SKILL.md`) — Design, build, configure, test and save complete network labs in Cisco
  Packet Tracer 9 on the user's Mac through packet-tracer-mcp (live IPC, port
  39000): topologies, cabling, Cisco IOS CLI (VLANs, trunks, STP,
  EtherChannel, inter-VLAN routing, OSPF/EIGRP/RIP/static, DHCP, NAT/PAT,
  ACLs, port security, SSH, HSRP, ASA), host IPs, ping/PDU verification,
  troubleshooting and the .pkt file.
- **social-media-manager** (`skills/social-media-manager/SKILL.md`) — Runs the work of a social media manager across every major platform
  (Facebook, Instagram, WhatsApp, Telegram, TikTok, YouTube, LinkedIn, X,
  Threads, Reddit, Snapchat, Pinterest, Google Business Profile, Discord) with
  sourced per-platform rules, limits, formats, policy hot spots, API and
  automation facts, and Egypt/Arabic notes.
- **media-buying** (`skills/media-buying/SKILL.md`) — Plans, launches, optimizes and reports paid media on Meta
  (Facebook/Instagram/WhatsApp), Google Ads (Search, Performance Max, Demand
  Gen), YouTube, TikTok, Snapchat, LinkedIn, X, Pinterest and Telegram Ads,
  with sourced per-platform rules, creative specs, policies, tracking and API
  facts, plus Egypt/MENA realities (payment, WhatsApp-first leads, cash-on-
  delivery, Ramadan and White Friday).
- **marketing-studio** (`skills/marketing-studio/SKILL.md`) — Marketing strategy and planning for businesses and creators - audience and
  market research, positioning and messaging, offers and pricing angles,
  funnel and channel selection, content and SEO plans, email and WhatsApp
  marketing, launch plans, brand voice, competitor analysis, measurement
  frameworks and marketing OKRs, with Egypt and Arabic-market context.

This file follows the emerging `AGENTS.md` convention several agentic tools
(Cursor, GitHub Copilot, OpenAI Codex CLI, and others) read automatically
from a repo root. Copy this file (or symlink it) into the root of any
project where you want these skills auto-discovered, and keep the
`skills/` folder alongside it — or point your tool's rule/instructions
setting directly at `skills/<name>/SKILL.md`.
