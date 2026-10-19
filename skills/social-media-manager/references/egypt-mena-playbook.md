# Egypt and MENA playbook
Purpose: platform mix, Arabic norms, calendar logic, commerce and support habits for Egypt, the Gulf and the Levant, with sourced figures and clear uncertainty.
Last updated: 2026-10-19

Rule for this file: figures are quoted from the source with its date; anything else is marked `heuristic` (practitioner habit) or `unverified` (general knowledge not confirmed this session). Be respectful: these are generalisations, so check against the account's own audience data and local advice before acting.

## 1. Platform mix (sourced usage figures)
Source: DataReportal "Digital 2026" country reports (Simon Kemp, Kepios), published 2025-11-05 to 2025-11-08, data mostly October to late 2025, read 2026-10-19. Figures are advertising-tool ad reach in millions, not monthly active users; TikTok is 18+ only; LinkedIn counts registered members; DataReportal flags some values over 100% as likely implausible and warns that platform revisions distort year-on-year changes. They are about a year old by now.
| Platform | Egypt | Saudi Arabia | UAE | Jordan | Lebanon |
|---|---|---|---|---|---|
| Facebook | 51.6 | 17.7 | 9.70 | 5.55 | 3.45 |
| YouTube | 49.3 | 27.5 | 8.37 | 6.80 | 3.12 |
| TikTok (18+) | 48.8 | 38.6 (flagged by source as anomalous) | 12.5 | 2.34 | 4.58 |
| Messenger | 37.0 | 11.1 | 5.65 | 3.95 | 1.65 |
| Instagram | 21.7 | 18.2 | 8.05 | 4.55 | 2.95 |
| Snapchat | 20.6 | 25.3 | 5.13 | 4.20 | 1.46 |
| LinkedIn (members) | 15.0 | 12.0 | 10.0 | 2.20 | 1.40 |
| X | 4.64 | 15.0 | 2.85 | 0.83 | 0.56 |
| Threads | 3.15 | 1.55 | 0.89 | 0.55 | not listed |
| Reddit | 1.35 | 1.70 | 2.45 | 0.30 | not listed |
Totals (social media user identities): Egypt 51.6M (internet users 98.2M, 82.7% penetration, population 119M); Saudi Arabia 38.6M; UAE 12.5M; Jordan 6.80M; Lebanon 4.58M.
URLs: https://datareportal.com/reports/digital-2026-egypt , `...-saudi-arabia` , `...-united-arab-emirates` , `...-jordan` , `...-lebanon`.
Reading the table (inference, not sourced):
- Egypt is Facebook, YouTube and TikTok first; Instagram and Snapchat are a second tier; X and Reddit are niche. Do not drop Facebook for Instagram-only plans (`platforms/instagram.md` section 11).
- Saudi Arabia skews to Snapchat, YouTube, TikTok and X compared with Egypt; X is much stronger there.
- UAE: LinkedIn and Instagram matter more, audience is multinational: check language mix.
- WhatsApp is absent from DataReportal's pages. A vendor claim of about 52 million WhatsApp users in Egypt (chatdaddy.tech, 2026-03-24) is third-party and unsourced, so treat WhatsApp's weight as `unverified` (`platforms/whatsapp.md` section 1). Telegram user counts for Egypt: `unverified` (`platforms/telegram.md` section 1). Iraq, Kuwait, Qatar, Morocco and other MENA markets: not gathered, `unverified`.

## 2. Arabic content norms and dialect choice
- Egypt consumer content: Egyptian dialect. Formal notices, legal, medical, press, government: Modern Standard Arabic (MSA) or very light dialect.
- Gulf and Levant audiences: do not use Egyptian dialect for them by default; either neutral "white" Arabic or a native-written local version (Saudi/Khaleeji, Shami). Egyptian dialect is widely understood across the region through media (heuristic), but forced imitation of another dialect reads badly.
- Mixed-language audiences (UAE, Egyptian professionals): short bilingual captions, one language per paragraph, Arabic first for Arabic accounts.
- Politeness: address with "حضرتك", use titles (أستاذ/أستاذة، دكتور/دكتورة) in customer replies; keep jokes light and self-directed; avoid regional stereotypes.
- Orthography, numerals, RTL traps, diacritics, Arabizi: `content-craft.md` section 6.
- Subtitles: Egyptian-dialect speech is subtitled word for word in dialect on short video; keep lines short (`content-craft.md` section 5).
- Hashtags: one Arabic and one English per post is a safe default; check each platform's cap (`content-craft.md` section 7).
- Visuals: respect modest imagery norms for family-oriented audiences; local faces, landmarks and food outperform generic stock (heuristic).

## 3. WhatsApp-first commerce and cash on delivery
- WhatsApp and Messenger are the usual sales conversation in Egypt (`platforms/messaging-and-community-channels.md` section 1 calls the claim widespread but `unverified` for statistics). Plan for the chat as the checkout: bio link to WhatsApp click-to-chat, a Messenger/DM path, and a person ready to reply (`community-management.md` section 7).
- Cash on delivery (COD) is common in Egyptian e-commerce (general knowledge, `unverified` here; no statistic read). Mobile wallets and instant payment apps such as Fawry and InstaPay are named in a vendor guide (`platforms/whatsapp.md` section 11, third-party).
- COD routine (heuristic): confirm every order in chat with a summary (items, total, delivery fee, address with landmark, phone, delivery window); ask for a yes; send a pre-delivery reminder; offer reschedule; log failed deliveries; do not ask for card numbers in chat.
- Price transparency: customers ask "بكام؟" in comments; answer publicly (template 2 in `community-management.md`) to avoid repeat questions and mistrust.
- WhatsApp costs and templates: use the official rate card in WhatsApp Manager, Egypt amounts not confirmed (`platforms/whatsapp.md` section 11).
- Egyptian mobile numbers in E.164 format: country code 20 without the leading zero (`platforms/whatsapp.md` section 11).
- Marketing consent: Law 151/2020 explicit-consent rules (`compliance-and-ethics.md` section 6).
- Egypt's Facebook Shops/Instagram Shopping availability and local payment integration: `unverified`.

## 4. Voice-note culture
- Customers often send voice notes instead of typing (general observation, `unverified` as a statistic). Plan for it: acknowledge in text ("وصلتنا رسالتك الصوتية"), summarise what you understood, ask them to confirm price, address and quantity in writing.
- Reply by voice only when the brand voice and consent allow; always put numbers, prices and addresses in text as well.
- Transcription: if you transcribe customer voice with a tool, check the vendor's data terms and the consent position (`compliance-and-ethics.md` section 6) and do not paste personal data into LLM prompts.
- Brand voice notes (Channels, Telegram): short, under about one minute, with a text summary for accessibility (`content-craft.md` section 5).

## 5. Calendar logic (Ramadan, Eid, Mawlid, Coptic dates, White Friday, school)
Do not hard-code Gregorian dates for movable events. Method for any year (do this each planning cycle):
1. Islamic events follow the Hijri lunar calendar: Islamic New Year 1 Muharram; Mawlid 12 Rabi' al-Awwal; Ramadan is the 9th month; Eid al-Fitr 1 to 3 Shawwal; Eid al-Adha 10 to 13 Dhu al-Hijjah (holiday lengths as listed on Wikipedia "Public holidays in Egypt", read 2026-10-19). The Hijri year is about 354 to 355 days, so each event moves about 10 to 11 days earlier in the Gregorian calendar every year.
2. Start dates depend on moon sighting and an official announcement (in Egypt by the religious authority, Dar al-Ifta, as general knowledge, `unverified` here). Use an astronomical Hijri converter for a first estimate (can be off by 1 to 2 days), then confirm from the official announcement, which usually comes only 1 day or so before. Plan content for a 3-day window and keep date placeholders in pre-approved posts.
3. Coptic and Christian dates: Christmas is fixed on 7 January in the Gregorian calendar (Wikipedia, 29 Koiak in the Coptic calendar); Orthodox Easter is computed with the Orthodox method and falls in April or May; Sham El-Nessim is the Monday after Orthodox Easter (Wikipedia). Compute Orthodox Easter with a published computus table or library and confirm. Coptic fasting periods affect food brands (vegan demand); their exact lengths: `unverified`.
4. Fixed Egyptian national holidays: 25 Jan, 25 Apr, 1 May, 30 Jun, 23 Jul, 6 Oct (Wikipedia). Whether the government moves holidays to adjacent days in a given year: not confirmed; check the official Cabinet announcement.
5. White Friday: the regional name for Black Friday. Rule: Black Friday is the Friday after US Thanksgiving, which is the fourth Thursday of November (rule-based; for 2026 this gives 26 Nov Thanksgiving and 27 Nov Black Friday). Regional retailers often start earlier and run for days or weeks (heuristic); confirm the retailer or marketplace campaign dates, `unverified`.
6. Back to school and exams: dates are set by each ministry or school system and differ by country and school type; check the official academic calendars. Egyptian and Gulf dates: `unverified`.
7. Other recurring hooks (general knowledge, `unverified`): Egypt Mother's Day on 21 March (shared by several Arab countries), Saudi National Day (23 Sept) and UAE National Day (2 Dec), Valentine's Day (sensitive, check audience), Eidiya season after Eid.
Planning pattern: lock Ramadan and Eid calendar 6 to 8 weeks ahead (`strategy-and-planning.md` section 10); in Ramadan shift output to evening hours, shorter and warmer content, charity and community themes, less hard selling at fasting hours; avoid food imagery in daytime-focused creatives for fasting audiences (heuristic); do not use religious phrases or verses as sale decoration. Use `scripts/calendar_gen.py --skip <dates>` to block confirmed holidays.
Timezones: use `Africa/Cairo` in tools; Egypt reinstated daylight saving in 2023 as far as I know (`unverified` here); Saudi Arabia is UTC+3 all year and the UAE UTC+4 (general knowledge). Check tz data when scheduling across countries.

## 6. Posting-time heuristics (not facts)
- Starting hypotheses only: lunch break, and evening after work (about 20:00 to 23:00 local) on weekdays; later and longer evenings in Ramadan (after iftar and before suhoor; a vendor guide says activity peaks after iftar, `platforms/whatsapp.md` section 11); Friday late morning is low-attention around congregational prayer time; weekend Friday and Saturday in Egypt (general knowledge) change office-hours content.
- Replace with the account's own insights after 4 weeks (`analytics-and-reporting.md` section 7).
- Messaging hours: avoid marketing messages late night; 10 pm to 8 am Cairo is a practitioner suggestion (`platforms/whatsapp.md` section 11).
- Gulf audiences are in a different time zone; schedule per audience, not per team.

## 7. Sensitive topics and red lines (high level)
These are cautions, not a legal list. Laws and norms differ by country and change.
- Religion: no jokes about religion, no sacred texts or verses as promotional decoration, no mocking of any faith (Muslim or Christian communities live side by side in Egypt); greetings for Eid, Ramadan and Coptic holidays are welcome when sincere and approved. Prayer-time and fasting sensitivity in scheduling.
- Politics and security: avoid elections, parties, government criticism, military, security forces and regional conflicts unless the brand's field is news and the owner approves with counsel. A brand statement on a conflict can trigger boycott calls; decide once, in writing, in advance, who approves.
- Gender, sexuality, family: conservative norms for much of the audience; avoid content that mocks gender roles or touches LGBTQ topics in promotional material; respect modest imagery. Local law and platform enforcement may differ from the brand's global stance: owner decision with counsel.
- Alcohol, gambling, pork, adult imagery: restricted by norms, law or platform rules in many markets (platform files list restricted categories).
- Health and finance: strict claims discipline (`compliance-and-ethics.md` section 7).
- Advertising to children: platform and national rules apply; Egyptian rules unverified. Do not target under-13s; guardian consent for promotions; YouTube "made for kids" and TikTok branded content limits in the platform files.
- National symbols, flags, leaders: do not use in sales promotions; follow local rules, `unverified`.
- Cybercrime and media laws: Egypt's Anti-Cybercrime Law 175/2018 (Art. 25 is cited in the platform files on unauthorised marketing) and Media Law 180/2018 (reported in 2018 to treat accounts with 5,000+ followers as media outlets) can apply to online content; details `unverified`: get Egyptian counsel before sensitive or high-reach campaigns.

## 8. Local influencer norms
- Micro and nano creators are used heavily for niche trust (heuristic); gifted products and barter are common (`unverified`), and disclosure is often weak in practice. Require disclosure in contracts and check posts (`compliance-and-ethics.md` sections 2 and 3).
- Licensing: Egypt influencer or advertising licence rules `unverified`. Saudi Arabia and the UAE have published licence regimes for advertisers or influencers as far as I know from general knowledge (`unverified` here): check the current rules of the relevant regulator before paying a creator there.
- Negotiation norms: price by deliverable, usage rights and duration; ask for audience screenshots from the creator's own analytics; check comments for authenticity, not just follower numbers.
- Religious and political posts by creators can reflect on the brand: include a conduct and takedown clause.

## 9. Arabic customer support in practice
- Language: reply in the customer's language and script; default Egyptian dialect, polite "حضرتك"; keep sentences short; avoid heavy MSA on chat.
- Names and search: a customer name may appear in Arabic or Latin spelling; search both and common variants (أحمد/Ahmed/Ahmad).
- Addresses: Egyptian addresses rely on landmarks; ask for district, street, building number, a landmark and a second phone number.
- Greeting and closing samples:
  - Greeting: "أهلًا بحضرتك في [البراند]، أقدر أساعدك إزاي؟"
  - Order confirmation: "تمام يا فندم، بأكد معاك: [الأصناف]، الإجمالي [المبلغ] شامل التوصيل، الدفع عند الاستلام، العنوان [..]، الميعاد [..]. مناسب؟"
  - Delay: "معلش على التأخير، طلب حضرتك [الحالة] وهيوصل [الميعاد]. هنكلمك قبل ما نوصل."
  - Closing: "لو احتجت أي حاجة تانية إحنا موجودين. شكرًا لحضرتك."
- Public complaints: answer fast and politely, then move to private (`community-management.md` section 4 templates 3 to 5); public shaming spreads quickly, so act early.
- Working hours and holidays: publish them; set expectations for Friday, Ramadan hours and Eid (confirm dates per section 5).
- Escalation: religion, politics, harassment and threats go to the owner (`community-management.md` sections 2 and 8).
- Dialect reviewer: have a native speaker review templates for each country before use.

## 10. Campaign checklist for Egypt and MENA
1. Which country and dialect is each post for, and has a native reviewer seen it?
2. Is the platform mix justified by the figures in section 1 and the account's own insights?
3. Are movable dates confirmed from an official announcement, with placeholders in pre-approved copy (section 5)?
4. Is there a WhatsApp or DM path staffed during the hours the post runs, with COD confirmation steps (section 3)?
5. Are disclosure words and labels present ("إعلان" or "برعاية" plus the platform tool)?
6. Has the content passed the red-line review (section 7) and the release gate (`compliance-and-ethics.md` section 11)?
7. Are timezone, weekend and prayer-time effects handled in the schedule (section 6)?
8. Is there a plan for the comments you expect (price, delivery, complaints) with templates ready (`community-management.md` section 4)?

## 11. Sources
- DataReportal Digital 2026 reports, read 2026-10-19: https://datareportal.com/reports/digital-2026-egypt (published 2025-11-08), https://datareportal.com/reports/digital-2026-saudi-arabia (2025-11-08), https://datareportal.com/reports/digital-2026-united-arab-emirates (2025-11-05), https://datareportal.com/reports/digital-2026-jordan (2025-11-08), https://datareportal.com/reports/digital-2026-lebanon (2025-11-08). Pages were read through a summarising fetch tool: re-open them before quoting a figure in a client deck.
- Wikipedia, Public holidays in Egypt, read 2026-10-19: https://en.wikipedia.org/wiki/Public_holidays_in_Egypt (secondary source; holiday rules).
- DLA Piper, Data protection laws in Egypt, last modified 2026-02-13: https://www.dlapiperdataprotection.com/index.html?t=law&c=EG
- Platform files cited above (their Egypt notes and sources).
- Everything labelled heuristic or unverified is not sourced.
