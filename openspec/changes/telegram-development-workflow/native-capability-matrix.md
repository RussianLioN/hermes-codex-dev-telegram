# Матрица native-first gates

Статусы: SOURCE_PRESENT — обнаружен точный источник; UNVERIFIED — не выполнен behavioural probe; BLOCKING_GATE — нельзя объявить implementation-ready до проверки. Все gates остаются открытыми. После [local discovery E1](implementation-readiness.md#e1-source-discovery-2026-09-23) и выбора repo выполнен разрешённый [server read-only survey 2026-09-23](implementation-readiness.md#server-read-only-survey-2026-09-23), marker SERVER-E1-SURVEY-2026-09-23. Actual source/metadata не runtime acceptance; local focused checks 4/4/14 OK не закрывают production gates. Не устанавливать собственную замену штатных approvals или вторую очередь для обхода пробела.

| ID | Требование | Что известно | Что требуется для закрытия |
|---|---|---|---|
| N-01 | TG-01, TG-09, TG-11: штатное owner approval | SERVER_SOURCE_PRESENT: plugins/platforms/telegram/adapter.py:746/3802/4271/4280 → tools/approval.py:137; exact hashes в survey | Проверить owner-only routing, exact request/revision binding, timeout/restart/ambiguous reply; session/always не обходят точный merge/infrastructure decision. Найденный callback не whole-system enforcement; live canary отдельно разрешить. |
| N-02 | TG-02–04, REC-02: execution/delegation | SOURCE_PRESENT: tools/kanban_tools.py, gateway/kanban_watchers*.py, tools/delegate_tool.py:410 | Проверить actual schemas/create/claim/cancel/replay/restart на isolated state, совместимость controller без второй очереди и writer fencing. |
| N-03 | TG-04–05, SSH-01: native launch и Codex subscription | SERVER_SOURCE_PRESENT: manifest Hermes 0.21.2 отличается от local 0.21.4; terminal_tool.py:1170/1302, delegate_task:410, codex_runtime.py:382/470. Codex не найден PATH host/gateway; binary pin и OAuth UNVERIFIED | Выбрать credential-safe native exec seam и exact CLI pin; app-server не молчаливая замена exec/manual CLI и конфликтует с required checkpoint. Проверить auth refresh/single-owner и client/project isolation; не переносить токены, не переключаться на API billing. Missing suitable interface — blocker, не custom runner grant. |
| N-04 | ENV-01, TG-05–06: проектная изоляция | SOURCE_PRESENT только базовый Docker и лимиты Hermes; root SSH не является worker policy | Sentinel tests: нет credential/host/socket/чужой project access, YOLO не расширяет scope, cancel убирает task descendants, resource queue не трогает сторонний стек. Если OAuth-client/project process невозможно разделить штатно — архитектурный blocker владельцу. |
| N-05 | MEM-10–11: memory lifecycle | SOURCE_PRESENT local H: memory_manager.py:533/727 и conversation_compression.py:2916 в agent; старые :659/664/:2591 — server snapshot. Completed-turn sync async/best-effort; app-server + required checkpoint отвергается | Проверить server provider и оба harness на реальных completed turn/pre-compression/restart, retrieval/rebuild. Не выключать checkpoint; source hook/macOS autosave не server acceptance. |
| N-06 | UPD-01–02, ENV-02 | SERVER_SOURCE_PIN_MATCH ebd88a83: maintenance → launcher lock, stop gateway → zero writers → snapshot; timer loaded/active. Local pinned updater focused tests 4 OK. Existing launcher Python source не доказывает coordinated manual/project admission | Полный wrapper/service lock graph, manual sessions/cleanup/drain/defer/backup failure остаются непроверенными. Сохранить daily automation, stop→consistent snapshot и auth/rollback protections; server change только новым exact scope. |
| N-07 | BACK-01–03: GitHub backups | Интервью выбрало Github; Releases assets лишь кандидат. Public docs о размере assets не доказывают допустимость backup workload | Проверить актуальные официальные условия/лимиты, оценить sample объём без private data, encryption/manifest/reachability, lost upload response. Если непригодно — новое owner decision, без silent fallback. |
| N-08 | Реальная карта реализации | Выбран локальный `hermes-agent`, main без commit/remote; R clean feat/codex-runner at 8cbce955 только donor. Server metadata/UID/mounts/limits и source pins зафиксированы; `/usr/local/lib/hermes-launcher.py:170–241` создаёт per-invocation `docker run --rm`, не reusable ENV-01 | Repo choice и bounded server inventory выполнены. Approved project layout/budget/native credential boundary/lock graph и runnable first product test остаются BLOCKED_PATH_DISCOVERY (1.5.5). Own queue, ephemeral/destructive lifecycle не переносятся; placeholder implementation запрещена. |
| N-09 | SSH-01–02, TG-03/05, UPD-01: independent interactive session | SOURCE_ONLY: tmux — кандидат, но не найден PATH host/gateway. Existing launcher CLI/shell ephemeral; durable manual-session interface не доказан. Codex resume не живой PID | Owner выбор; отдельная manual identity/worktree, отсутствие duplicate, disconnect/death/recreate distinctions, negative access и updater drain tests. Read-only SSH survey выполнен; установка/session start/canary этим не разрешены. |
| N-10 | ENV-01, MEM-12: full history и hydration | SOURCE_ONLY: server memory hooks и persistence pins найдены; local codex_runtime_history_seed.py отсутствует на server. Provider local coverage не full archive; persisted projection не raw history. Candidate --ephemeral/обрезка логов не MEM-12 | Durable event/crash boundary, private server folder/ACL вне credential homes, session/attempt attribution, redaction и fail-closed hydration не реализованы. Actual pinned Codex storage schema/source UNVERIFIED. Recreate/rebuild/start canary обоих harness отдельно, без ручного paste. |
| N-11 | TG-04, MEM-10–12: два уровня расширений | SOURCE_ONLY compatibility matrix OpenSpec/MemPalace/skills/rules × Hermes/Codex заполнена с pins. Local CLI use доказан только docs командами; server adapters/load/use UNVERIFIED, Codex lifecycle hooks не подключены | Проверить loading/use обоих harness и project-only isolation. Shared tools/base image/permissions только после Telegram approval. Generated skill existence не runtime compatibility; C.17 остаётся отдельным protected gate. |

## Local design scope 2026-09-28

Последующее подтверждение владельца «+» разрешает E1-LOCAL-PACKET-2026-09-28 и pure local 3.1.1–3.1.8, не закрывает ни один runtime gate. Таблица выше хранит dated survey findings; следующие уточнения supersede только слова «не выбран» для design candidates, не UNVERIFIED runtime.

| Gates | Current scoped decision / evidence | Still blocked |
|---|---|---|
| N-03/N-04 | Source candidate Codex rust-v0.153.4 at 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a; exec/TUI bootstrap различаются, dotenv до main. C2 candidate, controller-owned remote-only config, separate trusted/worker identities | Binary install/auth/all-path mediation/native launch не проверены; pure input validation не OS sandbox |
| N-06 | Existing maintenance EX|NB → launcher blocking EX; long shared session lock отвергнут. Design bounded 60s drain/defer с учётом detached | Exact updater hook/diff, все entry points и race/deadline/rollback proofs; live script не менялся |
| N-08 | Repo выбран; exact новый local API/scripts/tests и stdlib T1 разрешены. Layout `/srv/hermes-projects/<owner>/<project>`, compact/large policy в design | 1.5.5/3.1 full runtime open: actual UID/ACL/quota, binding/locks/pool admission и pinned runnable image отсутствуют |
| N-09 | tmux 3.7c source-release candidate, exact owned attach вместо silent new/resume-last | Install/SSH identity/actual continuity/death/recreate/cleanup не запускались |
| N-10 | Private history/context/checkpoints/results отделены от worker work и credentials в design/data-only plan | Full archive schema/hooks/crash/hydration двух harness не реализованы; строки путей не durable history |

N-11 не закрыт; compatibility adapters отдельно. Local source/TDD evidence — [readiness](implementation-readiness.md), scopes design — [local policy slice](design.md#approved-local-policy-slice-2026-09-28). Полный E1 NOT_DEPLOYABLE, ORCH-01 / CRITICAL открыт.

## Историческое evidence 2026-09-11, автономный этап

- N-01: local real gate/hook negative probes; 40 tests, OK (expected failures=1). Generic selected-transport requirement НЕ закрыт. После трёх волн выбран обязательный executor privilege boundary; новый implementation scope пока не разрешён. `../../../.hermes/tooling/telegram-approval-prototype/boundary-evidence.md` и `boundary-council.md` в том же каталоге.
- N-02: настоящий local Kanban SQLite: конкурентный claim, stale run fencing, sequential replay, dependencies, reopen verified. Idempotency key не tenant-scoped; concurrent-create uniqueness НЕ доказана. Local/server sources различаются.
- N-03–06: read-only server metadata/source проверены; Codex не в PATH, default plugin directory пуст, task drain/offsite coordination не найдены в inspected updater source. Это не live acceptance.
- N-07: установленный age 1.3.1, synthetic roundtrip/tamper/wrong-key/permissions прошли; upload/remote restore не было. GitHub limits и AUP перечитаны, Releases остаётся bounded candidate без обещания unlimited backup.
- N-08: 14 pure historical manifest/JobStore tests прошли, repo не менялся; собственный queued claim старого runner требует адаптации к native task authority, не готов к deployment.

Воспроизводимые команды, SHA и ограничения: `../../../.hermes/research/telegram-hermes-codex/readiness-probes-2026-09-11.md`. Все gates остаются открытыми; эти результаты заменяют лишь старые отметки о полном отсутствии локальных behavioural probes. ORCH-01 / CRITICAL не реализован.

## Условия readiness

Для каждого gate сохранить: exact runtime revision, источник, команду, ожидаемый и фактический результат, scope canary, ограничения и этап E1/E2. `isPlanningComplete` OpenSpec означает только наличие артефактов, а не право выполнять tasks.

E1 требует относящиеся сценарии N-01–06/N-08–11, безопасное сосуществование с updater и exact revision/scope approval. N-07 и publication/offsite части остальных gates остаются E2/full-readiness blockers; частичный E1 pass не закрывает весь gate. N-09–11 — расширение существующей матрицы, не новая task queue. Полная readiness остаётся false до полного набора контрактов. ORCH-01 / CRITICAL не реализован и не закрывается E1.

## Источники для следующих probes

- https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
- https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin
- https://developers.openai.com/codex/cli/reference/
- https://containers.dev/implementors/json_reference/
- https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
- https://docs.github.com/en/site-policy/github-terms/github-terms-of-service

Ссылки — источники для проверки; перечисление не означает прохождения gates. ORCH-01 / CRITICAL ещё не реализован.

## Native launch preparation 2026-09-28

E1-NATIVE-PACKET-2026-09-28, [source/proof register](implementation-readiness.md#native-launch-preparation-2026-09-28). Следующие строки уточняют local-source knowledge, не меняют runtime gates на PASS. Local Hermes b22631ec4f349c64f50835c6d3434f89986ca05c; cached Codex 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a. Server survey остаётся dated evidence.

| Gates | Новое SOURCE_ONLY | Blocking proof |
|---|---|---|
| N-03/N-04 | Exec/TUI различаются manager imports/bootstrap; dotenv до main, env missing/empty допускает local snapshot; generic terminal не typed Codex input | B-SRC/B-LAUNCH/B-ISOLATION: definitions/all-tool dispatch и actual dual-CLI boundary |
| N-05/N-10 | Required checkpoint guard сохранён; filtered spool не full archive, prefetch не обязательная hydration, flush failure требует caller proof | B-HISTORY: originals/intent/result/crash/flush/current-context failures обоих harness |
| N-06 | Current/quarantine/rollback cleanup и managed stopped-container classification найдены в pinned updater | B-UPDATER: all-entry references/admission/drain/defer/races без изменения daily protections |
| N-08 | Первый native parent 3.2 установлен как цель, но exact runtime/test seam не найден; completed pure slice не изменён | 1.5.5 BLOCKED_PATH_DISCOVERY, Gate B; ни mock parser, ни invented test paths |
| N-09 | Separate manual new/attach/live/dead/recreate и worktrees сохранены как обязательные transitions | B-LIFECYCLE/B-HISTORY: actual SSH/TUI proof NOT_RUN |

N-01/N-02/N-07/N-11 не закрыты этим исследованием. E1 NOT_DEPLOYABLE; B-RESOURCE также блокирует admission. Full approval/readiness=false, ORCH-01 / CRITICAL открыт. Canary NOT_RUNNABLE, local source closure — следующий отдельно согласуемый scope.

## Native source follow-up 2026-09-28

E1-NATIVE-SOURCE-V2-2026-09-28, [readiness](implementation-readiness.md#native-source-follow-up-2026-09-28). Прежние preparation/survey строки — dated evidence, не текущая полнота source corpus. Ниже SOURCE_ONLY, не runtime PASS.

| Gates | Установлено | Remaining blocker |
|---|---|---|
| N-03/N-04 | Один reexported manager, SharedCliOptions; selected shell dispatch до remote backend/error propagation | B-LAUNCH/B-ISOLATION: bootstrap, hooks, patch/FS/extensions и actual exec/TUI boundary |
| N-05/N-10 | RolloutRecorder queue/flush/retry и Session append/compaction callers прочитаны | B-HISTORY: log-only append failure, replacement-before-append и ignored flush не mandatory checkpoint; store/crash/hydration proof open |
| N-08 | Upstream observation points известны; runtime adapter/test harness в workspace не выбран | 1.5.5/3.2 BLOCKED_PATH_DISCOVERY, Gate B; code children не добавлены |
| N-09 | Shared core не даёт automatic TUI acceptance | 3.7/SSH lifecycle, separate identity и mandatory history остаются open |

Остальные gates и updater protections не изменены; product 15/52, E1 NOT_DEPLOYABLE, full approval/readiness=false, ORCH-01 / CRITICAL открыт.
