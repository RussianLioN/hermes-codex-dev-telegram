## Why

В workspace уже есть OpenSpec и продуктовые delta specs, но нет единой точки входа, карты поддерживаемых компонентов и маршрута небольших следующих изменений. Первичный посев должен позволить новому исполнителю продолжить работу без догадок и без смешения работающих локальных средств, исследовательских результатов, будущего продукта и разрешений владельца.

## What Changes

- Создать `openspec/README.md` — порядок чтения, безопасные inspection-команды и ссылки на текущие gates.
- Создать `openspec/PROJECT.md` — as-is карта root scripts, tooling, собственного provider, прототипов, исследований и внешней установки Hermes; отдельно показать proposed продукт и границы подтверждённости.
- Создать `openspec/ROADMAP.md` — dependency index существующих product outcomes и правила декомпозиции на задачи по 2–5 минут. Не создавать второй checklist или очередь исполнения.
- Создать внутри этого change `research.md`, `coverage.md`, `verification.md`: применённые официальные практики, карта покрытия текущих требований/задач и реальные результаты проверки документов. Существующий полный scenario audit переиспользуется ссылками.
- Дополнить только `openspec/WORKFLOW.md` навигацией и точным форматом малой задачи; в текущий операторский индекс `tasks/todo.md` добавить одну ссылку на change. Сохранить историю, approvals и ограничения.
- Выполнять посев инкрементально через `tasks.md` этого change с проверками структуры, ссылок, полноты и непротиворечивости. Создание плановых артефактов не засчитывать как выполнение посева.

## Capabilities

### New Capabilities

Нет. Это документационное изменение без нового specified runtime behavior. В `.openspec.yaml` явно задано `skip_specs: true`; фиктивные requirements и каталог delta specs не создаются.

### Modified Capabilities

Нет. Требования `telegram-development-workflow` и текущие основные specs не изменяются. Пустой `openspec/specs/` не заполняется незавершённым продуктом ради внешней полноты.

## Impact

Разрешаемые новые planning artifacts: `.openspec.yaml`, `proposal.md`, `design.md`, `tasks.md` внутри `openspec/changes/seed-project-documentation/`. Будущий apply ограничен шестью новыми документами и двумя существующими документами, перечисленными в What Changes, плюс отметками исполнения в собственном `tasks.md`.

Runtime code, API, зависимости и конфигурация не меняются. `AGENTS.md`, `openspec/config.yaml`, оба прежних change, product approvals, root scripts, tooling/source, generated skills и внешний Hermes остаются неизменными. После разрешённых docs writes обновляется только производный индекс MemPalace для `tasks` и `openspec`; это не новый источник истины и не реализация продукта.

Работа опирается на установленный OpenSpec 1.13.0, штатную schema `spec-driven` и [сохранённый план](../../../.hermes/plans/2026-09-21_191959-openspec-project-documentation-seed.md). Применение официального brownfield-подхода и отказ от массового backfill обоснованы в `design.md`.

## Non-Goals

- Не реализовывать Telegram-продукт, контроллер, publisher, runner или memory lifecycle; не ремонтировать исследовательские тесты.
- Не выбирать production repository/runner и не объявлять исторические canary или mock результаты полной приёмкой.
- Не переинициализировать/обновлять OpenSpec, не менять schema, не переписывать vendor/core, не устанавливать зависимости.
- Не читать credentials, environment files, архивы, private histories или SSH keys/config; не делать backup/config/OAuth/server/profile изменений.
- Не выполнять Git init/commit/push, publication, deployment, sync или archive.
- Не закрывать R1–R3, OS-06/07/08/09, MEM-02b или ORCH-01 на основании документационной готовности.

## Owner Decisions

Следующий отдельный запрос на apply должен относиться к предъявленным `proposal.md`, `design.md` и `tasks.md` этого change. До него создаются только planning artifacts; посев README/PROJECT/ROADMAP и правки WORKFLOW/TODO не начинаются.

Согласование R1–R3 и защищённой записи AGENTS остаётся в `adopt-openspec-workflow`; exact product approval, выбор implementation repo/runner и runtime grants — в продуктовом change. Они не являются скрытыми условиями документационного apply и не выдаются этим proposal.

ORCH-01 / CRITICAL остаётся открытым: независимый production-контроллер не реализован. OpenSpec и MemPalace не мониторят и не перезапускают остановившихся агентов.
