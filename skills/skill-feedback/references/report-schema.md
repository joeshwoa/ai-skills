# Report schema (version 1)

JSON body (POST) or query string (GET) to `config.json` -> `endpoint`:

```json
{"install_id":"<uuid v4>","skill":"social-media-manager","event":"gap","outcome":"partial",
 "agent":"claude","surface":"desktop","os":"macos","skill_version":"01dd603",
 "tags":["missing-case"],"gap":"No case for recovering a hijacked Telegram channel",
 "suggestion":"Add recovery steps to the telegram platform file"}
```

Required: install_id, skill, event, and at least one of gap/suggestion (except success_note).
Tags: platform-rule-outdated, missing-platform, missing-case, script-bug, unclear-instructions, automation-gap, language-dialect, too-long, tool-unavailable, wrong-output, missing-reference, other.
Responses: 200 `{ok:true}` (or `duplicate:true`), 422 with the reason if rejected (fix and resend once), 429 rate limit (20/day per install; do not retry), 5xx queue locally.
Duplicates (same install, skill and text on the same UTC day) are ignored.
