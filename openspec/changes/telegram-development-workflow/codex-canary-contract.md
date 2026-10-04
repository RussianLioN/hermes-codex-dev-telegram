# Native Codex canary contract

Статус: LINUX_CANARY_PARTIAL_PASS / CLIENT_ROUTING_GATE_OPEN / VM_DELETED. Однократный local-linux-canary-scope.md разрешён владельцем `+` и исполнен; реальные результаты и ограничения — `linux-canary-evidence.md`. Полная матрица ниже не принята; повторный runtime не разрешается этим результатом. ORCH-01 / CRITICAL открыт.

## Выполненные cases

- `native-codex/test_native_sandbox.py`: actual macOS CLI; synthetic control read exit41, deny+project write exit0, minimal unknown outside/symlink denied, inherited synthetic env present. Это file policy evidence и env counterexample, не all-path proof.
- `native-codex/test_exec_server.py`: actual stdio handshake/FS fileURI/active duplicate rejection/terminate/EOF. sandbox=None разрешает read; descendants_verified=false.
- `native-codex/test_native_appserver.py`: existing Hermes native client, generated schema, no model/auth, outer no-network; последний valid thread/start FAIL из-за nested macOS sandbox helper. FAIL сохранить; не делать expectedFailure/skip и не включать в green integration count.

## Следующие Linux cases: синтетика, один owned runtime

| Case | Input/control | Условие зачёта / отказ |
|---|---|---|
| L1 provenance | pinned downloaded bundle, runtime version/OS/arch; help/schema | SHA и version совпадают, helper assets реально доступны; иначе no execution |
| L2 profile/native FS | fake HOME, fake protected file вне project, positive own file | unknown profile rejected; activePermissionProfile.id совпал; direct/symlink/FS RPC/apply path outside denied; no sandbox context не даёт client FS |
| L3 credentials/env/FD | только synthetic markers в parent env/argv/private dirs, closed FDs | worker не получает их через inherited env/argv/FD/mount/proc; позитивный собственный marker доступен; не читать real secrets |
| L4 namespace/network | owned UID/caps/mount/net/cgroup metadata, local synthetic socket | worker не имеет control socket/чужих namespaces; отрицательный egress с positive control в setup; отсутствие endpoint само не отказ sandbox |
| L5 descendants | bounded child writer, setsid, parent exit, authority stop | извне подтверждена пустая owned cgroup/нет писателей; не только EOF/killpg/однократный timestamp |
| L6 fail-closed routing | missing exec-server, include_local=false, project config/hook fixture | ошибка без host fallback и без загрузки project hook в credential namespace; отключение tool schema само не доказательство |
| L7 recovery fence | synthetic unknown intent/old run/late result | нового launch/effect нет до reconciliation; не выдавать SQL fixture за фактический OS stop |

Каждый case: pre-state/owned identity/deadline/exit/denial category/positive control/readback/cleanup. Не журналировать markers как auth values; markers заведомо синтетические. Не считать namespace metadata достаточной negative test. Не запускать real model, GitHub, Telegram или server update под этим scope.

Ordinary Codex task — отдельный следующий gate, после Linux boundary. Настоящий Telegram→tests→exact owner→private PR→Telegram и backup/ORCH acceptance остаются незавершёнными. Без этих результатов deploy/rollback packet не READY.
