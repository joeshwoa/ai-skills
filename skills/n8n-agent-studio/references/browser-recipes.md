# Browser recipes (browserd)

A recipe is JSON: `{"name","description","steps":[…]}`. Steps run top to bottom in one browser page. Stored by name in `recipes/` (skill) or
`~/.local/share/ai-skills/browserd/recipes/` (yours, wins). n8n calls `POST /run {"recipe_name","vars","session"}` → `{ok,status,data,files,url,ms,error,shot}`.
`{{var}}` = a value from `vars`; `{{secret:NAME}}` = a secret (never leaves browserd; scrubbed from output).

## Steps
| step | example | notes |
|---|---|---|
| goto | `{"goto":"{{url}}"}` | domain must be in `--allow`; HTTP ≥400 fails unless `allow_error` |
| click | `{"click":true,"selector":"#go","expect_navigation":true}` | or `"text":"Sign in"` / `"ref":"e12"`; `nth` for the n-th match |
| fill / type | `{"fill":true,"selector":"#user","value":"{{secret:USER}}"}` | `type` types key by key (for inputs that listen to keystrokes) |
| press | `{"press":"Enter"}` | optional selector |
| select / check / uncheck / hover | `{"select":true,"selector":"#country","value":"EG"}` | |
| wait | `{"wait":"#results"}` · `{"wait":1500}` · `{"wait":"network_idle"}` · `{"wait":true,"text":"Done"}` · `{"wait":true,"url":"/dashboard"}` | prefer waiting for an element |
| extract | `{"extract":true,"name":"orders","selector":"tr.order","fields":{"id":".oid","link":"a.view@href"},"append":true,"required":true}` | rows→list of records; single value without `fields`; `multiple:true` for list of texts; `@attr` for attributes |
| table | `{"table":"#orders","name":"rows"}` | header→cell dicts |
| text | `{"text":true,"selector":"h1","name":"title"}` | |
| paginate | `{"paginate":true,"next":"a.next","max":20,"steps":[…]}` | stops when the button is gone/disabled; `page` var available |
| repeat | `{"repeat":true,"max":10,"until_missing":".spinner","steps":[…]}` | `i` var |
| if | `{"if":".captcha","then":[…],"else":[…]}` · `missing` instead of exists | |
| assert | `{"assert":"#orders","message":"login failed"}` · `url_contains` / `text_contains` / `missing` | fail loudly, never return empty |
| download | `{"download":true,"selector":"#export","name":"o.csv","as":"file"}` | file path returned in `files` |
| upload | `{"upload":true,"selector":"input[type=file]","path":"/path"}` | |
| screenshot | `{"screenshot":"before-submit","full":true}` | path in `files` |
| scroll | `{"scroll":true,"times":5,"by":2000}` | infinite lists |
| pause_for_human | `{"pause_for_human":true,"message":"solve the captcha"}` | headless → returns `status:"needs_human"` (+screenshot); headed → waits for `until_selector` |
| set | `{"set":true,"name":"x","value":"…"}` | variables |
| eval | `{"eval":"document.title"}` | **off** unless `--allow-eval`; only code you wrote |

## Selectors that survive redesigns
Priority: `[data-testid]`/`[data-*]` > stable ids > `aria-label`/`name`/`placeholder` > visible text (`text`) > short semantic CSS (`table#orders tr.order`) > never `nth-child`, generated class hashes (`.css-1x2y3z`), or XPath through 8 divs.
Iframes: Playwright chains work in selectors, e.g. `iframe[name=app] >> #save`. Shadow DOM is pierced automatically. Hidden-until-hover menus: `hover` first.

## Making recipes robust
- **Assert at checkpoints** (after login, after each page) — a silent empty result is the worst failure.
- Return `required:true` on the extract the whole run exists for.
- One recipe = one job. Compose in n8n (login recipe → job recipes in the same `session`).
- Idempotency lives in n8n: key each row by id, dedupe with *Remove Duplicates* / DB upsert, so re-runs are safe.
- Rate: `pause` in `paginate`, a `wait` between actions that hit the server; never parallelise the same session.
- Selector drift alert: n8n error branch → notify with the `shot` screenshot; optional "repair" sub-flow: AI Agent re-discovers the element via /observe and proposes a new selector (human approves the recipe edit).

## Sessions & logins
`nx login URL --session shop` opens a visible Chrome with the persistent profile `sessions/shop`; the user signs in (2-step included) and closes it. Recipes pass `"session":"shop"`.
Expired? The recipe's `if` on the login form → `pause_for_human` → n8n notifies "re-login needed". Never script password typing for sites with 2-step; for plain logins `{{secret:…}}` is allowed if the user stored it.
One session = one browser context = one page at a time (calls are serialised). Use several session names for parallel accounts.

## Attach mode
`nx chrome` → start Chrome with `--remote-debugging-port=9222 --user-data-dir=<dedicated>` → `nx start --allow … --cdp http://127.0.0.1:9222`. Recipes act in that visible window.

## Agent loop (observe / act)
`POST /observe {"session","url"?}` → `{title,url,headings,text,elements:[{ref,tag,label,href…}]}` (password fields never show values). `POST /act {"session","action":{"type":"click|fill|press|select|goto|scroll","ref":"e7","value":"…"}}`
→ result + fresh observation. Refs are only valid until the page changes — observe again. After a successful agent run, turn the path into a recipe.
