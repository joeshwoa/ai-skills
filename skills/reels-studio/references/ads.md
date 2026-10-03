# Ads — scripts that sell, in every slot

An ad is a reel with a budget behind it: the viewer didn't choose it, the slot length is fixed, the
brand must register before they skip, and every claim is checked by the platform's ad review.
Set `brief.content_type: "ad"` — the validator then enforces slot lengths, cutdowns, CTA,
brand-early and ad-copy limits.

## Brief additions (ask in the intake)
- **Objective & KPI**: awareness (reach, ad recall), traffic (CTR, CPC), leads (CPL, lead quality),
  sales (CPA, ROAS), app installs, event registrations.
- **Placements** (`brief.placements`): `meta_reels`, `meta_feed`, `meta_stories`, `tiktok_infeed`,
  `youtube_skippable`, `youtube_non_skippable`, `youtube_bumper`, `youtube_shorts_ad`,
  `youtube_infeed`, `snapchat_ad`, `linkedin_video`, `x_video`, `tv_spot`, `ctv`, `cinema`, `ooh_digital`.
- **Ratios** (`brief.ratios`): 9:16 (Reels/TikTok/Shorts/Stories), 4:5 (Meta feed), 1:1, 16:9 (YouTube/TV).
  Shoot for all of them at once: keep the action in the centre, leave headroom, no key text near edges.
- **Offer**: price, discount, deadline, guarantee terms — from the user only; legal line if needed (`super` block).
- **Brand name** (`brief.brand_name`) — the validator checks it's seen/heard in the first 5 s.
- **Budget level & production**: UGC/phone, studio, animation, AI-generated (→ flow-studio-director).

## Structures (pick one per ad)
| Framework | Beats | When |
|---|---|---|
| **PAS** | Problem → Agitate → Solution → (Proof) → CTA | problem-aware audiences, most performance ads |
| **AIDA** | Attention → Interest → Desire → Action | cold audiences, product launches |
| **BAB** | Before → After → Bridge (the product) → CTA | transformations (real, typical results only) |
| **Hook–Demo–Offer** | 3 s hook → product doing the job → offer + CTA | e-commerce, apps, tools |
| **Testimonial (UGC)** | result first → before → what changed → CTA | consideration/retargeting — real customers only |
| **Us vs them / old vs new** | the old painful way → the new way → CTA | category education (don't name competitors unfairly) |
| **Founder / authority** | why we built it → what it does → proof → CTA | trust-heavy categories (education, finance, health) |
| **Event / deadline** | what · when · why attend · scarcity that's true → register | launches, webinars, free events |

## Slots and lengths (verify live — platforms change these)
| Placement | Hard limit | Script it as |
|---|---|---|
| YouTube bumper | 6 s, non-skippable | one idea + brand + CTA card; no dialogue scene longer than ~4 s |
| YouTube non-skippable | 15 s (some TV inventory allows 30 s) | full mini-ad, CTA in the last 3 s |
| YouTube skippable in-stream | no hard max (skip after 5 s); 15–60 s typical | brand + hook before 5 s, then earn every second |
| YouTube Shorts ads | vertical; keep under ~60 s (not a hard cap — verify) | like a reel |
| Meta Reels / Stories | 9:16; up to 60 s+ but 15 s or less recommended | hook 3 s, captions, CTA in the last 3 s |
| Meta feed | 4:5 or 1:1 | sound-off first: on-screen text carries it |
| TikTok in-feed | 9:16, from 5 s up to ~10 min; 21–34 s often recommended | native, creator-style, not a TV ad |
| Snapchat | 9:16, 3–180 s | short and native |
| LinkedIn | 15–30 s recommended | professional pain/number hook, captions |
| TV / cinema | 15 / 20 / 30 / 45 / 60 s | the slot is exact to the frame; legal supers per market |

## Cutdowns — one master, every slot
Write a master (e.g. 30 s), then define `cutdowns` that reuse its scenes:
```json
"cutdowns": [
  {"name": "15s", "target_sec": 15, "scenes": [1, 3, 5], "ratio": "9:16 + 4:5", "placement": "meta_reels"},
  {"name": "6s bumper", "target_sec": 6, "scenes": [1], "end_frame_sec": 2, "ratio": "16:9", "placement": "youtube_bumper"}
]
```
Rules the validator checks: scene numbers are whole numbers that exist, every cutdown opens on a
scene with words (its own hook), fits its slot (≤ target + 5%), respects the placement's maximum,
and ends on a scene with words or has `end_frame_sec` for the end card. Visual-only scenes need
`duration_sec` so the cut can be timed. A placement with a hard limit (bumper 6 s, non-skippable
15 s) needs a cutdown with that `placement` that fits — otherwise it's an error.
Design scenes so they *can* stand alone: each scene one idea, the CTA in its own scene.

## Creative testing matrix
Ads win on volume of good variants, not one perfect film.
- **3–5 hooks × 1–2 bodies × 1–2 CTAs** — keep the body, swap the first 3 s (store hooks in
  `posting.alt_hooks`). Record each hook as a separate opening so the editor can swap them.
- Test one variable at a time; let each variant get enough spend to read (the media buyer decides).
- Read: hook rate (3-s views ÷ impressions), hold rate (watch-through / ThruPlays ÷ 3-s views),
  CTR, then CPA/CPL. Low hook rate → new hooks. Good hook, low hold → body. Good hold, low CTR → offer/CTA.
- Creative fatigue: rising frequency + falling CTR → rotate new hooks, not just new colours.

## Ad copy (posting.ad_copy)
- **Primary text**: first ~125 characters visible — the hook again, in words; value; CTA.
- **Headline**: Meta recommends ~27 characters (cut around 40), the offer or outcome.
- **Description**: ~27 characters (often hidden).
- **CTA button**: the platform's set (Learn More, Sign Up, Shop Now, Book Now, Contact Us, Download…).
- Same dialect as the video. No claims the landing page doesn't back up.

## Ad policy — what gets ads rejected (Meta, TikTok, Google — check the current policies)
- **Personal attributes**: never assert or imply the viewer's health, weight, finances, religion,
  ethnicity, sexuality, age, criminal record ("Are you overweight?", "إنت مديون؟"). Talk about the
  situation, not the person ("Want a plan that fits a busy week?").
- **Unrealistic or unprovable claims**: guaranteed results, "100%", income promises, miracle
  before/after (health and weight loss are restricted categories).
- **Misleading formats**: fake buttons, fake notifications, fake news looks, clickbait that the ad
  doesn't deliver.
- **Restricted categories**: health/medicine, finance/credit/crypto, employment, housing,
  education claims (accreditation, job guarantees), alcohol, gambling, politics/social issues — need
  disclaimers, special ad categories or are banned in some markets.
- **Rights**: licensed music (commercial libraries), talent releases, no third-party logos
  implying endorsement.
- **Disclosure**: creator/UGC ads run as paid partnerships with the platform label.
The reviewer runs `references/review-checklist.md` section 5b for every ad.

## Writing ads in the user's dialect
Same rule as reels: the audience's spoken variety. Ads in Egypt usually work best in friendly
Egyptian Arabic; MSA only for institutional or pan-Arab corporate briefs.
