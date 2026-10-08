// Level 5 · ORCHESTRATOR: weekly → list customers → call the "Score customer" sub-workflow once per
// customer (reusable, testable on its own, its own error handling) → aggregate → one report.
// Deploy the sub-workflow FIRST; `autokit deploy` resolves workflowId "name:Score customer (sub-workflow)"
// to the real id on the target instance.
import { workflow, node, trigger, expr } from '@n8n/workflow-sdk';

const weekly = trigger({
  type: 'n8n-nodes-base.scheduleTrigger', version: 1.4,
  config: { name: 'Every Monday 08:00', parameters: { rule: { interval: [{ field: 'weeks', weeksInterval: 1, triggerAtDay: [1], triggerAtHour: 8 }] } } },
});

const list = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'List customers', parameters: { method: 'GET', url: 'https://dummyjson.com/users',
    sendQuery: true, queryParameters: { parameters: [{ name: 'limit', value: '5' }, { name: 'select', value: 'id,email' }] }, options: {} } },
});

const each = node({ type: 'n8n-nodes-base.splitOut', version: 1,
  config: { name: 'One per customer', parameters: { fieldToSplitOut: 'users', options: {} } } });

const call = node({
  type: 'n8n-nodes-base.executeWorkflow', version: 1.4,
  config: { name: 'Score customer', parameters: {
    mode: 'each', source: 'database',
    workflowId: { __rl: true, mode: 'id', value: 'name:Score customer (sub-workflow)' },
    workflowInputs: { mappingMode: 'defineBelow',
      value: { customer_id: expr('{{ $json.id }}'), email: expr('{{ $json.email }}') },
      matchingColumns: [], schema: [
        { id: 'customer_id', displayName: 'customer_id', required: false, defaultMatch: false, display: true, canBeUsedToMatch: true, type: 'number' },
        { id: 'email', displayName: 'email', required: false, defaultMatch: false, display: true, canBeUsedToMatch: true, type: 'string' }] },
    options: { waitForSubWorkflow: true },
  }, onError: 'continueRegularOutput' },
});

const report = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Build report', parameters: { mode: 'runOnceForAllItems', jsCode: `
const rows = $input.all().map(i => i.json).filter(r => r.tier);
const by = t => rows.filter(r => r.tier === t).length;
const failed = $input.all().length - rows.length;
const top = [...rows].sort((a, b) => b.spent - a.spent).slice(0, 3).map(r => \`\${r.email} (\${r.spent})\`);
return [{ json: { scored: rows.length, failed, gold: by('gold'), silver: by('silver'), bronze: by('bronze'), new: by('new'),
  text: \`Weekly customers: \${rows.length} scored\${failed ? ', ' + failed + ' failed' : ''} — gold \${by('gold')}, silver \${by('silver')}, bronze \${by('bronze')}. Top: \${top.join(', ')}\` } }];` } },
});

const post = node({ type: 'n8n-nodes-base.slack', version: 2.7, config: { name: 'Post report', parameters: { resource: 'message', operation: 'post',
  select: 'channel', channelId: { __rl: true, mode: 'name', value: '#sales' }, text: expr('{{ $json.text }}'), otherOptions: {} } } });

export default workflow('orchestrator', 'Weekly customer scoring (orchestrator)')
  .add(weekly).to(list).to(each).to(call).to(report).to(post);
