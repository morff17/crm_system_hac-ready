# Архитектура

## Компонентная схема

```mermaid
flowchart LR
  Browser[React Web UI] --> Nginx[Nginx]
  Nginx --> API[FastAPI API]
  API --> PG[(PostgreSQL)]
  API --> Redis[(Redis)]
  API --> Files[(File volume)]
  API --> KC[Keycloak]
  LMS[LMS] --> API
  CMS[Website/CMS] --> API
```

`docs/architecture.xml` — ArchiMate Model Exchange файл, который можно импортировать в Archi для дальнейшей детализации модели.

## Функциональные блоки

- каталоги ВУЗов, ИТ-направлений, ИТ-продуктов и ответственных;
- workflow и история переходов;
- комментарии и вложения;
- отчёты XLS/XLSX/PDF/JSON и экспорт диаграмм PNG/PDF;
- RBAC и data-scope через Keycloak;
- импорт XLS/XLSX;
- интеграционный ingest LMS/website с идемпотентностью по `source + external_id`;
- аудит административных и пользовательских действий.
