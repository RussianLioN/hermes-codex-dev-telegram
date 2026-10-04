# OpenSpec: рабочий процесс проекта

Эта инструкция обязательна для feature, bugfix, refactor, документационных, конфигурационных и tooling изменений. Она использует установленный OpenSpec, а не вводит новую платформу. Полномочия владельца и ограничения текущего запроса всегда важнее плановых артефактов. Markdown/config guidance не являются техническим sandbox или enforced approval gate.

Навигация: [точка входа](README.md), [карта workspace](PROJECT.md), [индекс инкрементов openspec/ROADMAP.md](ROADMAP.md). Требования и implementation checklist остаются в выбранном change; roadmap не создаёт вторую очередь.

## 1. Источники истины

| Что | Где |
|---|---|
| Требования и scenarios | `openspec/specs/` и delta specs выбранного change; in-flight delta не означает уже работающее поведение |
| Почему и что меняется | `openspec/changes/<change>/proposal.md` |
| Архитектурное решение | `design.md` соответствующего change |
| План проверяемых результатов | `tasks.md` этого change |
| Execution attempts | Штатный Hermes Kanban, когда реально подключён; не создавать вторую очередь |
| Результаты исполнения | Реальные receipts/tests с exact source/candidate revision и явно указанным масштабом |
| Полномочия | Явное разрешение владельца на конкретную revision/операцию |
| Операторские напоминания | `tasks/todo.md`, не дублирующий implementation tracker |
| Retrieval | MemPalace как производный индекс; найденный current source перечитывается |

Не переносить в основные specs незавершённый продукт ради заполнения каталога. `review-status.json` — вспомогательная запись, не штатный security token. Готовность документов, выполнение tasks, structural validation, runtime acceptance и owner approval — разные утверждения.

## 2. Начало работы и выбор change

Из root workspace:

```sh
./run-openspec context --json
./run-openspec list --json
./run-openspec list --specs
```

Проверить возвращённый root. Если root не найден или неверен — остановить запись; не выполнять init автоматически. Если выбран store, сохранять его явный scope для последующих поддерживающих его команд. В этом workspace по умолчанию используется repo-local root.

Прочитать AGENTS.md, tasks/todo.md и relevant installed skill. Новое самостоятельное намерение — отдельный небольшой change. Продолжение той же feature/fix — существующий подходящий change. Не создавать change на каждый checkbox и не складывать всё в бессрочный change. Если несколько вариантов реально равнозначны — уточнить scope, не угадывать.

Установить переменную на точное имя из list (пример текущей миграции):

```sh
CHANGE=adopt-openspec-workflow
./run-openspec status --change "$CHANGE" --json
```

Файлы и dependency order брать из `artifactPaths`, `requires`, `contextFiles`, не из памяти. Не редактировать glob как имя файла.

## 3. Explore: уточнение без реализации

Прочитать `.hermes/skills/openspec-explore/SKILL.md` (для Codex — соответствующий `.agents/skills/` файл). Исследовать конкретный вопрос через repo/source/tests, отделять факты от гипотез. Не писать runtime implementation в explore. Результат, влияющий на design, возвращать в canonical artifacts через согласованный update; не оставлять единственным решением очередной research report.

## 4. Propose: согласуемый контракт

Прочитать установленный `openspec-propose/SKILL.md`. Для нового свободного имени:

```sh
./run-openspec new change <new-kebab-case-name>
./run-openspec status --change <new-kebab-case-name> --json
```

Угловые скобки означают placeholder: заменить именем, не вставлять буквально в shell. Затем получать инструкции для каждого готового артефакта по dependency graph:

```sh
./run-openspec instructions proposal --change "$CHANGE" --json
./run-openspec instructions specs --change "$CHANGE" --json
./run-openspec instructions design --change "$CHANGE" --json
./run-openspec instructions tasks --change "$CHANGE" --json
```

Не исполнять этот блок механически: сначала записать выбранный артефакт по template, перечитать dependencies следующего, проверить status. Language — Russian; структурные headings и SHALL/MUST согласно шаблону.

Behavior change требует delta specs с проверяемыми WHEN/THEN, включая отказы. Изменяемый existing requirement копируется целиком со всеми scenarios, не фрагментом. Чистые docs/tooling/refactor без изменения specified behavior могут явно ставить `skip_specs: true` в change metadata с обоснованием в proposal. Не создавать фиктивное требование ради validation; skipped specs не записывать. Если bugfix восстанавливает уже заданное поведение, не изобретать новый контракт — сослаться на существующее требование и добавить regression task.

После proposal выполнить validation и предъявить артефакты. Установленный propose требует следующего отдельного запроса на apply. Он не означает переспрашивание на каждом subsequent task: внутри разрешённого apply работать до завершения или настоящего blocker.

## 5. Update: согласованная правка planning artifacts

Прочитать `openspec-update-change/SKILL.md`. По `status` загрузить concrete existingOutputPaths и сопоставить все связанные planning artifacts в обе стороны. При существенном rewrite запросить актуальные artifact instructions.

Показать proposed revisions по файлам и получить подтверждение перед записью. Допустим один пакет с однозначными per-artifact edits и одним подтверждением всего перечня. Не выдавать общее «работай автономно» за approval ещё неизвестной product revision. Если revision отклонена — не применять её. Update не создаёт новые artifacts и не пишет implementation code; для недостающего артефакта использовать instructions соответствующего artifact, для реализации — отдельный apply.

Смена intent — новый change; refinement той же цели — текущий. Изменение design во время coding требует возврата к плану, не молчаливого расширения или урезания задачи.

## 6. Apply: задачи и доказательства

Прочитать `openspec-apply-change/SKILL.md`, объявить выбранный change. Разрешение на один docs change не разрешает deployment другого.

```sh
./run-openspec status --change "$CHANGE" --json
./run-openspec instructions apply --change "$CHANGE" --json
```

Прочитать каждый файл из `contextFiles`, `context` и `operationGuidance`. Состояние CLI `blocked` нельзя обходить. `ready` означает готовность checklist к работе, не выдачу полномочий. Если guidance конфликтует с controlling workflow/user scope — объяснить конфликт, а не подменять CLI state.

Каждый task содержит: requirement/scenario или docs criterion; exact implementation/test paths; команду/наблюдаемый результат проверки; границы scope. Отдельная задача должна быть небольшой. После выполнения — actual evidence и только затем `- [x]`. Частичная реализация, known failure, skip и ожидаемый провал не закрывают полный acceptance criterion.

Контракт малой задачи: `ID`, `Outcome`, `Criterion`, `Files`, `Depends on`, `Verify`, `Evidence`, `Size`. Files проверяются discovery; Verify содержит точную команду/cwd/ожидаемое наблюдение, Evidence — фактический exit/assertion и source/candidate revision после исполнения. Size — 2–5 минут focused работы; больший task до исполнения разбить на children `X.Y.1` и далее, сохранив parent ID и полный criterion. Частичный child не закрывает parent; после декомпозиции пересчитать progress штатным CLI/parser. Неизвестный repo/runner/path — `BLOCKED_PATH_DISCOVERY`, а не придуманный API. Правила и зависимости — [ROADMAP](ROADMAP.md#increment-rules).

Для кода — TDD (RED → GREEN → regression):

1. Прочитать definitions/usages и manifest. Не выдумывать import/API/dependency.
2. Написать минимальный failing behavior test; выполнить точную команду и удостовериться в нужной причине RED. Синтаксически оборванный файл не meaningful RED.
3. Минимально реализовать; та же команда GREEN, затем относящиеся regressions.
4. Зафиксировать command/cwd/exit/assertion, source/candidate revision, scope и limitations; связать с task/scenario.
5. Commit только в Git repo и при явном разрешении. Этот workspace нельзя git-init/commit автоматически.

Для docs/config: настоящие CLI checks, проверка ссылок/coverage/инструкций и tabletop cases. Не создавать фиктивные tests вместо проверки результата.

Классы evidence: SOURCE_ONLY, LOCAL_SYNTHETIC, NATIVE_LOCAL, AUTHORIZED_CANARY, LIVE_ACCEPTANCE, FAILED, NOT_RUN. Mock response не превращается в live API result; no-model probe не доказывает project model routing; fresh-context review не является runtime test. Parent task остаётся открытым, если выполнена только локальная подзадача.

Если проблема требует нового scope/прав — заблокировать затронутое действие, подготовить общий owner packet и продолжить независимые разрешённые задачи. Не останавливаться только ради промежуточного итогового отчёта. При прямой остановке пользователя прекратить работу.

## 7. Verify: три независимых вопроса

```sh
./run-openspec validate "$CHANGE" --strict --json
./run-openspec validate --all --strict --json
./run-openspec instructions apply --change "$CHANGE" --json
```

Каждый exit проверять отдельно или связывать обязательные проверки `&&`, не полагаться на exit последней команды после `;`.

- `status`: существуют ли planning artifacts; isPlanningComplete/isComplete не означает законченный продукт.
- `instructions apply`: сколько checklist задач выполнено; checkbox сам не доказательство.
- `validate`: корректна ли структура; успешный validator не исполняет acceptance tests.

Semantic verification по штатному template `.hermes/tooling/openspec/node_modules/@fission-ai/openspec/dist/core/templates/workflows/verify-change.js`:

- Completeness — все tasks и scenarios покрыты mapping, незавершённые пункты видны.
- Correctness — implementation/evidence действительно выполняют критерий в заявленной среде.
- Coherence — design, specs, tasks и implementation не противоречат друг другу.

Отчёт с CRITICAL/WARNING/SUGGESTION, путями и конкретными действиями. Неполный change не готов к archive. Разделять проблемы tooling migration и незавершённого продукта. Optional generated verify skill использовать лишь после подтверждения его наличия; терминальной команды `openspec verify` здесь нет.

## 8. Sync/archive

Прочитать установленный sync/archive skill и перед допустимой операцией:

```sh
./run-openspec instructions archive --change "$CHANGE" --json
```

Sync и archive меняют baseline — это не косметическая очистка списка. Для текущего продукта требуются действительная runtime acceptance и owner authorization. Для docs change приёмка определяется docs criteria, а не несуществующим deployment; archive всё равно отдельно разрешается. Не использовать `--no-validate`, не принуждать archive незавершённой работы. Следовать фактическим archive instructions/help, потом перечитать точный результат и validate. Не архивировать весь MVP1 при завершении одного tooling change.

## 9. Полномочия и безопасность

Никаких core patches/fork/monkeypatch, новых profiles/services/схем, зависимости без approval, credential copying, real VM/canary/publication/deployment автоматически. Перед config/dependency/update work соблюдать private backup policy AGENTS; snapshot не индексируется и не публикуется. Legacy approvals одноразовых canary не действуют повторно. Approval защищённой операции после изменения revision требует нового решения. Council не может одобрить её за владельца.

Generated skills не редактировать вручную. Наличие skill-файла, его загрузка runtime и успешный вызов — разные проверки. При отсутствующем tool честно обозначить ограничение и применять доступный документированный CLI workflow, а не заявлять несуществующий slash invocation. Настройка/возможности Hermes сверяются с https://hermes-agent.nousresearch.com/docs; source контракта OpenSpec — установленная версия и её CLI instructions. Latest upstream не подменяет установленную версию.

## 10. Консилиум: только при споре или низкой уверенности

Сначала проверить доступный source/CLI. Не созывать совет для подсчёта tasks или чтения help. При спорном архитектурном решении, конфликте evidence/constraints или низкой уверенности после source lookup использовать полный состав E01–E19 из `.hermes/plans/2026-09-11_114507-autonomous-mvp1-expert-council.md`; старое правило 3–5 экспертов/двух раундов заменено последним запросом владельца.

1. Packet: ограниченный вопрос, source snippets, варианты, contract и proposed diff; без secrets/raw histories и навязанного вывода.
2. Волна 1 — варианты и сильнейшие контрпримеры, отдельный контекст каждого из 19 экспертов.
3. Ведущий классифицирует findings: actionable / contract misread / trade-off / noise. Волна 2 — adversarial проверка обезличенных выводов и доказательств.
4. Волна 3 — проверка исправленного варианта и критериев принятия. Максимум три волны; нерешённые существенные вопросы в единый owner packet.
5. До трёх параллельных контекстов, 180 секунд на попытку, запрет nested agents/tools, никаких повторов неизменённого packet ради голосов. Нет ответа — нет голоса. Отдельные контексты одной модели не независимые модели. Cross-model calls требуют отдельного согласия.
6. Проверить доступный штатный запуск до обещаний. Hardcoded lifecycle_council.py не приспособлять обходным способом. При отсутствии подходящего механизма — capability blocker; не имитировать ответы и не строить runner в docs change.
7. Только фактически полученные packets/transcripts/manifests (actual exits/input-output hashes) в `council/<decision-id>/`; decision возвращается в согласованные canonical artifacts. Majority не отменяет safety/requirements.

Консилиум не заменяет пароль, ручной тест владельца, выдачу прав или acceptance. Без технического спора обязательную авторизацию спрашивать прямо, не голосовать о ней.

## 11. Handoff и память

После разрешённых docs edits:

```sh
HF_HUB_OFFLINE=1 ./run-mempalace mine tasks --wing hermes-agent --agent hermes-default
HF_HUB_OFFLINE=1 ./run-mempalace mine openspec --wing hermes-agent --agent hermes-default
HF_HUB_OFFLINE=1 ./run-mempalace search "OpenSpec WORKFLOW" --wing hermes-agent
```

Проверить exits и точные найденные источники. Не индексировать home/credentials/backups/vendor/raw sessions. При сбое индексирования source не теряет authority; записать refresh blocked.

Финальный handoff: change/task IDs; что реально изменено; tests/validation/semantic verification отдельно; какой scope разрешён; blockers и единый необходимый owner action. Не заявлять «done», пока оставшиеся обязательные задачи открыты.

ORCH-01 / CRITICAL остаётся открытым до явного закрытия владельцем после реальной приёмки независимого контроллера. OpenSpec, MemPalace и этот workflow сами не следят за агентами и не перезапускают их.
