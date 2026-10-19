-- Anonymous, non-personal skill feedback for the ai-skills library.
-- Writes happen only through the `ingest` Edge Function (service role). RLS is on with no policies,
-- so the public API keys can neither read nor write this table directly.

create table if not exists public.skill_feedback (
  id            uuid primary key default gen_random_uuid(),
  received_at   timestamptz not null default now(),
  schema_version smallint not null default 1,
  install_id    uuid not null,               -- random per installation, not derived from the user
  skill         text not null check (skill ~ '^[a-z0-9][a-z0-9-]{1,63}$'),
  event         text not null check (event in ('gap','failure','wrong_info','suggestion','new_skill_request','success_note')),
  outcome       text check (outcome in ('success','partial','failure')),
  agent         text not null check (agent in ('claude','cursor','gemini','antigravity','windsurf','chatgpt','codex','copilot','other')),
  surface       text not null check (surface in ('cli','desktop','web','mobile','ide','api','other')),
  os            text not null check (os in ('macos','windows','linux','ios','android','other','unknown')),
  skill_version text check (skill_version ~ '^[A-Za-z0-9._-]{1,40}$'),
  tags          text[] not null default '{}',
  gap           text check (char_length(gap) <= 300),
  suggestion    text check (char_length(suggestion) <= 500),
  gap_hash      text not null,
  status        text not null default 'new' check (status in ('new','reviewed','accepted','rejected','duplicate')),
  review_note   text,
  reviewed_at   timestamptz
);
create unique index if not exists skill_feedback_dedup on public.skill_feedback (install_id, skill, gap_hash, ((received_at at time zone 'UTC')::date));
create index if not exists skill_feedback_skill_status on public.skill_feedback (skill, status, received_at desc);
create index if not exists skill_feedback_install_day on public.skill_feedback (install_id, received_at);

alter table public.skill_feedback enable row level security;
revoke all on public.skill_feedback from anon, authenticated;

create table if not exists public.skill_feedback_reviews (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  period      text not null,               -- e.g. 2026-11
  summary     text not null,
  actions     jsonb not null default '[]'
);
alter table public.skill_feedback_reviews enable row level security;
revoke all on public.skill_feedback_reviews from anon, authenticated;

comment on table public.skill_feedback is 'Anonymous skill improvement reports. No personal data by design; see skills/skill-feedback/references/privacy.md';
