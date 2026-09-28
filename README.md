# CRM ИТ Школы Ростелекома — fullstack

Готовый к контейнерному развёртыванию прототип CRM по ТЗ хакатона.

## Что реализовано

- React web-интерфейс, адаптивный для desktop/mobile;
- FastAPI backend и Swagger UI;
- PostgreSQL + Alembic baseline migration;
- Keycloak: роли `user`, `manager`, `admin`, управление ролями через Keycloak Admin API из admin UI;
- разграничение данных: обычный пользователь видит ВУЗы назначенного ему менеджера, руководитель/admin — весь контур;
- назначение ответственного за ВУЗ;
- каталоги ВУЗов, направлений, продуктов и ответственных;
- XLS/XLSX импорт всех каталогов;
- базовый workflow из 14 этапов, создание и изменение workflow с версионированием;
- переходы только на соседний этап (admin может выполнить служебный переход);
- комментарии, вложения и история workflow;
- формирование XLS, XLSX, PDF, JSON отчётов с фильтрами по периоду, ВУЗу, направлению, продукту, ответственному и статусу;
- выбор колонок отчёта;
- реальные dashboard/analytics данные без моковой аналитики;
- экспорт диаграммы в PNG/PDF;
- API ingest для LMS/website, идемпотентность по `external_id`;
- Redis cache с инвалидацией при изменениях;
- журнал аудита;
- встроенная документация `/help` со скриншотами элементов интерфейса;
- пример ArchiMate exchange-модели в `docs/architecture.xml`;
- перечень библиотек и компонентов в `docs/COMPONENTS.md`;
- smoke-test и Locust-сценарий для проверки 50 пользователей / параллельных отчётов.

## Быстрый запуск на Linux-сервере

Нужны Docker Engine и Docker Compose v2.

```bash
cp .env.example .env
nano .env            # ОБЯЗАТЕЛЬНО поменять пароли и CRM_CLIENT_SECRET
docker compose up -d --build
```

После старта:

- CRM: `http://SERVER/`
- Swagger: `http://SERVER/docs`
- Keycloak: `http://SERVER:8081/`

Для проверки:

```bash
BASE_URL=http://SERVER CRM_USER=admin CRM_PASSWORD='<ваш DEMO_ADMIN_PASSWORD>' ./tests/smoke.sh
```

## Демо-учётки

Они создаются только для демонстрационного контура из `.env`:

- `user` / `DEMO_USER_PASSWORD` — видит только назначенные ему ВУЗы;
- `manager` / `DEMO_MANAGER_PASSWORD` — видит все ВУЗы и может менять ответственных;
- `admin` / `DEMO_ADMIN_PASSWORD` — дополнительно получает администрирование и workflow editor.

Перед публичным развёртыванием замените все пароли в `.env`.

## Импорт XLS/XLSX

Примеры находятся в `samples/`:

- `institutions.xlsx`;
- `directions.xlsx`;
- `products.xlsx`;
- `managers.xlsx`.

Для ВУЗов поддерживаются поля из ТЗ: название, вендор, ПО, номер договора, дата подписания лицензии, срок действия лицензии, статус передачи, ФИО менеджера, ответственный от ВУЗа, комментарий; дополнительно регион и город.

## API интеграции

Поддерживаются оба сценария: приём JSON webhook/ingest и активная синхронизация CRM с внешним API.

```http
POST /api/integrations/lms/ingest
POST /api/integrations/website/ingest
POST /api/integrations/lms/sync
POST /api/integrations/website/sync
```

Для `sync` задайте в `.env` `LMS_API_URL`, `LMS_API_TOKEN`, `WEBSITE_API_URL`, `WEBSITE_API_TOKEN`. Внешний API должен вернуть JSON-массив либо `{ "items": [...] }` по согласованному маппингу.

Пример JSON:

```json
{
  "external_id": "lms-12345",
  "institution": "МГТУ им. Баумана",
  "direction": "DevOps",
  "product": "Deckhouse",
  "students_count": 240,
  "streams_count": 2,
  "applications_count": 310
}
```

Повторная отправка того же `source + external_id` обновляет существующее взаимодействие вместо создания дубля.

## Безопасность

JWT проверяется по JWKS Keycloak с фиксированным алгоритмом RS256, issuer и client (`azp`). Реализованы RBAC/data-scope и аудит действий. Загружаемые файлы ограничены разрешёнными расширениями и размером.

**Важно:** приложение не может само по себе гарантировать организационно-техническое соответствие 152-ФЗ и приказу ФСТЭК №117. В продуктивном контуре дополнительно требуются TLS, защищённое управление секретами, резервное копирование, журналы ОС/СУБД, антивирус/сканирование вложений, регламенты доступа, аттестационные и иные меры конкретного класса системы.

## Нагрузка

FastAPI запускается с 4 worker-процессами; синхронные генераторы отчётов выполняются в threadpool и не блокируют event loop. Пул PostgreSQL настроен на 10 соединений + 20 overflow на процесс.

Для стендовой проверки используйте `loadtest/locustfile.py`. Сам факт соответствия лимиту «≤1 сек», 50 пользователей и 10 одновременных отчётов должен подтверждаться именно на целевом сервере, потому что результат зависит от CPU/RAM/диска/сети.

## Структура

```text
backend/             FastAPI + SQLAlchemy + Alembic
src/                 React UI
keycloak/            realm import
samples/             примеры XLSX
public/guide/         изображения для встроенной документации
docs/                архитектура и ArchiMate exchange
loadtest/            Locust
/tests               smoke test
docker-compose.yml   PostgreSQL + Keycloak + Redis + backend + frontend
```

## Обновление схемы БД

При запуске backend выполняет:

```bash
alembic upgrade head
```

Для будущих изменений схемы:

```bash
cd backend
alembic revision --autogenerate -m "change"
alembic upgrade head
```
