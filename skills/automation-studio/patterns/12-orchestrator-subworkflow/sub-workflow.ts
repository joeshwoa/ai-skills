// Level 5 · SUB-WORKFLOW "Score customer" — called by the orchestrator, one customer per call.
// Inputs are declared (typed) so the caller gets a form of fields; it returns one item.
import { workflow, node, trigger, expr } from '@n8n/workflow-sdk';

const start = trigger({
  type: 'n8n-nodes-base.executeWorkflowTrigger', version: 1.2,
  config: { name: 'When called', parameters: { inputSource: 'workflowInputs',
    workflowInputs: { values: [{ name: 'customer_id', type: 'number' }, { name: 'email', type: 'string' }] } } },
});

const carts = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'Get carts', parameters: { method: 'GET', url: expr('https://dummyjson.com/carts/user/{{ $json.customer_id }}'), options: { timeout: 20000 } },
            retryOnFail: true, maxTries: 3 },
});

const score = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Score', parameters: { mode: 'runOnceForAllItems', jsCode: `
const input = $('When called').first().json;
const carts = $input.first().json.carts || [];
const spent = carts.reduce((s, c) => s + (c.discountedTotal || c.total || 0), 0);
const tier = spent >= 5000 ? 'gold' : spent >= 1000 ? 'silver' : spent > 0 ? 'bronze' : 'new';
return [{ json: { customer_id: input.customer_id, email: input.email, carts: carts.length, spent: Math.round(spent * 100) / 100, tier } }];` } },
});

export default workflow('score-customer', 'Score customer (sub-workflow)').add(start).to(carts).to(score);
