# Матрица соответствия ТЗ

| Требование | Реализация |
|---|---|
| Каталоги ВУЗов, ИТ-направлений, ИТ-продуктов, ответственных в БД | PostgreSQL-модели `Institution`, `Direction`, `Product`, `Manager`, `InstitutionContact` |
| Актуализация XLS/XLSX | `/api/import/{institutions,directions,products,managers}`, UI импорта, примеры в `samples/` |
| Фильтрация | API и UI: период, ВУЗ, направление, продукт, ответственный, статус |
| Статистика/диаграммы | `/api/dashboard`, `/api/analytics/programs`, React-компоненты используют реальные данные |
| PNG/PDF визуализации | `/api/reports/chart?format=png|pdf` + UI |
| Workflow и переходы | 14 базовых этапов, переходы, комментарии, история, соседние переходы |
| Корректировка/создание workflow | admin UI + API, versioning используемых workflow |
| Вложения | png/jpeg/pdf/zip/gzip/rar/doc/docx/xls/xlsx, UI + download |
| Отчёты XLS/XLSX/PDF | `/api/reports/export`, UI, выбор фильтров/колонок |
| Результирующий JSON | формат `json` в том же endpoint |
| LMS / web-site JSON API | ingest endpoints и активный `sync` по настроенным URL/token, idempotency `source+external_id` |
| Keycloak | login/refresh, JWKS RS256 validation, issuer/client check |
| Ролевая модель | `user/manager/admin`, data-scope по назначенному менеджеру, управление ролями через Keycloak Admin API |
| Руководитель меняет ответственного | selector менеджера в карточке ВУЗа + PATCH API |
| Администратор управляет доступами | admin UI: роли Keycloak и привязка username к менеджеру |
| Кэш действий пользователя | Redis user draft cache + dashboard cache/invalidation |
| Без полной перезагрузки страниц | React SPA, API mutations + local reload данных |
| Swagger | `/docs`, OpenAPI `/openapi.json` |
| Docker/Linux | Dockerfiles + Compose: nginx, FastAPI, PostgreSQL, Redis, Keycloak |
| Миграции | Alembic baseline + upgrade legacy schema |
| Документация в платформе | `/help` с пользовательской/админской инструкцией и иллюстрациями |
| Архитектура в Archi | `docs/architecture.xml` (ArchiMate exchange), `docs/ARCHITECTURE.md` |
| Перечень библиотек | `docs/COMPONENTS.md`, lock/requirements files |
| 50 пользователей / 10 отчётов | подготовлен Locust-сценарий; фактический SLA проверяется на целевом сервере |
| <= 1 сек интерфейс | архитектура/кэш оптимизированы; фактическое значение необходимо измерять на целевом сервере |
| 152-ФЗ / ФСТЭК №117 | в приложении: RBAC, минимизация видимости, аудит, секреты через env; полное соответствие требует инфраструктурных/организационных мер целевого контура |

## Осознанные ограничения

Контракты LMS и сайта в исходном ТЗ не предоставлены. Поэтому sync-адаптер принимает общий согласуемый JSON mapping и имеет конфигурационные URL/token. После получения реального контракта меняется adapter mapping, а доменная модель/идемпотентность остаются без изменений.

Требования производительности и нормативного соответствия нельзя достоверно подтвердить одним исходным кодом: они требуют измерения и организационно-инфраструктурной оценки на фактическом стенде.
