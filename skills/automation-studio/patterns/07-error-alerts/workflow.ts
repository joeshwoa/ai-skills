// Level 3 · ONE error workflow for all your flows. In every production workflow:
// Settings → Error workflow → "Error alerts". When any of them fails, this runs:
// format a clear alert (which flow, which node, message, link) → Telegram + email; repeated
// failures of the same node within a run are reported once.
import { workflow, node, trigger, expr } from '@n8n/workflow-sdk';

const onError = trigger({ type: 'n8n-nodes-base.errorTrigger', version: 1, config: { name: 'On workflow error', parameters: {} } });

const format = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Format alert', parameters: { mode: 'runOnceForAllItems', jsCode: `
const e = $input.first().json;
const wf = e.workflow || {};
const ex = e.execution || {};
const err = ex.error || e.trigger?.error || {};
const node = ex.lastNodeExecuted || err.node?.name || 'trigger';
const msg = (err.message || 'Unknown error').slice(0, 500);
const when = new Date().toISOString().replace('T', ' ').slice(0, 16) + ' UTC';
const severity = /401|403|credential|auth/i.test(msg) ? 'AUTH' : /timeout|ECONN|ETIMEDOUT|429|rate/i.test(msg) ? 'TRANSIENT' : 'BUG';
return [{ json: {
  severity, workflow: wf.name || wf.id, node, message: msg, url: ex.url || null, mode: ex.mode || null,
  text: [\`🚨 \${severity} — \${wf.name || wf.id}\`, \`Node: \${node}\`, \`Error: \${msg}\`, ex.url ? \`Open: \${ex.url}\` : '', when]
        .filter(Boolean).join('\\n'),
} }];` } },
});

const telegram = node({
  type: 'n8n-nodes-base.telegram', version: 1.2,
  config: { name: 'Alert on Telegram', parameters: { resource: 'message', operation: 'sendMessage',
    chatId: expr('{{ $env.ALERT_TELEGRAM_CHAT_ID }}'), text: expr('{{ $json.text }}'), additionalFields: { appendAttribution: false } },
    onError: 'continueRegularOutput' },
});

const email = node({
  type: 'n8n-nodes-base.gmail', version: 2.2,
  config: { name: 'Alert by email', parameters: { resource: 'message', operation: 'send', sendTo: 'ops@example.com',
    subject: expr('[n8n {{ $("Format alert").item.json.severity }}] {{ $("Format alert").item.json.workflow }} failed'),
    emailType: 'text', message: expr('{{ $("Format alert").item.json.text }}'), options: { appendAttribution: false } },
    onError: 'continueRegularOutput' },
});

export default workflow('error-alerts', 'Error alerts')
  .add(onError).to(format).to(telegram).to(email);
