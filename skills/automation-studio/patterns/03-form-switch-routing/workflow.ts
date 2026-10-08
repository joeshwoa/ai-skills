// Level 2 · Hosted n8n form → route by request type (Switch) → Slack / Gmail / triage list
// The form URL appears on the trigger node once the workflow is active (…/form/contact-us).
import { workflow, node, trigger, switchCase, expr } from '@n8n/workflow-sdk';

const form = trigger({
  type: 'n8n-nodes-base.formTrigger', version: 2.6,
  config: { name: 'Contact form', parameters: {
    formTitle: 'Contact us', formDescription: 'We reply within one working day.',
    formFields: { values: [
      { fieldLabel: 'Name', fieldType: 'text', requiredField: true },
      { fieldLabel: 'Email', fieldType: 'email', requiredField: true },
      { fieldLabel: 'Type', fieldType: 'dropdown', requiredField: true,
        fieldOptions: { values: [{ option: 'Sales' }, { option: 'Support' }, { option: 'Other' }] } },
      { fieldLabel: 'Message', fieldType: 'textarea', requiredField: true },
    ] },
    options: { path: 'contact-us', respondWithOptions: { values: { formSubmittedText: 'Thanks — we got your message.' } } },
  } },
});

const tidy = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Tidy fields', parameters: { mode: 'manual', assignments: { assignments: [
    { id: 'a', name: 'name', value: expr('{{ $json.Name.trim() }}'), type: 'string' },
    { id: 'b', name: 'email', value: expr('{{ $json.Email.trim().toLowerCase() }}'), type: 'string' },
    { id: 'c', name: 'type', value: expr('{{ $json.Type.toLowerCase() }}'), type: 'string' },
    { id: 'd', name: 'message', value: expr('{{ $json.Message.trim() }}'), type: 'string' },
    { id: 'e', name: 'submitted_at', value: expr('{{ $json.submittedAt || $now.toISO() }}'), type: 'string' },
  ] }, options: {} } },
});

const route = switchCase({ version: 3.4, config: { name: 'Route by type', parameters: {
  rules: { values: [
    { outputKey: 'sales', renameOutput: true, conditions: {
      options: { caseSensitive: false, leftValue: '', typeValidation: 'strict', version: 2 },
      conditions: [{ leftValue: expr('{{ $json.type }}'), rightValue: 'sales', operator: { type: 'string', operation: 'equals' } }],
      combinator: 'and' } },
    { outputKey: 'support', renameOutput: true, conditions: {
      options: { caseSensitive: false, leftValue: '', typeValidation: 'strict', version: 2 },
      conditions: [{ leftValue: expr('{{ $json.type }}'), rightValue: 'support', operator: { type: 'string', operation: 'equals' } }],
      combinator: 'and' } },
  ] },
  options: { fallbackOutput: 'extra', renameFallbackOutput: 'other' },
} } });

const slack = node({
  type: 'n8n-nodes-base.slack', version: 2.7,
  config: { name: 'Tell sales on Slack', parameters: {
    resource: 'message', operation: 'post', select: 'channel',
    channelId: { __rl: true, mode: 'name', value: '#sales' },
    text: expr('New sales lead from {{ $json.name }} <{{ $json.email }}>:\n> {{ $json.message }}'),
    otherOptions: {},
  } },
});

const support = node({
  type: 'n8n-nodes-base.gmail', version: 2.2,
  config: { name: 'Open support email', parameters: {
    resource: 'message', operation: 'send', sendTo: 'support@example.com',
    subject: expr('[Support] {{ $json.name }}'), emailType: 'text',
    message: expr('From: {{ $json.name }} <{{ $json.email }}>\n\n{{ $json.message }}'),
    options: { replyTo: expr('{{ $json.email }}'), appendAttribution: false },
  } },
});

const triage = node({
  type: 'n8n-nodes-base.set', version: 3.5,
  config: { name: 'Mark for triage', parameters: { mode: 'manual', includeOtherFields: true,
    assignments: { assignments: [{ id: 't', name: 'status', value: 'needs-triage', type: 'string' }] }, options: {} } },
});

export default workflow('form-switch-routing', 'Contact form → route by type')
  .add(form).to(tidy)
  .to(route.onCase(0, slack).onCase(1, support).onCase(2, triage));
