// Level 2 · Every morning: public API (no key) → summarise in Code → email the digest
// Open-Meteo weather for Cairo, 3 days. Swap the URL for any JSON API.
import { workflow, node, trigger, expr } from '@n8n/workflow-sdk';

const everyMorning = trigger({
  type: 'n8n-nodes-base.scheduleTrigger', version: 1.4,
  config: { name: 'Every morning 07:00', parameters: { rule: { interval: [{ field: 'days', daysInterval: 1, triggerAtHour: 7, triggerAtMinute: 0 }] } } },
});

const forecast = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: { name: 'Get forecast', parameters: {
    method: 'GET', url: 'https://api.open-meteo.com/v1/forecast',
    sendQuery: true,
    queryParameters: { parameters: [
      { name: 'latitude', value: '30.04' }, { name: 'longitude', value: '31.24' },
      { name: 'daily', value: 'temperature_2m_max,temperature_2m_min,precipitation_probability_max' },
      { name: 'timezone', value: 'Africa/Cairo' }, { name: 'forecast_days', value: '3' },
    ] },
    options: { timeout: 20000 },
  }, retryOnFail: true, maxTries: 3, waitBetweenTries: 3000 },
});

const digest = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: { name: 'Build digest', parameters: { mode: 'runOnceForAllItems', jsCode: `
const d = $input.first().json.daily;
if (!d || !Array.isArray(d.time)) throw new Error('Unexpected API response: no daily data');
const rows = d.time.map((day, i) => ({
  day,
  max: Math.round(d.temperature_2m_max[i]),
  min: Math.round(d.temperature_2m_min[i]),
  rain: d.precipitation_probability_max[i] ?? 0,
}));
const lines = rows.map(r => \`\${r.day}: \${r.min}–\${r.max}°C, rain \${r.rain}%\`);
const warn = rows.some(r => r.rain >= 50) ? 'Take an umbrella this week.' : 'No rain expected.';
return [{ json: {
  subject: \`Cairo weather — \${rows[0].day}\`,
  text: ['Cairo, next 3 days', ...lines, '', warn].join('\\n'),
  hot_days: rows.filter(r => r.max >= 35).length,
} }];` } },
});

const mail = node({
  type: 'n8n-nodes-base.gmail', version: 2.2,
  config: { name: 'Email digest', parameters: {
    resource: 'message', operation: 'send', sendTo: 'me@example.com',
    subject: expr('{{ $json.subject }}'), emailType: 'text', message: expr('{{ $json.text }}'),
    options: { appendAttribution: false },
  } },
});

export default workflow('schedule-api-digest', 'Daily API digest → email')
  .add(everyMorning).to(forecast).to(digest).to(mail);
