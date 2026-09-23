# Characters first — building and locking the cast

**No scene, keyframe or shot is made until every character in it is
built and approved.** This is enforced: `project_state.py` refuses scene
keyframes until gate `cast` is closed, and refuses any shot that uses a
character who is not approved. The reason is simple economics: identity
drift is the most common and most expensive failure in AI video, and the
only reliable fix is to lock identity *before* shots exist. Changing a
character after ten shots means regenerating ten shots.

## 1. Define each character (from the script analysis)

Write the character bible entry — binding facts from the script,
everything else a proposal for the client:
- name, role, relationship to the others
- age, build, height relative to the others, skin tone
- face: shape, eyes, brows, nose, mouth, distinguishing marks
- hair: colour, length, texture, style
- **IMMUTABLE wardrobe** `[NAME_LOCK v1]`: every garment with colour name
  (+ hex), fabric, fit, condition; accessories; shoes
- voice: gender, age, dialect, energy, texture, pace, default emotion
- personality in three words (drives performance notes in prompts)

## 2. Build the images (Nano Banana — 0 credits on Pro)

1. **Reference sheet** — front / three-quarter / profile, full body, neutral
   pose, plain light-grey backdrop, even light (template A in
   `prompt-architecture.md`). Use Nano Banana Pro for the final sheet.
2. **Expression sheet** (speaking characters) — 4–6 head shots: neutral,
   happy, surprised, worried, talking mid-word. Mouth shapes matter for
   lip-sync realism later.
3. **Consistency test** — 2–3 images of the character in the project's
   real lighting and a real location from the script, different poses.
   If the face or wardrobe drifts between these, fix the description (or
   the reference) now — it will drift in video too.

`project_state.py can-build-asset character` must say GO (gate `script`
approved) before this step.

## 3. Register in the platform

- **Flow Character**: add the approved sheet as a Character (sidebar
  "Characters"). Every shot the character appears in adds it as an
  ingredient.
- **Flow Voice** (speaking characters): create a custom voice — closest
  base voice + performance customization (template F). Preview it with a
  line from the script in the right dialect.
- Optional, recommended for leads: a **4 s voice test** on Omni at 360p
  (the cheapest generation) with the character saying one real line — it
  confirms voice, dialect and lip-sync before the production spends on it.

Record each step as it is done (every file must exist — the state refuses
paths that don't; names written into plan.json never count as built):
```bash
project_state.py cast-set HANA --sheet chars/hana_sheet.png --expressions chars/hana_expr.png \
    --consistency chars/hana_test.png --flow-character Hana --voice HANA_VOICE \
    [--voice-test takes/hana_voice_test.mp4]
```
Silent characters need sheet, consistency test and Flow Character; speakers
also need the expression sheet and the voice.

## 4. Approve

Show the client/user, per character: the reference sheet, the expression
sheet, the consistency test, and the voice preview (or voice test clip).
Approve one by one:
```bash
project_state.py cast-approve HANA --by user --note "client: 'Hana is perfect' (WhatsApp 14:02)"
```
When every character is approved:
`project_state.py gate cast approve --by user --note "<client's words>"`.
`--by` is always required; the note records what the user actually said,
so an approval can always be traced to a real "yes".

Name questions from the breakdown ("كرين" vs "كريم") are answered before
casting: if they are one person, re-run the breakdown with
`--alias "كرين=كريم"`; if the breakdown found a name that isn't a person,
`project_state.py cast-remove X --by user --note "..."`.

Rules:
- Only the user/client approves characters — never the agent, in any mode.
- Changing an approved character (new sheet, new voice) automatically
  un-approves it and reopens gate `cast`; shots that used the old version
  must be checked.
- A character added mid-project (a new role in a revision) goes through
  the same steps before any shot uses it.
- Background people who never recur and never speak don't need a cast
  entry — describe them generically in prompts ("a passer-by, back to
  camera, soft focus"). But anyone recognisable — a named or introduced
  person ("عم حسن (60)"), anyone in a close-up, anyone in two shots — is
  cast even without a line. The breakdown lists silent characters it
  finds ("Speaks: silent"), and always asks the client who else is on camera.
- The project's state is kept in step with the plan: after editing
  plan.json run `project_state.py sync-plan plan.json`. A new character
  reopens gate `cast` (and every gate after it) until it is built and
  approved.
