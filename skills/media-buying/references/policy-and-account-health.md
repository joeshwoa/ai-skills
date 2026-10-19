# Policy and account health
Purpose: avoid ad rejections and account restrictions, and recover correctly through official channels when they happen.
Last updated: 2026-10-19

Each platform's exact rules, review times and appeal routes are in the policy section (s8) of its file. This file gives cross-platform principles and workflows. Policies change often and many details are `unverified` in the platform files: read the current policy page cited there before promising an outcome. Nothing here is legal advice, and nothing here helps evade enforcement (section 8).

## 1. Principles that hold across platforms
1. **Ad, landing page and business must agree.** Claims, price, offer, brand name and product must match across the ad, the landing page and the checkout. Mismatch is a recurring cause on Meta, Google, TikTok, Pinterest and Snap (`meta-ads.md` s8, `tiktok-ads.md` s8, `pinterest-ads.md` s8, `snapchat-ads.md` s8, `google-ads.md` s8).
2. **Claims must be true, typical and substantiated.** No guaranteed results, miracle claims, unrealistic income or weight loss, fake urgency or fake reviews. Keep proof on file (test reports, licences, receipts).
3. **Do not address personal attributes.** Copy must not imply you know a viewer's health, finances, age, religion or sexual orientation ("Are you in debt?"). Write about the topic or the product (`meta-ads.md` s8; LinkedIn forbids sensitive-category targeting in `linkedin-ads.md` s8).
4. **Restricted categories need approval before spend**: finance and crypto, health and pharma, gambling, alcohol, political and social-issue, dating, real estate/off-plan in some markets, and age-restricted products. Egypt, KSA and UAE specifics are mostly `unverified` in the platform files; confirm per platform and per country (`mena-and-egypt-notes.md` s2, s8).
5. **Landing page quality is part of the ad.** Working page, fast on mobile, visible business identity, contact info, privacy policy, no deceptive pop-ups, no forced downloads, accessible to the platform's crawler.
6. **Authenticity**: real business, real name, real payment instrument, real testimonials, no impersonation of brands or public figures, no AI-generated media passed off as real (TikTok requires disclosure: `tiktok-ads.md` s8).
7. **Respect local law and culture**: price accuracy, delivery promises, religious and cultural sensitivity (`mena-and-egypt-notes.md` s4, s8).
8. **One compliant path**: fix the cause, then appeal once with evidence. Repetition and workarounds escalate enforcement.

## 2. Common rejection causes and fixes
| Cause | Typical trigger | Fix | Where details live |
|---|---|---|---|
| Misleading or unreliable claims | "guaranteed", "100% results", "lose X kg in Y days", income promises, fake countdown timers, news-style fake articles | Remove absolute and time-bound claims; show typical results with a disclaimer; substantiate or delete; make timers real | Meta s8; Google s8 (unreliable claims); TikTok s8; Pinterest s8; Telegram s8 |
| Before/after imagery | weight loss, skin, wrinkles, body change | Remove the comparison; show product, ingredients, usage, or testimonials without health outcome claims (Meta and Snap and Pinterest ban weight-loss before/after; Google's own rule `unverified`) | Meta s8; Snap s8; Pinterest s8 |
| Personal attributes | second-person health, debt, age, status phrasing | Rewrite to neutral topic phrasing | Meta s8 |
| Landing page mismatch | different price/offer, missing product, broken page, aggressive pop-ups, missing business details | Align the page with the ad (price, product, currency), fix errors, add company, contact, returns, privacy; make crawler-accessible | Meta s8; Google s8; TikTok s8; Snap s8; Pinterest s8 |
| Restricted category without approval | finance, crypto, health, gambling, alcohol, political | Stop; apply for certification/authorization or change the offer; do not reword around it | each s8 |
| Misleading buttons or UI | fake play/close buttons, fake notifications, blurred clickbait, a CTA that does not match the destination | Use platform CTA buttons that describe the real action; remove fake UI | TikTok s8; Meta s8 |
| Domain/URL issues | display URL differs from destination, redirects, URL shorteners, tracking redirects that look like cloaking | Match domains, final URL = what the user sees, no shorteners | Google s8; LinkedIn s8; Telegram s8 |
| Intellectual property | brand logos, music, celebrity likeness, copied creative | Use licensed or owned assets; get permissions in writing | TikTok s8; Snap s8; X s8 |
| Format/functionality | no audio, QR codes, spelling errors, excessive caps/symbols, text-heavy images, out-of-spec | Use the spec in the platform file s6; proofread | TikTok s8; platform s6 |
| Lead form issues | no privacy policy link, sensitive questions | Add the privacy policy; remove sensitive questions or obtain authorization | TikTok s8; LinkedIn s8 |
| Special ad category not declared | housing, employment, financial products | Declare; accept targeting limits | Meta s4 |
| Prohibited business practice | MLM, penny auctions, payday loans, counterfeit | Cannot be fixed by rewording; do not advertise | each s8 |
| Spam patterns | identical ads in volume, rapid resubmission, many near-duplicate ads | Consolidate, one corrected submission | Meta s8, Google s8, TikTok s8 |

Arabic notes: review Arabic copy for the same issues; a translated claim carries the same violation. Review RTL layout and numbers: a mis-rendered price can cause a "mismatch" flag (`creative-testing.md` s9).

## 3. Review and appeal workflow
1. **Read the exact reason** in the platform (rejection notice, Policy manager, Account Quality, ad review email). Note the policy name, the cited element (text, image, video, landing page, URL), the ad IDs and the date.
2. **Classify**: (a) real violation, (b) borderline/ambiguous, (c) likely false positive.
3. **Fix** (a) and (b) fully: every field, the creative, the landing page and the destination together. Do not edit one word and resubmit. Where the platform auto-resubmits on save (Google, LinkedIn: `google-ads.md` s8, `linkedin-ads.md` s8), the fix is the submission.
4. **Submit once.** If the creative changed substantially, submit as a new ad (Meta, TikTok, Snap guidance in each s8). Keep compliant ads running; do not pause an entire ad set because one ad is rejected.
5. **Appeal only if you believe it complies (c)**, using the platform route and its limits (Meta "Request review", Google Policy manager appeal with at most three unsuccessful appeals per ad and 24 hours between appeals, Pinterest email, X support ticket, Snap and Telegram forms or notices; per s8 of each file). Include evidence and a short explanation.
6. **Wait the stated review time**; there is no guaranteed SLA on most platforms. Do not stack appeals or contact multiple channels with the same case unless the platform file says to escalate.
7. **Record** the outcome in the policy log (below) and update the pre-launch review checklist so the pattern is caught next time.

Policy log columns: date, platform, ad/campaign ID, policy cited, element, action taken, appeal sent (yes/no), result, learning.

### Template A: appeal for a rejected ad (generic)
```
Subject: Request for review of ad [ID] ([ad name])
Account: [ad account ID], Business: [legal name], Website: [domain]
The ad was rejected for: [policy name and wording shown in the notice].
What the ad shows: [one-line neutral description].
Why we believe it complies: [claim substantiated by ... / product is not in the restricted category / the landing page shows the same price and offer, see URL].
Changes made (if any): [list of edits to text, image, landing page, with dates].
Evidence attached: [licence number, certificate, test report, screenshot of the landing page].
We would be grateful for a re-review. Contact: [name, email].
```
Rules: factual, short, no pressure or threats, no new claims, no repeated sending. Do not include passwords, tokens or payment details.

### Template B: request for review of a restricted account
```
Subject: Account review request, [ad account ID]
Business: [legal name, registration number, country], website, contact.
Notice received: [date and text of the restriction or disable message].
What we found: [our review of the cause: payment issue / policy violation of type / verification missing].
What we corrected: [steps with dates].
What we will do to prevent it: [process change].
Documents attached: [business registration, tax ID, utility bill or bank letter as requested by the platform, ID verification completed].
Please advise on next steps.
```
Use only official forms and support channels. A client contact with legal authority submits identity documents; the agent does not collect them in chat.

## 4. Why accounts get restricted or disabled and how to prevent it
| Cause | Prevention |
|---|---|
| Payment failures or unsettled invoices | Two valid payment methods in the client's name, alerts, balance monitoring, local card issues handled in advance (`mena-and-egypt-notes.md` s1; `meta-ads.md` s2; `google-ads.md` s2) |
| Unverified business or identity | Complete business and advertiser verification early; consistent legal name, address, website, card holder (`mena-and-egypt-notes.md` s2) |
| Policy strikes (repeated or severe) | Pre-launch policy review (section 7 checklist), clean ad history, no repeated resubmissions |
| Egregious violations (Google can suspend without warning for misrepresentation) | Never misrepresent business, product or identity (`google-ads.md` s8) |
| Unusual activity: sudden spend spikes, many new ads/accounts at once, new location or device logins, many failed logins | Ramp spend gradually, keep access on stable devices and IPs, avoid bulk-changing, use partner access rather than shared logins |
| Circumventing systems | Never create new accounts to run banned content (section 8) |
| Compromised access (phishing, leaked tokens, former staff) | Roles, 2FA, access reviews (section 6) |
| Risky vertical without approval | Certifications first (section 1 rule 4) |
| Third-party app or API misuse | Use official APIs, minimal permissions, rate-limit handling (`meta-ads.md` s11) |
| Personal profile dependency | Use business accounts with at least two admins (`meta-ads.md` s2; `google-ads.md` s2) |
Monitor: Account Quality (Meta), Policy manager and notifications (Google), email notices; check weekly (`optimization-playbook.md` s4).

## 5. Verification and ownership
- Business ownership: the client owns the ad account, business portfolio, domain, pixel/dataset and catalog; the agency has partner or role access (`mena-and-egypt-notes.md` s1; `meta-ads.md` s2).
- Domain verification and events: complete the platform's domain/ownership verification where it exists; it supports restricted features and prevents hijack (`meta-ads.md` s7 notes its current requirement status `unverified`).
- Business verification: have registration documents, tax ID, address proof and a website with the same legal name. Egypt-specific documents are `unverified` (`mena-and-egypt-notes.md` s2).
- Advertiser verification (Google): possible re-verification after payment-profile or legal-name changes; plan time (`google-ads.md` s2).
- Authorizations for restricted categories: gather licence numbers and approvals first; platform authorization pages are in each s8.
- Keep a document pack (registration, tax card, licences, website policies) in the client's folder.

## 6. Safe access practices
- **Roles and partner access, never password sharing.** Add the agency through the platform's partner/manager link or role invitation (Meta Business partners, Google manager account link, TikTok business center roles, LinkedIn roles; per s2 of each file). Never ask for or store a client's password, 2FA codes, recovery email access or payment card details in chat or files (SKILL.md hard rule).
- **2FA** on every admin and user; authenticator app rather than SMS where possible; store recovery codes with the client.
- **At least two admins** at the client side; one business email domain, not a personal mailbox.
- **Least privilege**: analysts read-only; media buyers standard; billing only with the client. Review roles monthly; remove ex-employees and ex-agencies the day they leave.
- **API tokens**: system users or service accounts, minimum scopes, rotated, kept in a secret manager, never in prompts, repos, spreadsheets or logs (`meta-ads.md` s11).
- **Logins**: use the client's approved devices; avoid logging in from many locations and VPN hopping; unusual login patterns can trigger security flags.
- **Payment**: payment instruments belong to the client; agency re-invoicing risks ownership and tax mismatches (`mena-and-egypt-notes.md` s1).
- **Change control**: approvals and the change log (`optimization-playbook.md` s7).
- **Offboarding**: transfer admin to the client, revoke partner access, export reports and audiences, hand over the tracking plan and creative library.

## 7. Pre-launch policy checklist (use with `templates/launch-checklist.md`)
- [ ] Category checked against the platform's prohibited and restricted lists; approvals in hand if restricted.
- [ ] No guaranteed, absolute or fear claims; claims substantiated; testimonials real and typical.
- [ ] No before/after imagery where banned; no personal-attribute phrasing.
- [ ] Landing page matches ad (price, product, currency); business identity, contact, returns, privacy visible; mobile fast; crawler-accessible.
- [ ] Buttons and CTAs match the destination; no fake UI.
- [ ] Rights for music, images, talent, brand marks; AI media disclosed where required.
- [ ] Special ad category declared if applicable.
- [ ] Arabic and English copy proofread by a native speaker; numbers/currency consistent.
- [ ] Spare compliant creatives ready for peak periods because review queues grow (`mena-and-egypt-notes.md` s7).
- [ ] Payment methods valid and verification complete.

## 8. When an account is disabled
1. **Stop and read**: capture the notice, date, account ID and reason; screenshot Account Quality or Policy manager. Do not create new ad accounts, do not move the pixel or payment card to a new account to keep running the same content.
2. **Diagnose the category**: payment, verification, policy violation, unusual activity, compromised access, or an error.
3. **Fix the cause**: settle invoices, complete verification, remove violating ads and fix the landing page, secure access (reset passwords, enable 2FA, remove unknown users).
4. **Appeal through the official channel** with Template B and evidence; one submission; wait; use the platform's support or partner channel if it exists (Meta business support, Google support form, Pinterest partner account manager: per s8 of each file).
5. **Keep business continuity without circumvention**: pause dependent campaigns on other legitimate accounts that follow policy; run organic and owned channels (email, WhatsApp opt-ins, SEO) while waiting; tell the client the realistic timeline (reported ranges from days to weeks, no guarantee: `meta-ads.md` s8; Google notes some decisions older than 6 months cannot be appealed in-account, `google-ads.md` s8).
6. **After reinstatement**: add the root-cause fix to the checklist, back up audiences and creatives, review roles.
7. **If permanently disabled**: accept the decision; any new account must be a legitimately separate business with compliant offers, never a workaround (Google may refuse return to advertisers disabled for egregious violations: `google-ads.md` s8).

## 9. Why circumvention backfires
Cloaking (showing reviewers a different page), account swapping, rotating domains, disguised restricted claims, buying "aged" accounts or using fake identities are treated as violations of their own, usually more severe than the original problem. Platforms link accounts, payment methods, devices, pages and domains; a ban can spread to linked assets, including the client's real business account (`meta-ads.md` s12, `google-ads.md` s8, `snapchat-ads.md` s8). Effects include permanent loss of the pixel, audiences and history, and legal exposure. If a client asks for a workaround, decline and offer the compliant path: change the offer, claim or page, obtain authorization, or choose a channel where the category is allowed.

## 10. Platform policy sections
| Platform | Policy, review and appeals |
|---|---|
| Meta | `platforms/meta-ads.md` s8 (also s4 for special ad categories) |
| Google Ads | `platforms/google-ads.md` s8 |
| YouTube | `platforms/youtube-ads.md` s8 (plus Google s8) |
| TikTok | `platforms/tiktok-ads.md` s8 |
| Snapchat | `platforms/snapchat-ads.md` s8 |
| LinkedIn | `platforms/linkedin-ads.md` s8 |
| X | `platforms/x-ads.md` s8 |
| Pinterest | `platforms/pinterest-ads.md` s8 |
| Telegram | `platforms/telegram-ads.md` s8 |

## Sources
- Policy and review details are cited in each platform file s8 (Meta Advertising Standards, Google Ads policy help, TikTok advertising policies, Snap Advertising Policies, LinkedIn Advertising Policies, X help center, Pinterest advertising guidelines, Telegram ad guidelines), dated 2026-10-19.
- `mena-and-egypt-notes.md` s1, s2, s8. Templates A and B are generic drafting aids, not platform forms; use the platform's own form where one exists.
