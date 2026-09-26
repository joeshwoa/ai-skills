# Example: dry run (captured, real output)

```bash
bash scripts/call.sh init_dev_universe @brief.json
```

```json
{"project_type":"flutter_app","name":"Sofra","backend":"supabase","dry_run":true,
 "description":"A recipe sharing app called \"Sofra\" for Egyptian home cooks. Cooks sign up, save favourite recipes offline, and search by ingredient. Launching in Egypt and the EU, so GDPR matters. iOS and Android."}
```

# Plan for Sofra (dry run — nothing written)

**Would write to:** `~/AI-Projects/devuniverse/projects/sofra`
**Summary:** Sofra: supabase, riverpod, 7 decisions (0 contested).
**App:** Flutter (riverpod, supabase, offline: drift) · **Service:** none
**Flutter dependencies:** go_router ^18.0.1, flutter_riverpod ^3.4.3, supabase_flutter ^2.17.2, drift ^2.35.0, drift_flutter ^0.3.1

## Decisions (full debate in MEETING_TRANSCRIPT.md)

| Topic | Ruling | Runner-up | Margin |
|---|---|---|---|
| Backend Platform | `supabase` | `firebase` | 42% |
| Custom Service Layer | `none` | — | 100% |
| Flutter State Management | `riverpod` | `bloc` | 57% |
| Micro-Interactions & HUD Animation | `rive` | `lottie` | 78% |
| Offline & Sync Layer | `drift` | — | 100% |
| Container & Isolation Strategy | `multistage_rootless` | — | 100% |
| Testing & Verification Strategy | `pyramid_golden` | — | 100% |

## Cross-examination preview — 8 passed, 0 fixed/warning

## Files (47)

**.env.example** (1)
- `.env.example`

**.github** (1)
- `.github/workflows/ci.yml`

**.gitignore** (1)
- `.gitignore`

**app (other)** (8)
- `app/.env.example`
- `app/analysis_options.yaml`
- `app/assets/generated/README.md`
- `app/assets/incoming/README.md`
- `app/pubspec.yaml`
- `app/README.md`
- `app/test/local_store_test.dart`
- `app/test/widget_test.dart`

**app/lib** (15)
- `app/lib/app.dart`
- `app/lib/bootstrap.dart`
- `app/lib/config/env.dart`
- `app/lib/data/auth_repository.dart`
- `app/lib/data/local_store.dart`
- `app/lib/data/supabase_auth_repository.dart`
- `app/lib/features/auth/auth_page.dart`
- `app/lib/features/explore/explore_page.dart`
- `app/lib/features/home/home_page.dart`
- `app/lib/features/settings/settings_page.dart`
- `app/lib/main.dart`
- `app/lib/router/app_router.dart`
- `app/lib/router/routes.dart`
- `app/lib/state/providers.dart`
- `app/lib/theme/design_tokens.dart`

**backend** (4)
- `backend/supabase/migrations/0001_init.sql`
- `backend/supabase/migrations/0002_storage_policies.sql`
- `backend/supabase/README.md`
- `backend/supabase/seed.sql`

**blueprint.json** (1)
- `blueprint.json`

**compliance** (3)
- `compliance/PRIVACY_POLICY.md`
- `compliance/STORE_COMPLIANCE_CHECKLIST.md`
- `compliance/TERMS_OF_SERVICE.md`

**design-tokens.json** (1)
- `design-tokens.json`

**design** (1)
- `design/DESIGN_LANGUAGE.md`

**docs** (8)
- `docs/adr/0001-backend-platform.md`
- `docs/adr/0002-service-layer.md`
- `docs/adr/0003-state-management.md`
- `docs/adr/0004-micro-interactions.md`
- `docs/adr/0005-offline-layer.md`
- `docs/adr/0006-container-strategy.md`
- `docs/adr/0007-testing-strategy.md`
- `docs/ENV_ROUTING.md`

**MEETING_TRANSCRIPT.md** (1)
- `MEETING_TRANSCRIPT.md`

**README.md** (1)
- `README.md`

**scripts** (1)
- `scripts/check_rls.sh`

Call `init_dev_universe` again with the same arguments and `dry_run: false` to write it.
