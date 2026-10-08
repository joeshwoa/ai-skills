# Building n8n workflows that work the first time

Source of truth = the n8n installed on this machine: `auto.sh node <type> --ts` (exact parameters of the
version), `auto.sh guide sdk` (n8n's own SDK rules), `auto.sh guide patterns` / `auto.sh guide <TOPIC>`
(n8n's best-practice notes: IF, SWITCH, SET, HTTP_REQUEST, TOOL, RESOURCE_LOCATOR, … — `guide list`).

## 1. Writing SDK code (`flow.ts`)
```js
import { workflow, node, trigger, ifElse, switchCase, merge, splitInBatches, nextBatch,
         languageModel, memory, tool, outputParser, expr, nodeJson, newCredential } from '@n8n/workflow-sdk';
const hook = trigger({ type: 'n8n-nodes-base.webhook', version: 2.2,
  config: { name: 'Order webhook', parameters: { httpMethod: 'POST', path: 'orders', responseMode: 'responseNode', options: {} } } });
const save = node({ type: 'n8n-nodes-base.postgres', version: 2.7, config: { name: 'Save order', parameters: { … },
  credentials: { postgres: newCredential('Shop DB') }, retryOnFail: true, maxTries: 3 } });
export default workflow('id', 'Readable name').add(hook).to(check.onTrue(save.to(ok)).onFalse(bad));
```
- Chain: `.add(trigger).to(a).to(b)`; branches: `ifElse.onTrue(x).onFalse(y)`, `switchCase.onCase(i, x)`;
  any multi-output node: `.add(n.output(0).to(x)).add(n.output(1).to(y))` (e.g. Remove Duplicates kept/discarded);
  loops: `sib.onDone(after).onEachBatch(work.to(nextBatch(sib)))`; merge: `a.to(m.input(0))`, `b.to(m.input(1))`.
- Node-level settings go in `config` next to `parameters`: `retryOnFail`, `maxTries`, `waitBetweenTries`,
  `onError: 'continueRegularOutput'|'continueErrorOutput'`, `alwaysOutputData`, `executeOnce`, `notes`.
- AI sub-nodes: `subnodes: { model, memory, tools: [..], outputParser }` on the root node.
- **Parser limits (tested):** no TypeScript type annotations, no helper functions/arrow functions/`.map()`
  at file level (write objects out), use `expr('{{ … }}')` for expressions, use double quotes inside string
  arrays (`["id"]` — `build` fixes simple cases). Template literals are fine inside `jsCode`
  (escape `` ` `` and `${` as `\``, `\${`).
- Versions: use the default (latest) version shown by `auto.sh node <type>`; validation warns when older.

## 2. Expressions
- `={{ … }}` (SDK: `expr('{{ … }}')`). JavaScript inside; `$json` is the current item of the **immediate
  predecessor**. Anything else: `$('Node name').item.json.field` (paired item), `.first()`, `.last()`, `.all()`.
  In SDK prefer `nodeJson(nodeVar, 'path')` for AI sub-nodes and after branches/merges.
- Built-ins: `$now`, `$today` (Luxon: `.toISO()`, `.toFormat('yyyy-LL-dd')`, `.minus({days:1})`), `$execution.id`,
  `$workflow.name`, `$env.VAR` (self-host; blocked on Cloud), `$vars.NAME` (Cloud/Enterprise variables),
  `$input.all()`, `$pageCount` / `$response` (HTTP pagination), `$fromAI('key','desc')` (tool params).
- Data helpers: `.isEmpty()`, `.extractEmail()`, `.toTitleCase()`, `.sum()`, `.unique()`, `$ifEmpty(a,b)`.
- An expression returning an object for a field typed `object`/`array` must be a real object, not a string.

## 3. Conditions (IF v2.3 / Filter v2.3 / Switch v3.4)
```js
conditions: { combinator: 'and', options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 },
  conditions: [{ id: 'c1', leftValue: expr('{{ $json.email }}'), rightValue: '^[^@]+@[^@]+$',
                 operator: { type: 'string', operation: 'regex' } }] }
```
- Operator types: string (equals, notEquals, contains, startsWith, endsWith, regex, notRegex, empty, notEmpty,
  exists), number (equals, gt, gte, lt, lte), boolean (true, false — add `singleValue: true`), dateTime
  (after, before), array (contains, lengthEquals, lengthGt, empty), object (empty, notEmpty).
- `caseSensitive: false` lower-cases the **value only** → write regex/right values in lower case.
- `typeValidation: 'loose'` when the input may be a numeric string ("350"); otherwise convert first.
- Switch: `rules.values[]` each with `outputKey`, `renameOutput: true`, full `conditions`; fallback via
  `options.fallbackOutput: 'extra'` → it becomes the last output index.

## 4. Set (v3.5)
`mode: 'manual'`, `assignments.assignments: [{ id, name, value, type: 'string'|'number'|'boolean'|'object'|'array' }]`,
`includeOtherFields: true` to keep incoming fields. Dotted names create nested objects. Types are enforced —
a non-number into `number` fails the run (good: fail loudly).

## 5. Code node (v2)
- `runOnceForAllItems`: `return $input.all().map(i => ({ json: {…} }))` — must return an array of `{json}`.
- `runOnceForEachItem`: use `$json` / `$input.item`; `return { json: {…} }`.
- Available: `$input`, `$json`, `$('Node')`, `$now`, `$execution`, `$workflow`, `$env` (if allowed), Luxon
  `DateTime`, `require` only for allow-listed modules (`NODE_FUNCTION_ALLOW_BUILTIN/EXTERNAL` on self-host).
  No network (`fetch` isn't available) → use HTTP Request. Python Code is available but slower — prefer JS.
- Throw `new Error('clear message')` for bad data so the error workflow fires with a useful message.
- Binary: `items[i].binary.data` (`data` base64, `mimeType`, `fileName`); prefer Extract from File / Convert to File.

## 6. HTTP Request (v4.5)
- Auth: `authentication: 'predefinedCredentialType'` + `nodeCredentialType: 'slackApi'` to reuse an app
  credential, or `'genericCredentialType'` + `genericAuthType: 'httpHeaderAuth'|'httpBearerAuth'|'httpBasicAuth'|'oAuth2Api'`.
  Never put keys in headers/query parameters.
- Query: `sendQuery: true, queryParameters: { parameters: [{name, value}] }`; JSON body:
  `sendBody: true, contentType: 'json', specifyBody: 'json', jsonBody: expr('{{ JSON.stringify({...}) }}')`
  or `specifyBody: 'keypair'` + `bodyParameters`. Raw XML/text: `contentType: 'raw'`, `rawContentType`, `body`.
- Pagination: `options.pagination.pagination = { paginationMode: 'updateAParameterInEachRequest',
  parameters: { parameters: [{ type: 'qs', name: 'page', value: expr('{{ $pageCount + 1 }}') }] },
  paginationCompleteWhen: 'other', completeExpression: expr('{{ $response.body.items.length === 0 }}'),
  limitPagesFetched: true, maxRequests: 100, requestInterval: 250 }` — or `responseContainsNextURL` with
  `nextURL: expr('{{ $response.body.next }}')`. Each page = one output item (then Split Out).
- Files: `options.response.response = { responseFormat: 'file', outputPropertyName: 'data' }`.
- Errors: `options.response.response.neverError: true` + `fullResponse: true` to branch on `statusCode`.

## 7. Webhooks & forms
- Production URL `/webhook/<path>` works only when the workflow is **active**; test URL `/webhook-test/<path>`
  only while "Listen for test event" is clicked in the editor.
- `responseMode`: `onReceived` (instant 200), `lastNode`, `responseNode` (use Respond to Webhook — any
  status/body/headers; it passes items through, so you can reply first and keep working).
- Secure it: `authentication: 'headerAuth'` (credential with header name + secret) or verify provider
  signatures in Code (Stripe `stripe-signature`, GitHub `x-hub-signature-256`, Meta `x-hub-signature-256`).
- Form Trigger v2.6: `formFields.values[]` (`fieldLabel`, `fieldType`, `requiredField`, `fieldOptions`);
  `options.path`, `respondWithOptions`. Output keys = field labels.

## 8. Loops, merging, waiting
- Loop Over Items (splitInBatches v3): output 0 = **done** (all processed items), output 1 = **loop**.
- Remove Duplicates v2 `removeItemsSeenInPreviousExecutions`: output 0 = new, 1 = already seen; history per
  workflow (or node), size `options.historySize`. Doesn't dedupe within one run → add
  `removeDuplicateInputItems` before it if the source can repeat inside a run.
- Merge v3.2: `mode: 'append' | 'combine'` (`combineBy: 'combineByFields' | 'combineByPosition' | 'combineAll'`) | `'chooseBranch'`.
- Wait v1.1: `resume: 'timeInterval' | 'specificTime' | 'webhook' | 'form'`. Waits > 65 s are offloaded to
  the database (safe across restarts). Send-and-wait (Gmail/Slack/Telegram/Teams) = approval in one node.

## 9. AI nodes
- Agent v3.1: `promptType: 'define'`, `text`, `options.systemMessage`, `maxIterations`; sub-nodes: model
  (lmChatOpenAi v1.3 `model: { __rl: true, mode: 'list', value: 'gpt-4.1-mini' }`, lmChatAnthropic,
  lmChatGoogleGemini, lmChatOllama for local), memory (memoryBufferWindow v1.4 `sessionIdType: 'customKey'`,
  `sessionKey`), tools (toolCode, toolWorkflow, httpRequestTool, app "…Tool" nodes with `$fromAI()`),
  outputParser (outputParserStructured).
- Information Extractor v1.2 (`schemaType: 'fromJson'`, `jsonSchemaExample`), Text Classifier, Sentiment
  Analysis, Basic LLM Chain (`chainLlm`), Summarization chain, vector stores + embeddings for RAG.
- Never trust model numbers/ids: re-check in Code (pattern 10). Validate input length before calling.

## 10. Errors & reliability
- Per node: `retryOnFail` (+ `maxTries` 2–5, `waitBetweenTries` ms) for network calls; `onError` to keep
  going per item and collect failures; Stop and Error node for deliberate failures.
- Per workflow: settings `errorWorkflow: '<id>'` → pattern 07 receives `{execution:{id,url,error,lastNodeExecuted}, workflow:{id,name}}`.
- `settings.executionOrder: 'v1'` (build sets it), timezone `settings.timezone: 'Africa/Cairo'` for schedules.
- Saving data: `saveDataSuccessExecution: 'none'` for high-volume flows (keep errors) to protect the DB/PII.

## 11. Sub-workflows
- Child: Execute Workflow Trigger v1.2 `inputSource: 'workflowInputs'` with typed inputs; last node's output is returned.
- Parent: Execute Workflow v1.4 `source: 'database'`, `workflowId` (write `name:<child name>` — `deploy`
  resolves it), `mode: 'each'|'once'`, `workflowInputs` (resource mapper), `options.waitForSubWorkflow`.
- Deploy children first. Test children on their own (cases with the inputs as trigger).

## 12. Common failure causes (check before shipping)
Wrong `$json` after a branch/merge (reference the node explicitly) · expression returns a string for an
object field · webhook test URL used in production · workflow not active · credential not selected on a node ·
OAuth token expired (reconnect) · API rate limit (batch + wait) · timezone of schedules · Code node returning
non-`{json}` · Google Sheets used as a concurrent database · large binary in memory
(`N8N_DEFAULT_BINARY_DATA_MODE=filesystem` on self-host).
