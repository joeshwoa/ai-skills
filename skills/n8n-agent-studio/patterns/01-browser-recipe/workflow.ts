// Level 3 · "A site with no API": n8n calls the local browser worker (browserd) with a RECIPE and gets structured rows back.
//   POST /webhook/web-run   {"vars": {"base": "http://127.0.0.1:7799"}}      (swap the Webhook for a Schedule Trigger in production)
// browserd holds the recipe by name (recipes/__RECIPE__.json — secrets stay on that side as {{secret:NAME}}), does the clicking (headless Chrome, saved login profile, domain allow-list); n8n does everything after: branching,
// retries, sinks (Sheets/DB/Slack…), alerts. Needs-human (captcha / 2-step login) is a first-class outcome, not an error.
import { workflow, node, trigger, ifElse, expr } from '@n8n/workflow-sdk';

const hook = trigger({
  type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Run request', parameters: { httpMethod: 'POST', path: '__PATH__', responseMode: 'responseNode', options: {} } },
});

const run = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'Run recipe in browser', parameters: {
    method: 'POST', url: '__BROWSERD__/run', sendBody: true, specifyBody: 'json',
    jsonBody: expr('{{ JSON.stringify({ recipe_name: "__RECIPE__", vars: $json.body.vars || {}, session: "__SESSION__" }) }}'),
    options: { timeout: 180000 },
  }, onError: 'continueRegularOutput', retryOnFail: true, maxTries: 2, waitBetweenTries: 3000 },
});

const ok = ifElse({ version: 2.3, config: { name: 'Recipe ok?', parameters: {
  conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'loose', version: 2 },
    conditions: [{ id: 'o', leftValue: expr('{{ $json.ok }}'), rightValue: true, operator: { type: 'boolean', operation: 'true', singleValue: true } }] },
  options: {} } } });

const human = ifElse({ version: 2.3, config: { name: 'Needs a human?', parameters: {
  conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'loose', version: 2 },
    conditions: [{ id: 'h', leftValue: expr('{{ $json.status }}'), rightValue: 'needs_human', operator: { type: 'string', operation: 'equals' } }] },
  options: {} } } });

const shape = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Rows', parameters: { mode: 'runOnceForAllItems', language: 'javaScript',
    jsCode: `// browserd returns {ok, data:{<name>: [...]}, files, url, ms}. One n8n item per row of the first list found.
const d = $input.first().json;
const key = Object.keys(d.data || {}).find(k => Array.isArray(d.data[k]));
const rows = key ? d.data[key] : [d.data];
return rows.map(r => ({ json: { ...r, _source_url: d.url } }));` } },
});

// ↓ Replace with your destination: Google Sheets / Postgres / Slack / Notion … (see automation-studio/references/platforms.md)
const sink = node({ type: 'n8n-nodes-base.noOp', version: 1, config: { name: 'Destination (replace me)', parameters: {} } });

const summary = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Summary', parameters: { mode: 'runOnceForAllItems', language: 'javaScript',
    jsCode: `return [{ json: { ok: true, count: $input.all().length, sample: $input.all().slice(0, 3).map(i => i.json) } }];` } },
});

const replyOk = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 200',
  parameters: { respondWith: 'json', responseBody: expr('{{ $json }}'), options: { responseCode: 200 } } } });
const replyHuman = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 202 needs human',
  parameters: { respondWith: 'json', responseBody: expr('{{ { needs_human: true, message: $json.error, screenshot: $json.shot } }}'), options: { responseCode: 202 } } } });
const replyErr = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 502',
  parameters: { respondWith: 'json', responseBody: expr('{{ { ok: false, error: $json.error || "browser worker unreachable" } }}'), options: { responseCode: 502 } } } });

export default workflow('browser-recipe', 'Site without API → browserd recipe → rows')
  .add(hook)
  .to(run)
  .to(ok.onTrue(shape.to(sink).to(summary).to(replyOk)).onFalse(human.onTrue(replyHuman).onFalse(replyErr)));
