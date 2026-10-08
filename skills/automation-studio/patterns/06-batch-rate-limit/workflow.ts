// Level 3 · Bulk job without hitting rate limits: accept the job (reply 202 at once) → split the list
// → batches of 10 → call the API per item (errors don't stop the run) → pause 1 s between batches
// → when done: count successes/failures → report.
import { workflow, node, trigger, splitInBatches, nextBatch, expr } from '@n8n/workflow-sdk';

const job = trigger({
  type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Bulk job', parameters: { httpMethod: 'POST', path: 'bulk-notify', responseMode: 'responseNode', options: {} } },
});

const accepted = node({
  type: 'n8n-nodes-base.respondToWebhook', version: 1.5,
  config: { name: 'Reply 202 accepted', parameters: { respondWith: 'json',
    responseBody: expr('{{ { accepted: ($json.body.contacts || []).length } }}'), options: { responseCode: 202 } } },
});

const each = node({
  type: 'n8n-nodes-base.splitOut', version: 1,
  config: { name: 'One item per contact', parameters: { fieldToSplitOut: 'body.contacts', options: {} } },
});

const batches = splitInBatches({ version: 3, config: { name: 'Batches of 10', parameters: { batchSize: 10, options: {} } } });

const call = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'Notify contact', parameters: {
    method: 'POST', url: 'https://httpbin.org/post',
    sendBody: true, contentType: 'json', specifyBody: 'keypair',
    bodyParameters: { parameters: [
      { name: 'to', value: expr('{{ $json.phone }}') },
      { name: 'text', value: expr('Hi {{ $json.name }}, your order is ready.') },
    ] },
    options: { timeout: 15000, response: { response: { neverError: true, fullResponse: true } } },
  }, onError: 'continueRegularOutput', retryOnFail: true, maxTries: 2 },
});

const pause = node({
  type: 'n8n-nodes-base.wait', version: 1.1,
  config: { name: 'Pause 1 s', parameters: { resume: 'timeInterval', amount: 1, unit: 'seconds' } },
});

const summary = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Count results', parameters: { mode: 'runOnceForAllItems', jsCode: `
const all = $input.all();
const ok = all.filter(i => (i.json.statusCode ?? 200) < 400 && !i.json.error).length;
return [{ json: { total: all.length, ok, failed: all.length - ok,
  text: \`Bulk notify finished: \${ok}/\${all.length} sent, \${all.length - ok} failed.\` } }];` } },
});

const report = node({
  type: 'n8n-nodes-base.slack', version: 2.7,
  config: { name: 'Report on Slack', parameters: { resource: 'message', operation: 'post', select: 'channel',
    channelId: { __rl: true, mode: 'name', value: '#ops' }, text: expr('{{ $json.text }}'), otherOptions: {} } },
});

export default workflow('batch-rate-limit', 'Bulk job in rate-limited batches')
  .add(job).to(accepted).to(each)
  .to(batches
    .onDone(summary.to(report))
    .onEachBatch(call.to(pause).to(nextBatch(batches))));
