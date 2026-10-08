// Level 3 · Nightly sync: page through an API (HTTP node's built-in pagination) → one item per record
// → map/clean fields → upsert into Postgres (re-runs never duplicate rows: upsert on "id").
import { workflow, node, trigger, expr } from '@n8n/workflow-sdk';

const nightly = trigger({
  type: 'n8n-nodes-base.scheduleTrigger', version: 1.4,
  config: { name: 'Nightly 02:30', parameters: { rule: { interval: [{ field: 'cronExpression', expression: '30 2 * * *' }] } } },
});

const pages = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'Fetch all pages', parameters: {
    method: 'GET', url: 'https://dummyjson.com/products',
    sendQuery: true,
    queryParameters: { parameters: [{ name: 'limit', value: '50' }, { name: 'select', value: 'id,title,price,stock,category,rating' }] },
    options: {
      pagination: { pagination: {
        paginationMode: 'updateAParameterInEachRequest',
        parameters: { parameters: [{ type: 'qs', name: 'skip', value: expr('{{ $pageCount * 50 }}') }] },
        paginationCompleteWhen: 'other',
        completeExpression: expr('{{ $response.body.skip + $response.body.limit >= $response.body.total }}'),
        limitPagesFetched: true, maxRequests: 100, requestInterval: 250,
      } },
      timeout: 30000,
    },
  }, retryOnFail: true, maxTries: 3, waitBetweenTries: 5000 },
});

const records = node({
  type: 'n8n-nodes-base.splitOut', version: 1,
  config: { name: 'One item per product', parameters: { fieldToSplitOut: 'products', options: {} } },
});

const mapRow = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Map to table row', parameters: { mode: 'manual', assignments: { assignments: [
    { id: '1', name: 'id', value: expr('{{ $json.id }}'), type: 'number' },
    { id: '2', name: 'title', value: expr('{{ $json.title.trim() }}'), type: 'string' },
    { id: '3', name: 'price_cents', value: expr('{{ Math.round($json.price * 100) }}'), type: 'number' },
    { id: '4', name: 'in_stock', value: expr('{{ $json.stock > 0 }}'), type: 'boolean' },
    { id: '5', name: 'category', value: expr('{{ $json.category }}'), type: 'string' },
    { id: '6', name: 'synced_at', value: expr('{{ $now.toISO() }}'), type: 'string' },
  ] }, options: {} } },
});

const upsert = node({
  type: 'n8n-nodes-base.postgres', version: 2.7,
  config: { name: 'Upsert products', parameters: {
    operation: 'upsert',
    schema: { __rl: true, mode: 'list', value: 'public' },
    table: { __rl: true, mode: 'name', value: 'products' },
    columns: { mappingMode: 'autoMapInputData', value: {}, matchingColumns: ['id'], schema: [] },
    options: { queryBatching: 'transaction' },
  } },
});

export default workflow('paginated-api-to-postgres', 'Paginated API → Postgres upsert')
  .add(nightly).to(pages).to(records).to(mapRow).to(upsert);
