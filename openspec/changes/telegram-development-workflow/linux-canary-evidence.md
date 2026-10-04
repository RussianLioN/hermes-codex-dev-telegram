# Linux canary — фактический результат 2026-09-14

Статус: LINUX_CANARY_PARTIAL_PASS / CLIENT_ROUTING_GATE_OPEN / NOT_DEPLOYABLE.
ORCH-01 / CRITICAL остаётся открыт. Это результат одной разрешённой временной VM, не приёмка production.

## Scope и ресурсы

Владелец подтвердил `local-linux-canary-scope.md` сообщением `+`. Перед созданием проверено отсутствие профиля `hermes-boundary-canary`; private backup wrapper завершился exit0 с подтверждением verification. Создана только эта VM: Colima0.10.3/VZ, aarch64, 1CPU, 2147483648bytes RAM, data8589934592bytes, root disk10GiB. Kernel6.8.0-117-generic, Python3.12.3. `findmnt` не показал virtiofs/9p/sshfs host mounts; SSH-agent, project port forwarding и context activation отключены.

Создание началось18:19:42 MSK, VM ready18:20:08, полное удаление18:48:54. От создания до удаления1752s, внутри лимита1800s. Default VM осталась Stopped,4CPU/6442450944bytes RAM/64424509440bytes disk; активный Docker context остался `colima`, socket default. На сервер не подключались; ядро, конфигурация и profiles Hermes не изменялись. Ни model turn, ни Telegram/GitHub/API публикаций не было.

## Provenance

Машиночитаемые receipts: `.hermes/research/telegram-hermes-codex/native-codex/linux-run/receipts.json` от root workspace. Полный public Codex bundle сохранён рядом; Linux binaries извлекались и исполнялись только внутри VM.

- Colima commit `00f6c297e92a82c04a4ab507db0a61435650d7e8`.
- Base image взят из существующего Colima cache. Затем SHA512 сверена с `embedded/images/images.txt` этого commit: совпадение. Source: `https://github.com/abiosoft/colima-core/releases/download/v0.10.4/ubuntu-24.04-minimal-cloudimg-arm64-docker.raw.gz`.
- Base SHA256 `1fc0354f4f99734ce3886628cc7af8b0437c1a1d391b126bd09cba0df35ee53f`.
- Codex0.153.4: `https://github.com/openai/codex/releases/download/rust-v0.153.4/codex-package-aarch64-unknown-linux-musl.tar.gz`; 117238842bytes; SHA256 `fc395cb043a1093ab0db34f44aba3199bfaa9ce640cd9be7fd588f44b0da64a4`. Hash совпал до извлечения; проверены типы/path traversal/duplicates архивных entries.
- Executable SHA256 `4d76e542c222ea8c75861d8c4ade60a1a332a63255ce1c60bdaebf7c2a2869e6`; bundled bwrap `c547cbdc762a70ed216789ffaa4c6c0e7d2beabe32245a498f8e365a9fc8dab4`.

## Исполненные проверки

Здесь L1–L6 — идентификаторы именно `local-linux-canary-scope.md`. У `codex-canary-contract.md` более широкая матрица, включая ещё не выполненные проверки.

| Scope case | Фактический результат |
|---|---|
| L1 native Hermes client | `test_linux_appserver.py -v`: 1test OK. Настоящий неизменённый CodexAppServerClient → native Linux Codex через Colima stdio; initialize, unknown profile rejected, named active profile readback, approvalPolicy=never. Outer Linux network namespace. Без turn/start. |
| L2 native execution/FS | `linux_probe.py --baseline`: exit1 именно на разрешённом protected read. Тот же `linux_probe.py` с C2 containment: exit0; native positive FS read и пять native fileURI denials, включая traversal/symlink/proc. Реальный process/start запустил Python challenge; independent project write readback совпал. |
| L3 worker authority | 19 проверок challenge прошли: VM-global UID/GID65534, empty effective/bounding capabilities, no-new-privileges, clean env/FD, own read/write; protected files/DAC/symlink, parent environ/mem/signal, outside write/cgroup escape, control/Docker socket, controller TCP и outbound route отвергнуты. Только синтетические данные. |
| L4 missing/exited executor | НЕ ПРОЙДЕН. С include_local=false и explicit environments=[canary-dead] thread/start всё равно возвращает успех как для отсутствующей программы, так и для /bin/false. Gate test: exit1, два failed subtests. Создание thread не доказывает готовность выбранного helper. Реальное локальное fallback-исполнение НЕ проверялось и этим результатом не доказано. |
| L5 descendants | Реальный fork+setsid child начал heartbeat. До остановки в owned cgroup были пять PID. После cgroup.kill и wait — cgroup.procs пуст; контроллер/защищённый marker целы; cgroup удалена. Проверено извне, не только через EOF/terminate. Double-fork отдельно не проверялся. |
| L6 cleanup | До shutdown нет оставшихся codex/bwrap/python probe processes и owned cgroups. После stop/delete --data --force отсутствуют profile directory, Lima VM directory, datadisk directory, owned Docker context и hostagent PID82682; management SSH port57489 закрыт. Default context/VM сохранены. |

Первый unprivileged bwrap --unshare-all запуск завершился exit1: `loopback: Failed RTM_NEWADDR: Operation not permitted`. Sysctl/AppArmor/security policy не ослаблялись. Проверенный вариант использовал доверенный root launcher ТОЛЬКО внутри одноразовой VM: native bwrap создаёт mount/pid/net/ipc/uts/cgroup namespaces, затем штатный setpriv сбрасывает VM-global UID/GID и все capabilities перед exec-server. Это не одобрение privileged launcher на сервере.

Unix/TCP listeners были созданы в controller namespace; отдельный positive connect к ним не выполнялся. Отсутствие внешних интерфейсов проверено, попытка RFC5737-route отвергнута. Это ограниченное evidence, не полная проверка network/proxy/MCP policy.

Colima delete сообщил warning об unlock data disk. Отдельный readback подтвердил отсутствие самой data directory и VM; warning не проигнорирован. `docker context inspect colima-hermes-boundary-canary` вернул ожидаемый context-not-found/exit1 — это доказательство отсутствия, не ошибка создания.

## Почему thread/start недостаточно

Нельзя исправлять результат L4 заявлением «fallback доказан» или превращать тест в expectedFailure. Он остаётся открытым readiness gate. После cleanup дополнительно прочитан pinned source Codex `codex-rs/app-server/src/request_processors/environment_processor.rs`: environment_info вызывает get_environment и force_info, environment_status различает Ready/Pending/Disconnected/Unknown. Эти отдельные native методы — следующий предмет проверки; в этой VM они не вызывались. Их наличие в source не является runtime acceptance. Новый запуск удалённой VM этим разрешением не покрывается.

Нет end-to-end связи model client → selected contained worker → все file/apply/MCP/hooks paths. Нет подтверждённого publisher/updater admission или real model/Telegram E2E. ARM Linux не эквивалентен production amd64. Поэтому CODEX_SOURCE_READY=false и runnable deployment packet остаётся заблокированным.

## Артефакты и регрессии

Под `.hermes/research/telegram-hermes-codex/native-codex/`:
- `linux_probe.py` — исполненный одноразовый probe; привязан к boot_id удалённой VM, не production launcher.
- `test_linux_appserver.py` — переиспользует `child` из `test_native_appserver.py`; последнее изменение только добавляет optional environments argument в research helper, не в Hermes core.
- `test_linux_environment_failure.py` — открытый readiness gate, два failed subtests; временный environments.toml удалялся в finally с exact readback.
- `linux-run/{ownership,receipts}.json` — scope, provenance, real outcomes, cleanup.

Повторно выполнены: integration44 OK (0.739s), protected23 OK (0.720s), transport40 / expected failures=1 (3.712s). MacOS app-server повторно FAIL (0.588s) с прежним nested sandbox_apply/exit71; не скрыт и не включён в green44. Linux-required probes не запускать после удаления VM и не добавлять их как бесконтекстный автоматический discover-suite. Результаты сохранены; повторная VM требует отдельного ограниченного scope.
