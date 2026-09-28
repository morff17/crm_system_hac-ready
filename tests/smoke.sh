#!/usr/bin/env sh
set -eu
BASE="${BASE_URL:-http://localhost}"
USER="${CRM_USER:-admin}"
PASS="${CRM_PASSWORD:-admin123}"
curl -fsS "$BASE/api/health" >/dev/null
TOKENS=$(curl -fsS -X POST "$BASE/api/auth/login" -H 'Content-Type: application/json' -d "{\"login\":\"$USER\",\"password\":\"$PASS\"}")
TOKEN=$(printf '%s' "$TOKENS" | python3 -c 'import json,sys;print(json.load(sys.stdin)["access_token"])')
AUTH="Authorization: Bearer $TOKEN"
curl -fsS "$BASE/api/auth/me" -H "$AUTH" >/dev/null
curl -fsS "$BASE/api/institutions?size=5" -H "$AUTH" >/dev/null
curl -fsS "$BASE/api/dashboard" -H "$AUTH" >/dev/null
curl -fsS "$BASE/api/reports/export?format=json" -H "$AUTH" >/dev/null
curl -fsS "$BASE/api/workflows" -H "$AUTH" >/dev/null
echo "Smoke tests passed"
