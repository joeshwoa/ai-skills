// Level 4 · AI support agent behind a webhook (website chat widget, WhatsApp/Telegram relay …):
// validate → AI Agent (OpenAI model + per-customer memory + an order-lookup tool) → reply.
// Guardrails: empty/too-long messages rejected before any AI cost; the agent can only answer from
// its tool + policy, and hands off to a human (handoff:true) when unsure.
import { workflow, node, trigger, ifElse, languageModel, memory, tool, nodeJson, expr, newCredential } from '@n8n/workflow-sdk';

const chatIn = trigger({
  type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Chat message', parameters: { httpMethod: 'POST', path: 'support-chat', responseMode: 'responseNode', options: {} } },
});

const okInput = ifElse({ version: 2.3, config: { name: 'Valid message?', parameters: {
  conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'loose', version: 2 },
    conditions: [
      { id: 'a', leftValue: expr('{{ ($json.body.message || "").trim().length }}'), rightValue: 0, operator: { type: 'number', operation: 'gt' } },
      { id: 'b', leftValue: expr('{{ ($json.body.message || "").length }}'), rightValue: 2000, operator: { type: 'number', operation: 'lte' } },
      { id: 'c', leftValue: expr('{{ $json.body.session_id }}'), rightValue: '', operator: { type: 'string', operation: 'notEmpty', singleValue: true } },
    ] },
  options: {} } } });

const model = languageModel({
  type: '@n8n/n8n-nodes-langchain.lmChatOpenAi', version: 1.3,
  config: { name: 'OpenAI model', parameters: { model: { __rl: true, mode: 'list', value: 'gpt-4.1-mini' }, options: { temperature: 0.2 } },
            credentials: { openAiApi: newCredential('OpenAI') } },
});

const mem = memory({
  type: '@n8n/n8n-nodes-langchain.memoryBufferWindow', version: 1.4,
  config: { name: 'Conversation memory', parameters: { sessionIdType: 'customKey',
    sessionKey: nodeJson(chatIn, 'body.session_id'), contextWindowLength: 12 } },
});

const orders = tool({
  type: '@n8n/n8n-nodes-langchain.toolCode', version: 1.3,
  config: { name: 'lookup_order', parameters: {
    description: 'Look up an order by its number (e.g. "A1023"). Returns status, ETA and items. Call this whenever the customer mentions an order.',
    language: 'javaScript',
    jsCode: `// Replace this demo table with an HTTP call or a database query.
const db = { A1023: { status: 'shipped', eta: '2026-10-10', items: ['Headphones'] }, A1024: { status: 'processing', eta: '2026-10-14', items: ['Keyboard'] } };
const id = String(query || '').toUpperCase().match(/[A-Z]\\d{3,}/)?.[0];
return JSON.stringify(id && db[id] ? { order: id, ...db[id] } : { error: 'order not found', asked: query });`,
  } },
});

const agent = node({
  type: '@n8n/n8n-nodes-langchain.agent', version: 3.1,
  config: { name: 'Support agent', parameters: {
    promptType: 'define', text: expr('{{ $json.body.message }}'),
    options: {
      systemMessage: `You are the support assistant of "Cominde Store". Reply in the customer's language (Egyptian Arabic if they write Arabic), short and friendly.
Facts you may use: the lookup_order tool, and this policy — returns within 14 days, delivery 2–5 working days in Egypt, support hours 9:00–18:00 Cairo.
Never invent order data. If you cannot help, or the customer is angry or asks for a human, end your reply with [HANDOFF].`,
      maxIterations: 6,
    },
  }, subnodes: { model: model, memory: mem, tools: [orders] } },
});

const shape = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Shape reply', parameters: { mode: 'manual', assignments: { assignments: [
    { id: 'r', name: 'reply', value: expr('{{ $json.output.replace("[HANDOFF]", "").trim() }}'), type: 'string' },
    { id: 'h', name: 'handoff', value: expr('{{ $json.output.includes("[HANDOFF]") }}'), type: 'boolean' },
  ] }, options: {} } },
});

const reply = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply',
  parameters: { respondWith: 'json', responseBody: expr('{{ { reply: $json.reply, handoff: $json.handoff } }}'), options: { responseCode: 200 } } } });
const reject = node({ type: 'n8n-nodes-base.respondToWebhook', version: 1.5, config: { name: 'Reply 422',
  parameters: { respondWith: 'json', responseBody: '={{ { error: "message (1-2000 chars) and session_id are required" } }}', options: { responseCode: 422 } } } });

export default workflow('ai-support-agent', 'AI support agent (webhook)')
  .add(chatIn)
  .to(okInput.onTrue(agent.to(shape).to(reply)).onFalse(reject));
