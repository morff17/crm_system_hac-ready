# Выполненная проверка перед упаковкой

Проверки выполнялись в среде сборки репозитория.

- `python -m compileall backend/app backend/alembic` — успешно.
- YAML `docker-compose.yml`, JSON realm Keycloak и XML ArchiMate — синтаксически валидны.
- Alembic `upgrade head` на чистой SQLite БД — успешно до `0002_upgrade_legacy`.
- Backend smoke через FastAPI `TestClient` (SQLite, auth-disabled тестовый режим):
  - health, auth/me;
  - каталог ВУЗов;
  - dashboard;
  - 14 этапов workflow;
  - переход workflow + история;
  - XLSX/PDF/JSON отчёты;
  - PNG диаграмма;
  - XLSX импорт направления;
  - versioning workflow;
  - Redis user-cache API;
  - integration idempotency;
  - RBAC data-scope на уровне query.
- 10 параллельных XLSX-отчётов через локальный TestClient: все HTTP 200, wall time около 0.12 с на демонстрационном наборе.
- 50 параллельных запросов списка ВУЗов: все HTTP 200, wall time около 0.28 с, max request около 0.24 с на демонстрационном наборе.

Эти числа **не являются подтверждением SLA на продуктивном сервере**: SQLite/TestClient не эквивалентны Docker/PostgreSQL/сети. Для целевого стенда приложен `loadtest/locustfile.py`.

Полный `docker compose build/up` и `npm ci` в текущей среде выполнить невозможно из-за отсутствия сетевого доступа к npm/PyPI/Docker registry и Docker daemon. Конфигурация контейнеров и исходный код проверены статически/локальными backend-тестами; финальный smoke после скачивания образов выполняется командой `tests/smoke.sh`.
