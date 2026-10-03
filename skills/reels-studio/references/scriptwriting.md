# Scriptwriting, direction and editing notes

## Structures that work (pick one, don't mix)
| Structure | Beats | Best for |
|---|---|---|
| Hook → Problem → Insight → Positioning → CTA | the Neo AI trend reel | thought leadership, offers |
| Hook → 3 steps → Result → CTA | tutorial / listicle | saves, followers |
| Myth → Why people believe it → Truth → Proof → CTA | myth-bust | consideration |
| Story: Situation → Conflict → Turn → Lesson → CTA | story | trust, founder pieces |
| Experience → Observation → Question → Brand → Vision → "Next" | founder statement (HERO REEL — Mr. Wael) | brand film |
| Question → Who it's for (list) → Common ground → Why us → CTA | audience call-out (REEL 04) | events, programmes |
| Why → Experience → Network → Offer → Value → CTA | event value (REEL 03) | registrations |
| Setup → Escalation → Twist (brand) | skit | reach, shares |

## Writing rules (any language)
- Write for the ear: one idea per sentence, ≤ ~15 words, the important word at the end.
- Second person, present tense, concrete nouns, numbers people can picture ("4 minutes", not "quickly").
- Contrast lines carry reels: "Not X… but Y" / "مش… لكن…"; "It's not just… it's…" / "ده مش مجرد… ده…".
- Use `{"pause": true}` where the talent needs a beat — after the hook, before the payoff, before the CTA.
- Cut every line that doesn't move the viewer toward the payoff. Then cut 10% more.
- Facts, names, prices, dates, results: only from the user or a cited source.
- The CTA is one action, said once clearly, matched to the goal; end frame repeats it visually.
- Runtime = spoken words ÷ speaking rate (Arabic ≈ 2.1 w/s, English ≈ 2.5 w/s, see
  `scripts/reelspec.py`) + pauses + silent visual beats. The validator checks it against the target.

## Blocks (what goes in each scene)
- **visual** (blue) — framing, movement, what's on screen. Camera language: wide / medium /
  medium close-up / close-up; eye level / slightly low; static, slow push-in, gimbal drift,
  handheld; 45° side angle for variety; cut on idea change.
- **dialogue / voiceover** (red) — exactly what's said; `speaker` = talent name.
- **onscreen_text** (blue) — 3–7 words, appears with the line it supports, ≥ (0.3 s × words + 0.5 s).
- **broll** — specific shots, not "AI visuals": "screen recording: same prompt in a cheaper model, result appears".
- **sfx / music** — only where they add meaning; music builds into the payoff; Voice > Music > Environment.
- **camera / transition / note / direction** — as needed.

## Director's checklist
- The first frame is not static and not a logo.
- Visual change every 2–4 s (angle, crop, B-roll, text, gesture) — fewer for premium/founder pieces
  (3–4 main shots, cut only when the idea changes).
- Performance notes where tone shifts: "more confident, no smile", "small confident smile", "no gestures".
- Where they look: direct eye contact for hooks and CTAs.
- Wardrobe/location only when it matters (founder pieces: full brief in `sections`).
- Avoid clichés the brand dislikes (e.g. robots, futuristic screens, generic AI stock).

## Editor's checklist (editor_notes)
- Cut rhythm and where the music builds.
- SFX policy (e.g. only on the glitch transitions).
- Captions: burned-in, 1–2 lines, high contrast, inside safe zones (see `platforms.md`); Arabic captions
  right-aligned, a font that shapes Arabic (Cairo/Tajawal).
- On-screen text timing and position; no text under the platform UI.
- Loudness: speech clear, music ducked under voice (~-14 LUFS integrated is a common delivery target).
- End frame: what, how long (1.5–3 s), minimal animation.
- Export: 1080×1920, 9:16, 30 fps (or source fps), H.264/H.265, AAC.

## Length guide
7–15 s: one punch (loops well) · 20–35 s: one idea with a payoff · 45–60 s: explanation or
offer · 60–90 s+: only with a strong story/tutorial and re-hooks every ~15 s.
