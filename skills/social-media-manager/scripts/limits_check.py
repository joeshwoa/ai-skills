#!/usr/bin/env python3
"""Check a draft post against per-platform limits stored in data/limits/*.json.

Usage:
  limits_check.py PLATFORM [--field caption|post|title|bio|comment] [--file F | --text T]
  limits_check.py --list
  limits_check.py --merge            # writes data/platform-limits.json
  limits_check.py PLATFORM --formats # prints the format table

Reads the draft from --file, --text or stdin. Exit code 0 = pass/warn, 1 = hard error.
Limits that are null in the data are reported as "unknown", never guessed.
Characters are Unicode code points; fields documented as byte-limited are checked
in UTF-8 bytes (Arabic is 2 bytes per character).
"""
import argparse, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
LIMITS = os.path.join(DATA, "limits")
BYTE_FIELDS = {("youtube", "caption")}
FIELD_KEY = {
    "caption": ["caption_max_chars", "post_max_chars"],
    "post": ["post_max_chars", "caption_max_chars"],
    "title": ["title_max_chars"],
    "bio": ["bio_max_chars"],
    "comment": ["comment_max_chars"],
}
HASHTAG = re.compile(r"(?<!\w)#[\w؀-ۿ]+", re.UNICODE)
MENTION = re.compile(r"(?<!\w)@[\w.]+", re.UNICODE)
URL = re.compile(r"https?://\S+|www\.\S+", re.I)
ARABIC = re.compile(r"[؀-ۿ]")
LATIN = re.compile(r"[A-Za-z]")
BAIT = re.compile(r"(?i)\b(like (and|&) share|tag (3|three|5) friends|follow for follow|f4f|l4l|dm for)\b|اعمل لايك|تابعني وهتابعك")


def load(platform):
    p = os.path.join(LIMITS, platform + ".json")
    if not os.path.exists(p):
        names = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(LIMITS, "*.json")))
        sys.exit("Unknown platform '%s'. Known: %s" % (platform, ", ".join(names)))
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("platform", nargs="?")
    ap.add_argument("--field", default="caption", choices=list(FIELD_KEY))
    ap.add_argument("--file")
    ap.add_argument("--text")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--formats", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.list or a.merge:
        allp = {}
        for f in sorted(glob.glob(os.path.join(LIMITS, "*.json"))):
            d = json.load(open(f, encoding="utf-8"))
            allp[d["platform"]] = d
        if a.list:
            for k, d in allp.items():
                print("%-34s verified %s" % (k, d.get("verified")))
        else:
            out = os.path.join(DATA, "platform-limits.json")
            json.dump({"generated_from": "data/limits/*.json", "platforms": allp},
                      open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("wrote", os.path.normpath(out), "(%d platforms)" % len(allp))
        return 0

    if not a.platform:
        ap.error("platform required")
    d = load(a.platform)
    if a.formats:
        for f in d["formats"]:
            print(json.dumps(f, ensure_ascii=False))
        return 0

    if a.text is not None:
        text = a.text
    elif a.file:
        text = open(a.file, encoding="utf-8").read()
    else:
        text = sys.stdin.read()
    text = text.rstrip("\n")

    t = d["text"]
    res = {"platform": a.platform, "field": a.field, "verified": d.get("verified"),
           "errors": [], "warnings": [], "info": []}
    limit = next((t.get(k) for k in FIELD_KEY[a.field] if t.get(k) is not None), None)
    n_chars, n_bytes = len(text), len(text.encode("utf-8"))
    if limit is None:
        res["info"].append("no verified %s limit in data for %s (unknown, not guessed)" % (a.field, a.platform))
    else:
        by_bytes = (a.platform, a.field) in BYTE_FIELDS
        used = n_bytes if by_bytes else n_chars
        unit = "bytes" if by_bytes else "chars"
        if used > limit:
            res["errors"].append("%s is %d %s, limit %d" % (a.field, used, unit, limit))
        elif used > 0.9 * limit:
            res["warnings"].append("%s uses %d of %d %s (>90%%)" % (a.field, used, limit, unit))
        else:
            res["info"].append("%s: %d of %d %s" % (a.field, used, limit, unit))

    tags = HASHTAG.findall(text)
    hm = t.get("hashtags_max")
    if hm is not None and len(tags) > hm:
        res["errors"].append("%d hashtags, platform allows %d" % (len(tags), hm))
    elif len(tags) > 10:
        res["warnings"].append("%d hashtags: most platforms reward few, relevant tags" % len(tags))
    mm = t.get("mentions_max")
    if mm is not None and len(MENTION.findall(text)) > mm:
        res["errors"].append("more mentions than the platform allows (%d)" % mm)

    urls = URL.findall(text)
    if urls and t.get("links_clickable_in_post") is False:
        res["warnings"].append("links are not clickable in this field; use bio/link-in-bio or a link sticker")
    if urls and a.platform == "x-twitter":
        res["warnings"].append("on X, posts containing a URL cost more through the API (see platform file)")
    if ARABIC.search(text) and LATIN.search(text):
        res["warnings"].append("mixed Arabic/Latin: check RTL ordering of hashtags, numbers and links in the preview")
    if BAIT.search(text):
        res["warnings"].append("engagement-bait phrasing; most platforms demote or remove it")
    if not text.strip():
        res["errors"].append("empty draft")
    if d.get("unverified"):
        res["info"].append("%d fact(s) for this platform are marked unverified in data; re-check on publish day" % len(d["unverified"]))

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, tag in (("errors", "ERROR"), ("warnings", "WARN"), ("info", "info")):
            for m in res[k]:
                print("%-5s %s" % (tag, m))
        print("RESULT:", "FAIL" if res["errors"] else "PASS")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
