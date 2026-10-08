// Level 5 · Human-in-the-loop: expense request → reply 202 at once → small amounts auto-approved,
// big ones emailed to a manager with Approve / Decline buttons (the run WAITS, up to 3 days, for the click)
// → decision recorded → requester notified on Slack. No extra infrastructure: n8n holds the waiting run.
import { workflow, node, trigger, ifElse, expr } from '@n8n/workflow-sdk';

const request = trigger({
  type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Expense request', parameters: { httpMethod: 'POST', path: 'expense', responseMode: 'responseNode', options: {} } },
});

const norm = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Normalise', parameters: { mode: 'manual', assignments: { assignments: [
    { id: '1', name: 'employee', value: expr('{{ $json.body.employee }}'), type: 'string' },
    { id: '2', name: 'amount', value: expr('{{ Number($json.body.amount) }}'), type: 'number' },
    { id: '3', name: 'reason', value: expr('{{ ($json.body.reason || "").slice(0, 300) }}'), type: 'string' },
    { id: '4', name: 'request_id', value: expr('{{ $execution.id }}'), type: 'string' },
  ] }, options: {} } },
});

const ack = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 202',
  parameters: { respondWith: 'json', responseBody: expr('{{ { received: true, request_id: $json.request_id } }}'), options: { responseCode: 202 } } } });

const big = ifElse({ version: 2.3, config: { name: 'Over 1000 EGP?', parameters: {
  conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 },
    conditions: [{ id: 'a', leftValue: expr('{{ $json.amount }}'), rightValue: 1000, operator: { type: 'number', operation: 'gt' } }] },
  options: {} } } });

const ask = node({
  type: 'n8n-nodes-base.gmail', version: 2.2,
  config: { name: 'Ask manager', parameters: {
    resource: 'message', operation: 'sendAndWait', sendTo: 'manager@example.com',
    subject: expr('Approve {{ $json.amount }} EGP for {{ $json.employee }}?'),
    message: expr('{{ $json.employee }} requests {{ $json.amount }} EGP.\nReason: {{ $json.reason }}\nRequest #{{ $json.request_id }}'),
    responseType: 'approval',
    approvalOptions: { values: { approvalType: 'double', approveLabel: 'Approve', disapproveLabel: 'Decline' } },
    options: { limitWaitTime: { values: { limitType: 'afterTimeInterval', resumeAmount: 3, resumeUnit: 'days' } } },
  } },
});

const approvedQ = ifElse({ version: 2.3, config: { name: 'Approved?', parameters: {
  conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'loose', version: 2 },
    conditions: [{ id: 'b', leftValue: expr('{{ $json.data && $json.data.approved }}'), rightValue: '', operator: { type: 'boolean', operation: 'true', singleValue: true } }] },
  options: {} } } });


const autoOk = node({ type: 'n8n-nodes-base.set', version: 3.5, config: { name: 'Auto-approved', parameters: { mode: 'manual', includeOtherFields: true,
  assignments: { assignments: [{ id: 's', name: 'status', value: 'approved', type: 'string' }, { id: 'b', name: 'decided_by', value: 'policy (≤ 1000)', type: 'string' }] }, options: {} } } });
const okByMgr = node({ type: 'n8n-nodes-base.set', version: 3.5, config: { name: 'Approved by manager', parameters: { mode: 'manual',
  assignments: { assignments: [
    { id: 'e', name: 'employee', value: expr('{{ $("Normalise").item.json.employee }}'), type: 'string' },
    { id: 'a', name: 'amount', value: expr('{{ $("Normalise").item.json.amount }}'), type: 'number' },
    { id: 's', name: 'status', value: 'approved', type: 'string' }, { id: 'b', name: 'decided_by', value: 'manager', type: 'string' }] }, options: {} } } });
const noByMgr = node({ type: 'n8n-nodes-base.set', version: 3.5, config: { name: 'Declined or timed out', parameters: { mode: 'manual',
  assignments: { assignments: [
    { id: 'e', name: 'employee', value: expr('{{ $("Normalise").item.json.employee }}'), type: 'string' },
    { id: 'a', name: 'amount', value: expr('{{ $("Normalise").item.json.amount }}'), type: 'number' },
    { id: 's', name: 'status', value: 'declined', type: 'string' }, { id: 'b', name: 'decided_by', value: 'manager', type: 'string' }] }, options: {} } } });

const tell = node({
  type: 'n8n-nodes-base.slack', version: 2.7,
  config: { name: 'Notify requester', parameters: { resource: 'message', operation: 'post', select: 'channel',
    channelId: { __rl: true, mode: 'name', value: '#expenses' },
    text: expr('{{ $json.employee }}: {{ $json.amount }} EGP → *{{ $json.status }}* (by {{ $json.decided_by }})'), otherOptions: {} } },
});

export default workflow('human-approval', 'Expense approval with human in the loop')
  .add(request).to(norm).to(ack)
  .to(big
    .onTrue(ask.to(approvedQ.onTrue(okByMgr.to(tell)).onFalse(noByMgr.to(tell))))
    .onFalse(autoOk.to(tell)));
