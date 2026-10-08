// Level 4 · Safe webhook for payments/orders: senders RETRY, so the same event can arrive twice.
// Require an idempotency key → n8n remembers keys it processed (Remove Duplicates, across executions)
// → new key: process + 201 · seen key: 200 {duplicate:true}, nothing processed again · no key: 400.
// Remove Duplicates v2 has TWO outputs: 0 = kept (new), 1 = discarded (seen before).
import { workflow, node, trigger, ifElse, expr } from '@n8n/workflow-sdk';

const hook = trigger({
  type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Order webhook', parameters: { httpMethod: 'POST', path: 'orders', responseMode: 'responseNode', options: {} } },
});

const key = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Read key', parameters: { mode: 'manual', assignments: { assignments: [
    { id: 'k', name: 'key', value: expr('{{ $json.headers["idempotency-key"] || $json.body.event_id || "" }}'), type: 'string' },
    { id: 'o', name: 'order', value: expr('{{ $json.body.order }}'), type: 'object' },
  ] }, options: {} } },
});

const hasKey = ifElse({ version: 2.3, config: { name: 'Has key?', parameters: {
  conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 },
    conditions: [{ id: 'h', leftValue: expr('{{ $json.key }}'), rightValue: '', operator: { type: 'string', operation: 'notEmpty', singleValue: true } }] },
  options: {} } } });

const firstTime = node({
  type: 'n8n-nodes-base.removeDuplicates', version: 2,
  config: { name: 'First time we see it?', parameters: {
    operation: 'removeItemsSeenInPreviousExecutions', logic: 'removeItemsWithAlreadySeenKeyValues',
    dedupeValue: expr('{{ $json.key }}'), options: { historySize: 10000 } } },
});

const fulfil = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'Send to fulfilment', parameters: {
    method: 'POST', url: 'https://httpbin.org/post', sendBody: true, contentType: 'json', specifyBody: 'json',
    jsonBody: expr('{{ JSON.stringify({ key: $json.key, order: $json.order }) }}'), options: { timeout: 20000 } },
    retryOnFail: true, maxTries: 3 },
});

const created = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 201',
  parameters: { respondWith: 'json', responseBody: expr('{{ { ok: true, key: $("Read key").item.json.key } }}'), options: { responseCode: 201 } } } });
const dup = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 200 duplicate',
  parameters: { respondWith: 'json', responseBody: expr('{{ { ok: true, duplicate: true, key: $("Read key").item.json.key } }}'), options: { responseCode: 200 } } } });
const bad = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 400',
  parameters: { respondWith: 'json', responseBody: '={{ { ok: false, error: "Idempotency-Key header or event_id required" } }}', options: { responseCode: 400 } } } });

export default workflow('idempotent-webhook', 'Idempotent order webhook')
  .add(hook).to(key)
  .to(hasKey
    .onTrue(firstTime)
    .onFalse(bad))
  .add(firstTime.output(0).to(fulfil).to(created))   // output 0 = keys never seen before
  .add(firstTime.output(1).to(dup));                 // output 1 = already processed (discarded) items
