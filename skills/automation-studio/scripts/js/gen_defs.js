// Generate the n8n Workflow SDK node definitions (TypeScript types + zod schemas) for the installed n8n.
// usage: node gen_defs.js <n8n_dir>
const path = require('path');
const dir = process.argv[2];
const g = require(path.join(dir, 'node_modules/@n8n/workflow-sdk/dist/generate-types/generate-node-defs-cli.js'));
(async () => {
  await g.generateNodeDefinitions({ nodesJsonPath: path.join(dir, 'node_modules/n8n-nodes-base/dist/types/nodes.json'),
    outputDir: path.join(dir, 'node-defs/n8n-nodes-base'), packageName: 'n8n-nodes-base' });
  await g.generateNodeDefinitions({ nodesJsonPath: path.join(dir, 'node_modules/@n8n/n8n-nodes-langchain/dist/types/nodes.json'),
    outputDir: path.join(dir, 'node-defs/n8n-nodes-langchain'), packageName: '@n8n/n8n-nodes-langchain' });
})().catch(e => { console.error(String(e && e.stack || e)); process.exit(1); });
