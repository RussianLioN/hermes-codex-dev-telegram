## Purpose

Подтверждать качество конкретного результата воспроизводимыми проверками, соответствующими типу проекта, и отличать проверенный статический интерфейс от работающего backend.

## ADDED Requirements

### Requirement: TG-07 Independent immutable evidence
Система SHALL подтверждать verified только по доверенным обязательным проверкам неизменяемого candidate, связанным с task/run/spec/policy/skill revision. Сообщение модели, exit0 или native done MUST NOT сами по себе означать пользовательскую приёмку.

#### Scenario: Tampered tests on faulty implementation
- **WHEN** заведомо ошибочный candidate сопровождается always-pass локальным runner или поддельным отчётом
- **THEN** доверенная обязательная проверка обнаруживает ошибку и verified не выставляется

#### Scenario: Changed candidate
- **WHEN** код или обязательный acceptance pack изменён после проверки
- **THEN** прежний receipt не разрешает приёмку изменённого результата

### Requirement: TG-08 Project-appropriate acceptance
Система SHALL выбирать реальные проверки по типу проекта и согласованному инкременту. Первая промежуточная приёмка SHALL проверять рабочую среду: Telegram → Hermes/Codex → реальные code changes/tests → отчёт, отдельный интерактивный SSH Codex, disconnect/reconnect, параллельные worktrees/интеграцию, сохранение полной истории и автоматическую загрузку контекста после нового запуска/пересоздания контейнера. Эта приёмка SHALL NOT означать полную готовность MVP1 или закрытие ORCH-01. Для первого демонстрационного проекта последующего инкремента SHALL проверяться локальная file:// страница, desktop/mobile viewport, клавиатурная навигация, отсутствие console errors и обязательных внешних запросов, локальные assets и явная маркировка вымышленной студии. Backend/full-stack не требуется этому fixture; будущая full-stack задача MUST проверять настоящий тестовый API и error path, а не выдавать demo за backend evidence. Консультации отдельных контекстов одной модели SHALL называться именно так, не независимыми моделями.

#### Scenario: Static guide success
- **WHEN** preview/index.html открывается через file:// без сети и проходит согласованные desktop/mobile и keyboard сценарии
- **THEN** система сохраняет команды, коды выхода, assertions, console/network evidence и screenshots того же candidate, не заявляя наличие проверенного backend

#### Scenario: Files exist but browser flow fails
- **WHEN** файлы созданы, но обязательный браузерный сценарий не работает или требует CDN/API
- **THEN** задача не признаётся verified и возвращается на исправление с фактическим evidence

#### Scenario: Working environment acceptance
- **WHEN** все согласованные проверки первого этапа выполнены на разрешённой среде для точных revisions, включая негативные isolation/history/SSH случаи
- **THEN** evidence разделяет проверку рабочего окружения и конкретного code candidate; принимается только этот инкремент, а private PR, dance-guide, offsite backup/restore и production ORCH-01 остаются отдельными незавершёнными обязательствами

#### Scenario: Mounted files without automatic context
- **WHEN** файлы пережили пересоздание контейнера, но новый Hermes или Codex не загрузил актуальный проектный контекст автоматически
- **THEN** первая приёмка не проходит; существующий mount, MemPalace search и ручной paste истории не заменяют MEM-12 evidence
