# Серверный baseline и границы доказательств

Источник: разрешённое read-only обследование `ssh -o BatchMode=yes ainetic.tech` в текущей сессии 2026-09-10/11. Ни updater, ни live chat/approval, ни auth команды не запускались. Значения credentials, полный Docker inspect/env/config и backup archives не читались и не публиковались.

## Подтверждено

- SSH identity: root; host `ainetic-tech`, Linux 5.15.0-185-generic.
- `nproc`: 2; `free -m`: RAM total 5921, available 4020 на момент исходного обследования. `df -h /`: 79G total, 35G used, 41G available. Это snapshot, не reservation.
- `docker ps -a`: 17 работающих контейнеров, в том числе сторонние VPN, n8n, PostgreSQL, Redis, Traefik. Рабочие ресурсы не выделены исключительно Hermes.
- `docker exec hermes-agent-hermes-gateway-1 /opt/hermes/bin/hermes --version`: v0.21.1 (2026.9.7), upstream 2237be35, install `/opt/hermes`, docker, Python 3.13.5.
- Image: `nousresearch/hermes-agent:v2026.9.7@sha256:b3190406963c6b51ac955397ecef45346efaae9563ee305108f8eef0a77e267b`.
- Выборочный inspect: user root, cwd /workspace, privileged false, memory limit 1610612736 bytes, nano_cpus 1000000000. Docker socket среди mounts отсутствует.
- Mounts: `/srv/hermes-agent/data` → `/opt/data`; `/srv/hermes-agent/work` → `/workspace`; `/opt/ainetic-stack/local-files/hermes` → `/files`, все RW.
- Networks: `ainetic_net`, `hermes-agent_hermes_cli_net`. Это текущая сеть Hermes, не разрешённые будущие сети Codex.
- Compose: `/srv/hermes-agent/compose.yml`.
- Codex не найден `command -v codex` ни на host, ни в Hermes container. Не доказано отсутствие установки вне PATH.

## Существующее обслуживание

`systemctl show hermes-stable-update.service -p FragmentPath -p ExecStart -p Result -p ExecMainStatus`:
- unit `/etc/systemd/system/hermes-stable-update.service`;
- ExecStart `/usr/bin/python3 /srv/hermes-agent/bin/hermes_stable_updater.py apply`;
- Result success, ExecMainStatus 0. Это статус unit, не доказательство текущей последней stable версии.

Статическое чтение `/srv/hermes-agent/bin/hermes_stable_updater.py`:
- `maintenance_window_open`, строки 119–126: 02:00–05:00 Москвы;
- функции snapshot, candidate validation, verify_post_deploy, rollback, cleanup_docker, protected_configured_image_ids присутствуют;
- `_apply_locked`, строки 1535–1545: launcher lock → verify_single_gateway_writer → begin_gateway_disruption → stop_gateway → check remaining writers → snapshot;
- ожидание project tasks в этом участке не найдено. Полный lock graph/drain semantics ещё не проверен;
- glob верхнего уровня `/srv/hermes-agent/tests/*.py` не вернул файлов; это не утверждение об отсутствии вложенных тестов. Требуется точечное дальнейшее discovery.

## Штатные interfaces: только статическое подтверждение

На серверном source `/opt/hermes` AST и ограниченное чтение выявили:
- `tools/approval.py:137` — resolve_gateway_approval(session_key, choice, resolve_all=False, reason=None, request_id=None), выбор по request_id либо FIFO;
- `tools/approval.py:930` — request_tool_approval(tool_name, reason, *, rule_key='', approval_callback=None), общий native gate; docstring описывает once/session/always/deny и fail-closed без human. Это описание source, а не runtime canary;
- `tools/delegate_tool.py:410` — delegate_task;
- `agent/memory_manager.py:659` — supports_pre_compress_checkpoint, :664 on_pre_compress;
- `agent/conversation_compression.py:2591` — _pre_compress_memory_context;
- обнаружены `tools/kanban_tools.py`, `tools/kanban_tools_schemas.py`, `gateway/kanban_watchers*.py`;
- предполагаемый `gateway/platforms/telegram.py` отсутствует. Не использовать этот придуманный путь в реализации; реальный adapter требует discovery.

Наличие общего approval gate не гарантирует точное подтверждение merge и переживание restart: broad session/always approvals и route ownership должны быть отдельно проверены. Аналогично наличие checkpoint API не доказывает установленного серверного MemPalace provider.

## Безопасные команды повторной сверки

    ssh -o BatchMode=yes -o ConnectTimeout=15 ainetic.tech 'hostname; uname -sr; nproc; free -m; df -h /'
    ssh -o BatchMode=yes ainetic.tech 'docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"'
    ssh -o BatchMode=yes ainetic.tech 'systemctl show hermes-stable-update.service -p FragmentPath -p ExecStart -p Result -p ExecMainStatus'

Ожидание: exit 0, фактические ресурсы/версии сравниваются с snapshot, а не обязаны совпадать. Полный inspect и compose config выводить нельзя: они могут раскрыть env/credentials. Любой canary с внешними side effects требует отдельного scope.
