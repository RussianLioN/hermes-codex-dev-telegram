# Карта проекта

## Scope

Это локальный macOS operations/documentation и выбранный implementation repository `/Users/s060874gmail.com/coding/projects/hermes-agent`, не исходный репозиторий upstream Hermes и не установленный Telegram-продукт. Владелец выбрал его 2026-09-23; local Git создан на main без initial commit/remote. [Repo decision/reuse](changes/telegram-development-workflow/implementation-readiness.md#repository-decision-2026-09-23), [root README](../README.md). Собственные root entrypoints — Z shell scripts; единого root build/test runner нет. Исследовательские Python/Node harnesses имеют свои локальные окружения и не становятся production code от присутствия в этом каталоге.

Внешняя установка Hermes — `~/.hermes/hermes-agent`, launcher — `~/.local/bin/hermes`. Её runtime, profiles, credentials и backups не принадлежат документационному change и не редактируются напрямую. Источник правил — [AGENTS.md](../AGENTS.md); процесс изменений — [WORKFLOW](WORKFLOW.md).

Будущий продукт задан [telegram-development-workflow/proposal.md](changes/telegram-development-workflow/proposal.md), его delta specs и design. Он остаётся NOT_DEPLOYABLE / CLIENT_ROUTING_GATE_OPEN. Владелец разрешает scope и exact revision; исполнитель меняет только разрешённые paths, verifier подтверждает результат, а runtime attempts должны принадлежать штатному Hermes Kanban. Наличие этих ролей в design не доказывает работающую интеграцию.

Operations/tooling inventory основан на source/document review 2026-09-22 и проверен в `seed-project-documentation`. Proposed product overview обновлён по интервью 2026-09-23; это не новая проверка сервера или приёмка runtime. Historical seed coverage/receipts не переписываются под текущую product revision.

## Existing Operations

Ниже SOURCE_ONLY контракты по прочитанным scripts, дополненные syntax check. Это не новое исполнение backup/update/provisioning. Для wrappers OpenSpec/MemPalace inspection/index receipts отдельно записаны в [verification](changes/seed-project-documentation/verification.md). Не запускать mutating entrypoints для знакомства с проектом.

| Entry point / source | Input → output | Отказы и ограничения | Side effects / следующий gate |
|---|---|---|---|
| [run-hermes](../run-hermes) | Произвольный argv передаётся через `exec` в абсолютный `~/.local/bin/hermes`; устанавливается `HERMES_WRITE_SAFE_ROOT=/Users/s060874gmail.com/coding/projects` | Ошибка запуска/код дочернего CLI; wrapper не содержит `set -euo pipefail`. Safe root относится к file-write tools, не является OS sandbox и не запрещает произвольный terminal access | Effects определяет подкоманда Hermes; перед config/dependency/update нужен private backup. Не запускать chat ради shell edit |
| [backup-hermes-oauth](../backup-hermes-oauth) | Без аргументов; штатный `hermes backup` → private timestamped ZIP, integrity/permission checks, сообщение с путём | `set -euo pipefail`: отказ любой команды останавливает цепочку; `unzip -t` доказывает ZIP integrity, не полноценный restore и не сохранность OAuth у провайдера | `umask 077`, backup directory 700, archive 600; создаёт state snapshot вне workspace. Архив не читать/копировать/индексировать/публиковать; restore acceptance отдельно |
| [update-hermes-stable](../update-hermes-stable) | Только пустой argv или `--check`; GitHub latest non-draft/non-prerelease release → tag object/peeled commit/default branch. `--check` печатает release и commit | Неверный argv → 64; curl/jq/git, пустые tag/branch, отсутствующий install clone, backup/auth/installer/post-check failures останавливают выполнение. Это lookup stable release, не обещание новой версии относительно installed | `--check` использует сеть, но не backup/установку. Real update: backup → auth status → fetch/служебная branch → installer, закреплённый на commit → auth/config/version checks. Меняет внешний clone/dependencies; требует явного upgrade scope, здесь не выполнялся |
| [configure-hermes-pilot-ssh](../configure-hermes-pilot-ssh) | Фиксированный alias `hermes-codex-pilot`; добавляет localhost pilot stanza к пользовательскому SSH config, если Host ещё не найден | Повторный Host даёт no-op только для stanza; создание config/chmod выполняются раньше. Fail-fast на filesystem errors; не проверяет, что сам pilot доступен | Создаёт `.ssh`, chmod 700/600, backup config и atomic replacement через temporary file. Не inspection command; private SSH files/keys этим docs apply не читаются. Provisioning отдельно |
| [configure-codex-sandbox](../configure-codex-sandbox) | SSH `-tt` к pilot, embedded base64 operator script → sudo apt update/install bubblewrap/AppArmor, install штатного profile и reload, version output | SSH/sudo/package failures; отсутствие штатного profile → exit 1 без изменения глобального ограничения. Это не доказательство product credential isolation | Mutating remote provisioning с сетевыми/system effects; payload изучен без исполнения. Требуется отдельное разрешение; не запускать вместо status |
| [run-openspec](../run-openspec) | argv → pinned project-local CLI через абсолютный Node; JSON/status или эффект выбранной subcommand | Отсутствие Node/package/root, invalid artifacts/argv → CLI failure. Проверять root и exits, `status` planning-complete не равно implementation-complete | `OPENSPEC_TELEMETRY=0`, `DO_NOT_TRACK=1`; inspection не применяет change. new/update/sync/archive — отдельные writes/approvals; существующий install не переинициализировать |
| [run-mempalace](../run-mempalace) | argv → isolated venv CLI; `--mcp` выбирает stdio MCP. Palace path закреплён относительно wrapper, Chroma + embeddinggemma | Model/cache/storage/process errors не исправляются fabricated search. MCP disconnect не доказывает corruption; CLI status/search позволяет отделить transport от index | `umask 077`, telemetry off; search читает индекс, `mine` пишет индекс. `HF_HUB_OFFLINE=1` задаётся при scoped refresh, wrapper сам его не экспортирует. Только tasks/openspec; без bulk home mining |

Если индекс отстаёт: выполнить обе scoped mine-команды из [WORKFLOW §11](WORKFLOW.md#11-handoff-и-память), проверить exits, затем поиск по отличительной фразе и exact-source readback. После внешнего CLI mine долгоживущий MCP может сохранять stale in-memory HNSW: если CLI видит новый source, а MCP нет, вызвать штатный `mempalace_reconnect`, затем повторить тот же exact-source search и `get_drawer`. Эта последовательность реально восстановила поиск ROADMAP при посеве; receipts — в verification. При MCP disconnect сначала проверить CLI, не удалять palace и не менять provider/config вслепую. При отсутствующей модели остановиться, не скачивать её автоматически. Источник остаётся авторитетным даже при MEMORY_REFRESH_BLOCKED.

## Tooling and Evidence

Версии ниже — pins manifests либо датированные historical receipts, не заявление о latest. Обновление tooling требует отдельного scope. Обследование документации не перезапускает исторические tests.

| Domain / source | Назначение и граница | Evidence / следующий шаг |
|---|---|---|
| [OpenSpec manifest](../.hermes/tooling/openspec/package.json), `.hermes/tooling/openspec/` | Third-party CLI 1.13.0, schema spec-driven, package-lock; собственный wrapper выше | CLI validation — NATIVE_LOCAL tooling check, не runtime acceptance продукта. Формат берётся из installed instructions; [research](changes/seed-project-documentation/research.md) связывает версионные official sources |
| [Browser manifest](../.hermes/tooling/browser/package.json), `.hermes/tooling/browser/` | Pinned Playwright 1.63.0, chrome-devtools-mcp 1.9.0, MCP SDK 1.30.0; изолированный Chrome for Testing 153.0.8010.12 по historical installation receipt | [17-browser-tooling-installation.md](../.hermes/research/telegram-hermes-codex/17-browser-tooling-installation.md): реальные historical browser/API fixtures и MCP smoke, не Telegram product acceptance. Личный Chrome profile не используется; новые browser tests здесь не запускались |
| [MemPalace README](../.hermes/tooling/mempalace/README.md), `.hermes/tooling/mempalace/` | Upstream source pin v3.9.0, isolated venv, локальные embeddings/Chroma, palace — generated state. External embedding service/shared hub не настроены | NATIVE_LOCAL scoped CLI/MCP retrieval; повторная индексация только разрешённых docs. Wing/room не ACL; индекс не task scheduler и не authority |
| [Собственный memory provider](../.hermes/tooling/mempalace/provider/README.md) | Default-profile plugin-adapter, не vendor MemPalace: durable private completed-turn spool, daemon indexing и synchronous pre-compression checkpoint. Незавершённый streaming turn не гарантированно сохранён | Historical unit и direct synthetic lifecycle tests не доказывают actual new-session lifecycle: MEM-02b открыт. Redaction эвристическая, не гарантия отсутствия любого секрета; здесь private spool не читается и provider не перенастраивается |
| [Telegram approval prototype](../.hermes/tooling/telegram-approval-prototype/README.md) | Локальный Bridge на native transport/handler extension; NOT_INSTALLED, не policy engine | Historical LOCAL_SYNTHETIC и targeted NATIVE_LOCAL loader; generic mandatory transport expectedFailure остаётся незакрытым. Не live Telegram; N-01 boundary требует отдельной реализации/приёмки |
| [Protected-operation prototype](../.hermes/tooling/protected-operation-prototype/README.md) | Immutable manifest/journal, fencing/reconciliation на synthetic marker; не security boundary для same-UID caller | LOCAL_SYNTHETIC protocol; отдельный historical AUTHORIZED_CANARY OS DAC — [server-evidence](../.hermes/tooling/protected-operation-prototype/server-evidence.md). Однократное разрешение исчерпано, полного N-01 не доказывает |
| [MVP1 integration prototype](../.hermes/tooling/mvp1-integration-prototype/README.md) | Native Kanban fixture + toy controller, mock publisher/upload, temporary encrypted restore; NOT_INSTALLED / DEPLOY_PACKET_BLOCKED | NATIVE_LOCAL + LOCAL_SYNTHETIC, не production service. Toy successor не ORCH-01, mock PR не GitHub result; README содержит отдельные failed/open границы |
| [Native Codex research](../.hermes/research/telegram-hermes-codex/native-codex/) | Source/config/environment/lifecycle probes, receipts и harnesses, не утверждённый product runner | [native-environment-evidence](changes/telegram-development-workflow/native-environment-evidence.md), [native-bootstrap-evidence](changes/telegram-development-workflow/native-bootstrap-evidence.md), [linux-model-lifecycle-preparation](changes/telegram-development-workflow/linux-model-lifecycle-preparation.md), [linux-canary-evidence](changes/telegram-development-workflow/linux-canary-evidence.md). SOURCE_ONLY/NATIVE_LOCAL/LOCAL_SYNTHETIC и отдельный AUTHORIZED_CANARY; FAILED metadata probe не означает отсутствия OAuth |
| [Research tree](../.hermes/research/telegram-hermes-codex/) | Supporting research, варианты и provenance. [08-target-concept](../.hermes/research/telegram-hermes-codex/08-target-concept.md) и [10-implementation-plan](../.hermes/research/telegram-hermes-codex/10-implementation-plan.md) — background, не действующее разрешение строить ранний runtime/approval service | [18-openspec-sdd](../.hermes/research/telegram-hermes-codex/18-openspec-sdd.md), [16-agent-skills-completion](../.hermes/research/telegram-hermes-codex/16-agent-skills-completion.md); текущие ownership/решения — product deltas/design. No-core alternatives и expert reviews не новый acceptance |
| [Generated Hermes skills](../.hermes/skills/), [generated Codex skills](../.agents/skills/) | Разные integration paths, не редактировать generated skills вручную. Внешний Addy skills pack задаёт методику, не устанавливает отсутствующие tools | [Audit integrations](changes/adopt-openspec-workflow/audit.md#интеграции): existence не runtime loading; здесь skills прочитаны и CLI реально вызван, slash invocation не имитируется |
| [Планы](../.hermes/plans/), [TODO](../tasks/todo.md), [historical GitOps guide](../HERMES_CODEX_SWARM_GITOPS_GUIDE.md) | Планы/история/операторский индекс, не конкурирующие implementation queues. Guide описывает прежний control-repo design, не текущий grant | Canonical executable checklist — tasks выбранного change; historical outputs не переписывать. [Current scenario evidence map](changes/adopt-openspec-workflow/audit.md#current-coverage) вместо копирования receipts |

`node_modules`, venv, vendored upstream source, model/browser caches, palace, generated reports/screenshots и binary canary artifacts не являются собственным production code inventory. Их содержимое не требуется обходить для onboarding. Index/archives/private state не включать в Git или публикацию; соблюдение этого правила не гарантируется названием каталога.

## Architecture

As-is — локальные operations и документы:

```text
Оператор → root wrappers
  run-hermes ───────────────→ внешняя установка ~/.hermes/hermes-agent
  backup/update ────────────→ private snapshot / внешний install (по разрешению)
  configure-*-ssh/sandbox ──→ SSH config / pilot provisioning (по разрешению)
  run-openspec ─────────────→ pinned CLI → openspec documents
  run-mempalace ────────────→ local index ← scoped tasks + openspec
  provider (default) ───────→ private spool → отдельный conversation wing

Исследовательские prototypes/receipts ──→ documentary evidence, не production
```

Proposed, NOT_DEPLOYABLE — только обзор [canonical Capability Map](changes/telegram-development-workflow/design.md#capability-map), не новый design:

```text
Telegram owner → native Hermes intake/approval → native Kanban task/run
  → admission + reusable project container + server bind-mounted project folder
  → automatic Codex writer → frozen candidate → trusted tests → Telegram report
SSH owner → отдельный ordinary interactive Codex в том же project container
  → отдельный worktree/branch; disconnect/reconnect той же живой session
Manual + automatic writers → последовательная интеграция + повторные tests
Полная приватная история → автоматический актуальный context при новом запуске

Последующие инкременты: controlled publisher → private PR / owner-gated merge
  → contemporary-dance-guide → ручной Git / file:// preview

Независимый ORCH-01 controller → heartbeat / fenced retry / reconciliation
Snapshot/restore + existing updater → drain / backup / rollback coordination
```

Первый acceptance increment E1 — рабочая среда, не полная production readiness. Bind mount сохраняет данные при recreate, не живой процесс; SSH disconnect при живом контейнере сохраняет ручную сессию. Общие OpenSpec/MemPalace/skills/rules требуют проверенных Hermes/Codex adapters, project tools/skills/dependencies изолированы. Shared tools/base image/server/SSH/mount permissions — Telegram owner approval; существующая automatic daily update policy не отменена.

Unresolved boundaries: mandatory native approval/launch, credential/network isolation и actual model routing, Kanban fencing, SSH continuity, full-history/hydration, extension compatibility, shared-state ACL, publisher authority, locks/backup suitability. Telegram ingress/transport — предварительно проверяемая платформа; delivery не циклическая prerequisite intake. Design CLI-first; app-server research не обязательная замена обычного CLI. ORCH-01 not implemented: профиль или MemPalace не обеспечивают независимое наблюдение.

## Data and Trust Boundaries

| Данные | Canonical owner / source | Trust и publication boundary |
|---|---|---|
| Specs и spec revision | Владелец решения; OpenSpec product deltas/design, [review-status](changes/telegram-development-workflow/review-status.json) | Readable requirement не approval token; exact revision меняется → новое решение. Не переносить draft в main specs ради полноты |
| Tasks / attempts | Change tasks — implementation checklist; штатный Hermes Kanban — runtime task/run | Roadmap не scheduler; technical journal не должен claim новые user tasks в обход Kanban. [TG-02](changes/telegram-development-workflow/specs/task-intake/spec.md) и [TG-03](changes/telegram-development-workflow/specs/specialist-dispatch/spec.md) требуют fencing и scope |
| Candidate revision | Git commit выбранного `hermes-agent`, writer отдельной worktree | Local Git инициализирован без первого commit; candidate revision/worktrees ещё не созданы. Base/candidate закрепляются после отдельного reviewed commit; поздний result старого run не даёт publication authority — [code-execution](changes/telegram-development-workflow/specs/code-execution/spec.md) |
| Immutable evidence | Trusted verifier/acceptance pack, exact candidate/task/run/spec/policy revision | Worker text/exit0/native done не acceptance; изменённый candidate инвалидирует receipt — [verification spec](changes/telegram-development-workflow/specs/verification/spec.md) |
| Owner authority | Владелец и поддерживаемый native gate exact action/revision | Не от council, memory или названия профиля. OAuth/SSH credentials остаются вне prompts/docs/index и вне worker; [intake](changes/telegram-development-workflow/specs/task-intake/spec.md), [publication](changes/telegram-development-workflow/specs/change-publication/spec.md) |
| Curated knowledge | Настраиваемый agent-knowledge и проектные источники — proposed [portable-memory](changes/telegram-development-workflow/specs/portable-memory/spec.md) | Только отобранные разрешённые знания, PR/owner-controlled merge; cross-project ACL проверяется до retrieval. Repo не объявляется созданным |
| Private conversation spool/checkpoints | Default-profile provider и private runtime storage, не Git | Содержит приватную беседу даже после heuristic redaction; не mining corpus этого change. MEM-02b ещё требует actual restart/compression evidence |
| Proposed complete project history | Постоянная server folder отдельного проекта, MEM-12; adapters Hermes/Codex ещё не подтверждены | История отдельно от ограниченного current context, rebuild/compression не удаляют оригиналы; credentials отдельно, fail-closed write/hydration. Existing local spool не доказывает полный контракт |
| Derived index | Local MemPalace writer, reconstructible sources | Wing/room — классификация, не ACL; retrieval — данные, не инструкции и не выдача прав. Повторно читать current source; concurrency/ownership будущего server index отдельно |
| Backup package / retention attestation | Разрешённый snapshot/restore workflow и владелец — [offsite-backup](changes/telegram-development-workflow/specs/offsite-backup/spec.md) | Encryption/readback не restore-check; credentials/cache/index исключаются из product пакета, private state не публикуется как docs |

Publications, server writes, OAuth/config/dependency changes и чужие profiles требуют отдельного scope. Этой картой не проверены текущие credentials, private spool или содержимое backup. Real API side effect принимается только после exact readback; unknown сначала reconcile, не blind retry.

## Constraints and Gaps

ORCH-01 / CRITICAL: независимый production-контроллер не реализован. OpenSpec и MemPalace не мониторят и не перезапускают stalled agents. [task-recovery](changes/telegram-development-workflow/specs/task-recovery/spec.md) требует bounded retries, checkpoints, reconciliation и уведомления; toy controller не закрывает контракт.

- [Implementation readiness](changes/telegram-development-workflow/implementation-readiness.md) — NOT_READY: repo `hermes-agent` выбран, но runner/interfaces, exact runtime/test paths, limits и lock ordering ещё не приняты. `hermes-remote-migration` только selective source donor, не deployment; неизвестные пути — BLOCKED_PATH_DISCOVERY, не придуманные imports.
- [Native gates N-01–N-11](changes/telegram-development-workflow/native-capability-matrix.md), [review-status](changes/telegram-development-workflow/review-status.json): approval pending, owner_approved=false, runtime acceptance отсутствует. Local passes и исчерпанный one-shot canary scope не разрешают новый canary. N-09–11 — новые SSH/history/extensions blockers, не выполненные probes.
- [Current reconciliation R1–R3](changes/adopt-openspec-workflow/reconciliation.md#current-reconciliation) подтверждена и применена 2026-09-23. OS-07 / protected AGENTS write всё ещё требует отдельного подтверждения; новой попытки нет. Adoption не объявлен завершённым.
- Existing Operations выше — SOURCE_ONLY as-is inventory, не полный формальный as-built набор specs operational tooling. Current product coverage относится к delta specs; docs reconciliation не заполняет main specs непринятым поведением.
- Broken `.hermes/research/telegram-hermes-codex/native-codex/test_stock_lifecycle.py` остаётся BROKEN_SOURCE / NOT_RUN; syntax failure не meaningful RED. Исправление — отдельная code task, не часть посева.
- MEM-02b требует реального lifecycle после restart; unit/direct hook не достаточны. Полный список открытых операторских gates — [текущий TODO](../tasks/todo.md#текущий-операторский-индекс--openspec-reconciliation).
- Safe root и Markdown/config guidance не OS security enforcement. Source review + zsh syntax не удостоверяют isolation, успешный restore или production readiness. Новые численные product budgets этой картой не назначаются.
