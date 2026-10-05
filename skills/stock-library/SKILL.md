---
name: stock-library
description: Find, check and download free stock media from every free stock site with an official API — video footage, photos, illustrations, vectors, music, sound effects and icons from Pexels, Pixabay, Unsplash, Coverr, Freesound, Jamendo (free keys) and Openverse, Wikimedia Commons, Internet Archive, NASA, Iconify (no key) — with a stock researcher and a licensing/clearance officer: labelled contact sheets to choose from, verified downloads, licence sidecars, rejection of non-commercial, people and third-party-brand risks, and ready credits for the description. Use whenever a video, post, presentation or motion piece needs b-roll, footage, a background, a photo, an illustration, an icon, music or a sound effect, or the user asks for "free stock", "copyright-free", "royalty-free" or licences/credits.
---

# Stock Library

The sourcing department of the studio, on the user's MCP server **studio-mcp** (stock tools).
Official APIs only — no scraping. Every file arrives with its licence, attribution text and
source link, and every project keeps a credits ledger.

Paths are relative to this skill's folder (`skills/stock-library/` in the ai-skills repo).

## Setup
Shared environment with creative-studio (`bash ../creative-studio/scripts/bootstrap.sh` once).
Call: `bash scripts/call.sh <tool> '<json>'`. Check: `bash scripts/selftest.sh`.

**Keys (free, the USER creates them — never the AI):** the keyless providers work immediately.
Pexels, Pixabay, Unsplash, Coverr, Freesound and Jamendo need a free key each. Run
`call.sh stock_sources` — it lists which are active, writes `STUDIO_HOME/keys.json` with empty
entries (chmod 600) and gives the sign-up steps; the user pastes each key there himself (or sets
the same names as environment variables). Never ask for, type, read back or store key values;
never create accounts for the user. `references/providers.md` has the table and step-by-step
key instructions (Pexels + Pixabay are the biggest upgrade for video).

## The team
| Role | Does |
|---|---|
| Stock researcher | turns the brief into concrete English queries (object + action + setting + mood), searches several phrasings and kinds, picks by looking at the contact sheet |
| Licensing & clearance officer | keeps `commercial=true`, rejects NC/ND, identifiable people without releases (ads/promos), other brands' logos/trademarks, NASA insignia; makes sure attribution is delivered |
| Asset manager | downloads at the right quality, names/organises per project, writes credits, re-uses what's already in the ledger |

## Workflow
1. **Brief → shot list.** For each needed asset: kind (video/photo/illustration/vector/music/sfx/
   icon), orientation (portrait for reels/stories, landscape for YouTube), minimum length (video ≥
   the slot + 1 s), resolution (HD+), mood. Arabic briefs: translate the visual idea to English
   queries (the APIs index English).
2. **Search.** `stock_search {"query": "barista pouring latte art close up", "kind": "video", "orientation": "portrait", "min_duration": 4, "count": 12, "project": "<p>"}`.
   LOOK at the numbered contact sheet: relevance, quality, framing, licence badge (green = no
   credit, amber = credit, red = not commercial). Try 2–3 phrasings (synonyms, closer/wider, a
   different setting) before settling. Music: `kind: "music"` (+ mood/genre words); SFX:
   `kind: "sfx"`; icons: `stock_icon`.
3. **Clear.** Reject: anything red; identifiable people for ads/promos unless the provider's
   licence plus a release covers it (default: avoid); visible third-party logos/products (e.g. a
   coffee chain's cup); NASA insignia; watermarks; ND licences for edited use; CC BY-SA when the
   client can't share-alike the result (tell them).
4. **Download.** `stock_download {"ids": ["3", "7", "pexels:123"], "quality": "hd", "project": "<p>"}`
   → verified files + `<file>.license.json` + ledger. LOOK at the downloaded contact sheet.
5. **Credit.** At delivery: `stock_credits {"project": "<p>"}` → `credits.txt` into the video/post
   description, `CREDITS.md` for the client. Required attributions first.

## Rules
- Official APIs only (`references/providers.md` lists sites without an API — the user can browse
  those by hand: Mixkit, Videvo, Pixabay music pages, Uppbeat, YouTube Audio Library).
- Respect each API's terms: Pixabay 24 h caching and no hotlinking (handled), Unsplash download
  ping + attribution (handled), rate limits (handled with pacing/backoff).
- Licences travel with files; never strip sidecars; never present stock as the client's own work.
- Say honestly when the keyless catalogues are thin for a topic and suggest adding the free keys.

## Hand-offs
video-post-studio (b-roll in edits, `video_auto_edit` uses these tools itself) · motion-design-studio
(backgrounds, icons, Lottie) · creative-studio (photos for designs) · reels-studio (production
hand-off lists the stock needed).
