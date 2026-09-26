#!/usr/bin/env bash
# Prove a devuniverse-generated project really works before telling the user
# it does. Runs every toolchain that is installed and reports what it could
# NOT check — never silently skips.
#
#   verify_project.sh <project_dir> [--platforms android,ios] [--no-platforms] [--no-audit]
#
# App (app/):      flutter create <platforms> (only if the folders are missing),
#                  pub get, analyze (errors fail; warnings reported), test
# Service:         npm install, tsc --noEmit, npm test, npm run build
# Supabase:        scripts/check_rls.sh (every table has RLS)
# Compliance:      audit_compliance through call.sh (high severity fails)
# Exit: 0 all run checks passed · 1 a check failed · 2 usage error
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${1:-}"
[ -n "$PROJECT" ] && [ -d "$PROJECT" ] || { echo "usage: verify_project.sh <project_dir> [--platforms android,ios] [--no-platforms] [--no-audit]" >&2; exit 2; }
shift
PLATFORMS="android,ios"; ADD_PLATFORMS=1; AUDIT=1
while [ $# -gt 0 ]; do
  case "$1" in
    --platforms) [ $# -ge 2 ] || { echo "--platforms needs a value, e.g. android,ios" >&2; exit 2; }; PLATFORMS="$2"; shift ;;
    --no-platforms) ADD_PLATFORMS=0 ;;
    --no-audit) AUDIT=0 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
  shift
done
PROJECT="$(cd "$PROJECT" && pwd)"
have() { command -v "$1" >/dev/null 2>&1; }
RESULTS=(); FAILED=0
pass() { RESULTS+=("PASS     $1"); }
fail() { RESULTS+=("FAIL     $1"); FAILED=1; }
skip() { RESULTS+=("NOT RUN  $1 — $2"); }
LOG="$(mktemp -d)"

# ---------------- Flutter app
if [ -f "$PROJECT/app/pubspec.yaml" ]; then
  if have flutter; then
    cd "$PROJECT/app"
    PKG="$(sed -n 's/^name:[[:space:]]*//p' pubspec.yaml | head -1)"
    if [ "$ADD_PLATFORMS" = 1 ]; then
      missing=0
      for p in ${PLATFORMS//,/ }; do [ -d "$p" ] || missing=1; done
      if [ "$missing" = 1 ]; then
        if flutter create . --platforms="$PLATFORMS" --project-name "$PKG" >"$LOG/create.log" 2>&1; then
          pass "flutter create --platforms=$PLATFORMS"
        else fail "flutter create (see $LOG/create.log)"; fi
      fi
    fi
    if flutter pub get >"$LOG/pub.log" 2>&1; then pass "flutter pub get"; else fail "flutter pub get (see $LOG/pub.log)"; fi
    flutter analyze --no-fatal-infos --no-fatal-warnings >"$LOG/analyze.log" 2>&1
    errs=$(grep -c "^ *error •" "$LOG/analyze.log" || true)
    warns=$(grep -c "^ *warning •" "$LOG/analyze.log" || true)
    if [ "$errs" = 0 ] && ! grep -q "Error:" "$LOG/analyze.log"; then
      pass "flutter analyze (0 errors, $warns warnings)"
    else fail "flutter analyze ($errs errors — see $LOG/analyze.log)"; grep "error •" "$LOG/analyze.log" | head -10; fi
    if [ -d test ]; then
      if flutter test >"$LOG/test.log" 2>&1; then
        pass "flutter test ($(grep -Eo '\+[0-9]+' "$LOG/test.log" | tail -1 | tr -d +) tests)"
      else fail "flutter test (see $LOG/test.log)"; tail -20 "$LOG/test.log"; fi
    else skip "flutter test" "no test/ folder"; fi
  else
    skip "Flutter app" "flutter is not installed on this machine"
  fi
else
  skip "Flutter app" "project has no app/ (backend_api project)"
fi

# ---------------- Node service
if [ -f "$PROJECT/backend/service/package.json" ]; then
  if have npm; then
    cd "$PROJECT/backend/service"
    if npm install --no-audit --no-fund --loglevel=error >"$LOG/npm.log" 2>&1; then pass "service npm install"; else fail "service npm install (see $LOG/npm.log)"; fi
    if npx --no-install tsc --noEmit >"$LOG/tsc.log" 2>&1; then pass "service tsc --noEmit"; else fail "service tsc (see $LOG/tsc.log)"; head -20 "$LOG/tsc.log"; fi
    if npm test --silent >"$LOG/svc-test.log" 2>&1; then pass "service npm test"; else fail "service npm test (see $LOG/svc-test.log)"; tail -20 "$LOG/svc-test.log"; fi
    if grep -q '"build"' package.json; then
      if npm run build --silent >"$LOG/svc-build.log" 2>&1; then pass "service npm run build"; else fail "service build (see $LOG/svc-build.log)"; fi
    fi
  else skip "Node service" "npm is not installed"; fi
fi

# ---------------- Supabase RLS
if [ -d "$PROJECT/backend/supabase/migrations" ]; then
  if [ -x "$PROJECT/scripts/check_rls.sh" ] || [ -f "$PROJECT/scripts/check_rls.sh" ]; then
    if (cd "$PROJECT" && bash scripts/check_rls.sh) >"$LOG/rls.log" 2>&1; then pass "RLS on every table"; else fail "RLS check"; cat "$LOG/rls.log"; fi
  fi
  skip "migrations on a real Postgres" "run: cd backend && supabase init && supabase start && supabase db reset"
fi
if ls "$PROJECT"/backend/firebase/*.rules >/dev/null 2>&1 || [ -f "$PROJECT/firebase.json" ]; then
  skip "Firebase security rules" "test them with the emulator: firebase emulators:start (rules in backend/firebase/)"
fi

# ---------------- compliance audit
if [ "$AUDIT" = 1 ]; then
  # The server only writes inside its root: use the root this project lives in.
  case "$PROJECT" in */projects/*) export DEVUNIVERSE_ROOT="${PROJECT%/projects/*}" ;; esac
  AUDIT_ARGS="$(node -e 'process.stdout.write(JSON.stringify({project_dir: process.argv[1]}))' "$PROJECT")"
  if bash "$SCRIPT_DIR/call.sh" audit_compliance "$AUDIT_ARGS" >"$LOG/audit.log" 2>&1; then
    pass "audit_compliance (no high-severity findings)"
  else fail "audit_compliance (see $PROJECT/compliance/AUDIT_REPORT.md)"; head -15 "$LOG/audit.log"; fi
fi

echo
echo "== verify_project: $PROJECT"
for r in "${RESULTS[@]}"; do echo "  $r"; done
echo "  logs: $LOG"
exit "$FAILED"
