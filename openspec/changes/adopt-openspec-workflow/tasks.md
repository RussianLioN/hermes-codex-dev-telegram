## 1. Аудит источников и доказательств

Этот checklist начинается после отдельного запроса apply, предусмотренного пунктом A.8 исходного плана. Создание planning artifacts не считается реализацией нижеследующих задач. Основание: `.hermes/plans/2026-09-16_193737-openspec-workflow-reconciliation.md`; design.md задаёт границы docs-only change, product requirements не меняются под skip_specs.

- [x] 1.1 Создать `audit.md` с actual `./run-openspec context --json`, `--version`, `status --change telegram-development-workflow --json`, `instructions apply --change telegram-development-workflow --json`, `validate --all --strict --json`; проверить отдельные exits и разделение planning/progress/validation/approval.
- [x] 1.2 Проверить `.hermes/skills/openspec-*/SKILL.md` и `.agents/skills/openspec-*/SKILL.md`, штатную schema и verify template; записать в `audit.md` версии, source paths и отдельно runtime discovery или NOT_VERIFIED, не заявлять отсутствующий optional verify skill установленным.
- [x] 1.3 Сопоставить `specs/task-intake/spec.md` и `specs/telegram-delivery/spec.md` product change с audit; проверить каждое requirement/scenario TG-01–02 и TG-11–12: evidence с классом либо NOT_RUN, local Bot API fixture не считается live Telegram.
- [x] 1.4 Сопоставить product `specs/code-execution/spec.md` и `specs/project-environments/spec.md`; проверить TG-05–06/ENV-01–02, различие historical authorized canary, native local readiness и незакрытого client routing/model-turn gate.
- [x] 1.5 Сопоставить product `specs/portable-memory/spec.md` и `specs/specialist-dispatch/spec.md`; проверить MEM-10–11/TG-03–04: scope-before-retrieval, shared tools, параллельные contexts и ограничения local evidence.
- [x] 1.6 Сопоставить product `specs/local-preview/spec.md` и `specs/verification/spec.md`; проверить PRE-01–02/TG-07–08: все scenarios имеют evidence либо NOT_RUN, отсутствующий dance-guide E2E не считается реализованным.
- [x] 1.7 Сопоставить product `specs/change-publication/spec.md` и `specs/offsite-backup/spec.md`; проверить TG-09–10/BACK-01–03: synthetic/mock результаты отдельно от live publication/upload/restore acceptance.
- [x] 1.8 Сопоставить product `specs/task-recovery/spec.md` и `specs/maintenance-coordination/spec.md`; проверить REC-01–02/UPD-01–02: toy controller и updater fixtures не закрывают production recovery, ORCH-01 остаётся CRITICAL/open.
- [x] 1.9 Сопоставить все исходные пункты product `tasks.md` с `audit.md`, используя `.hermes/tooling/telegram-approval-prototype/`, `.hermes/tooling/protected-operation-prototype/`, `.hermes/tooling/mvp1-integration-prototype/` и `.hermes/research/telegram-hermes-codex/native-codex/`; проверить сохранение всех исходных IDs и каждого критерия, никакой галочки за partial/mock/failed.

## 2. Reconciliation без изменения полномочий

- [x] 2.1 Создать `reconciliation.md` с exact file/before/after/rationale/approval impact для product `design.md:9,17`, task 3.2, устаревших receipt pointers и TODO history; проверить явное отличие app-server research candidate от действующего MVP1 design.
- [x] 2.2 В `reconciliation.md` зарегистрировать повреждённый `.hermes/research/telegram-hermes-codex/native-codex/test_stock_lifecycle.py` как открытый дефект вне docs scope; проверить отсутствие его исправления/удаления и отсутствие заявления о meaningful TDD RED.
- [x] 2.3 Получить per-artifact confirmation предложенных product revisions одним однозначным пакетом; сохранить решение в `reconciliation.md`, оставить неполученные confirmations pending, не считать общий plan approval approval новой production spec.
- [x] 2.4 Через установленный `openspec-update-change` применить только подтверждённые изменения existing product planning artifacts; проверить `./run-openspec validate telegram-development-workflow --strict --json`, сохранение product IDs и отсутствие незаявленного изменения behavior.
- [x] 2.5 Сверить allowlisted digest и actual receipts product `review-status.json`, записать вычисление в `reconciliation.md`; обновлять bookkeeping только в подтверждённых пределах, проверить pending/owner_approved=false до настоящего exact approval и не менять historical receipts.

## 3. Единый рабочий процесс

- [x] 3.1 Создать `openspec/WORKFLOW.md` с source-of-truth, выбором change и штатными explore/propose/update/apply/verify/sync/archive; проверить наличие точных команд из CLI help, условий skip_specs и обязательных confirmation boundaries без выдуманной команды openspec verify.
- [x] 3.2 В `openspec/WORKFLOW.md` закрепить TDD для будущего кода, task→requirement→evidence linkage, local/live distinction, runtime Kanban vs plan checklist и handoff; проверить, что docs tests не заменяются dummy unit tests, а MemPalace не становится authority/controller.
- [x] 3.3 В `openspec/WORKFLOW.md` закрепить условный полный трёхволновой E01–E19 council из design.md; проверить bounded execution, фактические manifests, отсутствие автоматических cross-model calls/permissions, честный blocker при недоступности штатного механизма.
- [ ] 3.4 Добавить подтверждённый блок C.17 исходного плана в `AGENTS.md` без перезаписи других разделов; проверить ссылку на существующий WORKFLOW, сохранённые safety/skills/memory правила и отсутствие обхода protected write confirmation.
- [x] 3.5 Перед configuration work проверить `/bin/zsh -n backup-hermes-oauth` и выполнить `./backup-hermes-oauth` согласно AGENTS, не раскрывая private payload; затем точечно дополнить `openspec/config.yaml` ссылкой и task/evidence/local-live rules; проверить `instructions apply --change telegram-development-workflow --json` и `instructions tasks --change adopt-openspec-workflow --json`, approvals не ослаблены.
- [x] 3.6 Обновить `tasks/todo.md` как краткий текущий операторский индекс со ссылками на оба changes и явно отделённой неизменённой историей; проверить OS-07 только по фактически применённому AGENTS workflow, OS-06/OS-08/ORCH-01 остаются открытыми до своих критериев.

## 4. Verification и handoff

- [x] 4.1 Создать `verification.md` по Completeness/Correctness/Coherence штатного verify template; проверить отсутствие потерянных product tasks/scenarios, partial claims и задним числом выданных approvals; записать CRITICAL/WARNING отдельно для docs migration и продукта.
- [x] 4.2 В `verification.md` выполнить tabletop кейсы feature, bugfix, docs-only, architecture drift, plan-only, missing optional skill, unapproved external effect, failed/expected-failure test; проверить правильный change/workflow/stop condition для каждого.
- [x] 4.3 Выполнить `status` и `instructions apply` для обоих changes, затем `./run-openspec validate --all --strict --json`; записать actual output/exits в `verification.md`, подтвердить tooling specs skipped, product specs сохранены и structural pass не считается runtime acceptance.
- [x] 4.4 Провести read-only quality/security review разрешённого docs scope; зафиксировать в `verification.md` ограничения проверки и отсутствие выполненных core/server/profile/credential/dependency/publication действий; при спорном решении использовать bounded council, не имитировать экспертные ответы.
- [x] 4.5 Обновить только corpora командой `HF_HUB_OFFLINE=1 ./run-mempalace mine tasks --wing hermes-agent --agent hermes-default` и аналогично `mine openspec`, затем search `OpenSpec WORKFLOW adopt-openspec-workflow ORCH-01`; проверить actual exits и ссылки, при ошибке оставить refresh blocked.
- [x] 4.6 Представить итоговый отчёт с путём WORKFLOW, фактическим progress, validation/verification/approval статусами и оставшимися blockers; проверить отсутствие автоматического archive/commit/push и явное напоминание ORCH-01 / CRITICAL.
