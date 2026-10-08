// Level 1–2 · Webhook → clean → validate → Google Sheets → reply (200 / 400)
// POST /webhook/lead  {"name": "...", "email": "...", "phone": "...", "source": "..."}
import { workflow, node, trigger, ifElse, expr } from '@n8n/workflow-sdk';

const leadIn = trigger({
  type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Lead webhook', parameters: { httpMethod: 'POST', path: 'lead', responseMode: 'responseNode', options: {} } },
});

const clean = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Clean lead', parameters: {
    mode: 'manual',
    assignments: { assignments: [
      { id: 'n', name: 'name', value: expr('{{ ($json.body.name || "").trim() }}'), type: 'string' },
      { id: 'e', name: 'email', value: expr('{{ ($json.body.email || "").trim().toLowerCase() }}'), type: 'string' },
      { id: 'p', name: 'phone', value: expr('{{ ($json.body.phone || "").replace(/[^0-9+]/g, "") }}'), type: 'string' },
      { id: 's', name: 'source', value: expr('{{ $json.body.source || "website" }}'), type: 'string' },
      { id: 't', name: 'received_at', value: expr('{{ $now.toISO() }}'), type: 'string' },
    ] },
    options: {},
  } },
});

const valid = ifElse({ version: 2.3, config: { name: 'Valid email?', parameters: {
  conditions: {
    combinator: 'and',
    options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 },
    conditions: [{ id: 'c1', leftValue: expr('{{ $json.email }}'), rightValue: '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$',
                   operator: { type: 'string', operation: 'regex' } }],
  },
  options: {},
} } });

const saveRow = node({
  type: 'n8n-nodes-base.googleSheets', version: 4.7,
  config: { name: 'Add to Leads sheet', parameters: {
    resource: 'sheet', operation: 'append',
    documentId: { __rl: true, mode: 'list', value: '', cachedResultName: 'Leads' },
    sheetName: { __rl: true, mode: 'name', value: 'Leads' },
    columns: { mappingMode: 'defineBelow',
      value: { name: expr('{{ $json.name }}'), email: expr('{{ $json.email }}'), phone: expr('{{ $json.phone }}'),
               source: expr('{{ $json.source }}'), received_at: expr('{{ $json.received_at }}') },
      schema: [
        { id: 'name', displayName: 'name', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
        { id: 'email', displayName: 'email', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
        { id: 'phone', displayName: 'phone', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
        { id: 'source', displayName: 'source', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
        { id: 'received_at', displayName: 'received_at', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
      ] },
    options: {},
  } },
});

const ok = node({
  type: 'n8n-nodes-base.respondToWebhook', version: 1.5,
  config: { name: 'Reply 200', parameters: { respondWith: 'json', responseBody: expr('{{ { ok: true, email: $("Clean lead").item.json.email } }}'), options: { responseCode: 200 } } },
});

const bad = node({
  type: 'n8n-nodes-base.respondToWebhook', version: 1.5,
  config: { name: 'Reply 400', parameters: { respondWith: 'json', responseBody: '={{ { ok: false, error: "invalid email" } }}', options: { responseCode: 400 } } },
});

export default workflow('lead-to-sheet', 'Lead webhook → Google Sheets')
  .add(leadIn)
  .to(clean)
  .to(valid.onTrue(saveRow.to(ok)).onFalse(bad));
