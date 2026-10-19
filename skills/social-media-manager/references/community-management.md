# Community management
Purpose: answer, moderate and escalate comments, reviews and messages consistently, with reply templates in English and Egyptian Arabic.
Last updated: 2026-10-19

Nothing here is sent without approval: replies are drafted in the reply-pack format from SKILL.md (comment, proposed reply, risk tag, action) unless the user built an approved automation (`automation-recipes.md`). Templates use `[placeholders]`; never put customer personal data in public replies, logs or prompts beyond what is needed.

## 1. Response-time targets (heuristics)
Platform windows are rules (messaging windows, API limits: `platforms/whatsapp.md`, `platforms/instagram.md`, `platforms/facebook.md` section 8); the targets below are practitioner heuristics to adjust with the account's own data.
| Channel | First reply target (business hours) | Notes |
|---|---|---|
| WhatsApp / Messenger / Instagram DM | 15 min to 1 h | Reply inside the customer-service window; after it only approved templates (WhatsApp) |
| Public comments, questions | within 4 h | Same day for questions with purchase intent |
| Public comments, praise | within 24 h | Reply to a sample, not necessarily all |
| Complaints (any channel) | within 1 h acknowledge, resolve or hand off within 1 working day | Move details to private |
| Reviews (Google Business Profile, Facebook) | within 48 h | `platforms/google-business-profile.md` |
| X mentions, Threads replies | within 2 h during campaigns | Public, fast, short |
| Reddit, Discord, Telegram groups | same day | Follow each community's norms |
| Crisis | see `crisis-playbook.md` | Fixed update times, one approver |
Out of hours: auto-acknowledge only where the platform allows it and say when a human replies. Never promise a time you cannot meet.

## 2. Triage tags
Tag every item before replying.
| Tag | Meaning | Examples | Action |
|---|---|---|---|
| ok | routine, low risk | praise, simple FAQ, emoji, general question | reply from templates; auto-draft allowed |
| sensitive | reputational, emotional, or factual risk | complaints, refunds, delivery issues, health or legal questions, religion/politics, a customer who is clearly upset, public criticism by a known account | human drafts or approves; use private channel; log |
| escalate | needs an owner now | safety injury, fraud/scam, hacked-account signs, leaked data, threat or self-harm language, minors at risk, press, legal letter, viral thread | stop templates; notify owner; see section 9 and `crisis-playbook.md` |
Rules: when unsure, tag one level up. Never auto-reply to `sensitive` or `escalate`. Self-harm or abuse content: do not debate; follow the platform's report path and escalate to the owner (section 8).

## 3. Tone rules
1. Human, specific, short. Use the customer's name if public. One apology, not three.
2. Match language and script: Arabic comment gets Arabic; Arabizi comment gets Arabic script by default (`content-craft.md` section 6).
3. Egyptian dialect for consumer channels; MSA for formal notices, press and legal-adjacent text.
4. Do not argue, sarcasm, blame the customer or reveal private details publicly.
5. Do not promise what is not in policy: refunds, dates, compensation, medical outcomes.
6. Point to a private channel for details; never ask for card numbers, passwords or codes (`platforms/whatsapp.md` section 7 payment note).
7. Disclose automation where the platform or law requires and offer a human (`platforms/instagram.md` section 6).
8. Emoji: max one, none on complaints or serious topics.
9. Sign with the agent's first name only when the brand does that; keep a consistent persona.

## 4. Reply templates
Replace placeholders; keep the language of the commenter. Editable copy lives in `../templates/reply-library.md`.
**1. Praise**
EN: "Thank you, [name]! This made our day. We'll pass it on to the team."
AR: "شكرًا يا [اسم]، كلامك فرّحنا جدًا وهنوصله للفريق كله."
**2. Price question** (tag ok)
EN: "Thanks for asking! [Product] is [price], including [what]. Prices can change, so please check [link]. Want details on DM?"
AR: "أهلًا بيك! [المنتج] بـ [السعر] شامل [كذا]. الأسعار ممكن تتغير فياريت تتأكد من [اللينك]، ولو حابب نبعتلك التفاصيل على الخاص قولنا."
**3. Complaint, public first reply** (sensitive)
EN: "We're sorry, [name], this isn't the experience we want for you. Please send your order number by DM and [owner] will look into it [today/within X]."
AR: "آسفين جدًا يا [اسم]، ده مش المستوى اللي عايزينه ليك. ابعتلنا رقم الطلب على الخاص و[الاسم] هيتابع معاك [النهارده/خلال كذا]."
**4. Delivery delay** (sensitive)
EN: "Sorry for the delay. Your order is [status], new expected date [date]. We'll update you by [time] on DM."
AR: "معلش على التأخير. طلبك دلوقتي [الحالة] والمتوقع يوصل [التاريخ]. هنبعتلك تحديث على الخاص قبل [الوقت]."
**5. Refund request** (sensitive)
EN: "We're sorry it didn't work out. Refunds follow our policy: [link]. DM your order number and we'll start the review; it usually takes [X] working days."
AR: "آسفين إن التجربة ماكانتش زي ما تتمنى. الاسترجاع بيمشي حسب السياسة دي: [اللينك]. ابعتلنا رقم الطلب على الخاص وهنبدأ المراجعة، وغالبًا بتاخد [X] أيام عمل."
**6. Spam / off-topic promo** (ok; usually no reply, hide and report; use only if a real partner posted by mistake)
EN: "Thanks, but we keep comments on topic, so we've removed this. For partnerships, email [address]."
AR: "شكرًا، بس بنحافظ إن التعليقات تكون على موضوع البوست فمسحنا ده. لو في تعاون ابعتلنا على [الإيميل]."
**7. Troll or insult** (sensitive; one calm reply or none)
EN: "We're glad to hear feedback shared respectfully. Insults are removed. If you have a real concern, DM us and we'll help."
AR: "بنرحب بأي رأي بشرط الاحترام، والإساءة بتتمسح. لو عندك مشكلة حقيقية ابعتلنا على الخاص ونساعدك."
**8. Scam impersonator** (escalate)
EN: "Our only official accounts are [list]. We never ask for payment, codes or passwords by DM. If someone did, please report that account and message us here."
AR: "حساباتنا الرسمية الوحيدة هي [القائمة]. إحنا عمرنا ما بنطلب فلوس أو أكواد أو باسوورد في الرسايل. لو حد طلب منك كده بلّغ عن الحساب وكلمنا هنا."
**9. Medical or legal question** (sensitive)
EN: "We can't give medical/legal advice here. Please ask a doctor/pharmacist/lawyer. For product information see [link]."
AR: "مقدرش نديك نصيحة طبية/قانونية هنا، فياريت تسأل دكتور/صيدلي/محامي. ولمعلومات عن المنتج شوف [اللينك]."
**10. Press inquiry** (escalate)
EN: "Thanks for reaching out. Please email [press address] with your outlet, deadline and questions; [name] will reply within [time]."
AR: "شكرًا على تواصلك. ابعت على [إيميل الصحافة] اسم الجهة والموعد النهائي والأسئلة، و[الاسم] هيرد عليك خلال [المدة]."
**11. Job seeker** (ok)
EN: "Thanks for your interest! Please apply here: [careers link]. We can't review CVs by DM."
AR: "شكرًا على اهتمامك! قدّم من هنا: [لينك الوظائف]. للأسف مش بنراجع السير الذاتية على الخاص."
**12. Partnership or collaboration** (sensitive)
EN: "Thanks! Please email a short brief (who you are, your audience, the idea) to [address]. We reply within [X] days."
AR: "شكرًا! ابعت لنا نبذة قصيرة (مين حضرتك، جمهورك، الفكرة) على [الإيميل] وهنرد خلال [X] أيام."
**13. Out of hours**
EN: "Thanks for your message. We're back at [time] and will reply then."
AR: "شكرًا على رسالتك. هنرجع [الوقت] وهنرد عليك وقتها."
**14. Stock or availability**
EN: "[Product] is [in stock/out of stock]. [Restock date if confirmed, else 'We'll post when it's back']."
AR: "[المنتج] [متاح/غير متاح] دلوقتي. [التاريخ لو مؤكد، أو: هننزل إعلان أول ما يرجع]."
**15. Correcting our own mistake**
EN: "Correction: we said [X] earlier; the right information is [Y]. Sorry for the confusion."
AR: "تصحيح: قلنا قبل كده [X] والمعلومة الصح هي [Y]. آسفين على اللخبطة."
**16. Asking permission to reuse a customer's post**
EN: "This is great, [name]! May we share it on our page with credit? Reply 'yes' or DM us."
AR: "ده جميل يا [اسم]! ممكن نشره على صفحتنا مع ذكر اسمك؟ رد بـ 'ماشي' أو ابعتلنا على الخاص."
**17. Customer shared personal data in a public comment**
EN: "Thanks! For your privacy please don't share phone numbers or addresses in comments; we've hidden this and will DM you."
AR: "شكرًا! حفاظًا على خصوصيتك مفيش داعي تكتب رقم تليفون أو عنوان في الكومنتات، خبّينا الرسالة وهنكلمك على الخاص."
**18. Negative review reply (Google/Facebook)**
EN: "Thank you for the feedback, [name]. We're sorry about [issue in general terms]. Please contact us at [channel] so we can make it right." (no private details, no offers in public; `platforms/google-business-profile.md` section 7)
AR: "شكرًا على ملاحظاتك يا [اسم]. آسفين بخصوص [المشكلة بشكل عام]. من فضلك كلمنا على [القناة] علشان نحل الموضوع."

## 5. Hide vs delete vs report vs block
| Action | Use when | Not when | Keep |
|---|---|---|---|
| Reply | genuine question, praise, valid complaint | trolling | reply link in log |
| Hide (comment hidden for others) | spam, repeated insults, personal data of others, off-topic promos | legitimate criticism | screenshot |
| Delete | doxxing, hate, threats (after saving evidence), our own error | critical but civil comments (deleting looks like cover-up) | screenshot, time, reason |
| Report | scam, impersonation, hate, child safety, copyright misuse | simple disagreement | report reference, platform path |
| Mute/restrict | repeat nuisance without clear violation (where the platform offers it) | threats | note |
| Block/ban | repeated harassment, scammers, persistent spam, threats | one-off rude comment | evidence and reason |
Per-platform tools differ: see section 6/10 of the platform file (Instagram `Restrict`, YouTube moderation status in `platforms/youtube.md` section 8, Reddit mod tools in `platforms/reddit.md`).
Publish a short house-rules text (be respectful, no spam, no personal data, no insults) in the bio/pinned post/group rules so moderation is predictable.

## 6. Moderating groups, channels and Discord
- Facebook Groups, Telegram groups, Discord servers: write rules (5 to 8 lines), assign 2+ moderators, set join questions, slow mode where available, keep a mod log. API limits and bot rules: `platforms/messaging-and-community-channels.md`, `platforms/telegram.md` section 8.
- Escalation ladder for members: gentle reminder, delete + warning, timeout/mute, ban with reason. Document each step.
- Bots help with spam filters and welcome messages; they must not run unofficial self-bots (`platforms/messaging-and-community-channels.md` section 8).
- Admin-only announcement channels: check the post twice; edits and deletions are visible.
- Reddit: you are a guest in other communities; read each subreddit's rules, disclose affiliation (Brand Affiliate tag, `platforms/reddit.md` section 7), no astroturfing.
- Rewards for participation (roles, shout-outs) are fine; paid or incentivised engagement must follow `compliance-and-ethics.md`.

## 7. DMs and WhatsApp
- Message people only after they contacted you or opted in; keep proof of opt-in (source, time, wording). Marketing without consent is a legal and account risk (`compliance-and-ethics.md` section 6).
- Respect the messaging windows and templates: free-form replies only inside the window, approved templates outside it (`platforms/whatsapp.md` section 8, `platforms/instagram.md` section 8, `platforms/facebook.md` section 8).
- First automated message: say it is automated, offer a human, state hours.
- Keep payment and identity details out of chat: no card numbers, passwords, OTP codes; send people to the secure checkout.
- WhatsApp groups and broadcast lists for customers: only with consent; give an easy exit; no adding people without asking.
- Voice notes: allowed and common in Egypt; transcribe key points to the log (`egypt-mena-playbook.md` section 4).
- Rate-limit all bulk sending; never use unofficial WhatsApp tools (`platforms/whatsapp.md` section 8 "Forbidden automation").

## 8. Minors and harassment
- Under-13s are not allowed on most platforms; if a child or a teen appears to be in trouble, do not engage in a public thread; report via the platform's child-safety path, escalate to the owner, and preserve evidence. Details per platform: section 6 of each platform file.
- Never solicit personal data from a minor; stop a promotion thread where a minor appears to be entering without a guardian (`compliance-and-ethics.md` section 7).
- Harassment of staff or customers: document, hide/restrict, report, block; give staff a break rota and a way to say stop; no retaliation in public.
- Threats of violence or self-harm: do not reply with a template; escalate immediately; follow the platform's emergency reporting and, for credible threats, the local authority path chosen by the owner. This skill gives no legal or clinical advice.

## 9. Hand-off to a human
Hand off when: tag is escalate; the customer asks for a human; two replies did not resolve; money, health, legal, safety or press is involved; the sentiment is rising; a template does not fit.
Hand-off note (one message): channel and link, customer first name or handle only, issue in one line, what was already said, deadline, risk tag, suggested next step. Tell the customer who will contact them and when, using a window you can meet. Platform handover rules for bots: `platforms/instagram.md` section 8 and `platforms/facebook.md` section 8 (human-agent tag).

## 10. Logging
Log every moderated or escalated item in a sheet or ticket: date, platform, item link, tag, action, owner, outcome, time to first reply, time to resolve. Rules: store the minimum personal data; no ID numbers, payment data or health details; keep screenshots of abusive content only as long as needed; delete on schedule. Review weekly: top 5 recurring questions (turn into content or FAQ), slowest replies, repeat offenders, template gaps. Feed counts into the monthly report (`analytics-and-reporting.md` section 4).

## 11. Sources
- Platform files linked above.
- Response-time targets and reply wording are practitioner heuristics (unsourced); Arabic templates are Egyptian dialect drafts, have a native reviewer check tone before use.
