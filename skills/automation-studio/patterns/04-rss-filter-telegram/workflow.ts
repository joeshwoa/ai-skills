// Level 2–3 · Every hour: read an RSS feed → keep posts matching keywords → drop ones already sent
// (n8n remembers them between runs) → at most 5 → one Telegram message each.
// NOTE: 'seen in previous executions' does not dedupe inside one run (the same link twice in one feed passes).
// NOTE: with caseSensitive:false n8n lower-cases the VALUE, not the pattern → write regexes in lower case.
import { workflow, node, trigger, expr } from '@n8n/workflow-sdk';

const hourly = trigger({
  type: 'n8n-nodes-base.scheduleTrigger', version: 1.4,
  config: { name: 'Every hour', parameters: { rule: { interval: [{ field: 'hours', hoursInterval: 1 }] } } },
});

const feed = node({
  type: 'n8n-nodes-base.rssFeedRead', version: 1.2,
  config: { name: 'Read feed', parameters: { url: 'https://hnrss.org/frontpage', options: {} }, retryOnFail: true, maxTries: 2 },
});

const relevant = node({
  type: 'n8n-nodes-base.filter', version: 2.3,
  config: { name: 'Matches keywords', parameters: {
    conditions: {
      options: { caseSensitive: false, leftValue: '', typeValidation: 'loose', version: 2 },
      conditions: [{ id: 'k', leftValue: expr('{{ $json.title }}'), rightValue: '\\b(ai|llm|n8n|automation|flutter)\\b',
                     operator: { type: 'string', operation: 'regex' } }],
      combinator: 'and',
    },
    options: { ignoreCase: true },
  } },
});

const fresh = node({
  type: 'n8n-nodes-base.removeDuplicates', version: 2,
  config: { name: 'Only new posts', parameters: {
    operation: 'removeItemsSeenInPreviousExecutions', logic: 'removeItemsWithAlreadySeenKeyValues',
    dedupeValue: expr('{{ $json.link }}'), options: { historySize: 2000 },
  } },
});

const top = node({ type: 'n8n-nodes-base.limit', version: 1, config: { name: 'Max 5', parameters: { maxItems: 5 } } });

const send = node({
  type: 'n8n-nodes-base.telegram', version: 1.2,
  config: { name: 'Send to Telegram', parameters: {
    resource: 'message', operation: 'sendMessage', chatId: expr('{{ $env.TELEGRAM_CHAT_ID }}'),
    text: expr('<b>{{ $json.title }}</b>\n{{ $json.link }}'),
    additionalFields: { parse_mode: 'HTML', disable_web_page_preview: false, appendAttribution: false },
  } },
});

export default workflow('rss-filter-telegram', 'RSS → keywords → new only → Telegram')
  .add(hourly).to(feed).to(relevant).to(fresh).to(top).to(send);
