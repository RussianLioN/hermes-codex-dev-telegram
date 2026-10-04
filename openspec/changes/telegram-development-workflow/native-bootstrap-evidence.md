# GitHub access и ограничения native bootstrap

## GitHub: причина остановки и проверка доступа

После разрешения владельца повторный GET pinned tree openai/codex вернул HTTP 200, truncated=false. В заголовках unauthenticated запроса remaining=59, limit=60. Authenticated `gh api user` подтвердил RussianLioN без интерактивного входа. `gh api rate_limit` на момент проверки вернул core 5000/5000 remaining и GraphQL 5000/5000 remaining. `gh api repos/openai/codex` подтвердил private=false, visibility=public.

Предыдущий отказ был сообщением среды о неподтверждённом выполнении, не HTTP-ответом GitHub об исчерпании квоты. Проверенный запрос относится к уже публичному upstream, не приватному проекту. Основания для условной замены репозитория отсутствуют; репозитории не публиковались, visibility не менялась. Эти проверки REST/GraphQL не выдаются за аудит GitHub Actions billing или всех квот аккаунта. Дальнейшее чтение исходников выполнялось через уже авторизованный gh, без вывода credential values.

## Воспроизводимые контрпримеры

Все новые native пробы закреплены на Codex 0.153.4, commit 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a. Исследовательские файлы находятся в `.hermes/research/telegram-hermes-codex/native-codex/`.

### Inventory не пассивен

`test_mcp_inventory_effects.py`: две реальные ситуации без модели/сети/настоящего MCP server. Configured executable — touch временного маркера, не поддельный MCP API.

- enabled=false: маркера нет до и после запроса; inventory содержит одну запись.
- enabled=true: до запроса маркера нет; mcpServerStatus/list(detail=toolsAndAuthOnly) создаёт маркер. Запуск процесса произошёл до model turn. Tools map остаётся пустым, поскольку touch не является MCP server.

Следовательно, пустой tools map или успешный inventory call не удостоверяет отсутствие начальных эффектов. Нельзя применять такой запрос к непросмотренным реальным слоям как безусловно пассивную проверку.

Pinned sources:
- `codex-rs/app-server-protocol/schema/typescript/v2/McpServerStatus.ts:11–15`: нет enabled field; runtimeStatus может быть null при отсутствии thread-runtime/изменении config.
- `codex-rs/app-server/src/request_processors/mcp_processor.rs:263–337`: latest config → collect_mcp_server_status_snapshot_with_detail.
- `codex-rs/codex-mcp/src/lib.rs:76–78`: export snapshot collector.

### До model turn — не то же самое, что полная конфигурация turn

`test_native_cli_config.py`: пять fixture-вариантов с намеренно некорректным output schema. Обычный base config и profile overlay показывают ошибку base config; --ignore-user-config позволяет пройти этот этап и остановиться на output schema. Пятый вариант с ошибочным project config также достиг раннего schema stop: это ограничение точки наблюдения, НЕ доказательство удаления project layers в настоящем turn.

CLI source сохраняет system/project/managed источники; profile v2 накладывается на base. Неизвестные слои нельзя считать выключенными. `codex-rs/arg0/src/lib.rs` дополнительно показывает load_dotenv ДО основной CLI/runtime логики: .env загружается из CODEX_HOME, лишь CODEX_* keys отфильтровываются. Настоящий .env агентом не открывался/не выводился. Флаг игнорирования config.toml не объявляется запретом dotenv bootstrap.

### Ограничение начальных эффектов на уровне ОС

`bootstrap_sandbox.py` создаёт только временный macOS sandbox-exec wrapper. До запуска native binary: network и process-fork запрещены; writes разрешены только под owned scratch. Чтения остаются широкими — это не защита секретов от чтения и не production isolation.

`test_bootstrap_sandbox.py`: два unittest, пять фактических наблюдений:
- живая loopback socket доступна без guard;
- тот же endpoint под guard отклонён с errno=1;
- обычный synthetic native bootstrap запускает MCP executable и пишет вне scratch;
- guarded bootstrap получает synthetic account=None, не запускает MCP executable, пишет внутри scratch и получает отказ снаружи;
- read-only synthetic CODEX_HOME не инициализируется: native EPERM и SDK TimeoutError. Redirect sqlite_home/log_dir в scratch не устранил отказ.

Последний пункт — сохранённый отрицательный результат, а не исправленная поддержка read-only home. Первоначальное ожидание успеха этой ветки реально упало; окончательная проверка удостоверяет отказ, не превращает его в acceptance.

## Отдельная попытка metadata через существующий native login

После положительных/отрицательных проверок guard выполнен только account metadata probe, без thread/model/config-read/MCP-discovery/login/refresh RPC. Перед RPC применены запреты fork/network/outside-scratch write. Схема GetAccountResponse не возвращает tokens; email не выводится. Native SDK использует существующий login обычным образом; код агента не разбирает credential files.

Результат: guarded_bootstrap_failed=true, error_type=TimeoutError. Содержимое реального stderr/config/auth не диагностировалось и не сохранялось. Plan type не получен. Повторная попытка после redirects не выполнялась: предшествующий synthetic readonly test упал, а команда была связана через &&. Последующее сохранение отрицательной проверки в suite не запускало metadata probe повторно.

Нельзя делать вывод «OAuth отсутствует» или «аккаунт не подпадает под managed policy». `codex-rs/cloud-config/src/service.rs:49–56` ограничивает cloud-config eligibility business/education/enterprise, но фактический plan здесь неизвестен. Никакого нового login, копирования tokens или ослабления sandbox для обхода отказа не выполнено.

## Evidence и оставшаяся работа

`environment-run/receipts-v5.json`: фактический запуск всех указанных synthetic suites, source/binary hashes, проверки отказа при optimized Python. Существующий account metadata probe НЕ входит в повторяемый recorder; его неуспех сохраняется отдельно в этом документе.

19/19 ответов нового bounded council: LOCAL_PREPARATION_REQUIRED (`council/linux-model-scope/decision.md`). B не предъявляется как готовое обязательное действие владельца. Требуются concrete lifecycle/identity/network harness и admission до credentialed effects. Bootstrap guard не поддерживает проектный model loop и не закрывает CLIENT_ROUTING_GATE_OPEN. ORCH-01 / CRITICAL открыт. Working Hermes core/profile configuration, сервер и видимость GitHub repositories агентом не изменялись; новых VM и проектных model turns не было.
