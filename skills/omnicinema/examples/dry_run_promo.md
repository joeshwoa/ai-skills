# Example: planning a vertical promo (captured, real output)

Command:

```bash
bash scripts/call.sh run_cinema_pipeline @film.json   # film.json below
```

```json
{"prompt":"a street food vendor in Cairo opening his cart at dawn","sceneCount":3,"shotsPerScene":2,"shotDurationSeconds":3,"width":1080,"height":1920,"narration":"Before the city wakes, Amm Hassan lights the fire. Every morning, the same promise: bread, beans, and a smile.","soundtrack":true,"musicStyle":"ambient","dry_run":true}
```

Output (no keys configured, so the plan is an offline animatic):

```text
DRY RUN — nothing was generated, downloaded or written.
The Street Food Vendor · 1080×1920 @ 30fps · 18s
A modern cinematic short in 3 scenes: street food vendor in Cairo opening his cart at dawn (setup → climax → resolution).

1. EXT. CAIRO — PRE-DAWN [setup] — Establish Cairo and the street food vendor, in Cairo opening his cart at dawn. Light: cool blue pre-dawn with the first practicals glowing.
   · scene-1-shot-1 (establishing, 3s, gentle push-in): Wide on Cairo in the blue pre-dawn. The street food vendor is a small figure on the left third.  ⟶ search "Cairo pre-dawn"
   · scene-1-shot-2 (close, 3s, slow push-in): Close on the street food vendor's face — calm, attentive, waiting.  ⟶ search "vendor portrait"
2. EXT. STREET — SUNRISE [climax] — The cart peaks and the street food vendor holds their ground. Light: low golden sunrise raking across the frame.
   · scene-2-shot-1 (wide, 3s, slow pull-out): The cart at its height over Cairo — a low golden sunrise.  ⟶ search "Cairo sunrise"
   · scene-2-shot-2 (detail, 3s, fast push-in): Extreme detail: the street food vendor's face. Everything rests on this moment.  ⟶ search "vendor portrait"
3. EXT. CAIRO — MORNING [resolution] — Aftermath: calm returns to Cairo. Light: soft bright morning, gentle and clean.
   · scene-3-shot-1 (establishing, 3s, crane up and pull back): Cairo falls still under soft morning light; the cart has passed.  ⟶ search "Cairo morning"
   · scene-3-shot-2 (close, 3s, slow push-in): A final beat on the street food vendor's face. Hold, then fade.  ⟶ search "vendor portrait"

Footage: no stock key configured; fallback: offline storyboard frames (SVG → PNG) with Ken Burns motion.
Generative video: off.
Audio: narration ~9s via flite (offline system TTS); soundtrack ambient.
Render: remotion.
Network: None — this run is fully offline.
Spend: Nothing — no paid API is used.

Next steps:
- Review the shot list above. To produce it, call run_cinema_pipeline again with the same arguments and dry_run:false.
- No stock key set: every shot will be an offline storyboard frame (an animatic). Set PEXELS_API_KEY / PIXABAY_API_KEY / UNSPLASH_ACCESS_KEY for real footage.

```

After `dry_run:false` the same run rendered an 18.0 s 1080×1920 MP4 with narration, captions and an ambient score; `check_media.sh` reported ≈ −16 LUFS, 0 % black frames.
