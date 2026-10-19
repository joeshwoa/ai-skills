# Email and WhatsApp marketing

Purpose: plan consent-based lifecycle messaging by email and WhatsApp (plus SMS caveats), with templates, deliverability basics, metrics and legal flags.
Last updated: 2026-10-19

Not legal advice. WhatsApp rules, limits, categories and prices change: read `../../social-media-manager/references/platforms/whatsapp.md` (Last verified 2026-10-19) and confirm in WhatsApp Manager or the official pricing page before quoting any price. Prices are deliberately not restated here.

## 1. Lifecycle map
| Stage | Trigger | Goal | Channel | Timing (heuristic) |
|---|---|---|---|---|
| Welcome | Opt-in / first purchase | Confirm consent, set expectations, one useful next step | Email, WhatsApp | Immediately, then day 2 to 3 |
| Nurture | Joined, not bought | Answer objections, show proof, one offer | Email (WhatsApp only if opted in for marketing) | 3 to 5 messages over 2 to 3 weeks |
| Cart / chat abandonment | Cart or inquiry left | Help finish; remove friction | Email, WhatsApp (utility/service window or opted-in template) | 1 to 24 hours, max 2 reminders |
| Order and delivery | Order placed | Confirm, reduce COD refusal, set delivery expectations | WhatsApp utility, email | Immediately and on each status |
| Post-purchase | Delivered | Usage tips, review request, cross-sell | Email, WhatsApp | Day 3 to 7 after delivery |
| Win-back | No purchase in N days | Re-engage or let go | Email, WhatsApp (opted in) | After a cycle longer than normal reorder time |
| Referral | Happy customer | Ask for referral with a fair, disclosed reward | Email, WhatsApp | After a positive moment (review, repeat order) |
| Sunset | Inactive after win-back | Stop sending to protect reputation | Email | After final attempt |
Map each to one metric and one owner. Start with three flows (welcome, order/confirmation, post-purchase) before building more.

## 2. List building with consent
- **Principle**: send only to people who asked to hear from you. Name the business and the kind of messages at the opt-in, one purpose per checkbox, no pre-ticked boxes, record source, timestamp and wording shown (WhatsApp file, section 7).
- **Ways to collect**: checkout checkbox, website form, QR code in shop or packaging, WhatsApp click-to-chat with an explicit "send me offers" quick reply, lead magnets (guide, sample, price list), event sign-up. Give a reason to join that matches what you will send.
- **Do not**: buy or rent lists, scrape numbers or emails, add chat contacts to broadcasts without a clear opt-in, reuse contest entrants' numbers without separate consent (WhatsApp file, section 6).
- **Double opt-in** for email (confirm address) reduces fake and mistyped addresses; Google's sender guidance asks senders to confirm each recipient before subscribing and to consider removing people who do not engage.
- **Egypt note**: Personal Data Protection Law No. 151 of 2020 requires explicit consent for direct electronic marketing, sender identity, a clear marketing label, an easy opt-out and consent records (DLA Piper summary recorded in the WhatsApp file); Anti-Cybercrime Law 175/2018 article 25 is cited for unsolicited marketing. Ask a lawyer about licensing for electronic marketing and about your specific setup.

## 3. Segmentation
Start simple, add only if it changes the message.
- By lifecycle (lead, first-time buyer, repeat buyer, lapsed).
- By interest or product category (from clicks, purchases, form answers).
- By language/dialect and city or delivery zone.
- By value (order size, frequency) for VIP treatment.
- By engagement (opened or read in last 30/90 days) for sending frequency and sunset rules.
Rule: a segment is only worth keeping if you will send it a different message or on a different schedule.

## 4. Email deliverability basics
Verified from Google's Email sender guidelines (support.google.com/a/answer/81126, read 2026-10-19; applies to personal Gmail recipients):
- **All senders**: set up SPF or DKIM; valid forward and reverse DNS (PTR) for sending IPs/domains; TLS; keep the spam rate reported in Postmaster Tools below 0.3 percent; format messages to RFC 5322; do not impersonate Gmail From: headers.
- **Bulk senders (more than 5,000 messages per day to Gmail)**: SPF, DKIM and DMARC for the sending domain (policy may be "none"); the From domain must align with the SPF or DKIM domain; marketing and subscribed messages must support one-click unsubscribe (the List-Unsubscribe and List-Unsubscribe-Post headers, RFC 8058) plus a visible unsubscribe link in the body.
- **DKIM**: key of 1024 bits or longer is required for personal Gmail recipients; 2048 bits recommended if the provider supports it.
- Messages must not mislead: no fake "Re:" or "Fwd:" subjects, no hidden content via HTML/CSS, clear sender identity, visible and understandable links.
- If you use an email service provider, verify it authenticates your domain with SPF and DKIM, and add its sending sources to your SPF record.
Operating practice (practitioner conventions; labelled):
- Send from a branded subdomain or domain you control, not a free mailbox, for marketing email.
- Warm up new domains with small, engaged segments before large sends.
- **List hygiene**: honour unsubscribes immediately, remove hard bounces, suppress addresses that never engage after a defined period, and never re-add unsubscribed people.
- Watch complaint rate, bounce rate, inbox placement tests and Postmaster Tools reputation; pause and fix when metrics worsen.
- Keep one clear call to action, plain text alternative, accessible images with alt text, balanced image-to-text ratio.
- Yahoo, Microsoft and other providers publish their own rules: `unverified` in this file; check each provider's sender page.

## 5. WhatsApp marketing at a high level
From the WhatsApp file (official sources recorded there). Check its `Last verified` date before relying on any number.
- **Opt-in**: businesses may only contact people who gave their number and agreed to receive messages from that business; the opt-in names the business; opt-outs must be honoured wherever made.
- **24-hour window**: free-form replies are allowed inside 24 hours of the customer's last message; outside it only approved templates can be sent.
- **Templates**: categories are marketing, utility and authentication; anything promotional or unclear is treated as marketing; Meta decides the category. Approved status is required before sending. Templates have format limits (body 1,024 characters and others in the WhatsApp file).
- **Quality**: user feedback and read rate drive a quality rating (green/yellow/red); low quality can pause templates or limit sending; blocks and reports hurt; cold-list sending is the fastest route to trouble.
- **Frequency**: Meta applies a per-user marketing limit based on engagement and does not publish the number; a practitioner heuristic is 2 to 4 marketing templates per opted-in user per month, one clear action per message, opt-out always visible.
- **Tooling**: the WhatsApp Business app suits small volume; the Cloud API (via a partner or direct) suits automation; use official routes only. No unofficial bulk-sender apps; they risk account bans and break the opt-in rule.
- **Operations**: reply SLA in minutes during business hours, owner rota, out-of-hours auto-reply, tags for source and stage. See `../../media-buying/references/mena-and-egypt-notes.md`, section 5, for click-to-WhatsApp handling.
- **Etiquette (Egypt, practitioner suggestions)**: greet in dialect, avoid 10 pm to 8 am Cairo time, Friday is the weekly day off, never use religion or politics to sell.

## 6. SMS caveats
- Use for time-critical utility (delivery, appointment) or where the customer chose SMS. For marketing SMS, consent and sender registration rules differ by country and operator; Egyptian rules and sender ID requirements are `unverified` in this skill. Ask the SMS provider and a lawyer.
- SMS has no read-quality feedback like WhatsApp, so frequency discipline and opt-out ("reply STOP" in Arabic and English) matter. Check Arabic (Unicode) message length: Unicode SMS fits fewer characters per segment, so cost per message can rise (practitioner knowledge; verify with the provider).

## 7. Templates: six key messages
Replace brackets; keep each under limits; WhatsApp templates must be approved. Mark the category the message likely needs; Meta decides.
**1. Welcome / opt-in confirmation (utility or service; marketing if it promotes)**
- EN: Welcome to [Brand]. You asked to get [offers/updates] on [channel]. We will send about [n] messages a month. Reply STOP any time to opt out.
- EG: أهلاً بيك في [البراند]. إنت طلبت توصلك [عروض/أخبار] على [القناة]. هنبعتلك حوالي [عدد] رسايل في الشهر. ابعت "إيقاف" في أي وقت وهنوقّف.
**2. Order confirmation (utility; reduces COD refusals)**
- EN: Hi [name], your order [#] ([item]) is received. Total [amount] EGP, cash on delivery. Reply YES to confirm or tell us what to change. Delivery in [days] days.
- EG: أهلاً [الاسم]، طلبك رقم [#] ([المنتج]) وصلنا. الإجمالي [المبلغ] جنيه كاش عند الاستلام. ابعت "تمام" عشان نأكد أو قولنا لو في تعديل. التوصيل خلال [عدد] أيام.
**3. Abandoned cart / unfinished inquiry (marketing unless inside 24-hour window)**
- EN: Hi [name], you left [item] in your cart. Need help with size, delivery or payment? Reply here and we will sort it. [Link]
- EG: أهلاً [الاسم]، سيبت [المنتج] في السلة. محتاج مساعدة في المقاس أو التوصيل أو الدفع؟ رد علينا هنا ونظبطها معاك. [لينك]
**4. Post-purchase and review request (marketing/utility mix; ask all customers, no incentive tied to a positive review)**
- EN: Hi [name], your [item] should have arrived. How is it going? If you have a minute, an honest review helps others: [link]. If something is wrong, reply here and we will fix it.
- EG: أهلاً [الاسم]، المفروض [المنتج] وصلك. عامل إيه؟ لو عندك دقيقة، رأيك الصريح بيساعد غيرك: [لينك]. ولو في أي مشكلة رد علينا هنا وهنحلها.
**5. Win-back (marketing; opted-in only)**
- EN: Hi [name], it has been a while. We added [new item/change]. Here is [real offer, valid until date]. Not interested? Reply STOP and we will not message again.
- EG: أهلاً [الاسم]، بقالنا فترة ما شفناكش. جبنا [الجديد]. وفي [عرض حقيقي لحد تاريخ]. لو مش مهتم ابعت "إيقاف" ومش هنبعتلك تاني.
**6. Referral (marketing; disclose the reward and conditions)**
- EN: Thanks for choosing [Brand]. Share your link with a friend: they get [benefit] and you get [benefit] after their first order. Terms: [link].
- EG: شكراً إنك اخترت [البراند]. ابعت اللينك ده لصاحبك: هو ياخد [ميزة] وإنت تاخد [ميزة] بعد أول طلب ليه. الشروط: [لينك].

## 8. Metrics and testing
- Email: delivered rate, bounce rate, complaint/spam rate, unsubscribe rate, click rate, conversion and revenue per recipient. Open rate is unreliable because mail clients can pre-load images (privacy features), so do not make decisions on opens alone (practitioner knowledge).
- WhatsApp: delivered, read, reply rate, opt-out/block rate, template quality rating, confirmation rate, revenue per message, first-reply time.
- Flow level: revenue per flow, conversion, time to second purchase.
- Testing: one variable at a time (subject or opening line, offer, send time, CTA), a hypothesis and a stop rule written first (`measurement.md`, section 5); test on a random split of the same segment; ignore tiny wins.

## 9. Legal and policy flags (checklist, not legal advice)
- Explicit consent and records; clear sender identity and marketing label; easy opt-out honoured at once; consent records retained as the law requires (Egypt per DLA Piper summary: three years after the last message).
- Licensing/permit requirements for electronic marketing in Egypt are reported in the summary: confirm with counsel.
- Cross-border data: do not export customer data to tools without checking transfer rules.
- Children's data is sensitive; do not market to minors.
- Sector rules (health, finance, education, real estate) restrict claims and messages.
- Platform policies: WhatsApp prohibits certain goods and services; buy-or-rent lists break opt-in.
- Misleading claims, fake scarcity, fake reviews and undisclosed partnerships are out of scope for this skill.
- EU/US rules (GDPR, ePrivacy, CAN-SPAM, TCPA) apply when you message people there: `unverified` here.

## Sources
- https://support.google.com/a/answer/81126 (Email sender guidelines, read 2026-10-19)
- `../../social-media-manager/references/platforms/whatsapp.md` (official WhatsApp/Meta sources listed in its section 13; DLA Piper Egypt summary: https://www.dlapiperdataprotection.com/index.html?t=law&c=EG)
- `../../media-buying/references/mena-and-egypt-notes.md` (sections 5 and 8)
- Unverified: Yahoo and Microsoft sender rules, Egyptian SMS sender registration, EU and US messaging law details.
