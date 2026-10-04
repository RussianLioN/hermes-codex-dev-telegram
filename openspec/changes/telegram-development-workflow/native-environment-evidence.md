# Native environment admission — локальные доказательства

Статус: LOCAL_NATIVE_READINESS_VERIFIED / CLIENT_ROUTING_GATE_OPEN / NOT_DEPLOYABLE.
Дата: 2026-09-16. ORCH-01 / CRITICAL открыт.

## Что действительно выполнено

Использован установленный Codex 0.153.4 и неизменённый Hermes CodexAppServerClient. Собственные временные homes, config, markers; macOS filesystem sandbox с запрещённой сетью. VM/сервер/бот/рабочие профили не менялись. Проектные model turns и реальная авторизация в probes отсутствуют; отдельно выполнены разрешённые model calls экспертного консилиума.

Код: `.hermes/research/telegram-hermes-codex/native-codex/`:
- `environment_gate.py`: одно первоначальное environment/info, затем non-recovering environment/status; unknown/disconnected/local-enabled → отказ. Ошибка закрывает экземпляр; повтор не делает RPC. Объект привязан к создавшему потоку. KeyboardInterrupt/SystemExit закрывают состояние и выбрасываются повторно.
- `test_environment_gate.py`: 14 unit tests PASS. Client здесь stub и не является runtime доказательством. Включены KeyboardInterrupt/SystemExit при local status внутри check_ready и отсутствие дальнейших RPC.
- `test_environment_readiness.py`: 1 native test, 6 сценариев PASS — local-control, missing, exited, healthy, died, hang.
- `test_client_overrides.py`: 1 native test, 4 сценария PASS — baseline, merged, late-untrust, owned. Содержит отрицательные контрпримеры, а не объявляет unsafe overrides безопасными.
- `owned_probe.py`, `test_owned_probe.py`: 4 tests PASS; отдельная POSIX process group, deadline, общий предел stdout+stderr, cleanup в finally. После замечания консилиума RED→GREEN устранён неограниченный Popen.__exit__ wait после cleanup timeout; pipes закрываются и при неуспешном reap. Этот крайний случай проверен mock, не настоящим kernel D-state. Создание процесса/cleanup не объявляются жёстким общим SLA. Это supervisor контролируемых fixtures, не production Linux cgroup и не защита от setsid.
- `test_code_mode_host.py`: настоящий bundled V8 host, 8 сценариев PASS: JS positive; process/Deno/require/fetch недоступны; node/file imports отклонены; незарегистрированный tool недоступен. enabled_tools=[]; ни модели, ни настоящих delegates. Не доказаны V8 exploit resistance или полная tool mediation.
- `test_managed_client_config.py`: 3 настоящих config-read сценария PASS: без task metadata; owned Kanban task; штатный delegated_child_context с inherited metadata. Временный MCP disabled и имеет несуществующую command; это не запуск MCP.
- `test_remote_provider.py`: настоящий native default provider CODEX_EXEC_SERVER_URL; запрет сети даёт disconnected до gate, local остаётся unknown, local FS/command endpoints отклонены. Это no-model negative, не положительное remote execution.
- `test_managed_mcp.py`: настоящий MCP 2.0.0 stdio server Hermes без core patches и тестовых подмен dispatch. Owned worker завершает задачу в синтетической канонической Kanban DB, native readback=done. Делегированному процессу complete не рекламируется, прямой tools/call отклоняется, status остаётся running. Прямые вызовы нерекламируемых terminal/execute_code также отклонены без marker. Два режима PASS; сеть/внешние процессы/чтение private state запрещены fixture. Это кооперативная actor fence, не OS boundary.

Фактические результаты нового повторного запуска: `.hermes/research/telegram-hermes-codex/native-codex/environment-run/receipts-v4.json`. Recorder проверяет pinned Codex/client hashes до и после запуска, сохраняет selected source/interpreter/host hashes и отказы шести direct child entrypoints при Python -O. Старые receipts не переписаны. Полный набор импортируемых зависимостей/происхождение сборки/TOCTOU этим не удостоверены. Использован существующий Hermes venv с MCP 2.0.0; зависимости не устанавливались.

Regression повторён: integration44 PASS; protected23 PASS; transport40 tests, OK с 1 expectedFailure (generic selected transport по-прежнему не mandatory).

## Readiness не равна thread/start

Первый Linux canary показал успешный thread/start даже при отсутствующем/завершившемся executor. Это не доказывало fallback. Новый реальный wire experiment различает:
- в проверенных stdio fixtures до подключения: pending; это не универсальное условие для всех transport;
- environment/info при working helper: ready;
- missing/exited: -32603 и disconnected;
- SIGKILL собственного helper: disconnected, gate закрыт; status/check_ready не перезапускают helper;
- намеренно зависший probe принудительно остановлен внешним supervisor, исчезновение записанного helper PID проверено внешним ps.

У native fs/readFile ошибка точно `-32603 / local filesystem is not configured`; у command/exec и thread/shellCommand — `-32603 / local environment is not configured`. Проверяются код и точное сообщение, не подстрока. При include_local=true положительные контроли действительно читают synthetic marker и создают отдельные command/shell markers. При false три endpoint отклонены и с явно выбранным canary в thread/start.

thread/shellCommand — local-only endpoint, не API remote model tool execution. Его отказ не доказывает исполнение модели внутри canary. В shell-only fixture project_doc_max_bytes=0: обработка AGENTS не покрыта.

Успешное исчезновение PID в новых probes относится к client close плюс cleanup supervisor; `owned_group_cleanup_sent` сохраняется отдельно. Нельзя приписывать принудительную очистку одному native close. Ранее сохранённый pre-supervisor receipt не переписывается. Исчезновение PID не доказывает отсутствие escaped потомков; это отдельный Linux gate.

## Два отвергнутых предположения о конфигурации

1. `-c mcp_servers={}` НЕ удаляет entries из исходной и доверенной project конфигурации. Реальный config/read сохраняет fixture/project_fixture. Оба fake MCP disabled и имеют несуществующие commands: опыт доказывает config retention, НЕ запуск постороннего MCP.
2. CLI override `projects.<path>.trust_level="untrusted"` не удаляет project layer, если исходная конфигурация уже trusted. В этом probe trust level при выборе слоёв нельзя подменять поздним override.

Положительный ограниченный вариант: controller-owned чистый config с untrusted, записанным ДО запуска клиента; project .codex/config тогда не попадает в effective MCP map. hooks/plugins/shell_snapshot=false readback подтверждён. Это synthetic конфигурация, не доказательство Linux DAC/mount isolation или real credential layout. Настоящий runtime config, auth.json и значения credentials не читались/не копировались.

app-server не предоставляет exec-флаг --ignore-user-config. Debug-only override в pinned app-server/src/lib.rs:1350–1372 выключен в release; как решение не используется. Pinned source: openai/codex 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a.

## Что не закрыто

Продолжение после этого checkpoint: `native-bootstrap-evidence.md`, фактический `environment-run/receipts-v5.json`. Native inventory имеет начальные эффекты; OS bootstrap guard проверен только в ограниченных fixtures. Read-only CODEX_HOME и guarded existing-account metadata остаются отказами. Новый scope-B council дал 19/19 LOCAL_PREPARATION_REQUIRED: не предъявлять незавершённую подготовку как необходимость owner action.

ReadyEnvironment — сохраняемый результат наблюдения, НЕ lease/право/отзывной token. Нет атомарной связи с операцией, защиты от другого клиента/нового gate, all-path mediation или production integration. Lifecycle deadlines функций не объявляются единым wall-clock SLA.

Нужны Linux privilege/cgroup/config-view доказательства; managed Hermes MCP/Kanban path без writable control root; source-driven проверка hooks/code-mode/config и реального model routing; safe existing OAuth recovery; installer/deployment/updater diff и отдельный exact owner scope. Канонический Kanban не отключается и не заменяется ledger.

Ни новые unit tests, ни экспертные ответы не закрывают CLIENT_ROUTING_GATE_OPEN. ORCH-01 / CRITICAL не реализован этими файлами.

## Native managed injection и маршрут без изменения ядра

Неизменённый `agent/transports/codex_app_server.py` добавляет свои CLI overrides ПОСЛЕ extra_args. При собственном HERMES_KANBAN_TASK режим read-only заменяется workspace-write, writable_roots получает каталог HERMES_KANBAN_DB, а managed MCP получает task/run/board identity. Реальный config/read это подтвердил даже при переданных раньше read-only, пустых writable_roots и mcp_servers={}.

Штатный `delegated_child_context` предотвращает именно эту owned-task инъекцию. Predicate `is_dispatcher_owned_worker_context()` сам не проверяет наличие TASK — client проверяет его отдельно. Это не повод подделывать identity владельца или выдавать ContextVar за privilege boundary. Кандидат разделения: каноническим Kanban владеет доверенный parent, project child не получает его write authority. Native MCP experiment выше подтверждает только локальный синтетический handoff/denial, не всю production схему.

Source: `agent/transports/hermes_tools_mcp_server.py:38–52,76–117` регистрирует фиксированный список инструментов; terminal/file/process/execute_code не входят. `tools/kanban_tools.py:118–124` отдельно отклоняет delegated mutations. Описательный текст MCP шире фактического списка; решение основывается на регистрации/прямых вызовах, не на описании.

## Pinned source routing

Источник всех Rust ссылок: https://github.com/openai/codex/tree/3d2ee51ca2d5db578f328aa75e20aa22c0197c9a

- `codex-rs/exec-server/src/environment_provider.rs:50–97`: при CODEX_EXEC_SERVER_URL создаётся remote, include_local=false. `environment_toml.rs:197–207`: environments.toml имеет приоритет; env default применяется только при отсутствии файла. Наличие файла в обычном local Codex home проверено только как metadata: отсутствовал; contents/config/auth не читались.
- `environment.rs:268–343`: manager запускает remote connection в background при построении snapshot. Поэтому ошибка может наблюдаться ДО environment/info. Gate не контролирует все начальные соединения native клиента. `:779–796`: remote uses RemoteProcess/RemoteFileSystem.
- `tools/code_mode/execute_handler.rs:45–75`: enabled delegates строятся из nested_tool_specs; `delegate.rs:109–179,270–293` передаёт вызовы CoreTurnHost/ToolCallRuntime. Пустой список в standalone V8 probe не доказывает ограничения enabled delegates.
- `tools/runtimes/apply_patch.rs:155–196`: выбранный turn_environment filesystem и явный sandbox context. `tools/runtimes/unified_exec.rs:260–278,383–410,508–538`: remote branch избегает local shell snapshot и передаёт выбранное environment process manager. Это source evidence, не выполненные model tools.

Bounded final council завершён: `council/environment-admission/decision.md`. Wave1 остаётся failed; waves2/3 имеют по 19 принятых записей старого классификатора. Не независимые модели; deployment не одобрен. Новую общую волну вместо работы не запускаем.
