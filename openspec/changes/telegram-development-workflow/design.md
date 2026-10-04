## Context

Мотивация — proposal.md; подтверждённые решения — interview-decisions.md; серверные факты — baseline.md. Документ остаётся draft до exact revision approval. Старые research-планы являются историческим материалом, не актуальным поручением создавать собственные approvals или full-stack preview. API выбранного серверного Hermes проверяются независимо от локальной установки и latest docs; native-capability-matrix.md отделяет факты от незакрытых gates.

## Goals / Non-Goals

**Goals:** native-first Telegram → Hermes → Codex на общем ainetic.tech, сначала принимаемая рабочая среда с отдельным обычным SSH Codex; сохранение identity/evidence, полной проектной истории и автоматическое восстановление актуального контекста. Approval только штатный, без новой платформы. Статический танцевальный гид — первый демонстрационный продукт последующего инкремента, не prerequisite окружения.

**Non-Goals:** собственные scheduler/approval service, общий writable Hermes/Codex home с credentials, обязательный app-server или takeover Hermes-задачи, внешний host monitoring, публичный preview и production deploy. Не обещать живой прежний процесс после разрушения контейнера.

## Decisions

1. **Разные источники истины.** OpenSpec — требования и spec revision; штатный Kanban — tasks/attempts; Git — candidate commits; runtime evidence — фактические проверки; MemPalace — индекс, а не authority. Обновление памяти не означает завершение задачи или выдачу полномочий.
2. **Штатное admission и approvals.** Telegram identity связывается с owner/project/spec/action. Проверяем replay/cancel/restart на точной версии. Без поддерживаемого gate действие blocked; не создавать `approvals.py`, custom buttons или альтернативную очередь из раннего плана. Разрешённая автоматическая публикация task branch/PR отделена от owner-controlled merge.
3. **Контейнеры на общем host.** Один reusable Dev Container на owner/project, не на задачу/SSH login. Планируемый root `/srv/hermes-projects/<owner_id>/<project_id>` отделён от existing `/srv/hermes-agent/data` и `/srv/hermes-agent/work`; `work/` монтируется worker в `/workspace`, включает repo/worktrees/WIP/specs. `private/history/{hermes,codex}`, `private/{context,checkpoints,results}` не монтируются worker целиком; только разрешённый read-only context packet. `cache/` воспроизводим, не хранит originals. Credentials вне project root. Root/control parents root-owned; private directories 0700/files 0600 с назначенным trusted writer, worker work subtree отдельного UID/GID. Production UID/ACL/quota allocation и symlink/TOCTOU/mount proof ещё BLOCKED; numeric test IDs не server accounts. Строковый parser ниже не доказывает изоляцию и не выдаёт admission. Не раздавать socket/root; env-конфигурацию применяет доверенный слой. Историческое root SSH обследование не задаёт пользовательский доступ.
4. **Параллельные worktrees.** Автоматический и ручной writer получают отдельные branch/cwd и packet внутри одного project container. Worktree не является credential sandbox: task containment и isolation проверяются отдельно. Интеграция последовательная, конфликт сохраняет обе работы, tests повторяются на объединённом candidate. Общий writable agent home исключён. Новые специализированные профили и их общение не требуются MVP1.
5. **Два штатных CLI пути.** Fixed source candidate Codex `rust-v0.153.4` / `3d2ee51ca2d5db578f328aa75e20aa22c0197c9a`, Linux x86_64 CLI bundle; не установлен и не admitted. Native Hermes exec seam с fixed argv/stdin/cwd ещё проверяется отдельно от ordinary interactive CLI. C2-кандидат разделяет trusted client и project process identities внутри того же project container: одного UID separation недостаточно, нужны FS/proc/ptrace/FD/IPC/network/config/all-tool negative checks. Automatic/manual homes не shared writable; OAuth provisioning/refresh требует отдельного scope, без copying/API billing fallback. Controller-owned environments.toml с explicit include_local=false/default предпочтительнее env-only policy; missing/dead/ambiguous endpoint блокирует, но actual dual-CLI routing/bootstrap/MCP/daemon containment пока BLOCKED. TUI и exec используют разные bootstrap paths; --ignore-user-config не credential sandbox. Embedded backend обычного CLI не означает выбор Hermes app-server runtime и не заменяет ordinary manual CLI. Native exec-server — процесс, не второй container проекта. Для SSH выбран tmux `3.7c` как НЕ УСТАНОВЛЕННЫЙ кандидат: exact owned attach-session после identity/generation/liveness check, без new-session -A/resume --last. New и attach различаются; death/recreate не сохраняет старый процесс. Ни custom runner, ни перенос trusted CLI вне контейнера для обхода SSH-01 не разрешены.

Исследовательский кандидат, не принятое runtime-решение: последующие app-server/exec-server/environment probes описаны в [native-environment-evidence.md](native-environment-evidence.md), [native-bootstrap-evidence.md](native-bootstrap-evidence.md) и [linux-model-lifecycle-preparation.md](linux-model-lifecycle-preparation.md). Их local/native/synthetic и отдельное историческое one-shot Linux canary evidence не закрывают CLIENT_ROUTING_GATE_OPEN / NOT_DEPLOYABLE и не разрешают повторный запуск. Они не отменяют два CLI пути и E1/E2 выше; app-server не обязателен для ordinary SSH CLI. Выбор production runner требует source discovery N-03/N-08/N-09 и отдельного согласования exact design/spec revision и runtime scope. Актуальная трассировка и границы исторических результатов: [current coverage](../adopt-openspec-workflow/audit.md#current-coverage).

6. **Результат и доставка.** Candidate и acceptance pack фиксируются; worker не может превратить провал в success подменой тестов. Первый pack проверяет рабочую среду по TG-08/SSH-01–02/MEM-12. Telegram возвращает реальные изменения/tests, task/session, worktree/branch/revision и явные blockers, без выдуманных PR/preview. Последующий demo pack сохраняет file://, keyboard/desktop/mobile, console/network/screenshots, sources/demo labels; публикационный отчёт дополняется repo/PR/preview. Git sync ручной, повтор доставки не запускает разработку заново.
7. **История, знания и стартовый контекст.** Полная приватная история проекта — отдельный durable источник, не только Markdown summaries или MemPalace. Запись событий Hermes/Codex сохраняет attribution/order и незавершённые события; compression/rebuild не удаляют оригиналы. При новом запуске адаптер автоматически собирает ограниченный актуальный packet из текущих specs/Git/task state/checkpoints с разрешёнными ссылками в историю. При reconnect живой SSH-сессии сохраняется её identity; reconnect не маскируется новым запуском. Retrieval сначала проверяет scope; ни история, ни индекс не меняют approvals. Роли/отобранные уроки — agent-knowledge, проектные specs — его repo, приватная история/checkpoints — вне Git и credential homes. PR знаний остаётся downstream. Для embedded DB нужен один владелец записи и проверенный доступ, не общий writable mount как ACL. Формат событий, полнота hooks и hydration ещё не доказаны (N-05/N-10).
8. **ORCH-01.** Независимый controller наблюдает штатное task state и heartbeat, не разговорную память. Не позднее пяти минут обнаруживает потерю heartbeat при живом host/controller; quiet build не считается dead. Повторы ограничены, старые процессы подтверждённо остановлены, unknown side effects сначала reconciled. Контроллер перезапускается средствами управления процессами, выбранными после обследования; новый профиль сам по себе не обеспечивает наблюдение.
9. **Maintenance/cleanup.** Existing updater продолжает согласованные автоматические daily stable updates; новая координация не означает approval каждого обычного update. Изменение скрипта/policy — отдельное owner approval. Drain охватывает automatic attempts и manual sessions, включая detached, и гонку допуска/старта; timeout означает defer, не kill. До E1 требуется доказать безопасное сосуществование или отдельно согласовать нужный diff, не игнорировать риск обслуживания. Существующие stop→consistent snapshot, auth, candidate validation, rollback и pins не ослабляются. Полный off-host gate добавляется в E2, а не ложно объявляется реализованным E1. Cleanup учитывает worktree/session/history references; глобальный prune запрещён.
10. **Backup.** Код доставляется обычным Git. Changed-only пакеты несут unpublished work, приватное состояние и manifest; snapshots БД должны быть согласованы. Шифровать public key, без private key на сервере. GitHub Releases suitability — blocking gate, не утверждённое бесконечное хранилище. Exact object readback не равен restore-check. Владелец локально проверяет комплектность без исполнения кода и сообщает ID/checksum через штатный Telegram; cleanup хранит последнюю verified copy и зависимости сверх 30 дней. При отсутствии verification данные не удаляются.
11. **Два уровня расширений.** Общие OpenSpec/MemPalace/skills/rules закрепляются по версии/commit и имеют проверенные отдельно Hermes/Codex adapters. Изолированные project tools/skills/dependencies устанавливаются автономно внутри разрешённого проекта. Shared updates/base image/server settings/SSH access/mount permissions требуют owner approval через Telegram. Наличие AGENTS.md или общего каталога не доказывает загрузку либо совместимость (N-11). Список установленных runtime integrations пока не назначен; native-first discovery предшествует выбору glue.

## Acceptance Increments

### Approved local policy slice 2026-09-28

Подтверждение владельца «+» относится к [пакету E1-LOCAL-PACKET-2026-09-28](../../../.hermes/plans/2026-09-28_e1-local-design-and-first-tdd.md), включая только local apply 3.1.1–3.1.8. Это parser/planner, не resource allocator/launcher и не runtime approval.

`scripts/project_environment.py:plan_project_environment(document)` — новый локальный stdlib API (Python 3.10+), не native Hermes symbol. Ровно семь полей: schema_version, owner_id, project_id, image_ref, worker_uid, worker_gid, resource_class. Только plain dict/строки/целые JSON-типы; bool не int. Schema ровно 1; UID/GID 1000..65533 лишь lexical policy. Opaque IDs `[a-z][a-z0-9]{0,15}` не нормализуются и не извлекаются из human names. Image — bounded lowercase repository@sha256:64-lowercase-hex; conservative repository grammar с сегментами и optional registry port, без tag/URL/userinfo/пустых/dot segments. Registry/image trust остаётся обязанностью future approved binding. Unknown/missing fields и invalid values дают фиксированный ValueError code без payload.

Data-only output сохраняет validated binding, строит `hproj-<owner>-<project>`, project_root, единственный RW worker mount `work`→`/workspace`, private history/context/checkpoint/result paths, cache path, fixed resources и всегда `runtime_admitted=false`. Grammar IDs исключает delimiter collision. Никаких filesystem/network/process/DB calls, mutable shared output, arbitrary host mounts/env/command/oauth/routing/privileged/socket полей; вход не изменяется. Tests — `tests/test_project_environment.py`; RED/GREEN T1 и отрицательная scratch mutation описаны в tasks.md.

Планируемый pool: максимум 2 running project containers, 1000 millicores / 2048 MiB RAM / 512 pids суммарно; compact 500/1024/256, large 1000/2048/512 занимает весь pool. До 2 writers/project и 3/pool, detached учитывается. Target disk hard quota 4 GiB/project, host free floor 20 GiB; pull/update/backup headroom дополнительно. Memory-swap равен memory; OOM killer не выключается. Это approved design candidates по dated survey, НЕ actual allocation/performance guarantee. Parser возвращает per-project значения, но не резервирует pool, не проверяет quota или свободный host. Без настоящего quota механизма bind mount запуск blocked; du/writable-layer limit не замена. Idle/stopped environment не удаляется автоматически, нехватка ресурсов оставляет работу в native Kanban, не новом scheduler.

History layout не определяет сам собой streaming/crash hooks и hydration. Mount всего CODEX_HOME как истории запрещён; origins/события и credentials раздельны, fake full-log не допустим.

Maintenance candidate: атомарно закрыть NEW admission с maintenance intent, учесть automatic/manual/detached и descendants, разрешить finish/cancel/status; не держать short gate всю session. Общий порядок existing maintenance → existing launcher-image → proposed project admission → proposed storage; reverse acquisition исключён. Proposed deadline 60s monotonic, active/unknown → DEFER без kill и release intent; corrupt registry fail closed. После reconciled zero writers — existing stop gateway → consistent snapshot → validation/deploy/rollback, все recovery/cleanup entry points проходят gate. Existing launcher EX сейчас blocking: long-held shared session lock отвергнут как unbounded wait. Hook/точный updater diff/race proofs отсутствуют; live updater не меняется без отдельного grant. Daily timer и backup/auth/rollback protections сохраняются.

### Runtime increments

| Этап | Принимаемый outcome | Что не закрывает |
|---|---|---|
| E1 — рабочая среда | Telegram → native Hermes/Codex → code/tests → truthful report; обычный независимый SSH Codex, reconnect, parallel worktrees и tested integration; bind mount, полная история и автоматический context recovery. Нужны относящиеся N-01–06/N-08–11, exact revision/scope approval и safe maintenance coexistence | Remote private repo/PR, PRE-01–02 demo, BACK-01–03, полный UPD-02 и production ORCH-01 не объявляются принятыми |
| E2 — последующие инкременты полного MVP1 | Private repo/task branch/PR и controlled merge, contemporary-dance-guide/file:// acceptance; encrypted offsite backup/restore/retention, полный maintenance/recovery и owner end-to-end acceptance | Production deploy и внешний host monitoring по-прежнему не входят в scope; archive отдельно |

E1 не отменяет ни одного исходного parent task. TG-09–10, PRE-01–02 и BACK-01–03 остаются полными downstream контрактами: «первый проект» PRE-01 означает первый демонстрационный продукт, а не запрет проверять E1 на разрешённой fixture. При ограниченном E1 approval admission не активирует publication. Native gates отмечаются по области/сценариям; частичный E1 pass не закрывает полный gate N-06 или весь MVP1. Нумерация E1/E2 — scope приёмки, не вторая очередь; единственный checklist — tasks.md.

## Capability Map

Зависимости ниже означают контракты данных, а не дополнительные сервисы. Карта включена в согласованный план подготовки; точная revision остаётся pending.

| Capability | Требования | Зависит от |
|---|---|---|
| task-intake | TG-01–02 | — |
| project-environments | ENV-01–02 | task-intake |
| portable-memory | MEM-10–12 | task-intake, project-environments |
| specialist-dispatch | TG-03–04 | task-intake, project-environments, portable-memory |
| code-execution | TG-05–06 | specialist-dispatch |
| interactive-access | SSH-01–02 | code-execution, project-environments, portable-memory |
| local-preview | PRE-01–02 | code-execution; E2 |
| verification | TG-07–08 | code-execution, interactive-access (E1); local-preview для demo E2 |
| change-publication | TG-09–10 | verification; E2 |
| task-recovery | REC-01–02 | code-execution, interactive-access; change-publication для reconciliation PR в E2 |
| offsite-backup | BACK-01–03 | portable-memory, project-environments, change-publication |
| maintenance-coordination | UPD-01–02 | code-execution, interactive-access; task-recovery/offsite-backup для полного E2 |
| telegram-delivery | TG-11–12 | события предыдущих capabilities |

Штатный Telegram ingress/transport доступен как проверяемая платформа до этих срезов; telegram-delivery описывает доставку результатов, не создаёт циклическую зависимость admission от собственной очереди.

## Risks / Trade-offs

- Изменяемые native API → capability probes по baseline; конкретные imports и callbacks не выбирать до проверки исходников.
- Shared state и поздние callbacks → generation fencing, blocked-until-mapped, authoritative reconciliation.
- Потомок выходит из process group → task cgroup/container stop, не обещать остановку по одному PID.
- Ложные test receipts → trusted acceptance pack на заведомо ошибочном candidate, проверка integrity, не только exit0.
- Schema completeness путают с approval → явный pending status, незакрытые implementation tasks, штатное согласование exact revision.
- Малый shared host → admission limits после измерений, без снятия ограничений ради параллелизма.
- Приватная память в Git и credential cloning → отобранные документы отдельно, encryption, single-owner OAuth refresh probe, запрет записи секретов.
- Потеря host → уведомление только после возврата; внешний мониторинг не входит в MVP1.
- Full-history hooks не покрывают streaming/crash или секреты → доказать полноту/границу durability и fail-closed paths, не выдавать текущий completed-turn spool за MEM-12.
- Detached ручная сессия удерживает drain → bounded timeout/defer, не принудительное убийство ради обновления.
- Bind mount сохраняет данные, но не процесс и не offsite копию → отдельные проверки recreate/hydration и downstream restore; explicit limited acceptance E1.

## Migration Plan

1. Repo выбран: `hermes-agent`. Сначала выполнить отдельно разрешённый pure local срез, не закрывая runtime parents. Для запуска E1 закрыть blocking probes, actual paths/UID/quota/client/updater interfaces; получить exact E1 revision approval и отдельно infrastructure/canary grants.
2. Маленькими TDD срезами проверить admission, контейнерную границу, writers, full history/hydration и SSH continuity. Тесты выбирать после discovery; не создавать fake APIs ради плана. Выполнить E1 live acceptance только в разрешённом scope, без обязательной real publication.
3. Отдельными E2 срезами пройти dance-guide, GitHub/Telegram readback и повторную проверку candidate; исходные obligations остаются в tasks.md.
4. Добавить и проверить production ORCH-01, backup/restore и полный maintenance failure contract на изолированных fixtures и разрешённой среде. До этого не заявлять full readiness.
5. Перед rollout получить infrastructure approval, сохранить snapshot; после rollback закрыть admission, остановить принадлежащие попыткам процессы, сохранить код/память/state и сообщить фактический статус. Archive только после runtime acceptance и owner decision.

## Blocking Gates and Deferred Parameters

Host ainetic.tech, owner RussianLioN, implementation repo и downstream проекты выбраны. Read-only survey от 2026-09-23 записан в readiness, не свежий runtime admission: server Hermes 0.21.2 отличается от local 0.21.4, existing launcher per-invocation --rm. Числа/layout выше — design candidates, actual capacity/UID/quota и enforcement не проверены. Safety boundaries, native approvals/launch, subscription flow, SSH, history/hydration/extensions и bounded updater coexistence блокируют E1; backup suitability блокирует E2/full readiness. Невозможность контракта возвращается владельцу, не маскируется условным планом.

Единственный checklist — tasks.md. Разрешён только указанный локальный data-only срез со stdlib unittest, без новых зависимостей; остальные runtime interfaces/commands BLOCKED_PATH_DISCOVERY. Full product owner approval/implementation_ready остаются false; частичный local scope фиксируется отдельно. Исторический research сохраняется без распространения прежних неподтверждённых решений.

## Native launch source findings 2026-09-28

Пакет E1-NATIVE-PACKET-2026-09-28 — Gate B, не runnable runtime design. Source pins: local Hermes b22631ec4f349c64f50835c6d3434f89986ca05c; cached Codex rust-v0.153.4 / 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a; updater fixture ebd88a8359b4ff8aa0161bb1e00147d36db1fc5b96e63642fb2947a21d43141a. Hash/line inventory и boundary matrix — [подготовленный пакет](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#native-codex-preparation--e1-native-packet-2026-09-28).

Exec: CLI dispatch → codex_exec::run_main → config/state DB → codex_app_server_client::EnvironmentManager → in-process client. TUI: ordinary CLI → codex_tui::run_main/startup → daemon/target selection → codex_exec_server::EnvironmentManager::prepare_from_codex_home/prepare_from_env. Связь двух manager imports и all-tool routing не установлена; один probe не доказывает другой. SharedCliOptions и recorder/flush definitions требуют pinned source closure. Generic Hermes terminal принимает shell command, не typed Codex request; prompt/stdin/base/cwd ownership до process creation ещё не доказаны.

Pre-main dotenv и последующая config/extension/daemon загрузка входят в boundary. Env-provider missing/empty URL запрашивает local; none означает Disabled; dead remote — отдельный непроверенный случай. environments.toml по умолчанию включает local. Controller-owned explicit remote-only/default остаётся кандидатом, не proof all-path mediation. Требуются отдельные exec/TUI negative checks FS/proc/ptrace/FD/IPC/socket/network/config/MCP/plugins/hooks с own-work positive control; UID split сам по себе недостаточен.

Hermes persistence flush имеет None/False paths, generic semantic prefetch может быть пустым/best-effort. Обязательное current-context admission не доказано. MemPalace filtered user/assistant spool не полный event archive. Required checkpoint guard Hermes codex_app_server сохраняется; не выключать его ради запуска. Full originals и fail-closed history/hydration остаются prerequisites MEM-12, не отложенной деталью. One container/separate worktrees, live attach/dead/recreate transitions и quotas сохраняют прежние требования.

Updater cleanup вызывается также на current/quarantined candidate и после rollback. Stopped-container removal проверяет managed image/labels и Running, но показанный path не проверяет будущие project references. Риск условен: будущий container должен совпасть с классификатором. Gate только перед stop_gateway недостаточен; нужны все cleanup/recover paths и admission races. Proposed 60s drain/defer не свойство текущего blocking launcher lock. Daily policy, snapshot/auth/rollback не меняются этим документом.

Альтернативы: shared-identity credential-bearing CLI не принят из-за непроверенной изоляции; перенос trusted client вне project container не принят как молчаливое изменение SSH-01; Hermes app-server не принят как обход checkpoint/ordinary CLI. C2 остаётся кандидатом до source closure и отдельных OS/model proofs. Первый TDD parent 3.2 остаётся BLOCKED_PATH_DISCOVERY; 3.7 проверяется отдельно. Exact canary NOT_RUNNABLE, ORCH-01 / CRITICAL открыт.

## Native source follow-up 2026-09-28

E1-NATIVE-SOURCE-V2-2026-09-28 уточняет прежние source gaps; [полные receipts и V2-F1–F7](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#native-source-follow-up--e1-native-source-v2-2026-09-28). Pin Codex 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a сохранён. Exec/TUI EnvironmentManager — один reexported type, но bootstrap branches разные. SharedCliOptions и RolloutRecorder найдены. Selected shell path: registry → ExecCommandHandler → process manager/runtime → environment backend; отсутствие environment отклоняется handler, remote start error не переключается на local spawn в показанной ветке. PreToolUse hooks и apply_patch interception предшествуют обычному spawn: это не all-tool/pre-effect proof.

Native history имеет queue, flush acknowledgements и retry. Однако Session.persist_rollout_items логирует append failure без возврата ошибки; replace_compacted_history меняет рабочую history до этой записи; resume/fork местами игнорируют flush result. Это source-level B-HISTORY, не выполненный fault test и не доказанное удаление originals. Native persistence сама по себе не принимается как обязательный fail-closed checkpoint MEM-11/12. Full store/extension/environment callers, crash и project-context hydration ещё требуют доказательства.

Gate B сохранён. Перед runnable TDD необходимо выбрать обязательную history/admission boundary для ordinary exec и отдельного SSH TUI без изменения installed upstream. Внешняя boundary — только кандидат, spawn-only gate/observer tailing недостаточны; обязательный checkpoint не отключается. История, C2 isolation, один reusable container/project, resource/lifecycle/updater contracts и false full approval/readiness не ослабляются.
