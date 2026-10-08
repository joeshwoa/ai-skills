// Validate a workflow JSON with the official n8n Workflow SDK (graph checks + per-node parameter schemas).
// usage: node sdk_validate.js <n8n_dir> <workflow.json>   → JSON {errors:[], warnings:[]}
const path = require('path');
const fs = require('fs');
const [dir, file] = process.argv.slice(2);
const sdk = require(path.join(dir, 'node_modules/@n8n/workflow-sdk'));
sdk.setSchemaBaseDirs([path.join(dir, 'node-defs/n8n-nodes-base'), path.join(dir, 'node-defs/n8n-nodes-langchain')]);
const wf = JSON.parse(fs.readFileSync(file, 'utf8'));
let r;
try { r = sdk.validateWorkflow(wf, {}); } catch (e) { r = { errors: [{ code: 'SDK_CRASH', message: String(e) }], warnings: [] }; }
const pick = (x) => ({ code: x.code, message: x.message, node: x.nodeName, severity: x.severity });
process.stdout.write(JSON.stringify({ errors: (r.errors || []).map(pick), warnings: (r.warnings || []).map(pick) }));
