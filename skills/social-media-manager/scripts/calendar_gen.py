#!/usr/bin/env python3
"""Generate a content calendar (CSV or JSON) with a daily platform rotation.

Example:
  calendar_gen.py --start 2026-11-01 --weeks 4 \
      --plan instagram:5,facebook:4,tiktok:4,linkedin:3,x-twitter:7 \
      --pillars "educate,proof,behind-the-scenes,offer,community" \
      --tz Africa/Cairo --skip 2026-11-06 --format csv > calendar.csv

Rules baked in (override with flags):
  * posts-per-week per platform are spread across weekdays, never twice the same
    day for one platform unless the count exceeds 7;
  * pillars rotate round-robin so the same pillar is not posted twice in a row
    on one platform;
  * every 5th post per platform is tagged "offer" slot unless --no-offer-slot;
  * format suggestion per platform comes from FORMATS below (edit to taste);
  * slot times are placeholders (heuristic); replace with the account's own insights.
Output columns: date,weekday,time_local,platform,pillar,format,status,notes
Nothing here posts anything; hand the file to n8n/Make or a human scheduler.
"""
import argparse, csv, datetime as dt, json, sys

FORMATS = {
    "instagram": ["reel", "carousel", "reel", "story-set", "image"],
    "facebook": ["video", "image", "link-or-text", "reel"],
    "tiktok": ["video", "video", "photo-mode", "video"],
    "linkedin": ["text", "document-carousel", "video", "text"],
    "x-twitter": ["post", "post", "thread", "post"],
    "threads": ["text", "text", "image"],
    "youtube": ["short", "short", "long-form"],
    "telegram": ["post", "post", "poll", "post"],
    "pinterest": ["pin", "video-pin", "pin"],
    "snapchat": ["story", "spotlight"],
    "reddit": ["discussion", "answer-thread"],
    "whatsapp": ["status", "channel-update"],
    "google-business-profile": ["update", "offer", "event"],
}
DEFAULT_TIME = {"linkedin": "09:00", "x-twitter": "12:00", "tiktok": "20:00", "instagram": "19:00",
                "facebook": "18:00", "telegram": "11:00", "youtube": "17:00", "threads": "13:00",
                "pinterest": "21:00", "snapchat": "20:30", "reddit": "10:00", "whatsapp": "10:30",
                "google-business-profile": "10:00"}


def spread(n):
    """Pick n weekday indexes (0=Mon) spread across the week."""
    if n >= 7:
        return list(range(7)) * (n // 7) + sorted(range(7), key=lambda d: d)[: n % 7]
    step = 7 / n
    return sorted({int(round(i * step)) % 7 for i in range(n)}) if n else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="YYYY-MM-DD (first day of the first week)")
    ap.add_argument("--weeks", type=int, default=4)
    ap.add_argument("--plan", required=True, help="platform:posts_per_week,... ")
    ap.add_argument("--pillars", default="educate,proof,behind-the-scenes,offer,community")
    ap.add_argument("--tz", default="Africa/Cairo")
    ap.add_argument("--skip", default="", help="comma list of YYYY-MM-DD with no posts (holidays, crisis pause)")
    ap.add_argument("--no-offer-slot", action="store_true")
    ap.add_argument("--format", choices=["csv", "json"], default="csv")
    a = ap.parse_args()

    start = dt.date.fromisoformat(a.start)
    skip = {dt.date.fromisoformat(s) for s in a.skip.split(",") if s}
    pillars = [p.strip() for p in a.pillars.split(",") if p.strip()]
    plan = {}
    for item in a.plan.split(","):
        k, _, v = item.partition(":")
        plan[k.strip()] = int(v or 3)

    rows, counters, last = [], {p: 0 for p in plan}, {}
    for w in range(a.weeks):
        for plat, per_week in plan.items():
            fm = FORMATS.get(plat, ["post"])
            for d in spread(per_week):
                day = start + dt.timedelta(days=7 * w + d)
                if day in skip:
                    continue
                i = counters[plat]
                counters[plat] += 1
                pillar = pillars[i % len(pillars)]
                if not a.no_offer_slot and (i + 1) % 5 == 0 and last.get(plat) != "offer":
                    pillar = "offer"
                last[plat] = pillar
                rows.append({"date": day.isoformat(), "weekday": day.strftime("%a"),
                             "time_local": DEFAULT_TIME.get(plat, "12:00") + " " + a.tz,
                             "platform": plat, "pillar": pillar, "format": fm[i % len(fm)],
                             "status": "idea", "notes": ""})
    rows.sort(key=lambda r: (r["date"], r["time_local"], r["platform"]))
    if a.format == "json":
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=1)
    else:
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()) if rows else ["date"])
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
