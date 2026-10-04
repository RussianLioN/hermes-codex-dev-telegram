# Implementation readiness — discovery

Статус: NOT_READY / BLOCKED_PATH_DISCOVERY, включая первый этап рабочей среды E1. Implementation repo — локальный `hermes-agent`; [решение и selective reuse](#repository-decision-2026-09-23) сохранены. По последующему «действуй» выполнен [bounded read-only server survey](#server-read-only-survey-2026-09-23): SSH/source inventory больше не ожидает разрешения, но обнаруженные interfaces не дают безопасного runnable E1. Exact revision approval остаётся pending. Предшествующие pins/receipts исторические; survey не разрешает server writes, install, config/OAuth changes, canary/model/deployment или вторую очередь вместо Hermes Kanban.

## Текущие блокеры рабочей среды

| Область | Gate / критерии | Что должно появиться до runnable implementation plan |
|---|---|---|
| Native automatic Codex | N-01–04, TG-01–06 | Installed server revision, штатный специализированный interface/schema + caller trace, lifecycle/fencing, OAuth-client/project-code boundary. Latest docs и наличие tool-name не доказательство |
| Project storage | N-04/N-08/N-10, ENV-01–02 | Approved host folder/UID/mount/permissions layout, private history отдельно от credentials, Git/worktree topology, limits и safe recreate/cleanup test paths |
| Full history/hydration | N-05/N-10, MEM-10–12 | Hermes и Codex event coverage, durability/crash boundary, current-context loader, redaction/ACL/attribution и negative tests; index не единственный источник |
| Interactive SSH | N-09, SSH-01–02 | Обычный CLI, отдельная session identity и worktree, проверенный detach/reconnect механизм, death/recreate distinctions. Exact runtime/source/test paths пока неизвестны |
| Extension levels | N-11, TG-04 | OpenSpec/MemPalace/skills/rules × Hermes/Codex version/adapter/load/use matrix, shared approval boundary и project-only install evidence |
| Maintenance coexistence | N-06/N-09, UPD-01–02 | Полный admission/session lock graph, active/detached session drain/defer, сохранение existing updater protections. Если нужна серверная правка — отдельный exact diff/approval, не запись в этом docs update |
| Implementation ownership | N-08, частично снят | Владелец выбрал текущий `hermes-agent`, локальный Git создан; `hermes-remote-migration` только source donor. Остались exact runtime/test paths, interfaces и manifest commands; выбор repo не закрывает весь N-08 |

Для E2 отдельно остаются N-07/storage suitability, publisher credentials/readback, PRE-01–02, BACK-01–03, полный UPD-02 и production REC-01–02. Их перенос не разрешает обойти общие safety gates E1. Existing server container/updater теперь сверены read-only; это не проверка будущих project containers и не runtime acceptance.

## Следующий ограниченный scope

Read-only discovery children 1.2.1, 1.3.1–1.3.2 и 1.5.1–1.5.4 завершены, repo выбран, разрешённый server survey выполнен. Следующий пакет — локальное закрытие design/admission решений по фактам survey, затем runnable TDD 1.5.5 для первого code parent. Не запускать `inventory`, если он может загрузить configured MCP или обратиться к модели. Server mutations/canary/install и cross-model вызовы требуют самостоятельного scope. C13 не закрывать placeholder тестом: server CLI/version, credential-safe native launch и updater/manual admission ещё не доказаны.

Плановые outputs только в существующих `native-capability-matrix.md`, `implementation-readiness.md`, `design.md`, `tasks.md`; изменение нормативной revision заново пересчитывает digest и требует review. ORCH-01 / CRITICAL остаётся открытым.

## Исторический кандидат для reuse

`/Users/s060874gmail.com/coding/projects/hermes-remote-migration`, branch `feat/codex-runner`, HEAD `8cbce95`, clean на момент прежней read-only проверки. Это не Git основного operations workspace; актуальность состояния нужно перепроверить при отдельном reuse discovery.

Прочитаны:
- `scripts/codex_runner.py:1–100`: policy/SQLite job core, стандартная библиотека; `ALLOWED_REPOSITORY` и URL на :34–35 жёстко фиксируют RussianLioN/hermes-remote-migration.
- `deploy/codex-runner/app/runner_service.py:1–100`: controller HTTP, executor polling, publisher candidates; imports из scripts/codex_runner.py, fixed `/app/scripts`.
- `deploy/codex-runner/README.md:1–60`: три роли, GitHub App publisher, отдельный updater, executor OAuth volume.
- Definition discovery `tests/test_codex_runner.py` и `tests/test_codex_runner_deployment.py`: unittest, manifest validation, job store, maintenance gate, controller transport и deployment checks. Тесты пока не запускались: полный setup/side effects ещё не прочитан.

## Решение, которое уже можно принять без переписывания

Этот runner нельзя разворачивать как готовую текущую систему: hardcoded repository исключает per-project создание; GitHub App auth отличается от согласованного publisher CLI flow; отдельный updater и custom technical state требуют проверки на дублирование. Это не означает выбросить код: reuse оценивать по функциям и тестам после полного caller trace. Исторические tests являются кандидатами regression, не acceptance current MVP1.

## Выполненный bounded discovery 2026-09-11

Read-only git повторно: clean `feat/codex-runner`, HEAD `8cbce9554d2644c0af0333b2b065978b2fb63c4b`. Полностью прочитаны ManifestValidationTests, JobStoreTests и JobStore :278–784; выполнен изолированный `probe_runner_reuse.py`: 14 tests, failures/errors/skipped 0. Реальных HTTP/controller/executor/publisher/deployment tests не запускали. Подробнее: `../../../.hermes/research/telegram-hermes-codex/readiness-probes-2026-09-11.md`.

Важное source finding: `JobStore.claim_next_queued` :480 выбирает работу самостоятельно. Reuse допустим лишь после явного подчинения native Kanban task/run authority; название «technical journal» не доказывает отсутствие второй очереди. N-01 дополнительно требует обязательного executor privilege boundary (см. owner-action-batch); прежний transport-only scope его не разрешает.

## Исторический список bounded discovery (частично выполнен выше)

1. Прочитать ManifestValidationTests/JobStoreTests fixtures и deployment tests полностью; проверить отсутствие real SSH/Docker/GitHub вызовов без mock до запуска.
2. Найти определения CodexExecutorConfig/CodexExecutor/GitHubPublisher/JobStore и их usages.
3. Сопоставить `tools/kanban_tools.py` runtime contract с technical journal: если journal отражает runner lease/artifact только, это не автоматически вторая task queue; проверять ownership/fencing, не судить по SQLite.
4. Только после этого назначить точные implementation diffs и команды tests. Не менять существующий repo в discovery фазе.

ORCH-01 / CRITICAL открыт. Runtime heartbeat/recovery этого исторического runner не принят как контроллер текущего MVP1.

## E1 Source Discovery 2026-09-23

SOURCE_ONLY snapshot до последующего выбора repo, без runtime tests, inventory, model calls, SSH, установки или изменения config. Выполнены C01–C12 согласованного плана; тогда C13 остановлен на выборе repo/interfaces. Git-факты этого snapshot исторические; актуальный owner decision ниже. Отрицательное source finding завершает документарный вопрос, но не N-gate. Current Coverage MEM-12 SSH-02: полная история, hydration и живой reconnect остаются NOT_RUN; наличие памяти не закрывает ORCH-01 / CRITICAL.

### Source pins and scope

Пути ниже используют явные корни:

- H = `/Users/s060874gmail.com/.hermes/hermes-agent`; `git status --short` пуст, branch `main`, HEAD `5a3e03ef37462000b5b13d03915eb3e7b1633b6f`, все три команды exit 0. `pyproject.toml:3–15`: Hermes `0.21.4`, Python `>=3.11,<3.14`. Это локальный installed source, НЕ installed revision сервера.
- R = `/Users/s060874gmail.com/coding/projects/hermes-remote-migration`; status пуст, branch `feat/codex-runner`, HEAD `8cbce9554d2644c0af0333b2b065978b2fb63c4b`, три exit 0. Candidate, не выбранный implementation repo.
- P = operations workspace `/Users/s060874gmail.com/coding/projects/hermes-agent`; Git status/branch exit 128, не Git repo. Git init/commit не выполнялись.
- R `deploy/codex-runner/Dockerfile:1–21`: base image и Codex version — обязательные build ARG, точные deployed значения этим файлом не установлены; Python stdlib, apt git/openssl/python3 и npm `@openai/codex`. README:3–19 описывает три роли/volumes без host bind mounts — не выбранную E1 topology. Candidate Python package manifest не установлен discovery; новый manifest не создан.
- P `.hermes/tooling/mvp1-integration-prototype/fixtures/server/hermes_stable_updater.py`: SHA256 `ebd88a8359b4ff8aa0161bb1e00147d36db1fc5b96e63642fb2947a21d43141a`, совпал с literal EXPECTED в `test_current_updater.py:12–23`. Это сохранённый source snapshot, CURRENT_SERVER_SOURCE_UNVERIFIED.
- P `.hermes/tooling/mempalace/provider/__init__.py`: SHA256 `288cb3998dfce6c5ba3f7e4de00e25624c78f117f9b95fdb9dc9a880a82fe362`; MemPalace source HEAD `d5250c788995cbdc17a6c095345a98a997ad1728` прочитан Git, README указывает v3.9.0. Raw session DB/private spool не открывались для discovery; проектный MemPalace index обслуживается отдельно в разрешённом scope.

Public documentation реально получена HTTP 200 2026-09-23; authoritative для возможностей, не grant на выполнение примеров:

- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime
- https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin
- https://developers.openai.com/codex/cli/reference/ перенаправляет на https://learn.chatgpt.com/docs/developer-commands?surface=cli — сохранён фактический URL, latest docs не версия установленного server binary.
- https://github.com/tmux/tmux/wiki/Getting-Started

### Native launch and task authority

| Task / вопрос | Definition/schema → caller → test или unresolved | SOURCE_ONLY finding / следующий gate |
|---|---|---|
| 1.2.1 / Codex exec launch | H `skills/autonomous-ai-agents/codex/SKILL.md:16,43–67` → H `tools/terminal_tool.py:1351–1398` schema → `_handle_terminal:1401–1468` → `terminal_tool:1224`; product-boundary test ещё не найден | Штатный skill с terminal recipe, не отдельный typed Codex-exec tool. Content search всех `tools/*.py`, затем `agent/*.py` и `hermes_cli/*.py` не дал такого tool schema; это ограниченный поиск, не утверждение об отсутствии всех native integrations. Pinned CLI argv/OAuth-client sandbox на server UNVERIFIED. |
| 1.2.1 / delegate_task | H `tools/delegate_tool.py:634–714` schema → registry :737 → `delegate_task:440`, `_build_child_agent:156–249` → `AIAgent`; docs delegation | Это Hermes child agent, не сам по себе Codex CLI. Child создан с `skip_memory=True`; общий provider не доказывает его hydration. Выбор child runtime — trusted config, не модельное имя поля. Прямые модельные overrides не придумывать. |
| 1.2.1 / native app-server alternative | H `agent/conversation_loop.py:1522` → `agent/codex_runtime.py:502–563,625–663` → `agent/transports/codex_app_server_session.py:208–307`, `thread/start` / `thread/resume`; test H `tests/agent/test_codex_app_server_thread_resume.py:62–95` | Native opt-in runtime действительно существует: заменяет Hermes tool loop, не равен отдельному Codex exec и не ordinary SSH attach. Не включён. Тест содержит mock wire/client, не выполнен здесь. |
| N-05/N-10 / app-server prerequisite | H `agent/codex_runtime.py:629–634`, `agent/agent_init.py:322` → H `tests/agent/test_pre_compress_checkpoint_contract.py:457–475`; memory-provider docs | `compression.checkpoint_required=True` с `codex_app_server` отвергается: нет truthful pre-compaction transcript boundary. Нельзя выключать обязательный checkpoint ради green. Требуется архитектурное решение после проверки native exec path, не silent substitution. |
| N-01 / exact approval | H `tools/approval.py:1095–1120` общий human gate; `resolve_gateway_approval:138–172` → H `gateway/slash_commands.py:1179–1216`; H `tests/tools/test_request_tool_approval.py` найден поиском, suite NOT_RUN | Request ID/FIFO, once/session/always и in-memory queues присутствуют. Slash caller не передаёт exact revision/action binding. End-to-end Telegram owner identity/restart/broad approval constraints UNVERIFIED; необходим deeper actual adapter trace и отдельный canary. Нет новой approval queue. |
| N-02 / task-run authority | H `hermes_cli/kanban_db.py:2263–2295` claim → H `hermes_cli/kanban_db_dispatch.py:2818–2859` pins task/run/board/workspace → H `tools/kanban_tools.py:185–259` worker guard | Source проверяет own task, run identity и delegated-child mutation boundary. Полный cancel/replay/database CAS и server-side tests не выполнены; source snippets не доказывают OS boundary против forged env. R JobStore не становится authority. |

Обнаружен version-sensitive конфликт recipe/schema: Codex skill :44 показывает foreground `pty=true`, но H `terminal_tool.py:1429–1434` отвергает PTY без background. Для будущего launch опираться на actual pinned schema/help, не копировать recipe. Рекомендация skill :89–97 про `danger-full-access` также не является удовлетворением ENV-01/credential boundary и не применяется.

### Candidate reuse, not deployment

| Seam | Exact source → caller → test | Решение / blocker |
|---|---|---|
| Fixed argv/cwd/process error | R `scripts/codex_runner.py:785–829,979–1057,1102–1147` → `CodexExecutor.run_next:871` → `deploy/codex-runner/app/runner_service.py:64–80`; tests `tests/test_codex_runner.py:734–829` | Можно рассматривать узкий повторный use validation/error patterns. Prompt передан argv, stdin=DEVNULL; это НЕ готовый fixed-stdin adapter. Nonzero/timeout имеют error codes, но exit 0 в :1105 даёт SUCCEEDED без проверки семантики JSONL. `_join_readers:1164` и kill wait не bounded; detached-descendant/cgroup contract не доказан. |
| Полная история/WIP | R `scripts/codex_runner.py:832–855,931–935,1017–1029` → `_run_codex:1032`; argv test :777–806 закрепляет `--ephemeral` | `--ephemeral` отключает session rollout persistence по official CLI reference. Bounded writer обрезает байты; прежний job workspace удаляется перед clone. В таком виде runner противоречит MEM-12/reusable worktrees; нельзя принять logs/hash за полный архив. |
| Authority / technical journal | R `scripts/codex_runner.py:480–515` → `CodexExecutor.run_next:871–875` → service polling :76–80; `tests/test_codex_runner.py:847` atomic-claim test | Собственный queued selector. Stable Kanban ID в manifest не доказательство native run fencing. Не разворачивать scheduler; возможна только отдельно спроектированная subordinate seam после native authority checks. |
| Publisher | R `scripts/codex_runner.py:1294–1411` → service `run_publisher:112–137`; tests `tests/test_codex_runner.py:1258–1360` setup/mock helpers | GitHub App, fixed repo, trusted publishing workspace и automatic polling отличаются от текущего publisher CLI contract. E2; не подключать и не выдавать credentials. |
| Container / updater | R Dockerfile:1–21, README:8–19/49–60; `tests/test_codex_runner_deployment.py:40–259` | Три роли/named volumes, отдельный runner updater; это не один E1 container с approved server bind mount и не изменение existing Hermes updater. UID 10001 из candidate НЕ выбранный server UID. |

1.5.1: source definitions/callers/test locations и Git проверены; reuse blocker установлен. Tests прочитаны статически, не запускались. AST inventory: `tests/test_codex_runner.py` — 63 test methods; deployment — 14. Эти числа не passed counts. Executor helper :764–775 mocks run/Popen, publisher setup :1258–1328 использует temp workspace/fake HTTP; deployment `load_preflight:18` / `load_updater:29` выполняют импорты. Broad suite нельзя считать side-effect-free по названию: controller использует HTTP/socket, fixtures создают SQLite/файлы, production module имеет Git/network/process paths. Markdown search не обнаружил documented unittest invocation; framework `unittest` подтверждён imports/entrypoint. Run authorization и полный transitive fixture audit отсутствуют — BLOCKED_TEST_COMMAND для предлагаемого product apply, не фиктивный runnable TDD.

### Hermes history and hydration

В таблицах lifecycle короткие `memory_manager.py`, `memory_provider.py`, `session_persistence.py`, `conversation_compression.py`, `turn_context.py`, `turn_tool_round.py`, `codex_runtime.py` относятся к `H/agent/`; `provider` — `P/.hermes/tooling/mempalace/provider/__init__.py`, `test_autosave.py` — `P/.hermes/tooling/mempalace/test_autosave.py`. Это source references, не runtime state files.

| Event | Persist hook / caller | Crash boundary / hydration | Evidence / limit |
|---|---|---|---|
| User/assistant completed turn | H `run_agent.py:912–943` → `memory_manager.py:533–557` → P provider `sync_turn:133–138` → `_save:69–94` | Host sync async/best-effort; provider fsync выполняется внутри worker после очереди. Crash до callback не покрыт spool. | P `test_autosave.py:25–39`; source-only, NOT_RUN. Доставленный turn ≠ гарантированно завершённый autosave. |
| Tool call | H `agent/turn_tool_round.py:96–134` → `session_persistence.py:388–417` / `_db_flush_write:258` → SessionDB batch | Native tool intent сохраняется до tool side effects, false flush блокирует эту ветку. P provider `evidence:21–38` не переносит tool_calls metadata. | Native source присутствует; project-attributed durable full export и crash tests UNVERIFIED. |
| Tool result | Hermes messages/SessionDB persistence seam, H `turn_tool_round.py:188–205` / `session_persistence.py`; P `evidence:25` отбрасывает role=tool | Точная транзакционная граница каждого результата и всей цепочки side effect → persist требует отдельного trace/test. | P `test_autosave.py:13–23` явно исключает tool role; MemPalace spool не полный event store. |
| Interrupted/crash | H `run_agent.py:925` пропускает external sync; SessionDB сохраняет уже committed rows | Не гарантируется каждый streaming token или незавершённый event. README provider:16–17 не доказывает отсутствие потерь до commit. | Full MEM-12 incomplete-attempt attribution и write-failure policy UNVERIFIED. |
| Pre-compression | H `conversation_compression.py:2916–2953` → `memory_manager.py:727–762` → P `on_pre_compress:144–147` | v2 checkpoint exception блокирует compression; сохраняется только filtered subset provider. DB lineage ≠ checked full original history archive. | P `test_autosave.py:49–58`, source only. Не выключать existing checkpoint gate. |
| Restart/new-session current context | H `turn_context.py:853–881` → `memory_manager.prefetch_all:447` → base `memory_provider.py:120–123` | P provider не overrides prefetch; startup `_schedule` только re-indexes spool. Предусмотренный hook ≠ автоматическая загрузка project context этим provider. Prefetch errors suppress в caller, что не доказывает MEM-12 fail-closed. | Separate project-bound hydration adapter/acceptance BLOCKED; manual MCP search не его замена. |

H `hermes_state.py:1–5,63,73` подтверждает SQLite/WAL/messages/compression lineage source seams, но БД и raw transcripts не читались. Проверка durability при kill, session lineage export, writer attribution/redaction/ACL и отказе storage остаётся отдельным разрешённым runtime scope. Нельзя копировать целиком credential-bearing home в project history folder.

### Codex history and hydration

| Event | Available source/interface | Persist/crash/hydration boundary | Status / next exact check |
|---|---|---|---|
| User/assistant turn | Official CLI `exec --json`, persisted rollout без `--ephemeral`; H app-server `codex_runtime.py:566–597,625–663` | Native projected messages flushed после turn; binding thread ID записывается после успешного flush. Не standalone CLI adapter. | SOURCE_ONLY interface; actual pinned CLI rollout schema/flush semantics UNVERIFIED. |
| Tool call/result | App-server docs описывают completed commandExecution/fileChange/mcpToolCall/dynamicToolCall projection; H `_persist_projected_messages` | Completion projection не raw event archive. P autosave снова отфильтрует tool data. | Full event export/sequence/dedup/crash completeness UNVERIFIED; сохранить прямые originals, не только projection. |
| Interrupted/crash | H `codex_runtime.py:612–616` не sync interrupted/error turn; :594–596 warning при persistence failure | User уже мог увидеть output до failed flush; NOT fail-closed MEM-12 acceptance. R bounded JSONL не гарантирует originals. | Fault fixture и project attribution требуются; ни один fault здесь не запускался. |
| Compression | H `codex_runtime.py:629–634`, checkpoint test :457–475 | App-server authoritative compaction не даёт required pre-compaction boundary. | BLOCKED_CHECKPOINT_COMPATIBILITY, не выключать gate. |
| Resume old session | Official `codex resume <id>` / `codex exec resume <id>`; H `CodexAppServerSession:258–307`, stored thread ID | Saved conversational identity, не продолжение старого PID. Unresumable thread в H создаёт новый с notice. | SOURCE_ONLY; exact identity/project filtering и new-attempt attribution runtime UNVERIFIED. Не использовать глобальный `--last/--all` как identity mapping. |
| Hydrate fresh context | H `_ensure_codex_session:502–563` → `agent/codex_runtime_history_seed.py:19–65` | Seed только текущей Hermes session, latest 32,000 chars / tool previews 400 chars; resume не пересылает seed. Это производный prompt, не удаление оригиналов и не весь актуальный проект. | Native helper пригоден для дальнейшего изучения, но standalone manual CLI/project hydration BLOCKED. |

Installed standalone Codex version/Rust source pin в этом bounded scope не установлен: Cargo.toml search в P native-codex research и R дал 0. Это BLOCKED_INSTALLED_SOURCE, НЕ утверждение, что Codex не установлен. Download/source checkout/help/login не выполнялись. `native-environment-evidence.md`, `native-bootstrap-evidence.md`, `linux-model-lifecycle-preparation.md` остаются историческими; broken stock lifecycle test не исправлялся и не запускался. Следующий source scope: получить approved exact CLI version/source/rollout contract без private sessions; затем согласовать synthetic durability/hydration fault fixture.

### Updater and session admission

1.3.2: сохранён daily automatic stable-update policy; никакой server write. P fixture :1452–1472 держит maintenance flock вокруг `_apply_locked`; :1485 делает recovery; :1535–1545 внутри launcher lock проверяет writer, объявляет disruption, останавливает gateway, требует zero writers, затем snapshot. `snapshot:864–884` повторно проверяет writers и задаёт 700/600. Известный nesting edge: maintenance lock → launcher lock в показанном apply path; это НЕ полный глобальный lock order.

В inspected apply path нет учёта ordinary SSH/manual/detached Codex sessions проекта. Не доказано, что существующий gateway writer check видит такие сессии. Unknown edges: task admission ↔ manual-session lease ↔ project worktree writer ↔ cleanup/history flush ↔ updater/backup. Нельзя назначать порядок без actual server/source trace и race tests. Candidate runner updater drain своей SQLite очереди эту границу не закрывает. CURRENT_SERVER_SOURCE_UNVERIFIED: fixture hash совпал, но последний server inventory исторический. Next check требует отдельного read-only SSH scope; любые изменения updater — затем exact diff/approval, с сохранением stop→consistent snapshot, auth checks/rollback и защит от удаления используемых ресурсов.

### Storage and worktree decision boundary

1.5.2: логический владелец project folder — владелец проекта; назначение Linux service identity/UID/GID, ACL и права provisioning требуют его infrastructure approval. Фактическая папка на ainetic.tech НЕ выбрана. Таблица — требуемая классификация данных, а не готовые mounts.

| Data class | Writer/owner | Persistence / reader scope | Credential exclusion / unresolved |
|---|---|---|---|
| Git object store + branches | Trusted project provisioning; writers через отдельные worktrees | Один approved project folder, история Git переживает recreate; доступ только project identity | Не размещать credentials/Git helpers в worker-visible data; actual path/ACL BLOCKED |
| Worktrees и uncommitted WIP | Один manual/automatic writer на worktree/branch | Persist вместе с repo metadata; no cleanup пока есть live/detached/reference lease | Worktree не OS sandbox; direct shared Git metadata mutations/integration требуют отдельной сериализации |
| OpenSpec/project rules | Owner-approved shared baseline + project-scoped writers | Версионированные project docs, same revision видна обоим harness | Shared global rules не writable project dependency layer |
| Full Hermes history | Trusted recorder, session/attempt/project attribution | Private durable originals отдельно от rebuildable index; authorised same-project readers | Secret exclusion/redaction policy, complete export/commit boundary/retention BLOCKED |
| Full Codex history, automatic/manual | Trusted recorder, разные session IDs | Durable raw history/tool events + context packet references; no `--ephemeral`-only archive | CODEX_HOME содержит не только историю; общий writable credential home не выбран |
| Test reports, logs, artifacts | Scoped job writers / trusted verification | Persist raw results с revision/run linkage, reader allowed by project | Логи могут содержать secrets; log truncation не заменяет original history contract |
| Dependencies/skills/cache | Project identity только в своём container/layer | Только project-local writes; shared versions отдельным approval | Host packages/base image/shared tools не изменять автономно |

Recreate восстанавливает данные/контекст, не прежний процесс. Actual bind options, owner UID/GID, disk/resource quotas, backup interaction и sibling access — BLOCKED_SERVER_INVENTORY. Конкретные цифры из старого snapshot и UID из candidate нельзя превращать в reservation/config.

### Ordinary SSH continuity candidate

1.5.3: tmux — SOURCE_ONLY кандидат для живого ordinary terminal, не выбранный/установленный компонент. Official Getting Started подтверждает detach/reattach программ при живом tmux server. Codex resume решает recovery сохранённого диалога, а не тот же PID. App-server mode не подменяет manual ordinary CLI.

| Boundary | Source / unknown | Будущий наблюдаемый acceptance |
|---|---|---|
| SSH disconnect/reconnect, container жив | tmux official docs; actual binary/session registry/test paths BLOCKED_PATH_DISCOVERY | Возвращается тот же живой Codex process/session/worktree, duplicate не создаётся |
| Codex process death | Codex documented resume, live-process continuity отсутствует | Явный новый attempt/process ID с сохранённой историей; не ложный «всё продолжалось» |
| Container destruction/recreate | Storage requirements выше, not runtime evidence | Данные/context доступны; прежний PID не обещан; отказ при missing history |
| Wrong project/identity | Actual SSH authorization/container selector не обследованы | Deny до чтения private history/attach; socket path/name не считается ACL |
| Multiple manual/automatic writers | Independent identities + worktree contract, implementation unknown | Нет общей writable worktree; deliberate integration с повторными tests |
| Updater/drain/cleanup | Fixture не покрывает manual sessions | Новая admission не пересекает maintenance; detached sessions остаются tracked; defer/drain безопасен |

Next check: после owner choice и отдельного server inventory получить installed tmux/Codex version/source, existing container entrypoint/session routing и actual test paths. Не добавлены guessed scripts и SSH shortcuts.

### Extension compatibility

1.5.4: source existence отдельно от loading/use. Source pins: OpenSpec `1.13.0` из P `.hermes/tooling/openspec/package.json:7`; generated skill metadata :10 = 1.13.0. SHA256 Hermes skill `c46c348c91cba294474e8ea9121976ccd38a476a435284e12d4017c22d425b0c`, Codex skill `fc957752fd96975165c3b21ebdb705d8617128039c092ffa853e276b36089b35`; разные adapters, не предполагать побайтовую идентичность. MemPalace/provider pins выше. P `AGENTS.md` SHA256 `00752daf4f84687625ef21227931d6af8f208dfb7454a5ce702934f4f4e4618d`, protected OpenSpec block всё ещё отсутствует.

| Shared artifact | Hermes source/loading adapter | Codex source/loading adapter | Actual use / project-only boundary |
|---|---|---|---|
| OpenSpec | P `run-openspec`, `.hermes/skills/openspec-explore/SKILL.md` | P `.agents/skills/openspec-explore/SKILL.md`, same CLI contract | Local CLI context/validate фактически выполнены; agent skill auto-loading и server use для обоих UNVERIFIED. Не копировать slash/tool names между harness |
| MemPalace | P `run-mempalace`, MCP и default provider source; provider README:26–34 | MCP — потенциальный совместимый interface; P README:72 говорит Codex hooks не подключены | Local scoped CLI search/mine — отдельные receipts; server automatic Codex/Hermes lifecycle UNVERIFIED. Project index ACL и trusted originals обязательны |
| Skills/tools | P generated Hermes skills и H native codex skill, trusted-config runtime adapters | Generated Codex skill exists; H app-server docs описывают отдельные plugins/MCP, не shared tool parity | Installed file ≠ loaded/use. Project dependency/skill install не может переписать global skill/base image/version |
| Rules/AGENTS | P AGENTS/WORKFLOW — advisory prompt conventions; H dispatcher pins TERMINAL_CWD | Codex project rule-loading на target не проверен; shared approved text требует своего adapter | OS permissions/fencing не заменяются Markdown. Protected C.17 требует отдельного grant; project rules не дают права менять host/shared tools |

### Decision packet and C13 stop gate

Пункт 1 обновлён по последующему решению владельца; остальные рекомендации не приняты автоматически:

1. Implementation repo: владелец выбрал P `hermes-agent`, а не предложенный R `hermes-remote-migration`. P теперь локальный Git repo для operations/docs и будущей integration; R — только selective source/test donor. Upstream H не редактировать, вторую очередь не создавать. Это принятое repo decision, не runtime architecture approval.
2. Native route: сначала проверять terminal-backed Codex exec в рамках native Kanban authority, поскольку это соответствует текущему contract. App-server сохранить как альтернативу с явным checkpoint/semantics blocker; его выбор потребовал бы отдельной revision, не молчаливой замены. tmux — proposed manual continuity candidate, не доказанная credential isolation.
3. Следующий отдельный read-only server scope: только версии/source identity, allowlisted metadata existing containers/mount destinations/UID/resources, non-secret updater/launcher/session-manager sources. Не full inspect/env/config, не credentials/private history, не auth/model/inventory/deploy. Exact команды и grants подготовить отдельно до SSH; этот пакет SSH не разрешает.
4. После получения actual server/source facts: согласовать credential-safe full history/hydration seams, manual session identity/leases и updater lock/admission graph в выбранном P repo. Затем runnable TDD packet первого code parent с exact paths, meaningful RED/GREEN/regression, а canary/model/credential/config changes — отдельными grants. Shared tools/base image/permissions требуют approval; daily updater не ослабляется.

C13 / task 1.5.5 остаётся BLOCKED_PATH_DISCOVERY: repo decision получен, но нет принятого launch/credential boundary, server layout и safe runnable product test command. Placeholder tests/implementation paths не созданы. Read-only children 1.2.1, 1.3.1, 1.3.2, 1.5.1–1.5.4 документированы с отрицательными результатами/unknowns; все production parents остаются открытыми. E1 environment НЕ реализована и НЕ принята; E2 и ORCH-01 / CRITICAL открыты.

## Repository decision 2026-09-23

REPO-HERMES-AGENT-2026-09-23. Владелец: «Мне кажется есть смысл использовать репозиторий hermes-agent, если его нет, создай, а из hermes-remote-migration возьми все что тебе необходимо для реализации дальнейших шагов».

Принято: implementation repository — P `/Users/s060874gmail.com/coding/projects/hermes-agent`. До действия Git exit 128 и `.git` отсутствовал; выполнен `git init --initial-branch=main --template= .`, exit 0. Readback: точный worktree root P, symbolic HEAD `main`, HEAD commit отсутствует, index пуст, remotes отсутствуют. Шаблоны hooks не импортировались. Это локальное создание, не создание GitHub repo, не fork установленного H и не merge истории R. AGENTS.md не изменён; его прежняя фраза об отсутствии Git — dated baseline. Никаких commit/add/push/network/server/runtime действий в bootstrap.

Root README описывает новую ownership boundary; `.gitignore` допускает существующие scripts, OpenSpec/tasks и project skill adapters, но по умолчанию исключает новые root paths. Credentials/env, private state, raw history, caches, installed tooling, research/plans и council transcripts не добавляются в Git. Исходные локальные файлы не удалялись; links на ignored evidence по-прежнему локальные, не обещание reproducible fresh clone. До первого commit — отдельное разрешение и content review; ignore не secret scanner и не sandbox. Parallel Git worktrees/candidate commits ещё требуют initial reviewed commit.

### Selective donor reuse

R повторно проверен: clean `feat/codex-runner`, HEAD `8cbce9554d2644c0af0333b2b065978b2fb63c4b`. Никакой код R не копируется без нужного implementation slice, не становится imported runtime dependency и не запускается. Сейчас в P перенесены source-backed reuse decisions и следующие regression obligations, а не whole runner:

| Source в R | Берём для следующих slices в P | Не переносим автоматически |
|---|---|---|
| `scripts/codex_runner.py:185–252`; `tests/test_codex_runner.py:56–192` | Closed-input validation и negative cases: unknown `command/environment/oauth/model/routing/api_key`, malformed SHA, absolute/traversal/noncanonical paths, schema/runtime parity | Hardcoded repository/draft_pr, исходный manifest как продуктовый API, string-path checks как OS boundary |
| `scripts/codex_runner.py:785–829,979–1151`; `tests/test_codex_runner.py:734–1240` | Fixed argv/cwd/process-error patterns и mock fixtures для будущих безопасных exec tests после full side-effect review | `--ephemeral`, prompt argv вместо required stdin, обрезка originals, удаление project WIP, unbounded joins, exit 0 как semantic success |
| `tests/test_codex_runner_deployment.py`; `deploy/codex-runner/Dockerfile`, `README.md`, `app/runner_service.py` | Comparison/negative requirements по role/volume/process boundaries; источник ограничений, не готовый deploy | Own JobStore selector/controller polling, GitHub App publisher, отдельный updater, три роли как E1 topology, фиксированный UID |

Source SHA256 для reproducible последующего отбора, вычислены без imports/runtime execution:

- `scripts/codex_runner.py`: `d405bd7dd7bd26e97623b71ee2a2526e2104cb1ee5e6c1cfa1fee6f9cdf05e4b`.
- `tests/test_codex_runner.py`: `215753a0f9aa4fb844f18edd253a03ccb7383894bc39e26974ccc931272bd330`.
- `tests/test_codex_runner_deployment.py`: `68b60a02bae68e8c5d7fe441177307613029176404f8d68eaba1725240ffcb85`.
- `deploy/codex-runner/app/runner_service.py`: `f1f22b56302eba61824caa0600c4cb83fa498951e61de4f3bc8de264fd88aba5`.
- `deploy/codex-runner/Dockerfile`: `c6a611f1272ac88dd3365309f523e78fae73dbda6e05cb095df9d153c78bc545`.
- `deploy/codex-runner/README.md`: `fe326f037e79045b7677bf93e1d9f8af6a2323dbcb3ef8510c1810053c07c4ab`.

Repository guard проверен настоящим `git check-ignore --no-index --stdin` с `core.excludesFile=/dev/null`: до `.gitignore` EXPECTED_RED — 5 synthetic sensitive path probes не защищены; после — GREEN, 18 denied / 15 admitted. Probe files не создавались, credentials не читались. Это проверка Git admission patterns, не runtime security tests и не content secret audit.

Закрыта только repo-choice часть N-08/1.5. Task 1.5/1.5.5 остаются открытыми; exact product approval pending/owner_approved=false, implementation_ready=false. Следующий scope — bounded server/source inspection packet до SSH и затем runnable TDD. ORCH-01 / CRITICAL не реализован.

Bootstrap documentary validation: `./run-openspec validate --all --strict --json` exit 0, 3 passed / 0 failed; apply progress adoption 25/26, product 7/44, seed 22/22 (unchanged). Existing V-PRESERVE exit 0: 36 protected fixed files, исторические prefixes/receipts и полные task criteria сохранены. Local link/heading checker проверил 143 links / 42 anchors в 13 документах, exit 0; это working-tree, не fresh-clone portability. Matrix N-08 изменена, поэтому current digest пересчитан в review-status/current coverage; прежние hash receipts не переписаны. Scoped memory refresh только tasks/openspec, с exact-source readback после записи.

## Server Read-only Survey 2026-09-23

SERVER-E1-SURVEY-2026-09-23. Владелец ответил «действуй» на предложение ограниченного read-only обследования `ainetic.tech`. Scope выполнен: host/container metadata, public application source/AST/hash, updater/launcher source, directory metadata без чтения содержимого data/history/credentials. Использовались короткоживущие Python probes через SSH stdin и `docker exec -i` в existing gateway; это реальные серверные процессы, но не запуск Hermes/Codex/model/task. Никаких install, container create/restart/remove, записей server config/source, auth checks или чтения `.env`/`auth.json`/tenant manifest/private history. Не заявляется отсутствие системных SSH audit logs или иных обычных следов выполнения.

Все SSH вызовы: `BatchMode=yes`, `StrictHostKeyChecking=yes`, `UpdateHostKeys=no`, `ConnectTimeout=15`, `ConnectionAttempts=1`, `ForwardAgent=no`, `ClearAllForwardings=yes`, `RequestTTY=no`, `ControlMaster=no`, `ControlPath=none`. Public docs Hermes/Codex/tmux использовались как справка, не заменяли installed source. Внутри gateway `git rev-parse HEAD` дал exit 128: `.git` отсутствует; commit не выдумывается, identity фиксируется image digest и file hashes.

### Actual host and gateway

Последний metadata readback: 2026-09-23, local clock 18:45 MSK; значения RAM/disk — моментальный sample, не обещание доступного project budget.

| Объект | Actual result | Ограничение |
|---|---|---|
| Host | `ainetic-tech`, Linux `5.15.0-185-generic`, x86_64, 2 CPUs, RAM 5921 MiB / available 3946 MiB, swap 1958 MiB | Не выдавать весь host за E1 allocation; сторонние сервисы не трогать |
| Disk / runtime | `/` 79G, available 38G, 50%; Docker `28.5.1` build `e180ab8`, cgroup v2/systemd; Python host `3.10.12` | Quota/inode/IO budget проекта не согласован |
| Gateway | `hermes-agent-hermes-gateway-1`, running; ID `a1240331bb689cabc438bd9937a87e496fd38e4f338196e0de34e79a4487b2b4`; started `2026-09-21T23:10:24.034208108Z` | Existing gateway, не E1 project container |
| Image | `nousresearch/hermes-agent:v2026.9.11@sha256:930b5b8ebfed43857c3a993f437f0e3a1bffc045c5b241794b35bf102298bdb2`; local image ID `sha256:3d1c312980e7d400ebf1fabca40f855a6ff16cab11e80930a9b3d4d3c920ef5e` | Manifest/image/config digest — разные identities |
| Application | `/opt/hermes/pyproject.toml` declares `0.21.2`, Python `3.13.5`; local H source ранее `0.21.4` | Manifest version, не выполненный `hermes --version`; source drift подтверждён |
| Gateway limits | UID/GID `0:0`, user `root`, memory `1610612736` bytes, NanoCpus `1000000000`, PidsLimit `512`, privileged=false, no-new-privileges=true; rootfs writable, CapDrop=null | Не security template для project code и не project admission budget |
| Mounts RW | `/srv/hermes-agent/work` → `/workspace`; `/srv/hermes-agent/data` → `/opt/data`; `/opt/ainetic-stack/local-files/hermes` → `/files` | `/opt/data` нельзя отдавать project worker как обычный shared home |
| Host directory metadata | work и files: `1000:1000`, `2770`; data: `1000:1000`, `700`; `/srv/hermes-agent` и bin: `0:0`, `750` | Только lstat, содержимое data не читалось; будущий project root/ACL не выбраны |
| Tool discovery | `codex` и `tmux` не найдены PATH host и gateway; проверенные global npm Codex package paths отсутствуют | Не утверждение об отсутствии установки во всём filesystem; auth status НЕ проверялся |
| Kernel prerequisites | cgroup controllers включают cpu/memory/pids; `max_user_namespaces=23221`, `unprivileged_userns_clone=1` | Не behavioural proof userns/cgroup isolation внутри будущего worker |

### Source pins and interface findings

| Exact source | SHA256 | Finding |
|---|---|---|
| `/usr/local/bin/hermes-run` | `4121e34313bb7adfb0f7bc89ba2cfe4bddbe0bc0e1a144dddc455bafefc224a3` | Regular file, `0:0`, `755`; source references `/usr/local/lib/hermes-launcher.py` |
| `/usr/local/lib/hermes-launcher.py` | `85326d70567574f1893a580aa9c095d1c3e214399b991d027597d137571f2d55` | `docker_base:170–241` строит `docker run --rm -i`, project/state mounts; `handle_request:299–366` вызывает его для CLI/shell; это per-invocation container, не ENV-01 reuse. Просмотрен source, launcher не вызывался |
| `/srv/hermes-agent/bin/hermes_stable_updater.py` | `ebd88a8359b4ff8aa0161bb1e00147d36db1fc5b96e63642fb2947a21d43141a` | Совпал с P fixture. Existing maintenance→launcher lock / stop→zero-writers→snapshot protection сохраняется; full manual/project writer admission не доказан |
| `/opt/hermes/plugins/platforms/telegram/adapter.py` | `78003266dc0a6beba7aaa69f6cf41391891ceccd0fd1374c8c29f0cd09f823d0` | Найден настоящий Telegram adapter. `_is_callback_user_authorized:746–781` → `_claim_callback_state:4271–4278` → `_handle_exec_approval_callback:4280–4323` → `resolve_gateway_approval(session_key, choice)`; `send_exec_approval:3802–3825` предлагает once/session/always по flags. Exact revision/owner-only product gate и restart/FIFO поведение этим не доказаны |
| `/opt/hermes/tools/approval.py` | `e48f1909968b253907fca01e9dad0593bee7a2bf7cf5278470c6d15a5150359f` | `resolve_gateway_approval:137–169`, `request_tool_approval:930–955` — source present, не принятие generic enforcement |
| `/opt/hermes/tools/terminal_tool.py` | `5ca8d06f9cc42f8f8672d76bca5efcc4c523a24244a345529a76e2b3c5c4cbb7` | `terminal_tool:1170–1241`, `_handle_terminal:1302–1354`; local line numbers/schema не переносить автоматически |
| `/opt/hermes/hermes_cli/kanban_db.py` | `d5823545140bfcfaa76f0a9ff677cdc62e705ac40f5dfa3b7d55fe149fc91709` | `claim_task:2130–2162`; native authority остаётся исходной, отдельный selector не добавляется |
| `/opt/hermes/agent/codex_runtime.py` | `c9867df36eedc3fafd40e5ce5a88a3ef31b959f2304758e42840bdb5771ec742` | `_ensure_codex_session:382–410`, `run_codex_app_server_turn:470–504`; required checkpoint конфликтует с app-server и на server source. Не ordinary CLI и не shortcut для MEM-12 |
| `/opt/hermes/agent/memory_manager.py` | `f9dd2a85dc4121687cea5c46e1956fab92565125cf853a57e9e581ecb548f2dd` | `prefetch_all:394–402`, `sync_all:480–504`, `on_pre_compress:674–709`; это hooks, не доказательство установленного server provider/full archive |
| `/opt/hermes/agent/session_persistence.py` | `83ee5c9f48a7790deb3f771e45990180e1fd714c7b1fabc24303944f17773a1b` | `_db_flush_write:212–222`; actual event/ACL/crash integration обоих harness остаётся открытой |

`/opt/hermes/agent/codex_runtime_history_seed.py` не существует на server при отдельном exists/symlink check; локальный history-seed seam нельзя предполагать здесь. Это отрицательное finding конкретного path, не отсутствие любой истории. В launcher Python source не найдены inspected lock/flock/tmux/Codex/manual-session registry seams; полный graph всех wrappers/services не доказан. Следовательно нельзя объявить updater coordinated с detached manual writers. Timer `hermes-stable-update.timer` loaded/active; last trigger `2026-09-23 01:55:02 UTC`, next `2026-09-23 23:00:00 UTC`. Это schedule, не receipt успешного обновления; policy не менялась.

### Executed local checks

Из P, системным Python `3.13.3`, без dependency installation и без product/server effects выполнены:

```sh
python3 -B -m unittest discover -s .hermes/tooling/mvp1-integration-prototype -p test_current_updater.py -v
python3 -B -m unittest discover -s .hermes/research/telegram-hermes-codex/native-codex -p test_guest_namespace_plan.py -v
python3 -B -m unittest discover -s .hermes/research/telegram-hermes-codex/native-codex -p test_environment_gate.py -v
```

Actual: соответственно 4 / 4 / 14 tests, каждый command exit 0, OK. Первый проверяет pinned updater source order/guard/quarantine и synthetic credential rollback; второй — pure namespace argv plan; третий — admission state machine с fake client. Это focused existing regression checks, не новый RED/GREEN cycle, не полный suite и не server canary. Ни один production task/N-gate ими не закрыт; Codex history/reconnect/model/Telegram effects НЕ запускались.

### Next bounded decision plan

Это следующий предложенный пакет, НЕ исполнимый deployment/TDD и не новая очередь. Task 1.5.5 остаётся BLOCKED_PATH_DISCOVERY по своему явному negative outcome; task criteria/checkbox не меняются. Read-only inventory завершён, повторное общее разрешение на него не требуется. Для code parent не выданы придуманные imports/commands или placeholder tests.

1. В существующих `design.md` / `implementation-readiness.md` уточнить native CLI client/credential boundary с pinned target version, исходя из actual server 0.21.2; ordinary exec/manual CLI не заменять app-server. Проектный code не получает credential home; silent local fallback запрещён. Если native seam не найден — назвать blocker, а не писать обходной runner.
2. Там же зафиксировать proposed persistent host layout, project UID/ACL/history/worktrees и численный resource budget с учётом 2 CPUs/5921 MiB host. Существующий per-invocation launcher не считать reusable; перенос donor queue/updater/ephemeral lifecycle запрещён. Эти предложения ещё не меняют server paths/permissions.
3. Согласовать отдельную manual identity/detach candidate и полный admission/drain/defer graph с existing daily updater. Не ослаблять locks/backup/auth/rollback protections; SSH disconnect и смерть process/container — разные acceptance cases.
4. После решения предыдущих пунктов и exact scoped approval оформить первый code parent в существующем `tasks.md`: 2–5-минутные RED → minimal implementation → GREEN/regression children, discovered paths/commands и negative controls. Local implementation — в P, server install/canary — отдельным exact grant; начальный commit/worktrees не выполнять без отдельного разрешения.

Self-review одного контекста, не независимый консилиум. Source facts не требуют голосования; нерешённый architecture/client boundary может потребовать отдельного bounded council, но его запуск здесь не выдуман. ORCH-01 / CRITICAL не реализован: MemPalace не мониторит и не перезапускает агентов. E1 NOT_READY, product approval pending, `owner_approved=false`, `implementation_ready=false`.

## Local Design Packet 2026-09-28

E1-LOCAL-PACKET-2026-09-28. По «Продолжай» подготовлен [локальный proposed packet](../../../.hermes/plans/2026-09-28_e1-local-design-and-first-tdd.md): source-backed candidates для CLI, storage/budget, SSH/updater и первый независимый data-only TDD slice. Это файл предложения per-artifact update по WORKFLOW §5, не применённая новая spec/design revision. Нормативные proposal/design/matrix/specs/tasks и digest не менялись; task 1.5.5 и parent 3.1 остаются open. Новые `scripts/project_environment.py` и `tests/test_project_environment.py` только предложены, не созданы; future test command не запускался.

- Fixed candidate Codex `rust-v0.153.4`, release/tag source commit `3d2ee51ca2d5db578f328aa75e20aa22c0197c9a`. Для server x86_64 проверена metadata именно CLI package, не historical aarch64/app-server-only bundle. Binary не скачан/не установлен; это не claim latest или runtime compatibility с Hermes 0.21.2. tmux `3.7c` также только release candidate для будущего image.
- Source tracing различает exec и TUI bootstrap: exec `--ignore-user-config` меняет способ загрузки EnvironmentManager; TUI `startup_orchestration.rs:200–207` имеет отдельную ветку. Native arg0 загружает dotenv до CLI main. `include_local` по умолчанию true, непустой remote URL и controller-owned environments.toml — разные конфигурационные пути. Это не доказательство credentials/all-tool isolation. Runtime client boundary остаётся BLOCKED; ordinary manual CLI не заменён Hermes app-server mode.
- Updater source: maintenance EX|NB, затем launcher-image blocking EX. Держать shared launcher lock всю manual session означало бы unbounded updater wait, не bounded drain/defer. Предложенный protocol требует собственного точного scoped diff/проверки всех entry points и отдельного server approval; current updater/timer не менялись. Filesystem quota/UID/ACL и full-history hooks не объявлены найденными.
- Resource values/path names в packet — предложения по dated survey от 23 сентября, не fresh host state и не выделенные ресурсы. SSH/Docker/client/model calls в этом пакете не выполнялись. Разрешённый независимый результат пока только проектирование pure policy slice без side effects/authority, не ENV-01 acceptance.
- Actual local baseline: `.hermes/research/telegram-hermes-codex/probe_runner_reuse.py` — 14 tests, failures/errors/skipped/expected_failures/unexpected_successes 0; updater focused suite — 4 OK; environment gate — 14 OK. Все commands exit 0; donor queue tests — historical regression, не выбор queue. `test_stock_lifecycle.py` остаётся BROKEN_SOURCE, full research suite не заявлен.
- OpenSpec strict: 3 passed / 0 failed; product 7/44 — только прежние discovery children. Для сохранности record-only update создан новый scoped scratch checker `e1-local-packet-check-20260928.py` и capture 33 protected file hashes + append-only prefixes/history/review. Старый scratch `e1-survey-doc-check.py` больше не существует; его прежний receipt не выдаётся за повторно выполненный check.

Self-review — один контекст; fresh-context/cross-model council не запускался, runtime/security design не принят. Следующее решение владельца: предложенные per-artifact edits и отдельно scoped local TDD apply; инфраструктура/OAuth/updater и real model canary не входят. ORCH-01 / CRITICAL не реализован. MemPalace refresh только tasks/openspec, не plans/raw histories.

## Local Policy Apply 2026-09-28

E1-POLICY-APPLY-2026-09-28. Последующее подтверждение владельца «+» разрешило
предъявленный пакет и только локальные 3.1.1–3.1.8. Предыдущий Local Design Packet
выше и одноимённый JSON receipt сохранены как исторический pre-approval этап,
не текущий запрет уже выполненного local apply. Full product approval по-прежнему
pending; parent 3.1, task 1.5.5, E1 runtime и ORCH-01 / CRITICAL открыты.

Применены предложенные proposal/design/matrix/tasks и current coverage; 13 delta
specs и исходные полные критерии не изменены. Derived revision:
`36ab4f6bbcb0895994b16a6ddedde03a55b537f39851e4c9428ffd2576a3d677`.
Approved packet SHA256:
`3fc340c6cf0bd05f40d918ec0c416ff4b5c84975da3116a00da3ba304309a758`.
Это привязка scope, не owner approval всего derived product revision.

### Implemented data-only contract

- Созданы [planner](../../../scripts/project_environment.py) и
  [tests](../../../tests/test_project_environment.py). API/ограничения —
  [README](../../../README.md#local-project-policy-slice) и
  [design](design.md#approved-local-policy-slice-2026-09-28).
- Только Python stdlib; строгие поля/типы, непреобразованные owner/project IDs,
  digest syntax, UID/GID и явный resource class. Стабильная identity и описание
  `/srv/hermes-projects/<owner>/<project>`; worker mount только work, private
  histories/context/checkpoints/results не входят в worker mounts. Это строки,
  не созданные directories и не проверенные OS permissions.
- Compact/large — фиксированные per-project CPU/RAM/swap/pids и поля quota/free
  floor/writers; fresh mutable output, input unchanged. Во всех результатах
  `runtime_admitted=false`. Нет CLI/runtime executor, reservation, Docker,
  filesystem inspection, credentials или принятого image trust.
- Same-context review обнаружил overly broad repository-separator grammar;
  отдельный failing test подтвердил приём invalid mixed/repeated separators.
  Минимальная regex correction сохранила допустимые double underscore и hyphen
  runs. Это не независимый review/council и не proof production isolation.

### Actual TDD and regression receipts

Все команды из root `/Users/s060874gmail.com/coding/projects/hermes-agent`,
Python 3.13.3. T1–T4:

```sh
PYTHONPATH=scripts python3 -B -m unittest discover -s tests -p test_project_environment.py -v
python3 -B .hermes/research/telegram-hermes-codex/probe_runner_reuse.py
python3 -B -m unittest discover -s .hermes/tooling/mvp1-integration-prototype -p test_current_updater.py -v
python3 -B -m unittest discover -s .hermes/research/telegram-hermes-codex/native-codex -p test_environment_gate.py -v
```

| Actual receipt | Command / scope | Observed result |
|---|---|---|
| input-red / input-green | T1 `-k rejects`, loadable stub → validator | 8 tests, exit 1 assertion failures → exit 0 OK |
| input-positive | T1 initial full suite | 9 tests, exit 0 OK |
| layout-red / layout-green | T1 `-k layout` | 5 tests, exit 1 assertion failures → exit 0 OK |
| resources-red / resources-green | T1 `-k resources` | 5 tests, exit 1 assertion failures → exit 0 OK |
| full-green | T1 before review correction | 19 tests, exit 0 OK |
| review-separator-red / review-separator-green | T1 `-k mixed_repository_separators` | 1 test, ValueError not raised/exit 1 → exit 0 OK |
| final-green | T1 final source | 20 tests, exit 0 OK |
| donor-regression | T2, unchanged donor pure tests | 14 tests, failures/errors/skipped/expected_failures/unexpected_successes all 0 |
| updater-regression | T3, pinned source/synthetic fixture | 4 tests, exit 0 OK |
| gate-regression | T4, fake-client state machine | 14 tests, exit 0 OK |
| negative-control | Isolated scratch accept-all module returning `{}`, exact copy of final tests | 20 tests, exit 1, 19 assertion failures; no import/syntax/zero-test error; originals unchanged |

Final focused total: 52 passing tests (20 new + 14 + 4 + 14 regressions), no
skips/expected failures. RED и mutant намеренно не проходят и не включены в
passing total. Полный research suite и реальные native/client/model tests не
запускались; historical BROKEN_SOURCE stock-lifecycle test не исправлялся.

Exact final SHA256:

- `scripts/project_environment.py`: `27cfcae369e3bcb8908b97645d0a88bc52b6437798a3157fe268da37df1f2a29`.
- `tests/test_project_environment.py`: `a9283bafcf50ab43167625e186c4cae276b607c91c8a4cba5ffedfe9a85a73d3`.

Full local command/output/source-hash records находятся в disposable scratch
`/Users/s060874gmail.com/.hermes/cache/scratch/e1-apply-20260928/`, включая
`final-green.json`, `negative-control.json` и `baseline.json`; сохранность scratch
не гарантируется. Этот документ сохраняет sanitized commands/results/hashes.
`e1-apply-check.py run` проверяет фактический child exit: wrapper exit 0 для RED
значит ожидаемый child exit 1, не green. Negative control запускается отдельным
Python process с cwd/PYTHONPATH scratch-копии, не меняет product module.

### Scope and handoff checks

- До config/document apply выполнены zsh syntax checks и approved local
  `./backup-hermes-oauth`: exit 0. Backup contents/credentials не читались и не
  выводились; это не новое OAuth authorization/change.
- `.gitignore` допускает ровно два новых source files. Actual hypothetical Git
  probes: 2 admitted / 22 denied, включая nested auth/env/state/archives и
  произвольные sibling scripts. Проверки не создают эти credential files.
- Оба Python файла проходят AST syntax Python 3.10; это не запуск Python 3.10.
  Семь неизменённых root zsh entrypoints проходят `/bin/zsh -n`.
- T1/T2/T3/T4 завершены; 3.1.1–3.1.8 закрыты по локальным критериям.
  `e1-apply-check.py check`: APPLY_PRESERVATION_PASS, 27 protected hashes,
  44 исходных полных criteria, historical prefixes/review receipts сохранены;
  digest computed=recorded=current coverage. `docs-check.py`: SCOPED_DOCS_PASS,
  9 scoped sections, 15 link targets, 17 anchors, 5 shell blocks; финальные
  source hashes совпадают с реально протестированными и negative-control originals.
  OpenSpec strict: exit 0, 3 passed / 0 failed. Progress после closure — 15/52
  (7 discovery + 8 local children), ни один production parent не закрыт.
- Git read-only assertions: main, без initial commit/staged/remote; donor clean
  на `8cbce9554d2644c0af0333b2b065978b2fb63c4b`. Scoped memory refresh/readback
  следует после final documentation; это не runtime monitoring.
- Server/SSH/Docker/model execution, install/deploy, OAuth/updater changes,
  publication, staging/commit/push/remote, sync/archive не выполнялись этим apply.
  AGENTS.md не менялся, C.17 не разрешён. Installed upstream и donor не редактировались.

Следующий отдельный scope должен связать pure policy с реально проверенным native
credential-safe exec/TUI boundary, filesystem UID/ACL/quota, durable history и
manual/updater lifecycle. Эти runtime gates не закрывает возвращаемый словарь;
новый срез и любой server canary требуют явно ограниченного разрешения.

## Native launch preparation 2026-09-28

Marker E1-NATIVE-PACKET-2026-09-28. **BLOCKED_WITH_ACTIONABLE_PACKET / NOT_IMPLEMENTATION_READY / NOT_RUNTIME_ADMISSION**. Разрешённая локальная подготовка завершена, но runnable native срез не установлен. [Exact proposed packet, source hashes, facts/hypotheses, boundary/lifecycle matrix, canary blockers](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#native-codex-preparation--e1-native-packet-2026-09-28). Product remains 15/52; 1.5.5/3.1/3.2/3.5/3.7/3.8/7.5/7.6/E1 open. Полный owner_approved/implementation_ready=false.

SOURCE_ONLY: current local Hermes HEAD b22631ec4f349c64f50835c6d3434f89986ca05c, cached Codex rust-v0.153.4 at 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a. Exec и TUI используют разные imported EnvironmentManager paths и bootstrap ветки; definitions/all-tool dispatch/SharedCliOptions/recorder source corpus неполон. Это локальный source gap. Generic terminal schema не доказывает typed launch; dotenv до main и local-default provider требуют отдельного admission proof. --ignore-user-config не исключает credential home.

History: filtered MemPalace text spool не full event archive; generic prefetch не fail-closed current-context gate; flush None/False требует caller/DB commit proof. Hermes app-server required-checkpoint guard сохраняется. Updater pin ebd88a8359b4ff8aa0161bb1e00147d36db1fc5b96e63642fb2947a21d43141a: current/quarantine/rollback cleanup paths и stopped managed-container classification требуют reference-aware project coordination, не только hook перед disruption. Actual server не менялся и не проверялся заново.

Blockers: B-SRC (pinned definitions), B-LAUNCH (native fixed input seam), B-ISOLATION (exec/TUI all-path OS boundary), B-HISTORY (originals/crash/hydration), B-LIFECYCLE (owned attach/dead/recreate), B-RESOURCE (image/UID/quota/pool readback), B-UPDATER (all-entry bounded drain/cleanup), B-REVIEW (нет нового fresh-context review). Первый parent 3.2 остаётся BLOCKED_PATH_DISCOVERY без guessed code/test paths. Следующий proposed scope — bounded public-source closure, не runtime canary. Canary manifest NOT_AUTHORIZED / NOT_RUNNABLE до exact platform/image/harness/limits/cleanup hashes и отдельного grant.

Фактические проверки подготовки: OpenSpec context/status/instructions четырёх artifacts, strict current tree product valid / all changes 3 passed 0 failed; CLI progress 15/52. Baseline preservation и source hash checks — см. receipt в плане. Это не валидация ещё не применённого runtime и не новый regression pass. test_stock_lifecycle.py: read-only AST SyntaxError line 4; не исправлялся. Code/native/model/VM/SSH tests, OAuth/credentials reads, network retrieval, install/server/updater changes, council/model calls, Git writes и mining в подготовке не выполнялись. Same-context documentary/source review, не независимый консилиум. ORCH-01 / CRITICAL не реализован.

## Native source follow-up 2026-09-28

E1-NATIVE-SOURCE-V2-2026-09-28: RETRIEVAL_COMPLETE / SOURCE_REVIEW_COMPLETE_WITH_BLOCKERS / NOT_RUNTIME_ADMISSION. [Exact evidence, source hashes, limits и proposed diff](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#native-source-follow-up--e1-native-source-v2-2026-09-28). По отдельному «+» сохранены полный tree и 12 полных source files pinned Codex commit; 2569692 HTTP body bytes, 78.91675279099945 seconds, SHA256/Git blob checks PASS. Это последующее разрешённое получение, не изменение исторического preparation receipt выше.

B-SRC сужен: EnvironmentManager reexports/SharedCliOptions/RolloutRecorder и selected dispatch/backend/compaction caller установлены. Остались LiveThread/ThreadStore implementations, environment resolver/wait, orchestrator и all-path FS/extensions. B-HISTORY конкретизирован: append failure в Session логируется без propagation; compaction меняет in-memory history до append; отдельные resume/fork flush results игнорируются. Очередь/flush/retry upstream существуют, но mandatory project-history barrier не доказан. Runtime fault/data-loss claims отсутствуют.

Первый native parent 3.2/1.5.5 остаётся BLOCKED_PATH_DISCOVERY для runnable local harness; 3.5/3.8 history и 3.7 TUI prerequisites открыты. Нужен выбор mandatory history/admission boundary до Apply, а не ещё один fake parser. Product 15/52, owner_approved=false, implementation_ready=false; B-ISOLATION/B-LIFECYCLE/B-RESOURCE/B-UPDATER/B-REVIEW не сняты. Code/native/model/VM/server/OAuth/updater tests и changes не выполнялись, council NOT_RUN. ORCH-01 / CRITICAL не реализован.
