## Why

Основной change `telegram-development-workflow` структурно валиден, но исследования и локальные прототипы недостаточно связаны с его задачами и актуальным design. Необходимо восстановить проверяемую трассировку и закрепить штатный OpenSpec workflow для всех доработок, не превращая документационную готовность в runtime acceptance.

## What Changes

- Сопоставить исходные product tasks и каждый requirement/scenario с implementation/evidence либо явным FAILED/NOT_RUN; сохранить различие local/mock/native/canary/live.
- Подготовить и согласовать точечные revisions существующих product artifacts. Исследование app-server остаётся кандидатом, а не задним числом принятым изменением MVP1.
- Создать единую инструкцию `openspec/WORKFLOW.md`, добавить короткую ссылку и обязательный workflow в `AGENTS.md`, дополнить context/rules в `openspec/config.yaml` без ослабления approvals.
- Привести `tasks/todo.md` к операторскому индексу с явно отделённой историей; product execution checklist остаётся в соответствующем change/tasks.md.
- Закрепить штатные explore/propose/update/apply, semantic verification и отдельно разрешаемые sync/archive. Переиспользовать установленные Hermes/Codex skills; не устанавливать новые плагины.
- Определить условный трёхволновой консилиум полного состава E01–E19 для спорных решений; советы не заменяют доказательства и полномочия владельца.

## Capabilities

### New Capabilities

Нет новых продуктовых capabilities. Это tooling/docs-only адаптация, `.openspec.yaml` содержит `skip_specs: true`; фиктивные delta specs не создаются.

### Modified Capabilities

Нет изменения пользовательских контрактов. Если сверка обнаружит необходимость изменить поведение Telegram, исполнителя, approvals или backups, изменение выносится на отдельное согласование product revision и не проводится под `skip_specs` этого change.

## Impact

Файлы процесса: `AGENTS.md`, `openspec/config.yaml`, новый `openspec/WORKFLOW.md`, `tasks/todo.md`. Плановые артефакты и доказательства адаптации находятся в этом change; согласованные уточнения existing product artifacts — в `openspec/changes/telegram-development-workflow/`.

Основание: `.hermes/plans/2026-09-16_193737-openspec-workflow-reconciliation.md`. Применяется локальный OpenSpec 1.13.0 через `./run-openspec`; зависимости, shared profiles и ядро Hermes не меняются. Полная инструкция и аудит являются результатами будущего apply, не завершёнными результатами создания proposal.

## Non-Goals

Не реализовывать runtime/lifecycle, не исправлять повреждённый `test_stock_lifecycle.py` в рамках docs change, не запускать новую VM/model canary, не изменять сервер/OAuth, не публиковать и не архивировать автоматически. Не удалять исследовательскую историю, не создавать scheduler/approval service, не включать дополнительные платные сервисы. ORCH-01 / CRITICAL и product readiness gates остаются открытыми.

## Owner Decisions

После предъявления proposal/design/tasks нужен отдельный запрос apply по установленному propose workflow и пункту A.8 согласованного плана. Product artifact edits требуют подтверждения предлагаемых revisions; docs migration не означает approval production spec. Изменение инфраструктуры, publication, archive и закрытие ORCH-01 остаются отдельными решениями владельца.
