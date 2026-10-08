// Print n8n's own building guidance shipped inside the installed n8n (always matches that version).
// usage: node guide.js <n8n_dir> list|sdk|patterns|params|<technique>|<PARAM_GUIDE_NAME>
const path = require('path');
const [dir, topic] = process.argv.slice(2);
const req = (p) => require(path.join(dir, 'node_modules', p));
const base = '@n8n/workflow-sdk/dist/prompts/';
const safe = (f) => { try { return f(); } catch (e) { return null; } };
const sdkRef = safe(() => req(base + 'sdk-reference/index.js')) || {};
const params = safe(() => req(base + 'node-guidance/parameter-guides/index.js')) || {};
const best = (safe(() => req(base + 'best-practices/index.js')) || {}).bestPracticesRegistry || {};
const str = (o) => Object.entries(o).filter(([, v]) => typeof v === 'string');
if (!topic || topic === 'list') {
  console.log('sdk        — Workflow SDK language, rules, expressions, patterns');
  console.log('patterns   — worked SDK workflow patterns');
  console.log('params     — parameter guides: ' + Object.keys(params).join(', '));
  console.log('techniques — ' + Object.keys(best).join(', '));
} else if (topic === 'sdk') {
  for (const [k, v] of str(sdkRef)) console.log(`\n### ${k}\n${v}`);
} else if (topic === 'patterns') {
  const p = safe(() => req('@n8n/ai-workflow-builder/dist/code-builder/prompts/index.js'));
  console.log((p && p.WORKFLOW_PATTERNS) || sdkRef.WORKFLOW_PATTERNS_DETAILED || 'not available in this n8n version');
} else if (topic === 'params') {
  for (const [k, v] of Object.entries(params)) console.log(`\n### ${k} (${(v.patterns || []).join(', ')})\n${typeof v === 'string' ? v : v.content}`);
} else if (params[topic]) {
  const v = params[topic]; console.log(typeof v === 'string' ? v : v.content);
} else if (best[topic]) {
  console.log(best[topic].documentation);
} else {
  console.log('unknown topic. Try: list'); process.exit(1);
}
