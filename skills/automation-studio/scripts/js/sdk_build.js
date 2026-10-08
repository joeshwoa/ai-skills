// SDK code (workflow builder JS/TS, no import line needed) → workflow JSON.
// usage: node sdk_build.js <n8n_dir> <workflow.ts> <out.json>
const path = require('path');
const fs = require('fs');
const [dir, src, out] = process.argv.slice(2);
const sdk = require(path.join(dir, 'node_modules/@n8n/workflow-sdk'));
let code = fs.readFileSync(src, 'utf8');
code = code.replace(/^\s*import[^;]*from\s*['"]@n8n\/workflow-sdk['"];?\s*$/mg, '');
// SDK parser quirk: a list of single-quoted strings (['id', 'email']) can be mis-escaped → use double quotes
code = code.replace(/\[(\s*'[^'\\\n]*'\s*(?:,\s*'[^'\\\n]*'\s*)*)\]/g, (m, inner) => '[' + inner.replace(/'([^'\\\n]*)'/g, (_, x) => JSON.stringify(x)) + ']');
try {
  const wf = sdk.parseWorkflowCode(code);
  fs.writeFileSync(out, JSON.stringify(wf, null, 2));
  console.log('ok');
} catch (e) {
  console.error(String(e && e.message || e));
  process.exit(1);
}
