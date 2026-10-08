// Level 4 · Document AI: invoice PDF URL in → download → extract text → AI pulls structured fields
// → CODE re-checks the maths (never trust the model on numbers) → valid: append to Sheets, invalid:
// flag for review → reply with the result.
import { workflow, node, trigger, ifElse, languageModel, expr, newCredential } from '@n8n/workflow-sdk';

const intake = trigger({
  type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Invoice URL', parameters: { httpMethod: 'POST', path: 'invoice', responseMode: 'responseNode', options: {} } },
});

const fetchFile = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'Download PDF', parameters: { method: 'GET', url: expr('{{ $json.body.file_url }}'),
    options: { response: { response: { responseFormat: 'file', outputPropertyName: 'data' } }, timeout: 30000 } } },
});

const toText = node({
  type: 'n8n-nodes-base.extractFromFile', version: 1.1,
  config: { name: 'PDF to text', parameters: { operation: 'pdf', binaryPropertyName: 'data', options: {} } },
});

const model = languageModel({
  type: '@n8n/n8n-nodes-langchain.lmChatOpenAi', version: 1.3,
  config: { name: 'OpenAI model', parameters: { model: { __rl: true, mode: 'list', value: 'gpt-4.1-mini' }, options: { temperature: 0 } },
            credentials: { openAiApi: newCredential('OpenAI') } },
});

const extract = node({
  type: '@n8n/n8n-nodes-langchain.informationExtractor', version: 1.2,
  config: { name: 'Extract invoice fields', parameters: {
    text: expr('{{ $json.text }}'),
    schemaType: 'fromJson',
    jsonSchemaExample: '{ "invoice_no": "INV-1", "date": "2026-01-31", "supplier": "Name", "subtotal": 100.0, "vat": 14.0, "total": 114.0, "currency": "EGP", "lines": [{ "item": "Paper", "qty": 1, "amount": 100.0 }] }',
    options: { systemPromptTemplate: 'Extract the invoice fields exactly as printed. Numbers as plain numbers (no thousands separators). If a field is missing use null.' },
  }, subnodes: { model: model } },
});

const check = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Check the maths', parameters: { mode: 'runOnceForEachItem', jsCode: `
const inv = $json.output || $json;
const n = v => (v === null || v === undefined || v === '') ? null : Number(String(v).replace(/,/g, ''));
const sub = n(inv.subtotal), vat = n(inv.vat), total = n(inv.total);
const lines = Array.isArray(inv.lines) ? inv.lines : [];
const linesSum = lines.reduce((s, l) => s + (n(l.amount) || 0), 0);
const problems = [];
if (!inv.invoice_no) problems.push('missing invoice number');
if (total === null) problems.push('missing total');
if (sub !== null && vat !== null && total !== null && Math.abs(sub + vat - total) > 0.01) problems.push(\`subtotal + VAT = \${(sub + vat).toFixed(2)} ≠ total \${total}\`);
if (lines.length && sub !== null && Math.abs(linesSum - sub) > 0.01) problems.push(\`lines sum \${linesSum.toFixed(2)} ≠ subtotal \${sub}\`);
return { json: { invoice_no: inv.invoice_no, date: inv.date, supplier: inv.supplier, subtotal: sub, vat, total,
  currency: inv.currency || 'EGP', valid: problems.length === 0, problems: problems.join('; '), source: $('Invoice URL').item.json.body.file_url } };` } },
});

const valid = ifElse({ version: 2.3, config: { name: 'Valid?', parameters: {
  conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 },
    conditions: [{ id: 'v', leftValue: expr('{{ $json.valid }}'), rightValue: '', operator: { type: 'boolean', operation: 'true', singleValue: true } }] },
  options: {} } } });

const save = node({
  type: 'n8n-nodes-base.googleSheets', version: 4.7,
  config: { name: 'Append to Invoices', parameters: { resource: 'sheet', operation: 'append',
    documentId: { __rl: true, mode: 'list', value: '', cachedResultName: 'Invoices' },
    sheetName: { __rl: true, mode: 'name', value: 'Invoices' },
    columns: { mappingMode: 'autoMapInputData', value: {}, schema: [] }, options: {} } },
});

const flag = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Flag for review', parameters: { mode: 'manual', includeOtherFields: true,
    assignments: { assignments: [{ id: 'f', name: 'status', value: 'needs-review', type: 'string' }] }, options: {} } },
});

const done = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply saved',
  parameters: { respondWith: 'json', responseBody: expr('{{ { ok: true, invoice_no: $("Check the maths").item.json.invoice_no, total: $("Check the maths").item.json.total } }}'), options: { responseCode: 200 } } } });
const review = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply needs review',
  parameters: { respondWith: 'json', responseBody: expr('{{ { ok: false, problems: $json.problems } }}'), options: { responseCode: 422 } } } });

export default workflow('document-extraction', 'Invoice PDF → AI fields → checked → Sheets')
  .add(intake).to(fetchFile).to(toText).to(extract).to(check)
  .to(valid.onTrue(save.to(done)).onFalse(flag.to(review)));
