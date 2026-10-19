# Content craft
Purpose: write hooks, captions, CTAs and Arabic copy that fit each platform, and turn one idea into many formats without pasting it.
Last updated: 2026-10-19

Limits (characters, hashtags, formats) are not repeated here: read section 3 of `platforms/<slug>.md` or run `python3 scripts/limits_check.py <platform> --field caption --file draft.txt`. Arabic examples below are Egyptian dialect unless marked MSA.

## 1. Hook patterns
The first line (or first 2 seconds of video) decides whether the rest is read. Write 5 hooks per idea, keep the best 2 for A/B across posts.
| Pattern | When | English example | Egyptian Arabic example |
|---|---|---|---|
| Result first | proof posts | "We went from 5 orders a day to 40. Here is the change." | "كنا بنبيع ٥ أوردرات في اليوم، دلوقتي ٤٠. غيرنا حاجة واحدة." |
| Mistake | educate | "The biggest caption mistake you do not notice." | "أكبر غلطة بتعملها في الكابشن وانت مش واخد بالك." |
| Number list | educate, saves | "3 things that save you an hour a day." | "٣ حاجات هتوفر عليك ساعة كل يوم." |
| Pain question | engagement | "Posting daily and nobody reacts?" | "بتنزل كل يوم ومحدش بيتفاعل؟" |
| Contrarian | LinkedIn, X, Threads | "You do not need to post every day." | "مش لازم تنزل كل يوم. دي الحقيقة." |
| Curiosity gap | video | "This is why your Reel stops at 300 views." | "ده السبب الحقيقي إن الريلز بتاعك بيقف عند ٣٠٠ مشاهدة." |
| Mini story | brand, LinkedIn | "Yesterday a customer sent us a message that changed our menu." | "إمبارح عميل بعتلنا رسالة غيّرت المنيو بتاعنا." |
| Callout | local, niche | "If you run a clinic in Nasr City, read this." | "لو عندك عيادة في مدينة نصر، ده ليك." |
| Show the outcome | demo | "Watch the difference in 10 seconds." | "شوف الفرق في ١٠ ثواني." |
| Myth vs fact | education, health-adjacent (needs proof) | "Myth: hashtags make you go viral." | "فكرة غلط: الهاشتاج لوحده هيعمل ترند." |
Rules:
- The hook must be true to the content; bait that the post does not pay off raises hides and unfollows (practitioner observation).
- Video: say or show the hook in the first 2 seconds, burn in captions (`platforms/tiktok.md`, `platforms/instagram.md` section 2 formats).
- Text posts: put the hook inside the visible preview length (feed truncation differs per platform; check section 2/3 of the platform file; Instagram file says first 125 characters).
- No fear, shame or fake urgency in health, finance or children's content (`compliance-and-ethics.md` section 7).

## 2. Caption structures
Pick one per post; do not stack.
1. Hook, value, CTA (default): line 1 hook; 3 to 5 short lines of value; last line one CTA.
2. Problem, agitate lightly, solution, proof, CTA: for offers; proof must exist.
3. Story: situation, turn, lesson, question; for LinkedIn/Facebook/Threads.
4. List: hook, numbered items one line each, "save this" CTA only if it is actually reference material.
5. Q&A: question quoted from a real customer (no names), answer, link to more.
6. Micro caption: 1 to 2 lines for strong visuals; put detail in the first comment or alt text.
Formatting rules: one idea per line break; no walls of text; emoji as bullets at most 3 per post; mixed-language lines kept short (section 6); put links and hashtags on their own lines.
Length rule of thumb (heuristic): Reels/TikTok/Shorts 1 to 3 lines; Instagram carousel 3 to 8 lines; LinkedIn 8 to 15 short lines; X one sentence plus link; Facebook 2 to 6 lines; Pinterest keyword-rich title and description (`platforms/pinterest.md`); Telegram/WhatsApp Channel short with a clear next step.

## 3. CTA rules
- One CTA per post. Ask for the action that matches the funnel stage (`strategy-and-planning.md` section 5): awareness = follow/save; consideration = comment a question/DM keyword; conversion = book/buy/WhatsApp.
- Say what happens next and what it costs: "DM us 'PRICE' and we reply within the day" (only promise a reply time you meet).
- Banned: "like and share to win", "tag 3 friends", follow-for-follow, engagement bait. `scripts/limits_check.py` flags common bait patterns; platforms demote or penalise engagement bait (see Meta's guidance in `platforms/facebook.md` section 5).
- Where links are not clickable (Instagram captions/comments, see `platforms/instagram.md` section 3), point to the bio, a Story sticker or a DM keyword.
- CTA wording Arabic: use the verb the user would say: "ابعتلنا رسالة", "احجز مكانك", "اكتب لنا في الكومنتات", "اضغط على اللينك في البايو". Avoid heavy MSA CTAs ("يرجى التواصل") on consumer channels.
- For comment-to-DM flows follow the platform's Private Replies limits and disclose automation (`platforms/instagram.md` case 10, `automation-recipes.md` recipe 3).

## 4. Repurposing matrix (one idea, many formats)
Idea example: "3 mistakes in product photos". Never paste the same text; change the hook, length and visual per platform. Check watermark and safe-area rules before cross-posting (`platforms/facebook.md`, `platforms/instagram.md` case 7).
| Target | Adaptation | Do not |
|---|---|---|
| Instagram Reel | 15 to 45 s, hook on screen, 3 mistakes as 3 beats, burned captions | reuse a watermarked TikTok file |
| TikTok | same script, native voice/trend-free first 2 s, search phrase spoken | add 30 hashtags |
| YouTube Short | add search-friendly title, loop ending | copy the TikTok title |
| LinkedIn | text or document carousel, "what I learned" framing, no @handles from other apps | paste the Reel link only |
| X | one sharp claim, image or clip, optional 3-post thread | exceed the post limit by splitting mid-sentence |
| Threads | conversational version, one topic tag | link-dump |
| Facebook | 2 to 4 line caption, native video, no external link in the first post if reach matters | duplicate on several Pages |
| Story (IG/FB/Snap) | one slide per mistake, poll or question sticker | long text slides |
| Telegram/WhatsApp Channel | short summary, key image, one link | send to non-opted-in numbers |
| Pinterest | vertical Pin with keyword title, 3-mistake graphic | generic image without keywords |
| Blog/GBP/Email | long version, or GBP "Update" post for local brands | promo in the GBP description |
Process: write the master (script + proof + 1 asset) once, produce per-platform variants from a post pack (`../templates/post-pack.md`), run limits check and checklist (section 12 of each platform file).

## 5. Accessibility
- Alt text on every image where the platform supports it: say what is shown and why it matters, 1 to 2 sentences, no "image of"; do not stuff keywords. Limits by platform: Instagram alt text in `platforms/instagram.md` section 3; Pinterest alt text in `platforms/pinterest.md`; X supports alt text (`platforms/x-twitter.md`).
- Captions/subtitles on all speech video, in the spoken language; for Egyptian Arabic voice use dialect captions word for word, max about 40 characters per line, 2 lines (practitioner standard). Platform caption features: see the platform files' format sections.
- Contrast: text on images at least 4.5:1 against its background (WCAG 2.1 AA for normal text); test brand colours before templating. Do not put key text in the bottom or side UI zones.
- Do not rely on colour or emoji alone to carry meaning; spell out numbers and prices; avoid flashing (more than 3 flashes per second) in video.
- CamelCase for multi-word English hashtags (#BrandNewDay) so screen readers read them as words; Arabic hashtags use underscore between words only if the platform accepts it (test).
- Audio: a caption or text version for voice-note-only content.

## 6. Arabic copy rules
Dialect choice:
- Egyptian audience, consumer brand: Egyptian dialect for captions, Reels voice, replies. Formal announcements, legal notices, health information, press: Modern Standard Arabic (MSA) or very light dialect.
- Pan-Arab audience: neutral "white" Arabic (MSA vocabulary with simple sentence shape) or separate Gulf/Levant versions written or reviewed by a native speaker; do not fake a dialect you cannot verify. Notes in `egypt-mena-playbook.md` section 2.
- Address gender neutrally when unknown: "تحب تعرف أكتر؟" rather than "عايز/عايزة".
- Egyptian markers that read natural: إزاي، دلوقتي، عايز، مش، كده، ده/دي، اللي. MSA markers to avoid in casual posts: كيف، الآن، أريد، لا، هكذا، هذا، الذي.
RTL traps (check the preview in the app before approving):
- Paragraphs take direction from the first strong character: start Arabic posts with Arabic, not a Latin brand name or number, or the line may align left.
- Numbers, percentages, parentheses and punctuation next to English words can jump position. Put prices as "٩٩ جنيه" or "99 جنيه" on a line that is entirely Arabic; use a right-to-left mark (U+200F) after a trailing English word if punctuation flips.
- URLs and hashtags: always on their own line; a URL in the middle of an Arabic sentence scrambles the order. Keep one language per hashtag (`platforms/instagram.md` section 11, `platforms/tiktok.md` section 11).
- Digits: Western (0-9) and Arabic-Indic (٠-٩) both read in Egypt. Pick one per brand; use Western digits for phone numbers, prices in links, and UTM; do not mix inside one price.
- Punctuation: Arabic comma ، and question mark ؟ are optional on social; be consistent.
- Diacritics (tashkeel): leave out except to resolve ambiguity; they break search and hashtag matching.
- Spelling variants split hashtags and searches: أ/إ/ا, ة/ه, ى/ي. Choose a canonical spelling for brand tags and keep it.
- Kashida (ـــ) and decorative stretching: avoid; screen readers read letters.
Arabizi (Arabic in Latin letters and numbers, e.g. 3 = ع, 7 = ح, 5 = خ): expect it in comments and DMs. Reply in Arabic script by default; mirror Arabizi only if the brand voice is deliberately youth-casual. Do not write ads in Arabizi unless the audience is explicitly that and the brand approves.
Emojis and religious wording: use sparingly and respectfully; avoid joking with religious phrases (`egypt-mena-playbook.md` section 7).

## 7. Hashtag and mention practice
- Caps and behaviour differ per platform; read section 3/5 of each file before choosing a number: Instagram `platforms/instagram.md` (strict low cap), Facebook `platforms/facebook.md` (guidance, no hard cap found), X `platforms/x-twitter.md` (guidance), Threads `platforms/threads.md` (topic tag), YouTube `platforms/youtube.md` (ignored if too many), TikTok `platforms/tiktok.md` (counts toward caption), LinkedIn `platforms/linkedin.md` (no official cap).
- Structure that works across platforms (practitioner): 1 brand tag, 1 campaign tag, 1 to 2 topic tags (one Arabic, one English if bilingual), 1 location tag when local.
- Hashtags describe the post; they do not create reach on their own (Instagram's head said so, reported in `platforms/instagram.md` section 5).
- Never hijack trending tags for sales; do not use unrelated tags; X treats it as spam (`platforms/x-twitter.md`).
- Mentions: tag only people/brands actually in the content, with their consent for partners; check the mention cap in the platform file; no mass tagging; thank collaborators in the first comment rather than tagging 20 accounts.
- Branded content needs the platform label plus a plain word (see `compliance-and-ethics.md` section 2).

## 8. First-comment usage
Use when: the platform hides links in captions, you want to keep the caption clean, or you add resources/credits.
- Put: link (with UTM), credits and collaborators, extra hashtags if still under the cap, a follow-up question.
- Timing: post immediately after publishing, from the brand account; pin it where the platform allows.
- Do not: hide disclosures or required legal text only in the first comment (disclose in the caption or video; `compliance-and-ethics.md` section 2); do not rely on it for key info because comments can be collapsed or filtered.
- Automation: allowed only through official comment endpoints, with logging (`automation-recipes.md`).

## 9. Evergreen vs timely content
| | Evergreen | Timely |
|---|---|---|
| Examples | how-tos, FAQs, explainers, case studies, Pins, long YouTube | news, events, Ramadan/Eid, drops, trends, outages |
| Shelf life | months | hours to weeks |
| Platforms that reward | YouTube, Pinterest, GBP, LinkedIn, blogs | X, TikTok, Stories, Threads |
| Workflow | write once, recycle every 60 to 90 days with new hook | plan the shell, fill the last 48 h, approval fast lane |
Mix rule (heuristic): 70% evergreen, 20% timely, 10% experiments. Timely posts need a named approver who can say yes within the hour and a kill switch (`crisis-playbook.md`). Reactive posts on tragedies or disputes: stay silent unless the brand is directly involved. Recycling: re-post the idea with a new hook and updated facts; delete or update posts with outdated prices or policies (`automation-recipes.md` recipe 5).

## 10. Copy checklist before it goes to approval
1. Does line 1 earn the next line, and is it true to the content?
2. One idea, one CTA, one audience?
3. Language and dialect match the audience; Arabic preview checked for RTL flips?
4. Numbers, prices, dates, phone numbers and links verified against the source of truth?
5. Hashtags and mentions within the platform file caps; none hijacked or unrelated?
6. Alt text and captions present; contrast checked?
7. Any claim (health, finance, results, "best", "guaranteed") has proof or is removed?
8. Disclosure present if paid, gifted, affiliate or own-brand ad where the platform requires?
9. Music, images, faces and customer words cleared (`compliance-and-ethics.md` section 5)?
10. UTM added (`scripts/utm.py`) and limits check run?
Fail any item: fix before approval, do not note it for later.

## 11. Sources
- Platform files linked above, each with sources.
- WCAG 2.1 contrast ratio 4.5:1 for normal text: https://www.w3.org/TR/WCAG21/#contrast-minimum (standard, not re-fetched this session).
- Arabic RTL and dialect guidance: practitioner observation, not an official rule.
