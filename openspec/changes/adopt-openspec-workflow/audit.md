# Аудит: implementation evidence не равно product acceptance

## Baseline и метод

Apply разрешён отдельным сообщением владельца «Применяй adopt-openspec-workflow». Этот документ — сверка текущих specs, tasks, README и сохранённых receipts; исторические runtime tests в этом ходе НЕ перезапускались. Evidence classes ниже описывают масштаб исторического результата, а не новую сертификацию.

Фактически выполнено при apply:

| Команда | Exit | Результат |
|---|---|---|
| `./run-openspec context --json` | 0 | текущий workspace, repo-local |
| `./run-openspec --version` | 0 | 1.13.0 |
| `./run-openspec status --change telegram-development-workflow --json` | 0 | isPlanningComplete=true |
| `./run-openspec instructions apply --change telegram-development-workflow --json` | 0 | 0/33, state=ready |
| `./run-openspec status --change adopt-openspec-workflow --json` | 0 | isPlanningComplete=true |
| `./run-openspec instructions apply --change adopt-openspec-workflow --json` | 0 | начальное 0/26, state=ready |
| `./run-openspec validate --all --strict --json` | 0 | 2 valid, 0 failed; INFO о skip_specs tooling change |
| `git status --short`, `git branch --show-current` | 128 каждый | workspace не Git repository |
| `/bin/zsh -n backup-hermes-oauth` и `./backup-hermes-oauth` | 0 | private snapshot проверен wrapper, permissions 700/600 и ZIP integrity; payload не читался агентом |

Общий exit compound с завершающим Git=128 не отменяет отдельные результаты OpenSpec: status/apply дополнительно запускались через subprocess с проверкой каждого returncode. Сравнение digest allowlisted revision_files вернуло совпадение recorded/computed `29163c1de50e501a82f85cc72ada9f011520a3a17828ee0027adf006b22c729f`, owner_approved=false. Этот hash не является approval.

## Интеграции

В обоих каталогах `.hermes/skills/` и `.agents/skills/` найдены generatedBy=1.13.0 файлы `openspec-{explore,propose,update-change,apply-change,sync-specs,archive-change}/SKILL.md`. Их наличие и версии проверены поиском по содержимому; apply/update/propose инструкции прочитаны. Runtime slash/skill discovery в новой Hermes/Codex model-session: NOT_VERIFIED. В этом ходе инструкции применяются чтением файлов и настоящим CLI, не заявляется вызов slash tool.

Schema: `.hermes/tooling/openspec/node_modules/@fission-ai/openspec/schemas/spec-driven/schema.yaml`, включая skip_specs и DAG proposal→specs/design→tasks. Verify source: `.hermes/tooling/openspec/node_modules/@fission-ai/openspec/dist/core/templates/workflows/verify-change.js`, три измерения Completeness/Correctness/Coherence. Generated optional verify skill не установлен в перечисленных каталогах; CLI команды `openspec verify` не предлагается. Дополнительные плагины/схемы не нужны.

## Индекс evidence и реализации

Пути от root workspace. Индексы E ниже являются общими ссылками для scenario mapping, не автоматическим доказательством всех сценариев группы.

| ID | Реализация / свидетельство | Класс / граница / источник разрешения |
|---|---|---|
| E1 | `.hermes/tooling/telegram-approval-prototype/plugin/bridge.py`, `plugin/__init__.py`; README.md, boundary-evidence.md, lifecycle-evidence.md того же каталога | LOCAL_SYNTHETIC + targeted native loader; исторически 40 tests с expectedFailure generic mandatory transport. Не live Telegram. Local scope указан в README и `.hermes/plans/2026-09-11_162951-native-telegram-transport-prototype.md` |
| E2 | `.hermes/tooling/protected-operation-prototype/protocol.py`; README.md, server-evidence.md того же каталога | LOCAL_SYNTHETIC protocol; AUTHORIZED_CANARY отдельно для OS DAC, не end-to-end policy. Разрешение `openspec/changes/telegram-development-workflow/protected-executor-scope.md`, одноразовый A; повтор не разрешён |
| E3 | `.hermes/tooling/mvp1-integration-prototype/native_probe.py`, ledger.py, controller.py, controller_demo.py, dataflows.py, backups.py, backup_uploads.py, test_current_updater.py; README.md | NATIVE_LOCAL Kanban + LOCAL_SYNTHETIC scope/publisher/upload/recovery. Исторические 44 tests, не новый запуск. Разрешение `openspec/changes/telegram-development-workflow/integration-readiness-scope.md` |
| E4 | `.hermes/research/telegram-hermes-codex/native-codex/environment_gate.py`, owned_probe.py и test_*; product `native-environment-evidence.md`, `native-bootstrap-evidence.md`; environment-run/receipts-v5.json | NATIVE_LOCAL/no model turn; SOURCE_ONLY маршрутизация. Не complete mediation. Guarded account metadata FAILED TimeoutError отдельно от успешных negative fixtures. Scope — local research, не новое canary permission |
| E5 | `.hermes/research/telegram-hermes-codex/native-codex/linux_probe.py`; product `linux-canary-evidence.md` | AUTHORIZED_CANARY исторический одноразовый Linux; VM удалена. Не real project model routing. Историческое разрешение `local-linux-canary-scope.md`, повтор не разрешён |
| E6 | `.hermes/research/telegram-hermes-codex/native-codex/guest_namespace_plan.py`, safe_canary_export.py; product `linux-model-lifecycle-preparation.md`; lifecycle-preparation/receipts-v2.json | LOCAL_SYNTHETIC command plan + реальные owned filesystem tests; не Linux runtime/quiescence admission, новый scope B не готов |
| E0 | Product specs/tasks и отсутствие принятого product receipt | NOT_RUN для полной production приёмки; не утверждение отсутствия всех исторических probes |

Прочитанные README/evidence сохраняют ограничения same-UID/cooperating writers, mock GitHub и toy controller. В настоящем ходе никакой producer, controller, model probe или canary не запускался.

Проверенные JSON receipts (разобраны runs/exit codes, сами тесты не перезапускались):

- environment-run/receipts-v4.json: 8d407ef40388d5a4a0993327cdf2a65bfc2b47d229635aeb35c4ca7735ec5db1; runs содержат exit_code=0, исторический coverage v4.
- environment-run/receipts-v5.json: bf818443a167b7d89680f2867f5e7707db7a26160ca9fe005434a3fafb756898; runs содержат exit_code=0, добавлены CLI/inventory/bootstrap negative probes. Не заменяет отдельный failed account probe.
- lifecycle-preparation/receipts-v2.json: e261a39196a32bdcc699402ef4d21af970c1013bcf93545a42dcb69886559211; обе runs exit_code=0, документ описывает 14 unittest. Не покрывает повреждённый stock lifecycle test.

## Полная карта requirements/scenarios

Все строки относятся к `openspec/changes/telegram-development-workflow/specs/<capability>/spec.md`. Имена scenarios сохранены дословно. Разделение сценариев внутри ячейки точкой с запятой — перечисление, не объединение acceptance criteria. Для КАЖДОГО перечисленного scenario полная product acceptance — NOT_RUN: приведённый E указывает лишь релевантный локальный материал; оставшийся критерий указан справа. Никаких LIVE_ACCEPTANCE не назначено. Source revision — текущий digest выше; source scope/authorization наследуются из E-индекса.

| Requirement / capability | Scenarios | Product task IDs | Свидетельство и выполненная часть | Осталось до полного критерия |
|---|---|---|---|---|
| TG-01 / task-intake | Unknown project; Revised specification; Unauthorized sender; New project agreement; Native approval unavailable | 1.1, 1.6, 2.1 | E1/E2: synthetic identity/revision binding и выявленный policy gap | Настоящий intake, project agreement и обязательный native gate во всех call paths |
| TG-02 / task-intake | Concurrent repeated delivery; Crash before mapping; Ambiguous previous producer | 1.1, 2.2, 2.3 | E2/E3: cooperating replay/fencing/unknown и local Kanban | Live update→durable intent→mapping atomic admission, noncooperating caller |
| TG-03 / specialist-dispatch | Unknown specialist; Cross-project access; Parallel writers | 1.1, 3.3 | E3: synthetic scope/context, E4: delegated MCP denial | Настоящие separate worktrees двух проектов, routing и serial integration |
| TG-04 / specialist-dispatch | Unsupported runtime interface; Dynamic skill substitution | 1.1, 1.5, 3.2, 3.6 | E3 provenance pins, E4 source/native config probes | Production admission/all-path substitution protection, actual runner selection |
| TG-05 / code-execution | Invalid base or injected command; Missing OAuth or resource budget; YOLO requests host control | 1.2, 3.1, 3.2 | E2/E5 ограниченная OS boundary, E4 readiness/negative config; account probe FAILED | Credential/network complete mediation и real model path; budgets/devcontainer admission |
| TG-06 / code-execution | Escaped child process; Late completion | 2.3, 3.4 | E2/E3 local fencing; E5 contained-process proof | Настоящий task containment + cancel/result integration, не один PID/process group |
| ENV-01 / project-environments | Resource admission; Untrusted environment change | 1.2, 1.5, 3.1 | E5 restricted temporary canary, E6 argv preparation | Persistent projects, actual quotas/UID/network и owner gate изменённого devcontainer |
| ENV-02 / project-environments | Unrelated resource; New use during cleanup | 7.5 | E0; E6 exporter ничего не удаляет | Ownership/reference locking при настоящей cleanup race, без global prune |
| MEM-10 / portable-memory | Cross-project lesson; Index loss | 3.5 | E3 dataflows scoped synthetic retrieval, локальный MemPalace index существует | Curated Git sources/agent-knowledge, реальные ACL до retrieval и rebuild в разрешённом scope |
| MEM-11 / portable-memory | Conflicting observations; Pre-compression failure; Resume in another harness | 1.3, 3.3, 3.5 | E3 conflicts/checkpoint/reopen, synthetic storage failure | Actual lifecycle pre-compression и resume обоих harness; авторизованные context packets |
| PRE-01 / local-preview | Demo is not presented as real service | 4.1, 4.2 | E0 | Реальная страница dance-guide с маркировкой вымысла и без PII/платежей |
| PRE-02 / local-preview | Offline local opening; Local modifications | 4.1, 4.2, 8.1 | E0 | Browser file:// exact commit offline/mobile/keyboard и безопасное Git обновление |
| TG-07 / verification | Tampered tests on faulty implementation; Changed candidate | 4.3 | E2 immutable marker evidence, E3 provenance; не page acceptance | Независимый acceptance pack на faulty guide/candidate, revocation после изменения |
| TG-08 / verification | Static guide success; Files exist but browser flow fails | 4.1, 8.1 | E0 | Настоящие browser assertions/screenshots/console/network нужного candidate |
| TG-09 / change-publication | Merge approval does not match; Approved task publication; Worker tries to publish directly | 1.6, 5.1, 5.2 | E2 digest/approval fixture, E3 MOCK publisher | Реальный isolated publisher, private repo/PR readback, exact merge gate |
| TG-10 / change-publication | Cancel wins admission race; Response lost after sending | 5.3 | E3 mock sending/unknown/reconcile | Разрешённый real API canary и поздний внешний эффект, отсутствие duplicate |
| TG-11 / telegram-delivery | Gateway cannot access artifact; Ambiguous owner reply | 6.1 | E1 callback identity, не artifact delivery | Actual source route и доставка/отказ, неоднозначный reply не запускает effect |
| TG-12 / telegram-delivery | Transport restart; Local preview delivery | 6.2, 8.1 | E0 | Durable delivery receipts, gateway restart без повторной разработки, Git preview report |
| REC-01 / task-recovery | Quiet build; Lost heartbeat | 6.3 | E3 toy controller: heartbeat не stdout, bounded retry | Independent production controller и измерение ≤5 минут; Telegram alerts; ORCH-01 открыт |
| REC-02 / task-recovery | Lost PR response; Whole host outage | 6.3, 8.2 | E3 unknown/reopen и toy successor | Production reconciliation/host return/provider failures, durable data preservation |
| BACK-01 / offsite-backup | Only one project changed; Unpublished work; Concurrent writes; Credential embedded in checkpoint | 1.4, 7.1 | E3 actual age/temp files + mock changed-only upload, limited secret filter | Настоящий согласованный snapshot/runtime writer ownership, scheduled/event integration |
| BACK-02 / offsite-backup | Upload response lost | 1.4, 7.2 | E3 mock exact checksum/unknown, E4 GitHub quota source не storage policy | N-07 policy suitability и live encrypted exact-object upload/readback |
| BACK-03 / offsite-backup | Retention without restoration evidence; Spoofed or mismatched report; Restore dependency retained; Different project backup | 7.3, 7.4 | E3 temporary restore и pure scoped retention; ничего не удаляется | Владелец restore-check + настоящий Telegram attestation, remote dependencies/retention races |
| UPD-01 / maintenance-coordination | Active task exceeds maintenance wait | 1.3, 7.6 | E3 pure/current-source fixture drain/defer | Интеграция actual updater/admission/locks и real task preservation |
| UPD-02 / maintenance-coordination | Candidate fails health checks | 1.3, 7.6, 8.2 | E3 historical/current-source helpers, backup revision gate | Live verified backup перед disruption, actual health/rollback/recovery; без запуска здесь |

## Все исходные product tasks

Во всех строках parent task остаётся unchecked. Таблица не сужает исходный текст критерия в product tasks.md; сверка произведена с полным текстом, а справа перечислен незакрытый outcome. Для задач, требующих и fixture, и live, fixture не засчитывает весь пункт.

| ID | Evidence | Незакрытый outcome |
|---|---|---|
| 1.1 | E1/E2/E3 | N-01/N-02 complete native owner/replay boundary |
| 1.2 | E4/E5 | N-03/N-04 OAuth/refresh/isolated model execution |
| 1.3 | E3 | N-05/N-06 real lifecycle/updater integration |
| 1.4 | E3/E4 | N-07 GitHub storage terms/limits и sample suitability |
| 1.5 | E0 | Реальный implementation repo/paths/limits/lock order |
| 1.6 | review-status.json pending | Exact owner spec и infrastructure/credential scope |
| 2.1 | E1/E2/E3 | Actual intake owner/project/revision gate |
| 2.2 | E3 | Full native mapping admission under failures |
| 2.3 | E2/E3 | Production generation/cancel-release integration |
| 3.1 | E5/E6 | Persistent pinned Dev Container admission |
| 3.2 | E4 | Выбор/подключение утверждённого runner; app-server candidate не CLI acceptance |
| 3.3 | E3 | Две actual write worktrees плюс второй проект, serial integration |
| 3.4 | E5 | Task cancellation и escaped-child integration |
| 3.5 | E3 | Real pre-compress/rebuild/adapters и access control |
| 3.6 | E3/E4 | Runtime policy/skill revision integrity весь run |
| 4.1 | E0 | Failing acceptance настоящего guide/runner |
| 4.2 | E0 | Реальная offline страница и GREEN |
| 4.3 | E2/E3 | Независимый immutable browser acceptance pack |
| 5.1 | E3 | Dedicated live publisher/repo/privacy credential boundary |
| 5.2 | E3 | Real push/PR и exact owner merge decision |
| 5.3 | E3 | После mock fault — разрешённый real canary/readback |
| 6.1 | E1 | Actual artifact/route notification |
| 6.2 | E0 | Gateway restart/delivery retry без нового run |
| 6.3 | E3 | ORCH-01 production independent recovery |
| 7.1 | E3 | Production snapshot wiring, не только pure fixture |
| 7.2 | E3 | N-07, encryption custody и actual offsite upload |
| 7.3 | E3 | Операторская restore-check команда для реального формата |
| 7.4 | E3 | Real owner attestation и protected remote retention |
| 7.5 | E0 | Ownership-aware cleanup/admission race |
| 7.6 | E3 | Полный declared lock/drain/backup/rollback contract и отдельное разрешение live script |
| 8.1 | E0 | Full Telegram→Codex→tests→PR→file:// journey |
| 8.2 | E3 | Разрешённые реальные fault/restart/provider/backup/maintenance scenarios |
| 8.3 | Structural pass only | Candidate/spec receipts, runtime acceptance и owner archive decision |

## Findings

1. Structural validation верна, но не закрывает implementation. Ноль production tasks — честное состояние, не повод массово проставить галочки.
2. Design CLI-only/non-goals и app-server research нуждаются в явной классификации candidate; proposed edits — reconciliation.md.
3. Review receipt v4 не ложный: это исторический baseline; v5 и lifecycle v2 надо добавить как последующие evidence, а не переписать старые.
4. `test_stock_lifecycle.py` синтаксически повреждён; не выполнялся этим audit и не покрыт lifecycle v2.
5. TODO смешивает историю и текущую сводку; текущий индекс будет отделён без удаления истории.
6. Не подтверждены runtime discovery generated skills в новой model-session, live publisher/controller/updater/E2E. OpenSpec и MemPalace сами этих возможностей не создают.

## Current Coverage

2026-09-28. Текущая карта заменяет прежнюю как индекс актуальных контрактов; всё выше — неизменённый historical snapshot. Scope: 13 capabilities, 28 requirements, 81 exact scenarios и 52 task IDs, включая 8 отдельно разрешённых pure local children 3.1.1–3.1.8. Источник каждой строки: `openspec/changes/telegram-development-workflow/specs/<Capability>/spec.md`; criterion не переопределяется сокращённым remaining description. Source tasks: [product tasks](../telegram-development-workflow/tasks.md).

Coverage revision: e399e363d3af14fee79a623b2e8e9dc93cc7836e28de5f157eeb1befc2d38533

H:E0–H:E6 отсылают к historical [evidence index](#индекс-evidence-и-реализации) и его source/receipt revisions. H:E1 — historical transport evidence, не increment E1. Классы наследуются из индекса, конкретная ограниченная часть указана в строке; H:E0 означает отсутствие accepted receipt, а не отсутствие всего research. READMEs transport/protected/integration и bootstrap/lifecycle evidence перечитаны; исторические тесты не перезапускались. Current acceptance NOT_RUN относится к полному текущему runtime сценарию; никакой source/doc check не переводит его в PASS. E1+E2 означает применимость в обоих инкрементах, не частичное закрытие полного parent.

| Capability | Requirement | Scenario | Tasks | Increment | Historical evidence | Current acceptance | Remaining criterion |
|---|---|---|---|---|---|---|---|
| task-intake | TG-01 | Unknown project | 1.1, 2.1 | E1+E2 | H:E1/H:E2 synthetic identity binding | NOT_RUN | Реальный Telegram выбор project до worker |
| task-intake | TG-01 | Revised specification | 1.6, 2.1 | E1+E2 | H:E2 immutable manifest/revision fixture | NOT_RUN | Отзыв прежнего approval во всех runtime admission paths |
| task-intake | TG-01 | Unauthorized sender | 1.1, 2.1 | E1+E2 | H:E1 synthetic nonowner routing; generic gate открыт | NOT_RUN | Live identity rejection без task/data disclosure |
| task-intake | TG-01 | New project agreement | 1.6, 2.1, 5.1 | E2 | H:E2 fixture binding, не GitHub project setup | NOT_RUN | Согласованный owner/repo binding сохраняется при publication |
| task-intake | TG-01 | Native approval unavailable | 1.1, 2.1 | E1+E2 | H:E1 generic transport expectedFailure; H:E2 не security boundary | NOT_RUN | Mandatory native gate fail-closed во всех call paths |
| task-intake | TG-01 | Local environment before remote publication | 2.1, 8.4 | E1 | H:E0 local-first runtime receipt отсутствует | NOT_RUN | Разрешённый local project запускается без provisioning remote |
| task-intake | TG-02 | Concurrent repeated delivery | 1.1, 2.2 | E1+E2 | H:E3 cooperating replay/native Kanban fixture | NOT_RUN | Concurrent real update даёт один intent/mapping/run |
| task-intake | TG-02 | Crash before mapping | 2.2 | E1+E2 | H:E2/H:E3 durable fixture journal | NOT_RUN | Crash card→mapping не допускает orphan dispatch |
| task-intake | TG-02 | Ambiguous previous producer | 2.2, 2.3 | E1+E2 | H:E2/H:E3 unknown/reconciliation fixture | NOT_RUN | Пустой lookup при живом producer не допускает duplicate |
| project-environments | ENV-01 | Resource admission | 1.2, 1.5, 3.1 | E1+E2 | H:E5 bounded one-shot canary, не multi-project admission | NOT_RUN | Actual limits/queue сохраняют чужие сервисы |
| project-environments | ENV-01 | Untrusted environment change | 3.1 | E1+E2 | H:E2 synthetic action binding; H:E6 argv only | NOT_RUN | Изменение mount/capabilities требует exact policy/owner grant |
| project-environments | ENV-01 | Recreate project container | 1.5.2, 3.8, 8.4 | E1 | H:E6 owned export, не persistent recreate | NOT_RUN | Same project storage/WIP/history и hydration обоих harness |
| project-environments | ENV-01 | Next task reuses environment | 3.8 | E1+E2 | H:E0 reuse receipt отсутствует | NOT_RUN | Same project container/storage, separate writer worktrees |
| project-environments | ENV-02 | Unrelated resource | 7.5 | E1+E2 | H:E0 cleanup acceptance отсутствует | NOT_RUN | Чужие images/networks не удаляются, global prune отсутствует |
| project-environments | ENV-02 | New use during cleanup | 7.5 | E1+E2 | H:E0 cleanup race не испытана | NOT_RUN | Protected recheck/reference admission исключает deletion race |
| project-environments | ENV-02 | Detached manual session is still active | 3.7, 7.5 | E1 | H:E0 manual reference tracking отсутствует | NOT_RUN | Detached session/worktree/history защищены от cleanup |
| portable-memory | MEM-10 | Cross-project lesson | 3.5 | E1+E2 | H:E3 synthetic scope checked before retrieval | NOT_RUN | Реальные ACL и source attribution; knowledge PR — E2 |
| portable-memory | MEM-10 | Index loss | 3.5 | E1+E2 | H:E3 synthetic checkpoint/readback; local index не server proof | NOT_RUN | Rebuild из durable разрешённых источников без credentials |
| portable-memory | MEM-11 | Conflicting observations | 3.3, 3.5 | E1+E2 | H:E3 CAS/conflict fixture | NOT_RUN | Runtime writers сохраняют обе версии и явный conflict |
| portable-memory | MEM-11 | Pre-compression failure | 1.3, 3.5 | E1+E2 | H:E3 propagated storage fault, не real lifecycle | NOT_RUN | Actual pre-compression failure блокирует потерю контекста |
| portable-memory | MEM-11 | Resume in another harness | 3.5 | E1+E2 | H:E3 synthetic reopen, не Hermes/Codex adapters | NOT_RUN | Rules/checkpoint загружаются обоими harness без общего home |
| portable-memory | MEM-12 | Start with current project context | 1.3.1, 3.5, 3.7, 8.4 | E1 | H:E0 automatic dual-harness hydration не принята | NOT_RUN | Exact current revision/status/WIP/checkpoint без manual paste |
| portable-memory | MEM-12 | Compression preserves original history | 1.3.1, 3.5, 3.8 | E1 | H:E0 full event/tool result retention не принят | NOT_RUN | Оригиналы доступны после compression и index rebuild |
| portable-memory | MEM-12 | History write or hydration fails | 3.5, 3.8, 8.4 | E1 | H:E3 storage failure fixture не покрывает full history | NOT_RUN | Dual-harness fail-closed при недоступном storage/current revision |
| portable-memory | MEM-12 | Parallel histories stay attributable | 3.3, 3.5 | E1+E2 | H:E3 synthetic scope, не concurrent history writers | NOT_RUN | Owner/project/session/attempt/worktree order без shared credentials |
| specialist-dispatch | TG-03 | Unknown specialist | 1.1, 3.2 | E1+E2 | H:E3 synthetic scope; H:E4 delegated denial | NOT_RUN | Missing/disallowed profile blocked без shell fallback |
| specialist-dispatch | TG-03 | Cross-project access | 3.3, 3.5 | E1+E2 | H:E3 local scoped retrieval | NOT_RUN | Реальные project ACL для контекста/артефактов обоих writers |
| specialist-dispatch | TG-03 | Parallel writers | 3.3 | E1+E2 | H:E3 packet fixture, не actual worktree integration | NOT_RUN | Separate worktrees/branches/packets, serial integration/retests |
| specialist-dispatch | TG-04 | Unsupported runtime interface | 1.2.1, 3.2 | E1+E2 | H:E4 negative config/readiness probes, routing gate открыт | NOT_RUN | Actual CLI/schema/hooks admitted до task, без unsafe fallback |
| specialist-dispatch | TG-04 | Dynamic skill substitution | 3.6 | E1+E2 | H:E3 provenance pins; H:E4 config probes | NOT_RUN | All-run policy/helper substitution технически отвергается |
| specialist-dispatch | TG-04 | Shared extension compatibility | 1.5.4, 3.6 | E1 | H:E0 installation не runtime use | NOT_RUN | OpenSpec/MemPalace/skills/rules load/use обоих adapters |
| specialist-dispatch | TG-04 | Project extensions remain local | 3.6 | E1+E2 | H:E0 project install isolation receipt отсутствует | NOT_RUN | Project deps/skills не меняют shared/host/соседний проект |
| code-execution | TG-05 | Invalid base or injected command | 3.1, 3.2 | E1+E2 | H:E2 typed manifest; H:E4 negative config | NOT_RUN | Actual base/argv/stdin/cwd admission до process/external effects |
| code-execution | TG-05 | Missing OAuth or resource budget | 1.2, 3.1, 3.2 | E1+E2 | H:E4 account metadata FAILED TimeoutError, не отсутствие login | NOT_RUN | Subscription-only fail-closed и resource wait без fallback/kill |
| code-execution | TG-05 | YOLO requests host control | 1.2, 3.1 | E1+E2 | H:E2/H:E5 отдельные OS denials, не complete mediation | NOT_RUN | Host/socket/чужой project недоступны на actual runner |
| code-execution | TG-05 | Manual launch has the same boundary | 1.2, 3.7 | E1 | H:E0 manual launch isolation не испытана | NOT_RUN | Same credential/network/resource policy для SSH/YOLO |
| code-execution | TG-06 | Escaped child process | 3.4 | E1+E2 | H:E5 canary contained-process kill, не task integration | NOT_RUN | Task containment empty readback до cancelled acknowledgement |
| code-execution | TG-06 | Late completion | 2.3, 3.4 | E1+E2 | H:E2/H:E3 generation fixture | NOT_RUN | Stale result сохраняется диагностически без продвижения task |
| interactive-access | SSH-01 | Open manual session alongside automation | 3.3, 3.7, 8.4 | E1 | H:E0 independent ordinary session не принята | NOT_RUN | Same container, separate identity/worktree/current context |
| interactive-access | SSH-01 | Unknown project or unauthorized access | 3.7 | E1 | H:E0 SSH project binding не испытан | NOT_RUN | Deny до файлов/истории, никакого privileged host fallback |
| interactive-access | SSH-01 | Concurrent integration conflict | 3.3, 3.7 | E1 | H:E3 conflict fixture относится к memory, не Git acceptance | NOT_RUN | Обе ветки сохранены, serial merge и candidate retests |
| interactive-access | SSH-02 | SSH drops and reconnects | 1.5.3, 3.7, 8.4 | E1 | H:E0 same-process reconnect не испытан | NOT_RUN | Та же session/worktree/output без duplicate launch |
| interactive-access | SSH-02 | Codex died while disconnected | 3.7 | E1 | H:E0 manual death/recovery receipt отсутствует | NOT_RUN | Truthful death status, новый authorized run и history recovery |
| interactive-access | SSH-02 | Container destroyed while disconnected | 3.7, 3.8, 8.4 | E1 | H:E6 exporter не container recovery | NOT_RUN | Старый process умер; сохранён storage и новый hydrated run |
| verification | TG-07 | Tampered tests on faulty implementation | 4.3, 8.4 | E1+E2 | H:E2 immutable marker; H:E3 provenance, не trusted product pack | NOT_RUN | Faulty candidate/always-pass runner отвергнуты trusted checks |
| verification | TG-07 | Changed candidate | 4.3, 8.4 | E1+E2 | H:E2/H:E3 immutable fixture digest | NOT_RUN | Изменённый candidate/pack отзывает actual receipt |
| verification | TG-08 | Static guide success | 4.1, 8.1 | E2 | H:E0 dance-guide browser acceptance отсутствует | NOT_RUN | File desktop/mobile/keyboard, console/network/screenshots exact commit |
| verification | TG-08 | Files exist but browser flow fails | 4.1, 8.1 | E2 | H:E0 real frontend failure receipt отсутствует | NOT_RUN | Обязательный browser failure/CDN не получает verified |
| verification | TG-08 | Working environment acceptance | 8.4 | E1 | H:E0 live E1 environment/candidate pack отсутствует | NOT_RUN | Полный разрешённый E1 positive/negative pack с exact revisions |
| verification | TG-08 | Mounted files without automatic context | 3.5, 3.8, 8.4 | E1 | H:E0 mount не dual-harness hydration evidence | NOT_RUN | E1 отвергается при отсутствии automatic current context |
| telegram-delivery | TG-11 | Gateway cannot access artifact | 6.1 | E1+E2 | H:E1 routing fixture, не artifact delivery | NOT_RUN | Недоступное вложение даёт реальный delivery failure |
| telegram-delivery | TG-11 | Ambiguous owner reply | 1.1, 6.1 | E1+E2 | H:E1 scoped callback identity | NOT_RUN | Неоднозначный ordinary reply не исполняет protected action |
| telegram-delivery | TG-11 | Working environment report without PR | 6.1, 8.4 | E1 | H:E0 E1 report receipt отсутствует | NOT_RUN | Source route получает truthful task/session/branch/tests и not_provisioned |
| telegram-delivery | TG-12 | Transport restart | 6.2 | E1+E2 | H:E0 durable gateway delivery recovery не принято | NOT_RUN | Отправляется старый результат без нового Codex/test/PR run |
| telegram-delivery | TG-12 | Local preview delivery | 6.2, 8.1 | E2 | H:E0 Git/file preview report отсутствует | NOT_RUN | Repo/branch/commit/PR/preview path без server sync/execution |
| maintenance-coordination | UPD-01 | Active task exceeds maintenance wait | 1.3, 7.6 | E1+E2 | H:E3 synthetic Ledger drain, не server integration | NOT_RUN | Timeout→defer без gateway/worker kill и с безопасным admission |
| maintenance-coordination | UPD-01 | Manual session survives servicing deadline | 1.3.2, 7.6 | E1 | H:E0 manual/detached drain не принят | NOT_RUN | Session учитывается до конца, deadline не убивает её |
| maintenance-coordination | UPD-02 | Candidate fails health checks | 7.6, 8.2 | E1+E2 | H:E3 source/pure candidate quarantine helpers | NOT_RUN | Actual updater rollback/recovery, admission закрыт до health/state checks |
| maintenance-coordination | UPD-02 | First increment is not backup acceptance | 7.6, 8.4 | E1 | H:E0 staged maintenance acceptance отсутствует | NOT_RUN | E1 report оставляет offsite gate открытым без ослабления защит |
| task-recovery | REC-01 | Quiet build | 6.3 | E2 | H:E3 toy heartbeat controller | NOT_RUN | Production controller не дублирует живой quiet build |
| task-recovery | REC-01 | Lost heartbeat | 6.3, 8.2 | E2 | H:E3 logical-time toy retry, не five-minute measurement | NOT_RUN | Independent controller detection ≤5 минут и actual notification |
| task-recovery | REC-01 | Transport disconnect is not agent death | 3.7, 6.3 | E1+E2 | H:E0 manual heartbeat/disconnect integration не принята | NOT_RUN | E1 reconnect без duplicate; полный controller contract остаётся E2 |
| task-recovery | REC-02 | Lost PR response | 5.3, 6.3, 8.2 | E2 | H:E3 mock unknown/reconciliation | NOT_RUN | Actual exact PR reconciliation с bounded retries/provider failure |
| task-recovery | REC-02 | Whole host outage | 6.3, 8.2 | E2 | H:E3 toy reopen не actual host return | NOT_RUN | После host return truthful reconciliation без обещания external monitor |
| change-publication | TG-09 | Merge approval does not match | 1.6, 5.2 | E2 | H:E2 revision binding; H:E3 mock publisher | NOT_RUN | Live merge отвергнут после изменения repo/PR/head |
| change-publication | TG-09 | Approved task publication | 5.1, 5.2 | E2 | H:E3 MOCK PR и exact fixture readback | NOT_RUN | Private repo/branch/commit/PR actual readback без auto merge |
| change-publication | TG-09 | Worker tries to publish directly | 5.1 | E2 | H:E2 отдельный OS DAC canary, не publisher boundary | NOT_RUN | Worker не получает publication credentials/прямой API route |
| change-publication | TG-10 | Cancel wins admission race | 2.3, 5.3 | E2 | H:E3 mock pre-admission fencing | NOT_RUN | Cancel-before-sending предотвращает real API request |
| change-publication | TG-10 | Response lost after sending | 5.3 | E2 | H:E3 mock unknown/no-repeat | NOT_RUN | Late effect и empty lookup не приводят к duplicate PR |
| local-preview | PRE-01 | Demo is not presented as real service | 4.1, 4.2 | E2 | H:E0 реальная страница отсутствует | NOT_RUN | Явные demo labels и отсутствие реальной PII/payment отправки |
| local-preview | PRE-02 | Offline local opening | 4.1, 4.2, 8.1 | E2 | H:E0 browser product receipt отсутствует | NOT_RUN | Exact commit file:// работает без сети/CDN, mobile/keyboard |
| local-preview | PRE-02 | Local modifications | 4.1, 8.1 | E2 | H:E0 owner Git update flow не принят | NOT_RUN | Divergence/conflict сохраняет правки без force/reset |
| offsite-backup | BACK-01 | Only one project changed | 1.4, 7.1 | E2 | H:E3 changed-only mock upload + real age fixture | NOT_RUN | Actual scheduled/event snapshot/upload только изменившегося project |
| offsite-backup | BACK-01 | Unpublished work | 7.1, 7.3 | E2 | H:E3 temporary restore files/dependency fixture | NOT_RUN | Snapshot включает unpublished commits/untracked и достижимые deps |
| offsite-backup | BACK-01 | Concurrent writes | 7.1 | E2 | H:E3 fixture reservation, не writer quiescence | NOT_RUN | Consistent filesystem/DB snapshot при active writes |
| offsite-backup | BACK-01 | Credential embedded in checkpoint | 7.1 | E2 | H:E3 explicit secret-pattern fixture, не универсальный scanner | NOT_RUN | Actual selected-content redaction/blocking и безопасный report |
| offsite-backup | BACK-02 | Upload response lost | 1.4, 7.2 | E2 | H:E3 exact checksum mock reconciliation | NOT_RUN | N-07 suitability и real encrypted exact-object readback до retry |
| offsite-backup | BACK-03 | Retention without restoration evidence | 7.3, 7.4 | E2 | H:E3 pure eligibility, ничего не удалено | NOT_RUN | Real owner attestation gate сохраняет последнюю copy |
| offsite-backup | BACK-03 | Spoofed or mismatched report | 7.4 | E2 | H:E3 synthetic scoped restore report | NOT_RUN | Owner-only Telegram ID/checksum binding без смены restoration |
| offsite-backup | BACK-03 | Restore dependency retained | 7.3, 7.4 | E2 | H:E3 temporary dependency/eligibility fixture | NOT_RUN | Real remote references повторно сверяются перед deletion |
| offsite-backup | BACK-03 | Different project backup | 7.4 | E2 | H:E3 pure owner/project-scoped retention | NOT_RUN | Backup B не разрешает удалить последнюю восстановимую A |

## Current Task Coverage

Сверено с полными checkbox criteria product tasks.md. Это mapping, не второй checklist. [Source discovery](../telegram-development-workflow/implementation-readiness.md#e1-source-discovery-2026-09-23) документирует семь read-only children; repo уже выбран, 1.5.5 остаётся blocked на full runtime interfaces. Отдельно разрешён pure local срез ниже; его tests не меняют NOT_RUN в 81 runtime строке. Actual progress читать CLI; DOC — документарный criterion. Все production parents открыты.

| Task | Requirements | Increment | Criterion / current evidence |
|---|---|---|---|
| 1.1 | TG-01, TG-02, TG-03, TG-04 | E1+E2 | N-01/N-02 actual native owner/replay/cancel; H:E1–3 частичны |
| 1.2 | TG-05, ENV-01 | E1+E2 | N-03/N-04 actual OAuth/refresh/sentinel boundary; H:E4/H:E5 не admission |
| 1.2.1 | TG-04, TG-05 | E1 | Source definition/schema/caller или bounded BLOCKED N-03 |
| 1.3 | MEM-11, UPD-01, UPD-02 | E1+E2 | Actual lifecycle/checkpoint/drain, не список source hooks |
| 1.3.1 | MEM-12 | E1 | Раздельная Hermes/Codex history/hydration event coverage |
| 1.3.2 | UPD-01, UPD-02 | E1+E2 | Source locks/manual drain gap, без invented server lock graph |
| 1.4 | BACK-01, BACK-02, BACK-03 | E2 | N-07 suitability/limits/sample и owner fallback decision |
| 1.5 | ENV-01, TG-04, MEM-12, SSH-01, SSH-02 | E1+E2 | Owner-selected repo/exact runtime tests/layout/limits/locks |
| 1.5.1 | TG-03, TG-05 | E1 | Actual candidate Git + definition/caller/deployment-test trace |
| 1.5.2 | ENV-01, MEM-12 | E1 | Storage classes/owner/worktrees, unknown host parameters BLOCKED |
| 1.5.3 | SSH-01, SSH-02 | E1 | Source-backed ordinary session candidate, exact test paths или BLOCKED |
| 1.5.4 | TG-04, MEM-10, MEM-11, MEM-12 | E1 | OpenSpec/MemPalace/skills/rules × harness evidence и project scope |
| 1.5.5 | DOC | E1 | Runnable RED/GREEN children только после выбора repo/interfaces |
| 1.6 | TG-01, TG-09 | E1+E2 | Exact owner revision/increment и separate infrastructure grant |
| 2.1 | TG-01 | E1+E2 | Actual owner/project/revision intake; local-first без remote creation |
| 2.2 | TG-02 | E1+E2 | Native mapping duplicate/crash/reopen, без собственного scheduler |
| 2.3 | TG-02, TG-06 | E1+E2 | Cancel/release generation race и late result fencing |
| 3.1 | ENV-01, TG-05 | E1+E2 | Pinned project container/resource/credential negative acceptance |
| 3.1.1 | ENV-01, TG-05 | E1 local only | RED closed fields/types/identifiers/digest, без native/OS admission |
| 3.1.2 | ENV-01, TG-05 | E1 local only | GREEN pure strict input validation |
| 3.1.3 | ENV-01 | E1 local only | RED owner/project identity и private/work layout |
| 3.1.4 | ENV-01 | E1 local only | GREEN deterministic paths; нет filesystem effects |
| 3.1.5 | ENV-01, TG-05 | E1 local only | RED exact resource profiles и no runtime admission |
| 3.1.6 | ENV-01, TG-05 | E1 local only | GREEN data-only limits без shared/input mutation |
| 3.1.7 | TG-07 | E1 local only | Actual local regressions и accept-all negative control; не full trusted runtime pack |
| 3.1.8 | DOC | E1 local only | Backup, narrow Git admission, docs/digest/progress, no commit |
| 3.2 | TG-04, TG-05 | E1+E2 | Actual supported launch argv/cwd/stdin/error semantics |
| 3.3 | TG-03, MEM-11, MEM-12, SSH-01 | E1+E2 | Real parallel worktrees, second project, conflicts/retests |
| 3.4 | TG-06 | E1+E2 | Task descendants stopped/readback без соседнего project impact |
| 3.5 | MEM-10, MEM-11, MEM-12 | E1+E2 | Real history/ACL/hydration/rebuild; knowledge PR остаётся E2 |
| 3.6 | TG-04 | E1+E2 | Actual adapter loading/use/pins и project-only install isolation |
| 3.7 | SSH-01, SSH-02, TG-05, MEM-12 | E1 | Ordinary manual session, same-process reconnect и death cases |
| 3.8 | ENV-01, MEM-12 | E1 | Reuse/recreate сохраняют WIP/history, fail-closed storage |
| 4.1 | PRE-01, PRE-02, TG-08 | E2 | Настоящий browser behavior RED и exact runner |
| 4.2 | PRE-01, PRE-02 | E2 | Минимальная real offline demo page GREEN |
| 4.3 | TG-07 | E1+E2 | Trusted candidate/pack negative checks; full frontend parent не закрыт E1 |
| 5.1 | TG-09 | E2 | Private repo/publisher isolation и exact privacy readback |
| 5.2 | TG-09 | E2 | Actual task push/PR, exact owner-controlled merge |
| 5.3 | TG-10 | E2 | Fault fixture плюс отдельно разрешённый real publication canary |
| 6.1 | TG-11 | E1+E2 | Source route/artifact report, E1 not_provisioned и E2 PR/preview |
| 6.2 | TG-12 | E1+E2 | Durable delivery restart без повторного development |
| 6.3 | REC-01, REC-02 | E2 | Independent production ORCH-01, bounded retry/fencing/readback |
| 7.1 | BACK-01 | E2 | Consistent changed-only encrypted package и embedded-secret negative |
| 7.2 | BACK-02 | E2 | N-07/grant, actual encrypted upload/exact readback/reconciliation |
| 7.3 | BACK-03 | E2 | Real restore-check separate target без code execution |
| 7.4 | BACK-03 | E2 | Telegram owner attestation и protected scope/dependency retention |
| 7.5 | ENV-02 | E1+E2 | Ownership cleanup race учитывает detached/manual/history references |
| 7.6 | UPD-01, UPD-02 | E1+E2 | Actual updater fixture/coordination; full offsite gate E2, daily protections |
| 8.1 | TG-01, TG-02, TG-03, TG-04, TG-05, TG-06, TG-07, TG-08, TG-09, TG-10, TG-11, TG-12, PRE-01, PRE-02 | E2 | Полный Telegram→Codex→tests→private PR→file preview journey со всеми TG-критериями |
| 8.2 | REC-01, REC-02, UPD-01, UPD-02, BACK-01, BACK-02, BACK-03 | E2 | Разрешённые provider/restart/maintenance/backup faults, host-return report |
| 8.3 | DOC | E2 | Exact candidate/spec receipts + owner runtime acceptance; archive отдельно |
| 8.4 | TG-07, TG-08, SSH-01, SSH-02, MEM-12, ENV-01 | E1 | Actual E1 working environment/trusted pack/owner acceptance, E2/ORCH open |

### Native verification mapping 2026-09-28

E1-NATIVE-PACKET-2026-09-28: supplement к текущей coverage; прежние scenario rows и task criteria сохранены. Источник — [native readiness](../telegram-development-workflow/implementation-readiness.md#native-launch-preparation-2026-09-28). Verification ниже — требуемое наблюдение, не выдуманная выполненная команда. Gate B запрещает runnable claim до exact native path discovery; все runtime результаты NOT_RUN.

| Requirement | Exact scenario | Existing parent | Required verification / blocker | Observed result |
|---|---|---|---|---|
| TG-05 | Invalid base or injected command | 1.5.5, 3.2 | Actual native deny до process/external effect; B-SRC/B-LAUNCH | SOURCE_ONLY; runtime NOT_RUN |
| TG-04 | Unsupported runtime interface | 1.2, 3.2, 3.7 | Missing/empty/disabled/dead environment и hostile bootstrap отдельно exec/TUI; B-SRC/B-ISOLATION | SOURCE_ONLY; runtime NOT_RUN |
| TG-05 | Manual launch has the same boundary | 1.2, 3.7 | FS/proc/ptrace/FD/IPC/network/config denials плюс own-work control; B-ISOLATION | NOT_RUN |
| MEM-11 | Pre-compression failure | 1.3, 3.5 | Required checkpoint/write failure реально блокирует потерю; B-HISTORY | Guard SOURCE_ONLY; runtime NOT_RUN |
| MEM-12 | History write or hydration fails | 3.5, 3.8 | Originals/current revision/checkpoint fail-closed обоих harness; B-HISTORY | SOURCE_ONLY; runtime NOT_RUN |
| MEM-12 | Compression preserves original history | 3.5, 3.8 | Intent/result/incomplete originals после crash/compression/rebuild; B-HISTORY | NOT_RUN |
| MEM-12 | Parallel histories stay attributable | 3.3, 3.5 | Owner/project/session/attempt/worktree attribution и scoped current packets; B-HISTORY | NOT_RUN |
| SSH-01 | Open manual session alongside automation | 3.3, 3.7 | Same container, separate writer/current context; B-LIFECYCLE/B-HISTORY | NOT_RUN |
| SSH-02 | SSH drops and reconnects | 3.7 | Same live identity, no duplicate; B-LIFECYCLE | NOT_RUN |
| SSH-02 | Codex died while disconnected | 3.7 | Truthful dead/new-run boundary, no blind retry; B-LIFECYCLE | NOT_RUN |
| SSH-02 | Container destroyed while disconnected | 3.7, 3.8 | Storage preserved, previous process dead, new hydrated run; B-LIFECYCLE/B-HISTORY | NOT_RUN |
| ENV-01 | Resource admission | 3.1 | Actual bind quota/UID/mount/pool readback; B-RESOURCE | Pure policy historical PASS, runtime NOT_RUN |
| ENV-02 | New use during cleanup | 7.5, 7.6 | Project-reference recheck во всех cleanup/recovery branches; B-UPDATER | Conditional source risk; runtime NOT_RUN |
| UPD-01 | Manual session survives servicing deadline | 7.6 | Detached writer учтён, bounded defer без kill; B-UPDATER | NOT_RUN |

Остальные TG-03/04/05/06, SSH-01 conflict/unauthorized, MEM-12 start и TG-08 acceptance obligations остаются в основной current table; negative matrix/transition mapping раскрыты в linked packet. Source-only подготовка не увеличивает product completion, не закрывает 1.5.5/E1/ORCH-01.

### Native source follow-up mapping 2026-09-28

E1-NATIVE-SOURCE-V2-2026-09-28: [current source follow-up](../telegram-development-workflow/implementation-readiness.md#native-source-follow-up-2026-09-28). Дополнение прежних coverage rows; original requirements/scenarios/parents не меняются, все runtime outcomes NOT_RUN.

| Requirement / exact scenario | Existing parents | Observed source / remaining proof |
|---|---|---|
| TG-05 / Invalid base or injected command | 1.5.5, 3.2 | Handler environment-denial найден, но не trusted pre-process argv/base gate; hooks/patch precede ordinary spawn |
| MEM-11 / Pre-compression failure | 1.3, 3.5 | Session replacement-before-append и log-only failure; mandatory checkpoint fault proof отсутствует |
| MEM-12 / History write or hydration fails | 3.5, 3.8 | Native queue/flush/retry существуют, ignored caller errors не fail-closed project admission |
| SSH-01 / Open manual session alongside automation | 3.3, 3.7 | Shared core не доказывает ordinary TUI isolation/hydration/continuity |

Product progress 15/52; Gate B остаётся, E1/ORCH-01 не приняты. Получение исходников не native test PASS.
