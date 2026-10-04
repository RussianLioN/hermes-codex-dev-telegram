# Текущие source и execution receipts

Дата проверки: 2026-09-14, MSK. Это evidence, не разрешение live deployment. ORCH-01 / CRITICAL открыт.

Последующий Linux canary выполнен по отдельному `+`: `linux-canary-evidence.md`. VM удалена; native Linux client/profile и C2 OS probe PASS, selected-helper readiness gate FAIL. Нижеследующие сведения об остановленном runtime/отсутствии Linux execution — baseline до этого разрешения, не текущий статус. Production по-прежнему NOT_DEPLOYABLE.

## A1 / среда

- `git status --short` и `git branch --show-current`: exit128, workspace не Git repo. Git init/commit/push не выполнялись.
- `codex --version`: codex-cli 0.153.4. Public release tag rust-v0.153.4 → annotated tag042fb41b7c813ac7999105e886b2b7aa715b5081 → commit3d2ee51ca2d5db578f328aa75e20aa22c0197c9a.
- Authoritative Hermes docs: https://hermes-agent.nousresearch.com/docs/ (HTTP read успешен). Codex reference: https://developers.openai.com/codex/security; current permissions page при предыдущем чтении redirected https://learn.chatgpt.com/docs/permissions. Latest docs отдельно от pinned source.
- `codex sandbox --help`: плоский COMMAND, не `sandbox macos`. `exec-server --listen stdio` и `app-server --listen stdio://` — РАЗНЫЕ значения двух CLI, не нормализовать.
- Installed schema generator help проверен, затем `codex app-server generate-json-schema --experimental --out <TemporaryDirectory>` exit0. Ничего не установлено; temporary artifacts удалены. Генерация была во временном каталоге ОС, а не runtime. `permissions` — string profile id; несовместим с sandbox/sandboxPolicy; `activePermissionProfile.id` — доступный readback.
- `colima version`: 0.10.3, commit00f6c297e92a82c04a4ab507db0a61435650d7e8. Default VM stopped; только default в `colima list`. Docker context colima, local unix socket. Ни VM, ни Docker daemon не запускались.
- `uname -m` x86_64 относится к переведённому процессу: `hw.optional.arm64=1`, `sysctl.proc_translated=1`; физический ARM capability подтверждён. `hw.memsize=17179869184`. Linux target сервера — x86_64. ARM Linux VM не будет полной amd64 acceptance.

## local-source / server-source

Сверка непосредственных app-server компонентов:

| Source | Local/server |
|---|---|
| agent/transports/codex_app_server.py | одинаковый264e1ebf1f99ae623f5da11e1a28d215ae51f31a130f5a77246612285dd4cd4a |
| agent/transports/codex_app_server_session.py | одинаковый18e25a83416ee1b7df427accdb45f1f8e41748283b28911068b0787f49eb4197 |
| agent/agent_runtime_helpers.py | одинаковый022b9c7afc52c645d577ea83e2ee57ea916562a7c3ddc9d0bf989bbfb33f8a14 |
| model_tools.py | local6990a410050915dd36010306d00e8d581264a583eac009d0049a52a6442be603; server699ddf9dbf9fc0397c8f93316616499d152e9ae841e7c81e7109265f0d4d71c7 |

У model_tools отличается также AST без line attributes: local d14029e2354964ce90601e893444066f163234726fe6dbb27cb09375c1edf091; server da16a9059a7adf4c80f384fb9c5e753547845a1a50a382b158e87f62313c8a06. Это не только перенос строк; semantic compatibility не заявляется. Пять прежних direct Kanban/plugin/approval совпадений из wave-1-packet не являются transitive proof. Никаких автоматических repin.

## server-baseline

Read-only SSH, gateway `hermes-agent-hermes-gateway-1`: running, StartedAt `2026-09-11T23:04:41.207398289Z`, image `sha256:3d1c312980e7d400ebf1fabca40f855a6ff16cab11e80930a9b3d4d3c920ef5e`. Старое start/image из canary A — история. Этот ход gateway не перезапускал.

Updater `/srv/hermes-agent/bin/hermes_stable_updater.py` SHA256 `ebd88a8359b4ff8aa0161bb1e00147d36db1fc5b96e63642fb2947a21d43141a`. Pristine source перенесён SCP только в `.hermes/tooling/mvp1-integration-prototype/fixtures/server/hermes_stable_updater.py`; exact hash совпал, AST parsed. Не импортировать целиком для запуска.

Проверенный порядок:
- apply1452–1472: maintenance window, flock, _apply_locked;
- _apply_locked1485: recover ДО prechecks;
-1535–1545: launcher lock, writer check, disruption, stop_gateway, no writers, snapshot;
-1554–1564: marker, candidate snapshot checks, OAuth probe, deploy, verify, commit manifest;
-1604–1627: rollback/current failed candidate/quarantine/marker handling;
- recover1379–1394 и _recover_locked1396–1450: собственный путь rollback/start_gateway;
- snapshot867–868 отвергает writers до mkdir/tar.

Это доказывает необходимость охвата recover/startup/admission, не готовый patch. Системные apply/recover/OAuth probe не вызывались.

## Реальные проверки

| Command / cwd=root, если не указан | Результат |
|---|---|
| `.hermes/tooling/telegram-approval-prototype/.venv/bin/python -B -m unittest discover -s .hermes/tooling/mvp1-integration-prototype -v` | 44 tests OK,0.779s |
| тот же python, discover -s .hermes/tooling/protected-operation-prototype -v | 23 tests OK,0.714s |
| cwd telegram-approval-prototype: `.venv/bin/python -B -m unittest discover -s tests -v` | 40 tests, expected failures=1,4.537s |
| тот же python, `.hermes/research/telegram-hermes-codex/native-codex/test_native_sandbox.py -v` | повторная проверка:1test OK,0.382s; actual macOS sandbox |
| `test_exec_server.py -v` | повторная проверка:1test OK,0.180s; actual stdio lifecycle; без model/auth |
| `test_native_appserver.py -v` | FAIL; не входит в integration44, не скрыт skip/expectedFailure |

Новые именованные integration cases: test_phase_transition.py (семь phase cases предыдущего хода); test_current_updater.py (четыре current-source cases): `test_rollback_excludes_current_synthetic_credentials`, `test_quarantine_binds_exact_tag_and_digest`, `test_real_snapshot_guard_rejects_writer_before_filesystem`, `test_current_source_order_is_not_a_drain_implementation`.

Фактический последний app-server failure: native initialize завершился и unknown profile был отклонён; valid thread/start error-32603, AGENTS.md filesystem helper → `sandbox-exec: sandbox_apply: Operation not permitted`, exit71. Whole-client outer macOS no-network sandbox конфликтует с nested native helper. Предыдущие ошибки missing default_permissions были в fixture и исправлены. Три запуска, дальнейший обход запрета не выполнялся. Test не доказывает недостаток Linux и не проверяет model turn. Auth отсутствовал в temporary HOME; model `turn/start` не вызывался.

## Что не делать из этих результатов

После docs edits: strict OpenSpec validation1passed/0failed/issues[], spec digest
не изменился:29163c1de50e501a82f85cc72ada9f011520a3a17828ee0027adf006b22c729f.
owner_approved=false. Три council packet/output manifests проверены программно;
scope shell blocks проходят zsh -n без исполнения VM commands. AST probes/pristine
fixture проверены; это не устраняет указанный native app-server FAIL.

- Нельзя выдавать CLI `:minimal`/symlink deny за изоляцию всех model tools. Синтетический env marker проходит в child: filesystem sandbox не env scrubber.
- Native client хранит provider auth по назначению; это само по себе не доказанная утечка child. Default owned-worker Kanban writable injection — отдельный неприемлемый путь без компенсации.
- `process/terminate` и EOF не подтверждают смерть detached descendants. Ни snapshot consistency, ни exactly-once не следуют из них.
- Updater source tests не проверяют live drain/startup/recovery; full deployment packet остаётся BLOCKED.
