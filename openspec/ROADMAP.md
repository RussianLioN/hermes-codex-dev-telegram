# Инкрементальное продолжение разработки

Эта roadmap — индекс outcomes и зависимостей, не вторая очередь, не набор новых changes и не разрешение реализации. Canonical [product tasks](changes/telegram-development-workflow/tasks.md) сохраняет полный критерий каждого parent; [Capability Map](changes/telegram-development-workflow/design.md#capability-map) задаёт зависимости контрактов. Runtime attempts принадлежат Hermes Kanban. Текущий продукт NOT_DEPLOYABLE; checklist условный, не implementation-ready план кода. По интервью 2026-09-23 первая приёмка E1 — рабочая среда; E2 объединяет последующие PR/demo/offsite/recovery инкременты полного MVP1, не отменяя их.

## Increment Rules

Один инкремент даёт один наблюдаемый результат. Focused task занимает 2–5 минут; если больше — до исполнения разбить на проверяемые children. Оценка не обещает длительность сети/тестов. План показывается владельцу в тексте чата; файл — дополнительный canonical артефакт.

| Field | Обязательное содержание |
|---|---|
| ID | Existing parent и уникальный child, например X.Y.1; не терять исходный parent ID |
| Outcome | Один наблюдаемый результат без расширения scope |
| Criterion | Requirement/scenario либо DOC criterion; сохранить полный parent criterion |
| Files | Exact source/test/document paths, проверенные discovery; неизвестные — BLOCKED_PATH_DISCOVERY |
| Depends on | IDs prerequisites и нужные approval/readiness gates |
| Verify | Точная команда, cwd, ожидаемый exit/assertion или документарный tabletop |
| Evidence | После исполнения actual command/exit/assertions, source/candidate revision, path receipt, limitations |
| Size | 2–5 минут focused действия; больший task сначала декомпозировать |

Для кода: manifests → definitions/usages → meaningful behavior test RED с нужной причиной → минимальный GREEN той же командой → regressions. Не выдумывать imports/runner; повреждённый source не meaningful RED. Для docs: links/headings/membership + semantic review, не dummy tests. Для API effects нужны собственный grant и exact readback; unknown сначала reconciliation.

Декомпозиция product tasks обновлена отдельным согласованным planning update, не задним числом в docs seed. Малые discovery children находятся в canonical tasks; остальные code children блокируются неизвестными paths/interfaces до discovery. Children X.Y.1 и далее не закрывают parent частичным успехом; полные criteria/IDs сохраняются, progress пересчитывается parser. Requirements не дублируются как ADDED в umbrella и отдельном change; новый самостоятельный intent получает отдельный небольшой change, не change на каждый checkbox.

Один writer shared artifacts; независимые read-only lookup можно параллелить. Параллельные product writers требуют отдельные worktrees и последовательную интеграцию с повторными tests. Subagent/cross-model capability не предполагается по наличию skill. Владелец отдельно разрешил local Git init текущего `hermes-agent`; он выполнен без initial commit. Frequent commits, remote/push и worktree bootstrap — после отдельного permission/review, не автоматически от roadmap. Рабочий процесс — [WORKFLOW](WORKFLOW.md).

## Dependency Map

| Slice | Original product task IDs | Один outcome и зависимости | Что не считать выполнением |
|---|---|---|---|
| I0 — readiness | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6 и их children | N-01–N-11, repo/runner/paths, limits/locks; E1 требует относящиеся N-01–06/N-08–11, E2 добавляет N-07/publication/offsite. Затем exact revision + increment scope approval и отдельные infrastructure grants; [native matrix](changes/telegram-development-workflow/native-capability-matrix.md) | SOURCE_PRESENT/OpenSpec ready/mock не native acceptance; partial E1 не закрывает full gates |
| I1 — один допущенный intent | 2.1, 2.2, 2.3 | После относящихся I0 gates один owner/project/revision-bound intent переживает replay/restart/cancel без нового неразрешённого run; [task-intake](changes/telegram-development-workflow/specs/task-intake/spec.md) | Не отдельный scheduler/approval service; unknown create не повторяется слепо |
| I2 — рабочее окружение и candidate | 3.1–3.8 | I1 + I0: один reusable container/project, server bind mount, full history/automatic context, отдельный ordinary SSH Codex с reconnect, manual/automatic worktrees и tested integration, shared/project extension levels, fenced cancellation | Mount не hydration, local autosave не full-history evidence; surviving SSH не surviving destroyed process; credential boundary проверяется отдельно |
| I3 — один verified preview, E2 | 4.1, 4.2, 4.3 | I2 → offline [local-preview](changes/telegram-development-workflow/specs/local-preview/spec.md) и trusted [verification](changes/telegram-development-workflow/specs/verification/spec.md) frozen candidate; trusted checks нужны и E1 без обязательного demo | HTML/screenshots/always-pass runner не acceptance; E1 не закрывает полный frontend parent 4.3 |
| I4 — один controlled PR, E2 | 5.1, 5.2, 5.3 | I3 + publisher credential/infra grant → private repo/task branch/PR с [exact publication readback](changes/telegram-development-workflow/specs/change-publication/spec.md); merge отдельно owner-controlled | Local project E1 не требует раннего remote repo; lost response не отсутствие эффекта; mock PR не реальный PR |
| I5 — доставка и recovery | 6.1, 6.2, 6.3 | E1: I1/I2 → truthful Telegram changes/tests report и retries без нового run, без обязательных PR/preview. E2 добавляет I4 reconciliation и production controller acceptance | [telegram-delivery](changes/telegram-development-workflow/specs/telegram-delivery/spec.md) не prerequisite ingress; no stdout/SSH disconnect не stall. Partial report не закрывает parent 6.1; ORCH-01 открыт |
| I6 — сохранность и maintenance | 7.1–7.6 | E1: I2 + manual/detached session ownership/drain/defer и сохранение updater protections. E2: I4 refs + I5 state, N-07/grants → changed-only backup/restore/retention и полный UPD-02 | Existing daily auto-update policy не отключается; E1 не offsite readiness, checksum не restore attestation; второй updater/global prune запрещены |
| I7 — acceptance по этапам | 8.1–8.4 | Сначала 8.4: E1-части I0/I1/I2/I5/I6 + trusted checks → рабочая среда с SSH/history recovery. Затем E2 I3/I4 и полные I5/I6 → 8.1–8.3 Telegram→tests→PR→file://, faults/restore и exact owner acceptance | E1 не full MVP1, ORCH-01 или archive; structural pass не runtime acceptance |

ORCH-01 / CRITICAL готовится уже в I0 (independent controller/heartbeat/containment contracts), проверяется локально рядом с I2 и принимается на полном I5/I7 evidence с нужными dependencies. Это не отложенная косметика. Порядок строк — топологический обзор outcomes, не запрет раннего bounded recovery research. Отдельный профиль сам по себе не запускает надёжный monitoring/restart.

## Next Ready Work

Документационный маршрут готов: [README](README.md) → [PROJECT](PROJECT.md) → WORKFLOW → эта карта → выбранный change. Исторический `seed-project-documentation` имеет собственные [tasks](changes/seed-project-documentation/tasks.md) и [verification](changes/seed-project-documentation/verification.md); его receipts не переписываются. R1-current/R2-current/R3 применены; [current coverage](changes/adopt-openspec-workflow/audit.md#current-coverage) сверяет все текущие scenarios/task IDs. AGENTS gate остаётся отдельным; product implementation не начат.

Bounded source discovery E1 выполнен для children 1.2.1/1.3.1–1.3.2/1.5.1–1.5.4; actual findings и [decision packet](changes/telegram-development-workflow/implementation-readiness.md#decision-packet-and-c13-stop-gate) не являются рабочей средой. Task 1.5.5 и все production parents остаются открытыми. Следующий маршрут до кода:

1. Repo decision получен: текущий `hermes-agent`, local Git создан; [selective donor reuse](changes/telegram-development-workflow/implementation-readiness.md#repository-decision-2026-09-23) из `hermes-remote-migration`. Candidate не разворачивать целиком: own queue, --ephemeral, bounded logs и destructive job workspace не переносятся. Native app-server не подменяет exec/manual CLI и конфликтует с required checkpoint.
2. Предъявить отдельный bounded read-only server inventory scope до SSH. Actual version/UID/mount/layout/session-manager/updater source неизвестны; не full inspect/env/config и не auth/model/inventory calls. Ежедневный updater не ослаблять.
3. С actual interfaces согласовать credential-safe full history/hydration, manual session tracking и lock/admission graph; затем runnable RED/GREEN plan 1.5.5, exact revision/scope approval и отдельный code/canary apply. Тесты candidates не запускались; полный fixture side-effect audit до их запуска обязателен.

Это последовательность исследования, не новый checkbox tracker и не blanket canary permission. Пока карта runtime/interfaces неизвестна — BLOCKED_PATH_DISCOVERY даже при выбранном repo. Здесь не назначаются guessed runtime/test paths и команды. Для других независимых docs intents доступен обычный propose; product approval по-прежнему отдельный gate.

## Blocked Work

- Product implementation: [review-status](changes/telegram-development-workflow/review-status.json) pending/owner_approved=false, [readiness](changes/telegram-development-workflow/implementation-readiness.md) NOT_READY. CLI state=ready не отменяет эти ограничения.
- N-01–N-11, actual model routing/credential isolation, full-history/hydration, ordinary SSH continuity, extension adapters, publisher grants, backup suitability, численные limits и lock ordering. Невозможность контракта возвращается владельцу как proposed revision, не молча исключается из acceptance.
- OS-07 / adoption 3.4: [current reconciliation](changes/adopt-openspec-workflow/reconciliation.md#current-reconciliation), отдельное подтверждение и successful protected write; R1-current/R2-current/R3 уже применены. Seed не обходит прежний timeout.
- Broken stock lifecycle test и MEM-02b — [PROJECT gaps](PROJECT.md#constraints-and-gaps), не скрытые задачи docs apply.
- ORCH-01 / CRITICAL не реализован. OpenSpec/MemPalace/toy-controller не production recovery; потеря целого host не покрыта внешним monitoring в MVP1.
- Runtime/canary/server/profile/OAuth/dependency/publication/merge/deployment, sync/archive и Git writes не разрешаются существованием roadmap. Старые one-shot scopes не переиспользовать. При отдельном config/dependency/update scope соблюдать backup policy.

Единый операторский индекс открытых вопросов — [tasks/todo.md](../tasks/todo.md#текущий-операторский-индекс--openspec-reconciliation). Исторические исследования и [current audit](changes/adopt-openspec-workflow/audit.md#current-coverage) помогают выбрать следующий check, но не выдают права и не закрывают parent criterion.
