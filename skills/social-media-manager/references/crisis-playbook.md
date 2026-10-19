# Crisis playbook
Purpose: act in the first hour and afterwards when something goes wrong in public: severity levels, checklists, statements, scenarios, recovery and post-mortem.
Last updated: 2026-10-19

Speed matters less than accuracy, but silence with scheduled cheerful posts is the worst option. Nothing is published or deleted on the user's behalf without approval; in a crisis the owner or approver named below signs off every public statement. Legal advice is out of scope: bring counsel for data breaches, injury, regulatory and defamation issues.

## 1. Severity levels
| Level | Definition | Examples | Response |
|---|---|---|---|
| S1 minor | one-off negative comment or error, no spread | a wrong price in one post, a rude comment | fix, reply, log (`community-management.md`) |
| S2 notable | spreading or touching trust, still contained to one platform | complaint thread with quotes/shares, review bombing starts, offensive reply by a team member | owner informed within 1 h; pause scheduled content on that platform; holding statement if asked |
| S3 serious | multi-platform spread, press, legal or regulator interest, customer harm risk | viral negative video, impersonation scam targeting customers, product complaint with injury claim, data exposure | owner + decision-maker now; pause all scheduled posts and ads; statement; daily updates; counsel |
| S4 emergency | physical safety, large breach, account takeover with abusive posts, threats | product recall, hacked official account posting scams, leaked customer data, a staff safety threat | stop everything; emergency contacts; platform escalation; authorities per counsel |
Re-rate every 2 hours in S3/S4: up, down or stay.

## 2. First-hour checklist (S2 and above)
1. Name one incident owner (decides), one approver for statements, one scribe (logs times and actions). Three people maximum in the core group.
2. Pause: scheduled posts and queued automations on affected platforms (use the kill switch in `automation-recipes.md` section 3), paid ads on the topic, auto-replies, giveaways in progress. Check that nothing tone-deaf is scheduled in the next 48 h.
3. Capture evidence: screenshots with URL and time, copy of the original post, the comment thread, account activity logs.
4. Verify facts: what happened, who is affected, what is confirmed vs rumour, what the company did. Write 3 columns: known, not known, to check by [time].
5. Decide posture (section 3): apologise, correct, explain, or stay silent.
6. Publish a holding statement within the hour if the issue is public and affects customers; no speculation.
7. Brief the team and the customer support team: approved wording, who answers press, what not to say, escalate everything unusual.
8. Switch moderation on: comment filters/hide words, slower replies via templates labelled sensitive, DMs handled by humans only.
9. Set the update schedule (for example every 2 to 4 hours for S3/S4, daily afterwards) and keep it.
10. Log everything in the incident log (section 8).

## 3. Apologise, correct or stay silent
- Apologise (specific, brief, with what changes) when: the brand or an employee did the wrong thing, a customer was harmed, a mistake was ours. Do not apologise for facts that are false; correct them.
- Correct when: a rumour or false claim spreads. Give evidence, once, calmly, on the channel where it spreads; do not quote-shame the person.
- Explain (without excuses) when: a delay, outage or policy needs context. Lead with what the customer can do now.
- Stay silent when: it is a troll or a tiny audience (S1), the issue is a private dispute better handled in DM, a legal process prevents comment (say "we cannot comment on ongoing proceedings" only if counsel agrees), or the topic is a national or religious tragedy the brand has nothing to do with: pause content instead.
- Never: delete criticism wholesale, buy or fake positive reviews, argue with influencers, blame customers, attack a competitor, or use a crisis to promote offers.

## 4. Statement templates
Placeholders in brackets. Approver reads aloud before posting. Arabic is Egyptian dialect for consumer channels; use MSA for press statements.
**Holding statement**
EN: "We are aware of [issue]. We are looking into it now and will share an update by [time]. If you are affected, please contact [channel]."
AR: "عرفنا بموضوع [المشكلة] وبنراجعه حاليًا. هننشر تحديث قبل [الوقت]. لو حضرتك متأثر بالموضوع كلمنا على [القناة]."
**Apology**
EN: "We got this wrong. [What happened, in one sentence.] We are sorry. Here is what we are doing: [action 1], [action 2]. If you were affected, contact [channel] and we will [remedy]."
AR: "إحنا غلطنا في [الحاجة]. [اللي حصل في جملة واحدة]. آسفين جدًا. وده اللي بنعمله: [إجراء ١]، [إجراء ٢]. لو حصلك ضرر كلمنا على [القناة] وهنعمل [التعويض/الحل]."
**Correction**
EN: "Correction: [claim] is not accurate. [Fact, with evidence]. Thank you to everyone who asked."
AR: "تصحيح: المعلومة اللي بتتداول عن [الموضوع] مش دقيقة. الحقيقة إن [الوقائع مع الدليل]. شكرًا لكل اللي سأل."
**Update**
EN: "Update [n] at [time]: [what changed]. Next update by [time]."
AR: "تحديث [رقم] الساعة [الوقت]: [الجديد]. التحديث الجاي قبل [الوقت]."
**Resolved / closing**
EN: "This issue is resolved. [What we fixed.] [What changes from now.] Thank you for your patience."
AR: "الموضوع اتحل. [اللي صلحناه]. [اللي هيتغير من دلوقتي]. شكرًا على صبركم."
**Product safety notice**
EN: "Safety notice: please stop using [product, batch] and contact [channel] for [refund/replacement/inspection]. [Short reason]."
AR: "إشعار سلامة: من فضلكم وقفوا استخدام [المنتج/التشغيلة] وكلمونا على [القناة] علشان [الاسترجاع/الاستبدال/الفحص]. [سبب مختصر]."
**Account compromised**
EN: "Our account was accessed without permission. Please ignore posts or messages from [time] to [time] and do not click links or send money. We are securing it and will confirm when it is safe."
AR: "حسابنا اتفتح من غير إذن مننا. تجاهلوا أي بوستات أو رسايل من [الوقت] لـ [الوقت] ومتضغطوش على لينكات ولا تبعتوا فلوس. بنأمّن الحساب وهنأكد لما يبقى سليم."
**Data exposure notice** (counsel reviews first)
EN: "We found that [type of data, no detail beyond need] may have been accessed on [date]. What we know: [..]. What to do: [change password/ignore suspicious messages]. Contact: [channel]."
AR: "اكتشفنا إن [نوع البيانات] ممكن يكون اتشاف يوم [التاريخ]. اللي نعرفه: [..]. المطلوب منك: [تغيير الباسوورد/تجاهل الرسايل المشبوهة]. للتواصل: [القناة]."

## 5. Scenarios
**Hacked account**
1. Use the platform's official recovery and security paths from a trusted device; tell the platform in-app (section 6). Do not pay "recovery" services (`platforms/tiktok.md` impersonation case, `platforms/pinterest.md` case).
2. Remove unknown logins and connected apps and schedulers, change passwords, enable two-factor, rotate API tokens and webhook secrets, revoke the workflow credentials in n8n/Make.
3. Post the account-compromised notice from another official channel; pin it when access returns.
4. Delete malicious posts after capturing evidence; check DMs sent; report scam links.
**Leaked data**
1. Contain: revoke access, rotate secrets, stop the exposing system. 2. Counsel and the data owner decide on notifications. Egypt: the Personal Data Protection Law is summarised by DLA Piper as requiring notice to the Personal Data Protection Centre within 72 hours and to data subjects within 3 days of the Centre notice; GDPR has a 72-hour authority notice for EU data. Treat as unverified until counsel confirms (`compliance-and-ethics.md` section 6). 3. Publish the data exposure notice only after approval; do not post affected people's details.
**Offensive or erroneous post by the brand**
Take it down only after screenshot; replace with the apology (not a silent delete if it already spread); check scheduled queue; review the approval process (release gate in `compliance-and-ethics.md` section 11). If an employee posted from a personal account about work, treat as S2 and involve HR.
**Product safety issue**
Safety first: product safety notice, stop promotion of the item, route all complaints to humans, preserve batch information, involve the safety/legal owner and regulators as counsel advises. Do not minimise or argue about causation online.
**Viral negative thread**
Check if the core claim is true. If true: apologise and act; if partly: correct the facts and own the real part; if false: provide evidence once. Reply under the original thread, then move to DM. Do not buy comments, use sock puppets or ask staff to flood replies. Keep an update cadence.
**Review bombing** (Google, Facebook, app stores, Trustpilot-type sites)
Collect samples (dates, text, reviewer names); report reviews that break policy via the platform tool (there is no API to remove others' reviews, `platforms/google-business-profile.md` section 8); reply once to genuine experiences; do not ask friends to post positive reviews or gate who is asked (policy and consumer-law risk).
**Impersonation / scam accounts**
Screenshot URL and profile, report via the platform path, post "our only official accounts" (template 8 in `community-management.md`), warn customers by email/WhatsApp opt-in list, pin warning in bio. See impersonation cases in `platforms/instagram.md` section 10, `platforms/tiktok.md`, `platforms/x-twitter.md`.
**Platform outage or API failure**
Not reputational by default; if scheduled content failed, publish a manual notice, run the failure alert path (`automation-recipes.md` section 8).

## 6. Recovery and appeal paths (by platform)
Open the platform file section 10 (cases) and section 6 (enforcement). One careful appeal beats many.
| Platform | Where |
|---|---|
| Facebook / Meta | `platforms/facebook.md` section 10 (restriction cases), Business Support Home |
| Instagram | `platforms/instagram.md` section 10 (restricted, copyright, impersonator) |
| WhatsApp | `platforms/whatsapp.md` sections 6 and 10 (enforcement ladder, appeals, template issues) |
| TikTok | `platforms/tiktok.md` section 10 |
| YouTube | `platforms/youtube.md` sections 6 and 10 (strikes, claims) |
| LinkedIn | `platforms/linkedin.md` section 10 |
| X | `platforms/x-twitter.md` section 10 |
| Threads | `platforms/threads.md` section 10 |
| Reddit | `platforms/reddit.md` section 10 |
| Snapchat | `platforms/snapchat.md` section 10 |
| Pinterest | `platforms/pinterest.md` section 10 |
| Telegram | `platforms/telegram.md` section 10 (@SpamBot, abuse contacts) |
| Google Business Profile | `platforms/google-business-profile.md` section 10 |
| Discord and DM channels | `platforms/messaging-and-community-channels.md` section 10 |
Common rules from those files: stop automation first; never create a replacement account to bypass enforcement; do not appeal repeatedly with copied text; keep the notice text, date and screenshots; use official channels only.

## 7. Recovery
- Day 0 to 2: stabilise (statements, support surge, no promotional posts).
- Day 3 to 7: show the fix (what changed), publish proof where relevant, thank people who helped, resume normal content gradually, keep sensitive topics out of humour.
- Week 2 to 4: monitor sentiment and search for the issue; refresh the reputation assets (GBP replies, pinned FAQ); keep the update promise until closed.
- Rebuild: restart automation only after the root cause is fixed and the approver re-enables it.

## 8. Incident log and post-mortem template
Incident log (live): time | event | source/link | decision | by | next check.
Post-mortem (within 5 working days, blameless):
1. Summary (what happened, severity, duration).
2. Timeline (first signal, detection, first action, statement time, resolution).
3. Impact (reach, complaints, sentiment, sales, accounts affected).
4. Root cause and contributing factors (process, tool, person, platform).
5. What worked / what did not.
6. Actions: owner, deadline, check (for example approval step added, token rotation, template updated, drill scheduled).
7. Statement review: was it fast, accurate, kind?
8. Update this playbook and the reply library.
Run a 30-minute crisis drill each quarter (`strategy-and-planning.md` section 8).

## 9. Sources
- Platform files linked above.
- Egypt breach-notice summary: DLA Piper, "Data protection laws in Egypt", last modified 2026-02-13, https://www.dlapiperdataprotection.com/index.html?t=law&c=EG (secondary summary, read 2026-10-19; confirm with counsel).
- GDPR 72-hour notice: Regulation (EU) 2016/679 Article 33, not re-fetched this session (unverified here).
- Severity levels and timings are practitioner heuristics.
