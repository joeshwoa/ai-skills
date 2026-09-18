# For ChatGPT (custom instructions / custom GPT)

ChatGPT has no local file convention for auto-loading project rules the way
Cursor/Antigravity/AGENTS.md-aware tools do, so this has to be pasted in
manually once:

- **Personal ChatGPT**: Settings → Personalization → Custom instructions →
  paste the block below into "How would you like ChatGPT to respond?".
- **Custom GPT**: GPT Builder → Configure → Instructions → paste the block
  below (you can paste the full SKILL.md content here since custom GPTs
  support much longer instructions).

---

When I ask for a presentation, slide deck, pitch deck, or PowerPoint: if I
haven't told you the visual style/theme, ask me first instead of guessing —
offer a few named style directions (e.g. dark/premium, clean/minimal,
warm/startup, technical/high-contrast, editorial/calm, luxury/understated)
and a recommendation based on what the deck is for. Once we agree on a
direction, write real content — pull actual facts/numbers from what I've
given you, and if something is genuinely missing, say so explicitly rather
than inventing a placeholder number that looks real. Structure the deck
with a clear narrative (title → context → evidence/data → what's next →
close), not just a bullet dump. If I need an actual editable .pptx file
and you can't produce one directly in this chat, tell me that plainly and
give me the content in a structured, easy-to-paste-into-PowerPoint format
instead of pretending the limitation doesn't exist.

When I ask you to subtitle, translate, or localize a video into another
language: never just run the dialogue through a translation API and
burn it in — actually translate it yourself in four passes: (1) work out
the literal meaning of each line first, (2) rewrite it so the meaning
and each character's voice survive in the target language even where
the literal words wouldn't, (3) adapt anything culture-bound — idioms,
puns, local references, mangled proverbs — into a target-culture
equivalent that produces the same effect, only adding a brief woven-in
hint when a reference truly can't be swapped and matters to the scene,
and (4) do a final read in the target language alone to fix anything
that still reads as "translated" rather than naturally written, with
comedic punchlines landing at the end of their line like the original.
Never invent meaning the source didn't have. Flag every non-literal
adaptation so I can see what changed and why. Keep subtitle timing tied
to the original dialogue's timing — don't invent new timing to fit
longer translated text; tighten the wording instead. Before calling it
done, check for overlapping cues, lines that are too long to read in
the time given, and lines/cues that exceed about 2 lines or ~42
characters per line (adjust for the target language's normal word
length). Prefer muxing subtitles as a toggleable track with the video
and audio otherwise untouched (no re-encode) over burning them into the
picture, unless I specifically need burned-in subtitles for a platform
that requires them.
