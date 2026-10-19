# Launch checklist (platform-neutral, 20 checks)
Client: | Platform(s): | Campaign: | Date: | Checked by: | Approved to launch by:
Run this, then the platform-specific checklist (section 13 of each file): `references/platforms/meta-ads.md`, `google-ads.md`, `youtube-ads.md`, `tiktok-ads.md`, `snapchat-ads.md`, `linkedin-ads.md`, `x-ads.md`, `pinterest-ads.md`, `telegram-ads.md`. Any unchecked item in 1-8 blocks launch. Nothing goes live without explicit user approval.

## Economics and plan
- [ ] 1. Break-even and target CPA/ROAS computed (`ads_math.py breakeven`), with COD/returns adjusted.
- [ ] 2. One primary conversion event and its value defined; weekly event volume at this budget meets the platform threshold (`ads_math.py budget`), or the event was moved up the funnel.
- [ ] 3. Media plan approved (`templates/media-plan.md`), budget cap and approval rule for increases written.

## Tracking
- [ ] 4. Events fire once at the right moment; value, currency and order ID passed; tested end to end by a human.
- [ ] 5. Browser and server events deduplicated; test codes removed (`references/tracking-and-attribution.md` s1, s8).
- [ ] 6. UTMs built with `scripts/utm_builder.py`; names built with `scripts/naming.py`.
- [ ] 7. Click ID captured to the CRM; reconciliation source (shop/CRM/courier) ready; consent handling in place.

## Account and access
- [ ] 8. Account currency and time zone correct; two valid payment methods in the client's name; spending cap set where supported (`references/policy-and-account-health.md` s4).
- [ ] 9. Client owns the account, pixel and domain; agency has partner/role access; 2FA on; no shared passwords (`policy-and-account-health.md` s6).
- [ ] 10. Business and domain verification done or started; restricted-category approvals in hand.

## Creative and landing page
- [ ] 11. At least 3 genuinely different creatives per ad set (fewer if the budget cannot feed them); each passes spec checks (platform file s6) and previews in placements.
- [ ] 12. Arabic/RTL checked by a native speaker; numerals, currency and prices match the landing page.
- [ ] 13. Policy review done: no banned claims, no before/after where banned, no personal-attribute wording, rights cleared (`policy-and-account-health.md` s7).
- [ ] 14. Landing page fast on mobile, matches the offer and price, shows business identity, contact, returns, privacy policy; checkout and payment (including COD) tested.

## Operations
- [ ] 15. Lead/WhatsApp response owner and SLA set; auto-reply outside hours; stock and delivery capacity cover the expected volume.
- [ ] 16. Structure is minimal for the budget (campaign, ad set count) and audience exclusions (customers, employees) are set.
- [ ] 17. Learning plan: no edits for the platform's window; evaluation date set; stop-loss rule agreed relative to break-even CPA.
- [ ] 18. Test plan and test log ready (`templates/test-log.md`); change log started.
- [ ] 19. Calendar checked for seasonal peaks and review-queue time (`references/mena-and-egypt-notes.md` s7); spare creatives ready.
- [ ] 20. Reporting set: weekly report (`templates/weekly-report.md`), dashboard or sheet, daily billing/rejection alerts.
