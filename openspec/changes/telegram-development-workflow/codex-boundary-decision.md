# Codex boundary decision

Статус: C2_LINUX_PARTIAL_PASS / CLIENT_ROUTING_GATE_OPEN / CODEX_SOURCE_READY=false / NOT_DEPLOYABLE.
Основание: `council/live-boundary/decision.md`, `live-source-evidence.md`. ORCH-01 / CRITICAL открыт.

Последующий факт, не новое решение консилиума: `linux-canary-evidence.md`. Реальный Linux exec-server в containment прошёл native FS/UID/caps/env/FD/network/descendant проверки; native Hermes client/profile probe прошёл. Но thread/start принимает absent/exited selected helper — readiness/fallback gate остаётся открытым; actual fallback execution не доказано. VM удалена после 1752s, default VM/context сохранены. Будущий native environment/info/status admission пока только source-driven candidate, не проверенная интеграция.

Уточнение 2026-09-16: `native-environment-evidence.md` и новые native macOS probes проверили environment/info/status, missing/exited/dead helper, три local-only endpoint и timeout cleanup. Это уже не только source candidate, но всё ещё не Linux/model routing integration. Выявлены контрпримеры: empty MCP table не стирает унаследованную конфигурацию; поздний CLI untrusted не удаляет project layer. Чистый controller-owned config с изначальным untrusted проверен только на synthetic fixture. CODEX_SOURCE_READY=false сохраняется.

## Selected approach

Native Codex0.153.4 `exec-server --listen stdio` в отдельном project OS containment; trusted model client остаётся отдельно. Его `environments.toml` должен исключать local fallback (`include_local=false`); exact selected environment/readback и отсутствие client-side code paths — обязательные gates. Native Hermes CodexAppServerClient переиспользуется только как wire primitive. Default Kanban-owned launcher с writable Kanban root отвергнут для выполнения недоверенного кода.

C1 strict permissions не отвергнут как технология: реальные :minimal и symlink deny работают на macOS. Отвергнуто использование filesystem policy как единственной границы credentials/IPC/environment. Исследовательский native app-server тест под внешним macOS sandbox остаётся FAIL; это не диагноз Linux.

## all-paths / evidence matrix

| Вход | Source / фактический результат | Необходимая отрицательная проверка |
|---|---|---|
| Shell / process | native exec-server initialize/start/duplicate/terminate/EOF PASS | Linux UID/caps/namespaces/cgroup, отсутствие credentials/env/FD; unknown launch не повторяется |
| File / apply_patch | pinned handlers/apply_patch.rs411–419,523–529; runtimes/apply_patch.rs87–112,179–197 передают context | FS RPC без context не получает client FS; ошибки path matching и context не приводят к host fallback |
| Client environment | environments.toml schema прочитана; include_local default=true | explicit false, выбранный environment missing→fail closed, запрет local execution |
| Native Hermes | CodexAppServerClient50–90 и Session180–199 | запрет writable Kanban injection у project child; схема/activePermissionProfile readback на Linux |
| MCP / deferred tools | local model_tools730–734 scope bridge;947–948 direct dispatcher; outer turn_tool_round92–114 фильтр имён | forged/deferred/delegated calls не достигают privileged capability; server AST отличается, source equivalence не доказана |
| Hooks / config | отрицательный gate, не проверено actual model | подложенные project config/AGENTS/hooks не исполняются в credential namespace |
| Descendants | exec-server EOF exit0, descendants_verified=false | setsid/double-fork/late writer; внешняя проверка пустой cgroup до нового run/snapshot |
| Telegram / unload | существующие Bridge/protocol suites | реальный owner event, exact payload/revision, authority admission; generic fallback не создаёт effect |
| Git | E12 threat finding, privileged publisher не реализован | чистый staging, отсутствие project hooks/helper/filter/alternates; fixed target/refs, remote readback после unknown |

## Native wire constraints

Не путать `exec-server --listen stdio` с `app-server --listen stdio://`. Для exec-server сначала initialize(clientName), потом initialized; file paths — fileURI. `--exit-on-stdin-close` несовместим с его stdio и не нужен. Успешный terminate означает ответ RPC, не отсутствие потомков.

Generated app-server schema: thread/start permissions:string, несовместим с sandbox; turn/start permissions:string, несовместим с sandboxPolicy. Для named profile требуется определённый default_permissions; capabilities.experimentalApi включается явно. Readback activePermissionProfile.id должен совпасть, unknown profile — отказ. В macOS probe последний valid thread/start до readback не дошёл, поэтому schema presence не compatibility PASS.

## Что блокирует runnable deployment

Production authority/launch cancellation, целевая Linux integration, all-path enforcement, source drift и actual updater admission ещё не доказаны. Не создавать runnable compose/installer с догадками. Однократный `local-linux-canary-scope.md` уже исполнен, не является разрешением повторного запуска. Продолжать независимые local/source работы; real model/Telegram/GitHub/server effects потребуют отдельного точного scope.
