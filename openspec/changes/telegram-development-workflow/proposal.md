## Why

Первый принимаемый результат — рабочая среда на ainetic.tech: задача из Telegram проходит через OpenSpec, Hermes и Codex до реальных изменений, тестов и отчёта, а владелец параллельно работает в обычном интерактивном Codex по SSH. Полный MVP1 дополнительно включает private PR, локальный preview и offsite backup/restore. Уточнения интервью 2026-09-23 — в interview-decisions.md; baseline.md остаётся датированным историческим evidence, не текущей проверкой сервера. Разрешение обновить документы не разрешает coding, GitHub publication или deployment.

## What Changes

- Telegram-запрос связывается с проектом, OpenSpec change/revision и единственным намерением исполнения.
- Hermes использует штатные Telegram, approvals и специализированные средства запуска Codex, если их совместимость подтверждена. Один переиспользуемый контейнер на проект, не на задачу; отдельная папка на диске сервера через bind mount сохраняет код, Git/worktrees, спецификации, полную историю и результаты при пересоздании контейнера.
- Отдельный обычный интерактивный Codex CLI доступен по SSH в том же project container. Разрыв SSH не прекращает ручную сессию, reconnect возвращает в неё. Ручной и автоматический writers используют разные worktrees/ветки; интеграция последовательная с повторными тестами. Полноценные специализированные профили и перехват автоматической сессии не требуются.
- Кандидат и сама рабочая среда проверяются реальным evidence; отчёт первого этапа не требует ещё не созданных PR/preview. Backend/API tests нужны только проектам с backend.
- На последующем publication-инкременте после согласования repository binding разрешены private repo, task-branch push и PR. Merge main, rights/visibility и infrastructure требуют отдельного owner decision штатными средствами; собственного approval service нет.
- Первый демонстрационный продукт последующего инкремента — RussianLioN/contemporary-dance-guide: русский статический гид и вымышленная студия, HTML/CSS/JS без framework/build; preview/index.html через file:// той же ветки/commit, без server preview. Это не prerequisite приёмки рабочей среды.
- Полная приватная история Hermes/Codex сохраняется отдельно от ограниченного актуального контекста, автоматически собираемого при запуске. Markdown/Git sources и MemPalace index дополняют историю, но не заменяют её; credentials и общий writable home не делятся.
- Два уровня расширений: общие OpenSpec/MemPalace/skills/rules с отдельной проверкой адаптеров Hermes/Codex и изолированные project tools/skills/dependencies. Внутри разрешённого проекта code/dependencies/tests автономны; shared tools/base image/server/SSH/mount permissions требуют Telegram approval.
- ORCH-01 / CRITICAL входит в MVP1: независимый контроль задач, обнаружение подтверждённой остановки в пределах пяти минут, ограниченные повторы и восстановление после restart.
- Существующий updater сохраняет автоматическую согласованную политику и все защиты; будущая координация учитывает также ручные сессии. Compact encrypted GitHub backups по изменениям/событиям с daily fallback — последующий инкремент. Их отсутствие не даёт права отключить уже действующие проверки обновления.
- Повторы, restart, отмена и неизвестный исход внешнего действия получают явные контракты восстановления.
- Addy Agent Skills определяют рабочие процедуры; OpenSpec хранит спецификации, а Kanban — runtime lifecycle. Вторую очередь OpenSpec не создаёт.

## Capabilities

### New Capabilities

- `task-intake`: авторизация, привязка spec revision, дедупликация и допуск задачи.
- `specialist-dispatch`: назначение профилей, проверка совместимости и границ полномочий.
- `code-execution`: ограниченный Codex, бюджеты, процессная изоляция и отмена.
- `verification`: независимые проверки того же candidate и контролируемые evidence.
- `change-publication`: автономные task branch/PR, owner-controlled merge и reconciliation.
- `telegram-delivery`: маршрутизация статуса/артефактов и независимое восстановление доставки.
- `portable-memory`: переносимые знания, полная история, разрешённый retrieval, автоматический стартовый контекст и checkpoints.
- `project-environments`: один reusable Dev Container на проект, постоянный server bind mount, владельцы ресурсов, ограничения и очистка.
- `interactive-access`: отдельный интерактивный Codex по SSH, reconnect той же сессии и изолированные ручные writers.
- `task-recovery`: ORCH-01, heartbeat, retry и reconciliation.
- `maintenance-coordination`: drain и безопасное взаимодействие с существующим updater.
- `offsite-backup`: зашифрованные пакеты, restore attestation и retention.
- `local-preview`: статическая локальная приёмочная страница без серверных сервисов.

### Modified Capabilities

Нет: `openspec list --specs` не обнаружил существующих спецификаций.

## Impact

Implementation repository — выбранный владельцем `/Users/s060874gmail.com/coding/projects/hermes-agent`; `hermes-remote-migration` только read-only donor. Ранние `runtime/` пути research не являются картой реализации. Подтверждением «+» от 2026-09-28 разрешены пакет E1-LOCAL-PACKET-2026-09-28 и только локальный data-only policy/layout срез 3.1.1–3.1.8, без запуска контейнеров/модели. Его новые файлы — `scripts/project_environment.py` и `tests/test_project_environment.py`; dependencies только Python stdlib. Runtime budget, UID/ACL/quota, native credential boundary, history и updater остаются gates, а не доказанными свойствами этого parser.

Текущий полный change — **draft, full runtime approval pending**. Отдельное разрешение local slice не закрывает E1/1.6, не разрешает server/OAuth/updater/deploy и не превращает schema validation в acceptance. Исходный анализ: `.hermes/research/telegram-hermes-codex/05-current-gaps.md`, `07-decisions.md`, `10-implementation-plan.md`, `13-reproduction.md`.

## Non-goals

- Автоматическое слияние, production deploy, выполнение инфраструктурных изменений в рамках подготовки спецификации.
- Поддержка всех языков/фреймворков без отдельных проверяемых adapters.
- Мультиарендная платформа, Kubernetes и собственная очередь поверх Kanban.
- Платные backup/preview сервисы, собственные approvals, удалённый preview и автоматическое исполнение кода на машине владельца.
- Перехват Hermes-launched сессии и обязательный переход на app-server; административное read-only обследование не равно пользовательскому SSH workflow.
- Непрерывность прежнего процесса при разрушении контейнера/host и production readiness по одной промежуточной приёмке.
- Обещание exactly-once для сетевых эффектов либо безопасности по одному имени профиля.

## Open Questions

Host, GitHub owner, implementation repo и первый downstream demo выбраны; первая приёмка — рабочая среда. До runtime реализации обязательны native/interface/isolation/history/SSH gates, actual resource admission и exact E1 revision approval. Разрешённый pure local slice независим от этих runtime действий и не закрывает их. GitHub backup suitability блокирует последующий инкремент/full readiness. Latest docs не доказывают installed compatibility; blocker не разрешает отвергнутую подсистему. Карта зависимостей и область этапов — design.md; full exact revision approval pending.

## Native launch preparation 2026-09-28

E1-NATIVE-PACKET-2026-09-28: подготовлен source-backed пакет раздельных Codex exec/TUI проверок, выбран Gate B — BLOCKED_WITH_ACTIONABLE_PACKET. Следующий минимальный outcome — установить native seam отказа до task/tool effects, затем предъявить один runnable TDD-срез; не добавлять mock parser вместо проверки CLI. Локального source corpus недостаточно для обоих EnvironmentManager/tool dispatch и Codex recorder. Это не утверждение об отсутствии upstream feature.

Один reusable container/project, постоянная server folder с полной историей и automatic current context, separate SSH/worktrees, credential isolation и daily updater protections остаются обязательными. Нового product intent или capability нет. C2 остаётся кандидатом; переход на Hermes app-server, shared credential identity или client вне project container не разрешён. Реализация, source download, model/VM/server/credentials/updater changes и Git writes не входят в этот документационный Update. Полный approval и implementation_ready остаются false. Evidence и следующие ограничения — implementation-readiness.md#native-launch-preparation-2026-09-28.
