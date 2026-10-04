# OpenSpec: начало работы

## Start Here

Это точка входа в macOS operations/documentation workspace, не руководство запуска готового Telegram-продукта.

1. Прочитать [AGENTS.md](../AGENTS.md) и [текущий операторский индекс](../tasks/todo.md#текущий-операторский-индекс--openspec-reconciliation): scope, skills, незакрытые gates.
2. [PROJECT.md](PROJECT.md): реальные entrypoints/tooling, as-is и proposed architecture, trust boundaries и ограничения.
3. [WORKFLOW.md](WORKFLOW.md): explore → propose/update → отдельный apply → verify; правила authority и evidence.
4. [ROADMAP.md](ROADMAP.md): dependency index небольших outcomes, правила задач по 2–5 минут и явные blockers.
5. Выбрать change через CLI, читать его proposal → specs (если не skipped) → design → tasks → первичное evidence. Progress брать из `instructions apply`, не из старого отчёта.

Контекст первичного посева: [proposal](changes/seed-project-documentation/proposal.md), [design](changes/seed-project-documentation/design.md), [checklist](changes/seed-project-documentation/tasks.md), [источники](changes/seed-project-documentation/research.md), [verification](changes/seed-project-documentation/verification.md). [Карта покрытия посева](changes/seed-project-documentation/coverage.md) — исторический снимок 2026-09-22, не current counts после интервью; актуальные contracts/tasks — в product change.

## Current State

OpenSpec pin из снимка 2026-09-22: 1.13.0, schema spec-driven. Обновление 2026-09-23: владелец выбрал текущий `hermes-agent` для реализации, local Git создан на main без commit/remote; [repo decision](changes/telegram-development-workflow/implementation-readiness.md#repository-decision-2026-09-23). Единого root application build/test runner ещё нет. Main `openspec/specs/` пуст: текущие product требования живут в in-flight delta specs. Это не неисправность init и не повод sync незавершённый продукт.

| Change | Назначение | Граница |
|---|---|---|
| [seed-project-documentation](changes/seed-project-documentation/proposal.md) | Docs-only inventory/navigation/coverage/increments, specs intentionally skipped | Checklist завершён; [tasks](changes/seed-project-documentation/tasks.md), historical [verification](changes/seed-project-documentation/verification.md). Не archived, не product acceptance |
| [adopt-openspec-workflow](changes/adopt-openspec-workflow/proposal.md) | Workflow adoption | [Current R1–R3](changes/adopt-openspec-workflow/reconciliation.md#current-reconciliation) применены; остаётся protected AGENTS/OS-07, seed его не закрывает |
| [telegram-development-workflow](changes/telegram-development-workflow/proposal.md) | Future native-first Telegram/Hermes/Codex продукт | NOT_DEPLOYABLE / CLIENT_ROUTING_GATE_OPEN, [approval pending](changes/telegram-development-workflow/review-status.json), [readiness NOT_READY](changes/telegram-development-workflow/implementation-readiness.md) |

Product planning update 2026-09-23: [D-27–34](changes/telegram-development-workflow/interview-decisions.md#уточнения-2026-09-23), [этапы E1/E2](changes/telegram-development-workflow/design.md#acceptance-increments). Сначала принимается рабочая среда: reusable container на проект + server bind mount, полная история/automatic context, independent [SSH Codex](changes/telegram-development-workflow/specs/interactive-access/spec.md), reconnect и parallel worktrees, реальные tests/report. PR, contemporary-dance-guide и offsite backup/restore остаются последующими инкрементами. [Bounded source discovery](changes/telegram-development-workflow/implementation-readiness.md#e1-source-discovery-2026-09-23) документирует native/runner/history/SSH gaps; завершение research children не implementation. Следующий [owner decision packet](changes/telegram-development-workflow/implementation-readiness.md#decision-packet-and-c13-stop-gate) предшествует runnable TDD. Docs update не approval exact revision и не runtime apply; текущие counts/digest — [review-status](changes/telegram-development-workflow/review-status.json).

`status.isPlanningComplete`/`isComplete` означает наличие planning artifacts. `instructions apply.progress` — отметки checklist. `validate` — структура. Ни одно не является runtime acceptance или owner approval. [Current coverage](changes/adopt-openspec-workflow/audit.md#current-coverage) охватывает 13 capabilities / 28 requirements / 81 scenarios и [44 task IDs](changes/adopt-openspec-workflow/audit.md#current-task-coverage), отделяя historical local/native/mock/canary evidence от полного NOT_RUN runtime acceptance. Предшествующие секции audit и seed receipts — historical snapshots.

## Safe Commands

Из `/Users/s060874gmail.com/coding/projects/hermes-agent`, без установки/инициализации и runtime effects:

```sh
./run-openspec context --json
./run-openspec list --json
./run-openspec list --specs
./run-openspec status --change seed-project-documentation --json
./run-openspec instructions apply --change seed-project-documentation --json
./run-openspec validate seed-project-documentation --strict --json
./run-openspec validate --all --strict --json
```

Проверять exit каждой команды. `instructions apply` только читает инструкции, не применяет change и не выполняет задачи. Для другого change заменить имя точным значением из list; при неожиданном root остановить запись, не выполнять init. `--check` у root updater не входит в этот quick start: он использует сеть.

## Continue Development

- Продолжение того же intent — существующий change, новое самостоятельное поведение — небольшой отдельный change. Сначала requirements/scenarios и discovery реальных source/test paths; для docs-only обоснованный `skip_specs: true`, без dummy requirements.
- Предъявить proposal/design/tasks и получить отдельный запрос apply; внутри разрешённого scope работать до завершения или настоящего blocker. Code: meaningful RED → minimal GREEN → regressions; docs: links/coverage/CLI/tabletop, не dummy tests.
- Если пользователь ограничил turn PLAN MODE: сохранять только разрешённый plan path; не создавать change, не применять edits и не выполнять mine под видом planning. Более узкий текущий scope всегда сильнее workflow.
- Repo выбран; unknown runner/API/test paths → BLOCKED_PATH_DISCOVERY, маршрут — [implementation-readiness](changes/telegram-development-workflow/implementation-readiness.md), не выдуманные imports или новый scheduler. Правила малых задач и outcomes — [ROADMAP](ROADMAP.md).
- Installed skills доступны в [.hermes/skills](../.hermes/skills/) и [.agents/skills](../.agents/skills/); existence не означает загрузку runtime. Если slash tool недоступен, прочитать skill и применить настоящий CLI. Несуществующий `openspec verify` не вызывать; semantic review — [WORKFLOW §7](WORKFLOW.md#7-verify-три-независимых-вопроса).
- После разрешённых docs edits обновить только tasks/openspec через [WORKFLOW §11](WORKFLOW.md#11-handoff-и-память) и проверить retrieval точного source. Index — не authority. Sync/archive, Git init/commit/push, runtime/publication/deployment требуют собственного разрешения.

## Open Gates

[Текущий TODO](../tasks/todo.md#текущий-операторский-индекс--openspec-reconciliation) — единственный операторский индекс:

- ORCH-01 / CRITICAL: отдельный независимый production-контроллер не реализован. MemPalace/OpenSpec/toy-controller не обеспечивают production monitoring/restart.
- OS-06 — approval exact product revision pending; docs completion его не выдаёт.
- OS-07 — protected AGENTS write заблокирована; не повторять и не обходить без нового разрешения.
- OS-08 — [N-01–N-11](changes/telegram-development-workflow/native-capability-matrix.md) и runtime readiness открыты; новые N-09–11 покрывают SSH, full history/hydration и расширения, не заменяют исходные gates.
- OS-09 — R1-current/R2-current/R3 применены; для завершения adoption остаётся AGENTS gate, не повторный посев.
- MEM-02b — actual new-session/restart/compression lifecycle, не direct unit hook.

Нужные owner decisions группируются в соответствующем change, а не запрашиваются заново после каждого docs task. Закрытие этого docs change не архивирует продукт, не выбирает production runner и не изменяет полномочия.
