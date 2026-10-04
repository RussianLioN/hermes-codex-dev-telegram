# Проверка seed-project-documentation

## Baseline

Дата: 2026-09-22, MSK. Cwd всех команд: `/Users/s060874gmail.com/coding/projects/hermes-agent`. Разрешение пользователя: «почини обновление индекса MemPalace и обнови индекс и следующим шагом Применяй seed-project-documentation». Это docs apply предъявленных proposal/design/tasks и scoped local index refresh; не product implementation/deployment/approval, не разрешение менять AGENTS или старые changes.

| Реальная проверка | Exit | Наблюдение |
|---|---|---|
| `./run-openspec --version` | 0 | 1.13.0 |
| `./run-openspec context --json` | 0 | Точный workspace, repo-local |
| `status --change seed-project-documentation --json` через wrapper | 0 | Planning complete; specs skipped |
| `instructions apply --change seed-project-documentation --json` через wrapper | 0 | Исходно 0/22, state=ready; contextFiles прочитаны |
| `status` и `instructions apply` обоих прежних changes | 0 каждая | adopt: 23/26; product: 0/33; planning complete |
| `./run-openspec list --specs` | 0 | No specs found |
| `./run-openspec validate --all --strict --json` | 0 | 3 passed / 0 failed; два INFO skip_specs |
| `git status --short`, `git branch --show-current` | 128 каждая | not a git repository; git init не выполнялся |
| V5: SHA256 sorted relative path + NUL + bytes | 0 | PRODUCT REVISION MATCH; APPROVAL PENDING; ORCH-01 OPEN |

Product spec digest: `29163c1de50e501a82f85cc72ada9f011520a3a17828ee0027adf006b22c729f`; product tasks SHA256: `9af6a6611582df65c9f7ff3d6ec097b283183a31960696bbe7ed47d90990604e`.

В terminal environment сохранён `SEED_APPLY_BASELINE`: hashes 231 файла (AGENTS/config/семь scripts, все файлы двух прежних changes и .openspec.yaml/proposal/design этого change). Aggregate SHA256 sorted path + NUL + bytes: `5dab6e15465468aabb24530c43f989d97cd0983560e5260677bc5dac4a65afcd`. Индекс, private state, credentials и vendor не входят в baseline.

| Неизменяемый source | SHA256 до apply |
|---|---|
| AGENTS.md | 00752daf4f84687625ef21227931d6af8f208dfb7454a5ce702934f4f4e4618d |
| openspec/config.yaml | 1af1dc4a909a35f28c1327f225efece03bfb4b24b2df6b3073474a6dd80025e1 |
| run-hermes | e41882100a3742e6d68c4331e44014f7a7e72be4e031f02c34ff987f89d77ba5 |
| backup-hermes-oauth | 2f8b3fa769d2a24e04e5c92beb9535c371ce93ee9b4b66c79dc230cd632b561a |
| update-hermes-stable | 0a1e84acf25c5deedca0e9b4f054a6e578060884d95e0a587c147df2b681f39f |
| configure-hermes-pilot-ssh | 571c4282c8655afd079b9813d19b55fd03eef20ce056ee99eae4e54e194fc1f7 |
| configure-codex-sandbox | 27c6053a26f7245206f5dc02f3cdb8899f8e2340285df8300b62d4e4e773be91 |
| run-openspec | ebe9541604f0605221d1174fdb5ea03ca506932db57ca8d34813a6429db66d7d |
| run-mempalace | b573ea2cda207e61138127251b26839c1470688a3b6ffd771d02a8ee7142047d |

## Results

### Предварительное восстановление индекса

`HF_HUB_OFFLINE=1`, `PYTHONDONTWRITEBYTECODE=1` заданы в session environment; wrapper отключает telemetry. Изменения кода, конфигурации, dependencies, rebuild/delete palace не понадобились.

| Реальная команда/операция | Exit / результат | Ограничение |
|---|---|---|
| `./run-mempalace --version`, `mine --help`, `instructions mine` | 0; 3.9.0, project mining | Инструкции не являются permission расширять corpus |
| `mine tasks --wing hermes-agent --agent hermes-default --dry-run` | 0; один source | Без filing |
| `mine openspec --wing hermes-agent --agent hermes-default --dry-run` | 0; обнаружено 225 files, processed 224, skipped 1 | Skip может быть short/non-indexable; scope только openspec |
| `./run-mempalace mine tasks --wing hermes-agent --agent hermes-default` | 0; processed 0, skipped 1, filed 0 | Источник уже в индексе |
| `./run-mempalace mine openspec --wing hermes-agent --agent hermes-default` | 0; processed 4, skipped 221, filed 77 | Индексированы новые planning artifacts, не весь home |
| CLI search `seed-project-documentation первичный посев DOC-06`, wing hermes-agent | 0; новые proposal/tasks присутствуют | До refresh этот запрос возвращал старые документы |
| Первый MCP search | FAILED, stdio subprocess lost | Не является corruption; write не выполнялся этим search |
| CLI `status` и повторный search после disconnect | 0; индекс доступен, новые tasks видны | Проверка состояния до повторного MCP обращения |
| Exact-source MCP search, затем get_drawer | Успех; source_path — новый proposal, drawer `drawer_hermes-agent_general_d795a4a1fe1f270d2d301658` | Точный фрагмент Impact совпал с перечитанным proposal |

Причина прежнего незавершённого refresh: операция не запускалась после timeout подтверждения отдельной команды проверки. Не доказан дефект miner. Предупреждение об отсутствии `openspec/mempalace.yaml` не меняет явно заданный `--wing hermes-agent`; дополнительная конфигурация не нужна. Процессные сбои MCP не обходятся удалением/пересозданием данных; сначала проверяется CLI state.

### Документационные задачи

Новые runtime tests/canary/browser/model turns не выполняются; evidence здесь — source/document checks и реальные локальные CLI операции. Cwd всех команд указан в Baseline; `check_doc` и `check_product_coverage` — read-only helpers из design.

| Task | Criterion | Actual command / inspection | Exit / result | Source / limitation |
|---|---|---|---|---|
| 1.1 | DOC-06 | Baseline-команды выше; `check_doc openspec/changes/seed-project-documentation/verification.md '## Results'` | 0; DOC OK; повторное сравнение 231 protected hashes — MATCH | Прочитаны все contextFiles; это не runtime acceptance |
| 1.2 | DOC-05 | `check_doc openspec/changes/seed-project-documentation/research.md '## Sources'`; review Sources/Applied Practices/Limitations | 0; DOC OK | S1–S9/H1 с датами и pin; source review, не independent council |
| 2.1 | DOC-01 | `check_doc openspec/PROJECT.md '## Scope'` | 0; DOC OK | Workspace/external/product разделены; root test runner не придуман |
| 2.2 | DOC-01 | Source review run-hermes/backup/updater; `/bin/zsh -n` семи entrypoints; check_doc Existing Operations | 0; syntax stdout пуст, DOC OK | SOURCE_ONLY + syntax, не исполнение операций; --check network, safe root и ZIP limitations отражены |
| 2.3 | DOC-01 | Source review SSH/sandbox/OpenSpec/MemPalace; payload decode без исполнения; тот же syntax check и check_doc | 0; DOC OK; INVENTORY/ANCHOR OK: 7 entrypoints | Mutating provisioning и mine отделены от inspection; private SSH state не читался |
| 2.4 | DOC-01 | Manifest/README review, `check_doc openspec/PROJECT.md '## Tooling and Evidence'` | 0; DOC OK | Pinned/historical versions; MEM-02b открыт, redaction не guarantee; unrelated suites NOT_RUN |
| 2.5 | DOC-01 | Prototype README/audit/research inventory review; тот же check_doc | 0; DOC OK | Canonical historical evidence links; vendor/generated/state исключены из собственного runtime inventory |
| 2.6 | DOC-01 | `check_doc openspec/PROJECT.md '## Architecture'`; exact `## Capability Map` assertion в product design | 0; DOC OK; anchor найден | Раздельные as-is/proposed схемы, NOT_DEPLOYABLE и ORCH-01 not implemented |
| 2.7 | DOC-01 | check_doc Data and Trust Boundaries / Constraints and Gaps; readiness/review/reconciliation review | 0; оба DOC OK | Owners/privacy/gates указаны; private state не читался; repo/runner/MEM-02b/broken test открыты |
| 3.1 | DOC-02 | `check_doc openspec/README.md '## Start Here'`; onboarding/quick-start review | 0; DOC OK | Все quick-start команды inspection, PLAN/apply/approval различены |
| 3.2 | DOC-05 | Полное чтение первых шести specs и product tasks, `check_doc .../coverage.md '## Product Coverage'` | 0; DOC OK для partial таблицы | Evidence из canonical audit; acceptance не переписана |
| 3.3 | DOC-05 | Полное чтение оставшихся шести specs, `check_product_coverage coverage` | 0; 12 capabilities, 25 requirements, 58 scenarios, 33 parent tasks | Scenarios найдены в canonical audit, а не скопированы |
| 3.4 | DOC-05 | check_doc coverage Documentation Criteria; повтор coverage mode | 0; DOC OK и те же counts | DOC-01–06, canonical owner/remaining gate, classification current/draft/historical/blocked |
| 4.1 | DOC-03 | `check_doc openspec/ROADMAP.md '## Dependency Map'`; `check_product_coverage all` | 0; DOC OK, 12/25/58/33 | I0–I7 со всеми IDs; roadmap без checkbox tracker |
| 4.2 | DOC-03 | check_doc ROADMAP Next Ready Work / Blocked Work; coverage all; readiness source review | 0; оба DOC OK, тот же coverage | Нет invented repo/test paths; N-08 discovery и ORCH-01 с I0, не postponed cosmetic |
| 4.3 | DOC-04 | `check_doc openspec/WORKFLOW.md 'openspec/ROADMAP.md'`; Python difflib + baseline | 0; DOC OK, только insert opcodes | Exact before/after ниже; approval/archive/security sections сохранены |
| 4.4 | DOC-02/DOC-04 | check_doc README Continue Development и TODO seed-project-documentation; exact diff/history equality | 0; оба DOC OK, TODO historical suffix identical | Одна operator link, без новых checkboxes; старые gates не закрыты |
| 5.1 | DOC-06 | `./run-openspec validate seed-project-documentation --strict --json`; `./run-openspec validate --all --strict --json`; installed parseTaskLines vs CLI; individual zsh -n; read-only full docs checker | 0; 1/1 и 3/3 valid, 0 failed, только INFO skip_specs; task accounting совпало (checkpoint seed 10/22, adopt 23/26, product 0/33); 11 docs, 168 local links, 27 anchors, coverage 12/25/58/33 | Protected 231 hashes и aggregate MATCH; product revision/approval/ORCH unchanged; main specs пусты. Counts ссылок относятся к этому checkpoint до дополнения отчёта |
| 5.2 | DOC-06 | Source/document review двенадцати cases ниже; per-row requirement IDs/task membership и anchors | PASS в заявленном docs scope | Review текущего исполнителя, не независимый council/model и не runtime acceptance |
| 5.3 | DOC-01/DOC-02/DOC-03/DOC-04/DOC-05/DOC-06 | Исправления findings ниже; повтор full checker | 0; все file/anchor/membership/preservation/exact diff assertions PASS | Только allowlist docs и ephemeral scratch checks; продукта/config/AGENTS/tooling edits нет |
| 5.4 | DOC-06 | Offline `mine tasks`, `mine openspec`, CLI search `seed-project-documentation PROJECT ROADMAP`; MCP reconnect/exact search/get_drawer; source ROADMAP:40–62 | Все CLI exit 0; tasks processed 1/filed 29; openspec processed 8/skipped 223/filed 184; CLI нашёл README/ROADMAP/PROJECT; exact-source MCP readback PASS после reconnect | Только разрешённые corpora, без model download; stale MCP index устранён штатно, код/config не менялись |
| 5.5 | DOC-06 | Финальная сверка criterion/evidence, повтор V1/V2/V5/coverage, installed parser/CLI; после этой записи — повтор scoped mine/reconnect/exact readback | До closing edit все checks exit 0: 11 docs, 168 links, 27 anchors, 12/25/58/33 coverage, protected 231 MATCH; parser seed 21/22, остальные 23/26 и 0/33; единственная оставшаяся запись — этот handoff | Final post-write receipt фиксируется terminal/MCP output, а не новой правкой документа после mining; при failure completion снимается и записывается MEMORY_REFRESH_BLOCKED |

### Подтверждённое восстановление MCP после CLI refresh

Первый vector MCP search с `wing=hermes-agent`, `source_file=/Users/s060874gmail.com/coding/projects/hermes-agent/openspec/ROADMAP.md` и query `Документационный маршрут готов N-08 source discovery` вернул `results=[]`, хотя свежий CLI search видел ROADMAP. Более широкий union/BM25 search нашёл новый source: это не отсутствие документа в persistent storage.

Штатный `mempalace_reconnect` предназначен для stale in-memory HNSW после внешних CLI writes; вызов вернул success=true, vector_disabled=false. Повтор ТОГО ЖЕ exact-source vector query вернул `drawer_hermes-agent_general_73096df21e103d58ae684e48`, source_path ROADMAP, фрагмент Next Ready Work. `get_drawer` вернул полный фрагмент, сверенный с ROADMAP:39–45. Это воспроизведённая проблема stale MCP view и проверенное восстановление connection/index handle, не исправление miner source и не rebuild/delete palace. Маршрут добавлен в PROJECT Existing Operations.

Helper incident: после восстановления контекста shell function `check_doc` отсутствовала, первый вызов exit 127; следующая syntax команда из `&&` тогда не запускалась. Read-only helper заново загружен из просмотренного design, повторный check и syntax дали exit 0. Shell functions не считаются персистентными: текст helpers сохранён в `SEED_DOC_HELPERS` и определяется через `eval` в том же вызове. Это не software defect проекта и не установка пакета.

Дополнительная syntax проверка выполнена отдельно для каждого из семи scripts через `subprocess.run(['/bin/zsh','-n',name])`: все exit 0, stdout/stderr пусты. Один `zsh -n` со списком filenames не считается проверкой каждого файла.

V2 helper limitations: полный ранний прогон вернул exit 1 только на `verification.md`: regex принял literal README.md внутри exact diff за ссылку verification. Полный read-only checker в `/Users/s060874gmail.com/.hermes/cache/scratch/seed-docs-check.py` исключает из Markdown links только fenced diff, а сам diff сравнивает побайтно с actual difflib output WORKFLOW/TODO; ссылки исходных WORKFLOW/TODO проверяются отдельно. Проверка не ослаблена до игнорирования документа. Scratch script — одноразовая проверка, не новый maintained test framework; может быть удалён автоматической cache cleanup. Для воспроизведения достаточны V1–V5 плана/design, семантика fenced diff и сохранённый exact diff этого отчёта.

## Semantic Review

Это source/document review текущего исполнителя. Проверены документационные маршруты, не реальные product flows; независимый review/council/model не заявляется. Классификация также учитывает readability (одна точка входа), architecture (без нового tracker), security (без дополнительных прав) и performance (runtime не меняется, profiling не нужен).

| Case | Expected route | Actual reference | Finding |
|---|---|---|---|
| 1. Zero-context onboarding | Реальный inventory, не придуманный application runner | README Start Here → PROJECT Scope/Existing Operations, семь scripts | PASS / Completeness: все entrypoints имеют source/input/output/failures/effects |
| 2. Docs-only skip | Один intent, explicit skip_specs, без фиктивного requirement | WORKFLOW §4, seed proposal Capabilities и metadata, research S1/S6 | PASS / Correctness: specs skipped, main specs пусты |
| 3. Behavior feature/TDD | Delta/scenario → exact discovery → отдельный apply → RED/GREEN/regression | WORKFLOW §4–6, README Continue Development, ROADMAP Increment Rules | PASS / Coherence: отсутствующие source/test paths не выдаются за готовые |
| 4. Нет implementation repo | NOT_READY/BLOCKED_PATH_DISCOVERY, сначала N-08 | ROADMAP Next Ready Work/Blocked Work → product implementation-readiness | PASS / Correctness: historical runner не принят, второй scheduler не создаётся |
| 5. Historical/mock/canary | Сохранить масштаб и дату, не объявлять live | PROJECT Tooling and Evidence → audit E0–E6; coverage Classification | PASS / Correctness: failed/expectedFailure/NOT_RUN не скрыты |
| 6. PLAN boundary | Только plan path, без new change/mine/apply | README Continue Development; WORKFLOW вводный приоритет текущего scope | PASS / Coherence: workflow не расширяет узкий turn permission |
| 7. Skill есть, loading неизвестен | Читать installed skill + настоящий CLI fallback | README Continue Development; WORKFLOW §7/9; audit Integrations | PASS / Correctness: нет выдуманного slash invocation или openspec verify |
| 8. R1–R3 / OS-07 pending | Отдельный approval/protected write, не обход | README Open Gates → TODO/reconciliation; protected hashes | PASS / Security: AGENTS/product/config unchanged |
| 9. Task больше пяти минут | Проверяемые children с сохранением parent criterion/ID | ROADMAP Increment Rules, additive WORKFLOW §6 | PASS / Completeness: поля ID/Outcome/Criterion/Files/Depends on/Verify/Evidence/Size, parser recount |
| 10. Restart/stall | Independent bounded recovery, не память вместо controller | PROJECT Constraints, ROADMAP I0/I2/I5/I7 → task-recovery spec | PASS / Coherence: ORCH-01 / CRITICAL открыт, внешнего host monitoring не обещано |
| 11. Safe root | Не OS sandbox/запрет terminal effects | PROJECT Existing Operations/run-hermes и Constraints | PASS / Correctness: strict mode wrapper не приписан, scope ограничен file-write tools |
| 12. Docs completion vs product authority | Принимается docs seed, не runtime/approval/archive | README Current State/Open Gates, coverage Classification, WORKFLOW §8 | PASS / Coherence: product owner_approved=false, archive отдельно |

Many-to-many review: каждая строка coverage сверена с полным spec и product tasks, а не одним audit token search. Общие 1.5/1.6 и 8.1/8.2/8.3 обозначены cross-capability, не сужают criteria. Requirement IDs сравниваются именно в строке соответствующего spec; все listed parent IDs существуют. Capability-map anchor и остальные local anchors проверены. Сценарии остаются в canonical audit.

Findings и действия:

- CRITICAL / docs scope: незакрытых нет. Product ORCH-01 и native readiness по-прежнему CRITICAL/BLOCKED вне docs acceptance, не исправлены этим change.
- WARNING / Correctness, исправлено: PROJECT Data and Trust Boundaries сначала связывал TG-02/TG-03 одной ссылкой на specialist-dispatch; разделено на точные task-intake и specialist-dispatch sources.
- WARNING / Verification tooling, устранено проверкой: helper function не пережила terminal call; baseline env потеряла final newline; V2 regex неверно интерпретировал fenced diff. Инциденты/exits и root causes записаны выше, не засчитаны как PASS до повторной проверки.
- SUGGESTION / Coherence, применено: после создания ROADMAP/coverage убраны промежуточные inline placeholders в README/coverage/research, добавлены рабочие canonical links.
- SUGGESTION / future work: не расширять посев ремонтом stock lifecycle или повторным canary. Следующий bounded N-08 discovery и необходимые grants уже явно обозначены; это не незавершённая обязательная задача docs seed.

## Preservation and Rollback

Перед изменениями: `tasks/todo.md` SHA256 `151c010cf5140fced1bbeeb65e712f15f03cd5cded9f3cfdbbe4a149c0300058`; `openspec/WORKFLOW.md` SHA256 `926549d25b4a0def69def4d08bd2fe2d264545de4f5037f85977b44ccee00337`. Before-тексты в `SEED_TODO_BEFORE`/`SEED_WORKFLOW_BEFORE` лишились ровно одного завершающего newline при shell command substitution. Первое exact comparison поэтому дало exit 1; до записи сверены recorded SHA256 обоих файлов и `env + '\n' == source`, drift отсутствовал. Exact diff ниже использует восстановленный newline, не молчаливую нормализацию изменённого источника.

После additive edits SHA256 TODO: `63d71a14c869274b552cb5a58736cefe2b8d4f4af6d1bcd62a37519067690c0a`; WORKFLOW: `6b017b835c59fe8bd0406daa8631059aff20c82986e68caaf4e3107dbf082f1a`. Python difflib подтвердил только insert, protected baseline 231 files совпал.

Exact before/after: context без префикса сохраняется, строки `+` добавлены; удалений нет.

```diff
--- openspec/WORKFLOW.md (before)
+++ openspec/WORKFLOW.md (after)
@@ -1,6 +1,8 @@
 # OpenSpec: рабочий процесс проекта
 
 Эта инструкция обязательна для feature, bugfix, refactor, документационных, конфигурационных и tooling изменений. Она использует установленный OpenSpec, а не вводит новую платформу. Полномочия владельца и ограничения текущего запроса всегда важнее плановых артефактов. Markdown/config guidance не являются техническим sandbox или enforced approval gate.
+
+Навигация: [точка входа](README.md), [карта workspace](PROJECT.md), [индекс инкрементов openspec/ROADMAP.md](ROADMAP.md). Требования и implementation checklist остаются в выбранном change; roadmap не создаёт вторую очередь.
 
 ## 1. Источники истины
 
@@ -90,6 +92,8 @@
 
 Каждый task содержит: requirement/scenario или docs criterion; exact implementation/test paths; команду/наблюдаемый результат проверки; границы scope. Отдельная задача должна быть небольшой. После выполнения — actual evidence и только затем `- [x]`. Частичная реализация, known failure, skip и ожидаемый провал не закрывают полный acceptance criterion.
 
+Контракт малой задачи: `ID`, `Outcome`, `Criterion`, `Files`, `Depends on`, `Verify`, `Evidence`, `Size`. Files проверяются discovery; Verify содержит точную команду/cwd/ожидаемое наблюдение, Evidence — фактический exit/assertion и source/candidate revision после исполнения. Size — 2–5 минут focused работы; больший task до исполнения разбить на children `X.Y.1` и далее, сохранив parent ID и полный criterion. Частичный child не закрывает parent; после декомпозиции пересчитать progress штатным CLI/parser. Неизвестный repo/runner/path — `BLOCKED_PATH_DISCOVERY`, а не придуманный API. Правила и зависимости — [ROADMAP](ROADMAP.md#increment-rules).
+
 Для кода — TDD (RED → GREEN → regression):
 
 1. Прочитать definitions/usages и manifest. Не выдумывать import/API/dependency.
--- tasks/todo.md (before)
+++ tasks/todo.md (after)
@@ -3,6 +3,8 @@
 ## Текущий операторский индекс — OpenSpec reconciliation
 
 Инструкция для всех доработок: `openspec/WORKFLOW.md`; implementation checklists находятся в соответствующих OpenSpec changes. Config включает ссылку в CLI context. Запись обязательного блока AGENTS.md заблокирована protected-write confirmation timeout и не повторялась; полная интеграция ещё не завершена.
+
+- Документационный посев [seed-project-documentation](../openspec/changes/seed-project-documentation/tasks.md): [точка входа](../openspec/README.md), [evidence](../openspec/changes/seed-project-documentation/verification.md); progress только в change, product approval и ORCH-01 этим не закрываются.
 
 - [ ] **ORCH-01 / CRITICAL.** Независимый production-контроллер не реализован. MemPalace и toy-controller не заменяют monitoring/restart. Напоминать до явного закрытия владельцем; контракт — `openspec/changes/telegram-development-workflow/specs/task-recovery/spec.md`.
 - [ ] **OS-06.** Exact product revision approval остаётся pending, `owner_approved=false`; docs apply не разрешает runtime/deployment.
```

TODO historical suffix после heading `## Исторические checkpoints до OpenSpec reconciliation`: SHA256 `18d6c8633244c844dcc76e3495ab6c9607215f4d8af55af2c5a1afd5b712f298`. Историю сохранять дословно.

Rollback: обратный patch только собственных вставок при отсутствии чужого drift. Новые документы не стирать автоматически; superseded только по решению владельца. Git и runtime rollback не выполняются.

## Handoff

Документарные артефакты созданы и проверены: PROJECT/README/ROADMAP, research/coverage/verification; WORKFLOW/TODO изменены только additive, собственный tasks отражает доказанные criteria. DOC-01–DOC-06 имеют evidence выше. Closing record: `SEED-DOCS-HANDOFF-2026-09-22`. Это docs implementation, не product acceptance.

Завершающий protocol после этой записи: V1/V2/V5/coverage и parser должны подтвердить 22/22; offline mine только tasks/openspec, затем штатный MCP reconnect, exact-source search и get_drawer этого closing record плюс финального task 5.5. Итог в чате объявляется только после этих фактических receipts. После успешного readback Markdown не редактируется, чтобы индекс не отставал от финального checklist; при отказе completion откатывается и blocker записывается явно. Expected future counts mining не выдаются за результаты.

Runtime/code/config/AGENTS/tooling/dependencies/OAuth/server/profiles не изменены; Git init/commit/push, sync/archive, publication/deployment не выполнялись. Product revision и approvals сохранены. Source документов авторитетен независимо от индекса. ORCH-01 / CRITICAL открыт; product approval pending; OS-07/R1–R3/MEM-02b не закрываются этим change. Следующий продуктовый шаг — bounded N-08 discovery из ROADMAP, не автоматически разрешённое внедрение. Archive docs change — отдельное решение владельца.
