# Переиспользование: без нового framework и core patch

Дата2026-09-14. NOT_INSTALLED; ORCH-01 / CRITICAL открыт.

| Артефакт | Решение | Граница |
|---|---|---|
| `.hermes/tooling/telegram-approval-prototype/plugin/{__init__.py,bridge.py,plugin.yaml}` | REUSE локального transport prototype и regressions | ctx.on_unload/native approval registration/Telegram handler; не новый bot consumer, не privileged authority |
| Native `agent/transports/codex_app_server.py:37–180` | REUSE wire primitive CodexAppServerClient | Реально импортирован и initialize проверен в temp HOME; default Kanban-owned launch с writable DB НЕ пригоден как boundary |
| Native `codex_app_server_session.py:151–199` | CONDITIONAL; source seam client_factory найден | Не переписывать session/core. Permissions/readback/launch isolation требуют подтверждения; default thread/start не передаёт permissions |
| Codex exec-server0.153.4, commit3d2ee51ca2d5db578f328aa75e20aa22c0197c9a | C2 candidate, native stdio smoke PASS | Не standalone authorization/OS isolation: sandbox=None разрешает FS RPC; native files/process paths и fallback ещё gates |
| `.hermes/tooling/protected-operation-prototype/protocol.py` | REUSE regression contracts | Synthetic marker, не shell RPC/publisher implementation |
| `.hermes/tooling/mvp1-integration-prototype` | REUSE phase/current-updater/failure fixtures |44passing tests не production acceptance |
| `.hermes/tooling/mempalace/provider/`, run-mempalace | REUSE scoped curated continuity | Не auth source; не читать credentials/raw histories, не менять профили |
| installed Colima0.10.3 | Только proposed temporary Linux test runtime | Уже установлена, но stopped. Startup/dependency bootstrap требует local-linux-canary-scope.md |

Официальная Hermes reference https://hermes-agent.nousresearch.com/docs/ прочитана; plugins route найден на https://hermes-agent.nousresearch.com/docs/plugins. Version-sensitive Codex source URLs и hashes — live-source-evidence.md/council packets. Новый внешний plugin не выбран и не установлен: concrete gap находится в authority/OS containment, а не в отсутствии SDK. Новых лицензируемых зависимостей в maintained code нет; AST/unittest probes используют stdlib и уже существующий venv. Scanner не отключался, существующие skill/core/profile файлы не менялись.
