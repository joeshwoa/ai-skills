# stock-library — tool reference

Generated from studio-mcp (`call.sh help <tool>` shows the same). Flags: **N** internet · **$** may spend (needs OK) · **I** installs (needs OK).

## stock (5)

### `stock_credits`

Write CREDITS.md (human-readable) and credits.txt (paste into a video/post description) from the
project's stock_credits.json — every stock item downloaded with stock_download/stock_icon, grouped
by provider, with REQUIRED attributions first, licence names + links, and any special terms (share-alike,
NASA insignia rules…). Regenerates both files each time from the ledger. Returns the credit text in data.

Arguments: `project: str = ''`; `out: str = ''`

### `stock_download` [N]

Download stock items found by stock_search (ids like "pexels:123", or the result numbers of the last
search like "3") into projects/<project>/stock/<kind>/<provider>-<title>.<ext>, each with a
<file>.license.json sidecar (licence, attribution, source URLs, date) and an entry in the project's
stock_credits.json (feed stock_credits). quality: best | 4k | hd (≤1080p / ≤1920 px photos) | sd (≤720p).
For video the closest rendition is chosen (mp4/H.264 preferred); for photos the largest ≤ max_width.
Every file is verified (ffprobe for video/audio, Pillow for images) and shown on a contact sheet (LOOK).
Unsplash download pings are sent as its API requires. Non-commercial items from a commercial=true search
are refused unless allow_noncommercial=true.

Arguments: `ids: list[str]`; `quality: str = 'best'`; `max_width: int = 0`; `allow_noncommercial: bool = False`; `project: str = ''`; `out: str = ''`

### `stock_icon` [N]

Find and download open-source icons from Iconify (200 000+ icons, 150+ sets: Material, Tabler,
Phosphor, Lucide, MDI…) as SVG plus a transparent PNG at `size` px, with the icon set's licence in a
sidecar and the project's stock_credits.json. query: words ("coffee cup") or an exact "prefix:name"
("mdi:coffee"). color: hex like "#C8102E" (applies to single-colour icons). count: how many of the best
matches to download. Returns the files, a preview, and (for word queries) a numbered sheet of other
matches with their exact names (data.alternatives) so you can pick a different style.

Arguments: `query: str`; `color: str = ''`; `size: int = 512`; `count: int = 1`; `project: str = ''`; `out: str = ''`

### `stock_search` [N]

Search FREE stock media across every free stock site with an official API and show a numbered,
labelled contact sheet to pick from (LOOK at it). kind: video | photo | illustration | vector | music |
sfx | icon | any. Providers fan out in parallel: videos from Pexels, Coverr, Pixabay, Wikimedia Commons,
NASA, Internet Archive; photos from Unsplash, Pexels, Pixabay, Openverse, Wikimedia, NASA; music from
Jamendo, Freesound, Openverse, Internet Archive; sfx from Freesound, Openverse, NASA…; icons from Iconify.
Keyless providers always work; keyed ones (free keys) join once the user adds them (see stock_sources).
orientation: landscape | portrait | square. min/max_duration in seconds, min_width in px.
commercial=true (default) keeps only licences allowing commercial use AND edits. providers: "auto" or
a comma list (e.g. "pexels,wikimedia"). Write queries in ENGLISH (Arabic is passed through but most
APIs index English). Returns data.results (n, id, size, duration, licence, attribution…) — pass ids
(or the numbers) to stock_download.

Arguments: `query: str`; `kind: str = 'video'`; `orientation: str = ''`; `count: int = 12`; `min_duration: float = 0`; `max_duration: float = 0`; `min_width: int = 0`; `commercial: bool = True`; `providers: str = 'auto'`; `page: int = 1`; `project: str = ''`; `out: str = ''`

### `stock_sources`

Which free stock providers are active right now (keyless ones always; keyed ones once the user adds a
free key), what each gives, licence + attribution rules, rate limits, and step-by-step "get a free key"
instructions for each keyed provider (Pexels, Pixabay, Unsplash, Coverr, Freesound, Jamendo). Also creates
STUDIO_HOME/keys.json with EMPTY entries for missing names, so the user only pastes keys in (existing
values are never touched or shown). Call this before telling the user a provider is unavailable.

Arguments: 
