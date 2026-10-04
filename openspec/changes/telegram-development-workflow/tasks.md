## 1. Owner approval and baseline gates

Production parents — будущая работа; отмеченные read-only children имеют [source discovery evidence](implementation-readiness.md#e1-source-discovery-2026-09-23), включая отрицательные findings, но не runtime acceptance. Исходные parent IDs/полные обязательства сохранены; D-27–34 меняют порядок приёмки. E1 — рабочая среда; E2 — последующие инкременты полного MVP1 (design.md#acceptance-increments). Для E1 закрыть относящиеся части 1.1–1.3/1.5 и N-09–11, затем получить exact revision + E1 scope approval в 1.6. N-07/1.4 и publication/offsite критерии остаются E2 blockers. Частичный gate/parent не отмечать выполненным целиком.

Историческая подготовка и current requirement/scenario/task mapping сведены в [current coverage](../adopt-openspec-workflow/audit.md#current-coverage). Наличие локального прототипа, source probe или mock результата не закрывает production outcomes; прежние разрешения действуют только в своих границах. Исходные parent IDs и полные критерии сохранены; завершение discovery child не означает завершение parent или runtime gate.

До 1.6 допустимы read-only исследования и отдельно разрешённый владельцем «+» 2026-09-28 pure local срез 3.1.1–3.1.8 из E1-LOCAL-PACKET-2026-09-28. Это не runtime/E1 approval: canary, установка, credentials, модели, server/updater и external effects отдельно. Repo `hermes-agent` выбран; [repo decision](implementation-readiness.md#repository-decision-2026-09-23). Остальные runtime interfaces/commands BLOCKED_PATH_DISCOVERY, ранние runtime/ пути не задания. Meaningful RED → минимальный GREEN → regressions, Git без staging/commit/remote. 1.5.5 сохраняет full code-parent criterion и остаётся open за пределами pure slice.

Малые discovery children ниже рассчитаны на 2–5 минут focused работы каждый; если исследование больше — остановить child на зафиксированном blocker и разбить дальше, не объявлять завершённым. Paths с префиксом `openspec/` или `.hermes/` даны от workspace; короткие document names — внутри `openspec/changes/telegram-development-workflow/`, а `scripts/`, `deploy/`, `tests/` в 1.5.1 — внутри указанного reuse-кандидата. Verify `V-DOC` и формат actual evidence определены в конце файла. Code parents 2–8 перед apply обязательно получают children с обнаруженными exact source/test paths, копируемой командой RED/GREEN и ожидаемой причиной/результатом; пока этого нет, их не исполнять.

- [ ] 1.1 Закрыть N-01/N-02 в native-capability-matrix.md: сверить installed source и разрешённый canary штатного Telegram approval/intake/Kanban; ожидается owner-only exact action, replay/restart без двойного запуска или явный blocker (TG-01–04).
- [ ] 1.2 Закрыть N-03/N-04: проверить subscription OAuth/refresh, CLI argv и изоляцию проектного кода от credentials на выбранном Codex; ожидается положительный запуск и отрицательный sentinel access test без API fallback (TG-05, ENV-01).
- [x] 1.2.1 Read-only: найти специализированный штатный Hermes Codex launch в `/Users/s060874gmail.com/.hermes/hermes-agent/tools` и официальной документации, проследить definition/schema/usages; записать exact source revision/пути или BLOCKED в native-capability-matrix.md N-03. Depends: нет; TG-04/05; verify: V-DOC и ссылка на настоящий source, не имя предполагаемой функции (2–5 минут).
- [ ] 1.3 Закрыть N-05/N-06: проверить реальные lifecycle memory callbacks и согласование существующего updater с задачами; ожидаются checkpoint readback и drain/defer evidence, а не только список функций (MEM-11, UPD-01–02).
- [x] 1.3.1 Read-only: сопоставить источник `.hermes/tooling/mempalace/provider/README.md` и installed lifecycle definitions с MEM-12; записать coverage completed-turn/tool-results/crash/hydration отдельно для Hermes/Codex в implementation-readiness.md и N-10. Depends: нет; verify: V-DOC, каждый непроверенный hook помечен UNVERIFIED, raw histories/credentials не читаются (2–5 минут).
- [x] 1.3.2 По baseline.md и `.hermes/tooling/mvp1-integration-prototype/test_current_updater.py` определить manual/detached session drain gap и границы existing policy; записать известные locks и неизвестное в implementation-readiness.md N-06/N-09. Depends: нет; UPD-01–02; verify: V-DOC, нет выдуманного lock order и server write, unresolved оформлен blocker (2–5 минут).
- [ ] 1.4 Закрыть N-07: проверить официальные условия/лимиты GitHub backup storage и размеры sample пакета; при непригодности получить новое решение владельца до upload (BACK-01–02).
- [ ] 1.5 Выбрать implementation repo и зафиксировать точные runtime/test paths, manifest commands, численные limits и порядок locks в существующем implementation-readiness.md; включить N-09–11, host-folder layout, history/hydration, SSH и extension adapters. Ожидается воспроизводимая карта без придуманных API и без второй очереди (ENV-01, TG-04, MEM-12, SSH-01–02).
- [x] 1.5.1 Read-only: повторить Git-проверку reuse-кандидата `/Users/s060874gmail.com/coding/projects/hermes-remote-migration`, связать `scripts/codex_runner.py` и `deploy/codex-runner/app/runner_service.py` с `tests/test_codex_runner_deployment.py`; записать reuse blockers в implementation-readiness.md. Depends: нет; N-08; verify: V-REUSE + V-DOC и exact definition/caller/test ссылки, без запуска fixtures (2–5 минут).
- [x] 1.5.2 Зафиксировать в implementation-readiness.md владельца server folder, требуемые классы данных/credential separation и worktree topology; actual host paths/UID/quotas только из подтверждённого discovery или BLOCKED. Depends: 1.5.1; ENV-01/MEM-12; verify: V-DOC, recreate не обещает прежний процесс и storage mount не объявлен готовым (2–5 минут).
- [x] 1.5.3 По официальным и установленным sources выбрать кандидата ordinary CLI session continuity и указать exact source/test paths либо BLOCKED в N-09/implementation-readiness.md. Depends: 1.2.1; SSH-01–02; verify: V-DOC, отдельно disconnect/reconnect/death/recreate, никакой установки/SSH/canary (2–5 минут).
- [x] 1.5.4 Заполнить в implementation-readiness.md compatibility matrix OpenSpec/MemPalace/skills/rules × Hermes/Codex с source pin и UNVERIFIED для непроверенной загрузки; выделить project-only layer. Depends: 1.3.1; N-11/TG-04; verify: V-DOC, ни один installed файл не выдан за successful runtime use (2–5 минут).
- [ ] 1.5.5 После выбора repo разложить первый code parent в tasks.md на 2–5-минутные RED/implementation/GREEN-regression children с exact discovered paths и командами; при отсутствии интерфейса оставить BLOCKED_PATH_DISCOVERY. Depends: 1.2.1, 1.3.1–1.3.2, 1.5.1–1.5.4; N-08; verify: V-DOC, нет guessed imports/placeholder test commands (2–5 минут на один parent).
- [ ] 1.6 Получить owner approval пересчитанной spec/design revision с явной областью E1 либо полного MVP1 и отдельный scope infrastructure/credential setup; pending→approved только по явному решению. E1 approval не закрывает N-07/E2 и не означает глобальную implementation_ready=true (TG-01, TG-09).

## 2. One admitted task survives replay and restart

- [ ] 2.1 Настроить owner/project binding и штатный intake; RED/GREEN: чужой Telegram user, неизвестный project и неутверждённая revision не запускают работу; разрешённый local E1 scope не требует и не создаёт remote repo (TG-01).
- [ ] 2.2 Проверить штатный task mapping на временном состоянии: duplicate update, crash-before-mapping и reopen дают одну задачу либо blocked, без собственного scheduler (TG-02).
- [ ] 2.3 Проверить cancel/release race и поздний результат: старое поколение не получает право публикации или запуска (TG-02, TG-06).

## 3. Scoped engineering execution

- [ ] 3.1 Подготовить pinned Dev Container и ресурсное admission; RED/GREEN: неразрешённый host mount/privileged/socket отвергнуты, approved project bind mount доступен только своему проекту, бюджет исчерпан — очередь ожидания, чужие сервисы сохранены (ENV-01, TG-05).
- [x] 3.1.1 RED closed fields/types, malformed IDs/digest и bool UID без normalization (ENV-01/TG-05 partial). Files: scripts/project_environment.py, tests/test_project_environment.py в P. Depends: scoped local approval «+». Verify: T1 -k rejects, exit 1 с assertion failure, не ImportError/SyntaxError/zero tests. Evidence: actual receipt в readiness. Size: 2–5 минут.
- [x] 3.1.2 GREEN минимальный строгий input contract (ENV-01/TG-05 partial). Files: scripts/project_environment.py. Depends: 3.1.1. Verify: T1 -k rejects exit 0 и valid fixture принят без ослабления negative tests. Evidence: actual receipt в readiness. Size: 2–5 минут.
- [x] 3.1.3 RED stable identity, collision pair и worker/private layout (ENV-01 partial). Files: tests/test_project_environment.py. Depends: 3.1.2. Verify: T1 -k layout exit 1, meaningful assertion; dict order не меняет identity. Evidence: actual receipt в readiness. Size: 2–5 минут.
- [x] 3.1.4 GREEN deterministic project/work/private paths без filesystem access (ENV-01 partial). Files: scripts/project_environment.py. Depends: 3.1.3. Verify: T1 -k layout exit 0, different owner/project разделены. Evidence: actual receipt в readiness. Size: 2–5 минут.
- [x] 3.1.5 RED exact compact/large resources и runtime_admitted=false (ENV-01/TG-05 partial). Files: tests/test_project_environment.py. Depends: 3.1.4. Verify: T1 -k resources exit 1 с assertion, unknown class/override не default. Evidence: actual receipt в readiness. Size: 2–5 минут.
- [x] 3.1.6 GREEN fixed data-only limits без admission, shared mutation или process/network/DB effects (ENV-01/TG-05 partial). Files: scripts/project_environment.py. Depends: 3.1.5. Verify: T1 целиком exit 0, input unchanged. Evidence: actual receipt в readiness. Size: 2–5 минут.
- [x] 3.1.7 Regression и scratch negative control (TG-07 partial, не runtime acceptance). Files: tests/test_project_environment.py; owned scratch copy только для mutation. Depends: 3.1.6. Verify: T1/T2/T3/T4 exit 0 без skips; accept-all mutation вызывает assertion failure, original unchanged. Evidence: exact commands/exit/hash в readiness. Size: 2–5 минут.
- [x] 3.1.8 Handoff/trackability без commit (DOC). Files: README.md, .gitignore, existing tasks.md/readiness. Depends: 3.1.7. Verify: backup wrapper до config edit; ровно два новых source paths admitted, nested auth/env/state denied; V-DOC и digest/progress согласованы, parent 3.1/E1 open. Evidence: actual checks в readiness. Size: 2–5 минут.
- [ ] 3.2 Подключить штатный запуск Codex exec: help parser и controlled fixture подтверждают fixed cwd/argv/stdin, nonzero/malformed/timeout не считаются success (TG-04–05).

Уточнение к 3.2: app-server/client-executor исследования остаются кандидатами, не утверждённой заменой Codex exec или обычного интерактивного SSH Codex. Конкретный native launch выбирается после N-03/N-08/N-09 и проверки model routing/credential boundary; native environment readiness и наличие Codex skill не закрывают этот пункт.

- [ ] 3.3 Создать две параллельные worktree одной задачи, включая manual/automatic writers, и независимый второй проект; тест подтверждает отсутствие общей записи, отдельные context packets, сохранение конфликтов и последовательную интеграцию с повторными тестами (TG-03, MEM-11–12, SSH-01).
- [ ] 3.4 Проверить отмену вместе с отделившимся потомком; cancelled только после подтверждения остановки task-owned процессов без остановки соседнего проекта (TG-06).
- [ ] 3.5 Подключить переносимую память и адаптеры: denied cross-project retrieval до чтения, conflict proposals сохранены, real pre-compression failure блокирует потерю контекста, rebuild/readback сохраняет полную исходную историю; новый Hermes и Codex автоматически получают current context, write/hydration failure блокирует продолжение (MEM-10–12). Knowledge PR/owner merge проверяется в E2, parent до этого не закрывается.
- [ ] 3.6 Закрепить общий OpenSpec/MemPalace/skill/tool/rules revision и отдельно проверить loading/use Hermes/Codex adapters; substitution/shared update без approval отклоняется, project tools/skills/dependencies автономны только в своей области и не меняют host/shared tools (TG-04, N-11).
- [ ] 3.7 Реализовать после N-09 отдельный ordinary interactive SSH Codex в том же контейнере проекта: manual identity/worktree, automatic current context, disconnect/reconnect возвращает ту же живую сессию без duplicate. RED/GREEN включает unknown project, unauthorized identity, Codex death и container destruction без ложной process continuity (SSH-01–02, TG-05, MEM-12).
- [ ] 3.8 Проверить reusable project container и server bind mount: следующая задача использует прежнюю среду; разрешённый recreate сохраняет Git/worktrees/WIP/specs/историю/results и восстанавливает контекст обоих harness. RED/GREEN включает недоступное хранилище и отделение credentials/чужого проекта; не имитировать offsite restore (ENV-01, MEM-12).

## 4. Verified candidate and downstream frontend

Trusted candidate verification нужна уже E1; полный frontend/dance-guide contract 4.1–4.3 относится к E2. Частичный ранний test pack не закрывает весь parent 4.3.

- [ ] 4.1 В согласованном contemporary-dance-guide сначала написать failing acceptance для preview/index.html: русский guide/demo labels, file:// без сети, desktop/mobile/keyboard. Зафиксировать настоящую команду browser runner перед реализацией страницы (PRE-01–02, TG-08).
- [ ] 4.2 Минимально реализовать preview/index.html и локальные assets без framework/build; GREEN подтверждает offline просмотр, корректные источники и отсутствие реальной отправки заявок/оплаты (PRE-01–02).
- [ ] 4.3 Проверить frozen candidate и tampered runner: заведомо неверная страница не проходит защищённый acceptance pack, изменение commit отменяет старый verified result (TG-07).

## 5. Review and controlled publication — E2

- [ ] 5.1 После credential setup approval проверить выделенный publisher: создаётся отдельный private repo под configured owner, credentials недоступны worker, repo privacy подтверждается exact readback (TG-09).
- [ ] 5.2 Проверить автоматические task-branch push/PR без approval на каждый push; затем штатное подтверждение merge и отказ после смены head commit. Реальный merge только по отдельному решению (TG-09).
- [ ] 5.3 Fault fixture: потерянный ответ/поздний PR/cancel не создают второй side effect; затем разрешённый canary подтверждает exact repo/branch/commit/PR readback (TG-10).

## 6. Telegram delivery and recovery

- [ ] 6.1 Проверить штатные route/notifications: исходный user/chat/topic, E1 отчёт содержит task/session/project/worktree/branch/revision, реальные изменения/tests и явные not_provisioned PR/preview; E2 добавляет repo/commit/PR/preview path. Недоставленное вложение не отмечается успешным; parent открыт до обоих этапов (TG-11).
- [ ] 6.2 Проверить gateway restart/failed send: повторная доставка использует сохранённый результат без нового Codex/test/PR run (TG-12).
- [ ] 6.3 Проверить ORCH-01 на dead worker и quiet build: detection до пяти минут при живом controller, bounded retries, unknown effects blocked; restart восстанавливает состояние без потери worktree. SSH disconnect при живой manual session не вызывает retry; production controller принимается отдельно от E1 (REC-01–02).

## 7. Backups and maintenance

7.1–7.4 и полный offsite contract 7.6 — E2. Safety cleanup 7.5 и относящиеся к active/manual sessions drain/defer/rollback checks 7.6 нужны уже E1; existing updater protections не отключаются ради промежуточной приёмки.

- [ ] 7.1 RED/GREEN compact snapshot: только изменившиеся проекты, unpublished commits/untracked файлы включены, credentials/cache/index исключены, искусственный секрет внутри checkpoint не попадает в пакет, активные записи не дают несогласованного пакета (BACK-01).
- [ ] 7.2 После N-07 и infrastructure approval проверить encrypted upload и exact GitHub readback; public key только на сервере, lost response reconciled, backup failure не выдаётся за успех (BACK-02).
- [ ] 7.3 Подготовить локальную restore-check команду и испытать на temporary target: manifest/checksums/commit dependencies восстановимы, код не запускается, рабочие проекты не перезаписываются (BACK-03).
- [ ] 7.4 Проверить owner-only Telegram attestation и retention: неверные ID/checksum отклоняются, старше 30 дней удаляется только при более новой verified copy с покрытием того же owner/project scope; backup B не разрешает удаление A, последняя и зависимости защищены (BACK-03).
- [ ] 7.5 Проверить ownership cleanup с race admission: чужие образы/сети, активные worktrees, detached manual sessions и пользовательские данные/история не удаляются (ENV-02).
- [ ] 7.6 На fixture существующего updater проверить drain/defer automatic/manual/detached sessions, backup failure, lock ordering, candidate failure и rollback; полный E2 offsite gate не закрывается E1. Daily stable policy сохраняется, изменение `/srv/hermes-agent/bin/hermes_stable_updater.py` только после отдельного разрешения (UPD-01–02).

## 8. Final acceptance

- [ ] 8.1 Выполнить разрешённый Telegram → согласование → Codex → tests → private PR → ручной Git/file:// preview journey для contemporary-dance-guide; сохранить действительные receipts в acceptance.md (новый документ по факту), без server preview (TG-01–12, PRE-01–02).
- [ ] 8.2 Выполнить согласованные restart/отказ provider/backup/maintenance сценарии без вреда работающему стеку; зафиксировать отсутствие внешнего host monitoring и проверить уведомление после возврата (REC-01–02, UPD-01–02, BACK-01–03).
- [ ] 8.3 Выполнить `./run-openspec validate --all --strict --json`, собрать exact candidate/spec receipts и получить owner runtime acceptance. Только после этого решать archive и закрытие минимального этапа ORCH-01; structural pass сам по себе недостаточен.
- [ ] 8.4 Первая промежуточная приёмка E1: разрешённый Telegram → Hermes/Codex → реальные code changes/tests → отчёт без обязательных PR/preview; параллельный SSH Codex, reconnect той же session, tested integration, recreate/full-history/automatic-context recovery. Trusted checks должны отвергать faulty candidate/tampered runner и stale revision. Сохранить реальные command/exit/assertion/candidate/spec/environment receipts в acceptance.md только после выполнения; отдельно перечислить открытые E2/ORCH-01 и owner acceptance именно E1 (TG-07–08, SSH-01–02, MEM-12, ENV-01).

Порядок: относящийся E1 discovery/approval → 2.x/3.x → E1 verification/delivery/maintenance safety → 8.4; затем согласованные E2 срезы 4.x/5.x/6.3/7.x → 8.1–8.3. Номер исходного parent не является жёстким chronological order. Каждый original parent закрывается только по полному критерию, не по новой подпроверке E1.

## Discovery Verification Commands

T1–T4 для разрешённого pure slice, cwd P `/Users/s060874gmail.com/coding/projects/hermes-agent`; Python stdlib, no install:

```sh
PYTHONPATH=scripts python3 -B -m unittest discover -s tests -p test_project_environment.py -v
python3 -B .hermes/research/telegram-hermes-codex/probe_runner_reuse.py
python3 -B -m unittest discover -s .hermes/tooling/mvp1-integration-prototype -p test_current_updater.py -v
python3 -B -m unittest discover -s .hermes/research/telegram-hermes-codex/native-codex -p test_environment_gate.py -v
```

Для focused T1 добавить `-k rejects`, `-k layout`, `-k resources`. T2 donor queue tests — regression, не импорт queue. Полный research suite не заявляется: unrelated test_stock_lifecycle.py повреждён. Proposed paths стали отдельно разрешёнными новыми файлами, не discovered native API. Фактические counts/RED/GREEN фиксируются после запуска.

V-DOC (cwd `/Users/s060874gmail.com/coding/projects/hermes-agent`; только структура/прогресс, не runtime):

```sh
./run-openspec validate telegram-development-workflow --strict --json
./run-openspec instructions apply --change telegram-development-workflow --json
```

Ожидается exit 0 каждого вызова, valid=true/без ERROR и фактический progress, в котором ни один незавершённый parent не закрыт. Дополнительно вручную проверить указанный в child source/таблицу: точные paths/revision, known vs UNVERIFIED, ожидаемый и фактический результат. Structural pass один не закрывает child discovery.

V-REUSE (read-only; ненулевой exit означает blocker, состояние не подменять историческим SHA):

```sh
git -C /Users/s060874gmail.com/coding/projects/hermes-remote-migration status --short
git -C /Users/s060874gmail.com/coding/projects/hermes-remote-migration branch --show-current
git -C /Users/s060874gmail.com/coding/projects/hermes-remote-migration rev-parse HEAD
```

Ожидается exit 0 и реальные status/branch/full SHA; чистое дерево или конкретный SHA не предполагаются заранее. До запуска tests дочитать setup/fixtures/side effects. Actual evidence каждого выполненного child записывается рядом с соответствующим gate в implementation-readiness.md/native-capability-matrix.md: task ID, source revision/path, command/tool, exit/result, limitations. Ни один child этого списка не выполнен самим обновлением требований 2026-09-23.

## Native launch blocker 2026-09-28

E1-NATIVE-PACKET-2026-09-28: 1.5.5 остаётся BLOCKED_PATH_DISCOVERY. Первый следующий code parent — 3.2, проверка actual native exec denial до task/tool effect при invalid/absent required environment; separate TUI parent 3.7 не наследует exec result. Недостающие определения: codex_app_server_client::EnvironmentManager, codex_exec_server::EnvironmentManager, SharedCliOptions, actual tool dispatch и RolloutRecorder/flush/compaction callers на pinned Codex commit. Их точные пути устанавливаются по upstream tree, не угадываются. Generic terminal/fake environment_gate не подмена native seam.

Новых code/test paths, RED/GREEN commands и checkbox children в этом Gate B нет. Минимальное продолжение — отдельно разрешённый bounded public-source retrieval из [пакета](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#native-codex-preparation--e1-native-packet-2026-09-28), затем exact failing test/implementation/regression/negative-control contract и отдельный local Apply approval. History/isolation/lifecycle/resources/updater runtime blockers остаются в readiness. 3.1.1–3.1.8 и все production parents сохраняют прежний статус; docs Update не разрешает canary/server/model/credentials/commit/push.

## Native source follow-up 2026-09-28

E1-NATIVE-SOURCE-V2-2026-09-28 уточняет blocker выше, не меняет checklist. EnvironmentManager reexports, SharedCliOptions, RolloutRecorder и selected shell/compaction callers уже найдены. 1.5.5 остаётся BLOCKED_PATH_DISCOVERY именно runnable local harness/adapter; первый launch parent 3.2, отдельный TUI 3.7. B-HISTORY теперь опирается на Session log-only append failure, replacement-before-append и ignored resume/fork flush; 3.5/3.8 не закрыты.

Перед code Apply выбрать обязательную history/admission boundary, затем предъявить actual native fault test: write/checkpoint failure блокирует дальнейший effect/compaction; durable own-project positive control проходит; originals/incomplete attribution восстанавливаются. Registry hooks и apply_patch interception не исключать из отрицательного охвата. [Source points и точные ограничения](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#native-source-follow-up--e1-native-source-v2-2026-09-28). Пока нет команды RED/GREEN и новых child IDs; methods upstream не выдаются за локальный test harness. Product 15/52, E1/ORCH-01 open, runtime/canary/server/model/credentials/Git writes не разрешены.
