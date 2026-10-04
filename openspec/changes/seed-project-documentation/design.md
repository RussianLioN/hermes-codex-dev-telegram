## Context

Мотивация и file scope — [proposal.md](proposal.md). Исходная детализация — [план посева](../../../.hermes/plans/2026-09-21_191959-openspec-project-documentation-seed.md); текущий исполняемый checklist после разрешения apply будет только в `tasks.md` этого change.

Обследование 2026-09-21: это macOS operations/documentation workspace, а не исходники upstream Hermes и не готовый Telegram runtime. Установлен локальный `@fission-ai/openspec` 1.13.0 со schema `spec-driven`; `run-openspec` отключает telemetry. Git отсутствует. Основные specs пока отсутствуют; `adopt-openspec-workflow` имеет 23/26 выполненных задач, `telegram-development-workflow` — 0/33. Эти числа — датированный baseline, не постоянные свойства.

Текущие product deltas и [audit](../adopt-openspec-workflow/audit.md) описывают 12 capabilities, 25 requirements и 58 scenarios. `review-status.json` продукта оставляет approval pending, implementation readiness false и ORCH-01 open. Локальные prototypes, native probes и исторические одноразовые canary не равны LIVE_ACCEPTANCE. `implementation-readiness.md` продукта не выбирает окончательные runtime/test paths. R1–R3 и защищённая запись AGENTS остаются вне этого change.

Исторические `08-target-concept.md`, `10-implementation-plan.md` и `HERMES_CODEX_SWARM_GITOPS_GUIDE.md` — background/alternatives, не разрешение создавать предложенный там `runtime/`, новую очередь, approval service или server preview. Их не переписывать; новый индекс ссылается на действующий продуктовый контракт.

## Goals / Non-Goals

Goals:

- Полнота измеряется покрытием поддерживаемых компонентов, контрактов и пробелов, а не количеством созданных spec-файлов.
- Новый исполнитель различает as-is, draft/to-be, historical evidence и blocked work по документам, без чтения private state и догадок об APIs.
- Каждый следующий разрешённый инкремент имеет один наблюдаемый результат, exact paths, зависимости, критерий и проверку.
- Посев можно принять независимо от завершения product runtime и прежнего governance change.

Non-Goals:

- Не создавать новую schema, store, ADR tree, tracker, validator package или maintained test suite. Decisions остаются здесь, требования — в существующих specs.
- Не превращать описание source в гарантию безопасности или работоспособности. Shell syntax check не является runtime acceptance; config/workflow guidance не являются sandbox.
- Не выбирать отсутствующие implementation interfaces и численные лимиты продукта; обозначить `BLOCKED_PATH_DISCOVERY`/authorization gate и точный источник вопроса.
- Не изменять scope из proposal. Возникшее требование к code/config/dependency/runtime работе блокирует соответствующее действие, а не расширяет docs apply автоматически.

## Decisions

### 1. Docs-only change, без массового backfill

Сохранить штатную schema и поставить `skip_specs: true`. S1 рекомендует delta-first brownfield и прямо предупреждает: “Resist the urge to back-fill everything.” S6 и локальные `instructions proposal` допускают explicit skip для документационного изменения без смены поведения.

Альтернативы отклонены: заполнить main specs незавершённым продуктом; переписать все historical research в requirements; переинициализировать OpenSpec. Они создают ложный принятый baseline и дублируют существующий контракт. Будущий as-built normative baseline возможен как отдельный согласованный scope с настоящей проверкой поведения, не побочный эффект этого посева.

### 2. Один canonical источник на вид информации

| Информация | Источник |
|---|---|
| Начало чтения | `openspec/README.md` |
| Состав workspace, as-is и границы | `openspec/PROJECT.md` |
| Процесс изменений и gates | `openspec/WORKFLOW.md` |
| Порядок outcomes/зависимостей | `openspec/ROADMAP.md`, без checklist |
| Нормативное будущее поведение | Существующие product delta specs |
| Исполняемый план | `tasks.md` выбранного change |
| Runtime attempts | Штатный Hermes Kanban, когда подключён; не Markdown roadmap |
| Historical scenario evidence | Существующий `adopt-openspec-workflow/audit.md` и первичные receipts |
| Полнота нового индекса | `coverage.md` этого change |
| Проверки нового docs apply | `verification.md` этого change |
| Операторские напоминания | Текущий индекс `tasks/todo.md`, без копии implementation tasks |
| Retrieval | Производный MemPalace index; current source перечитывается |

Альтернатива — копировать scenarios, receipts и checklists в каждый документ — отвергнута из-за drift. Ссылки на ещё не созданные файлы сначала давать inline code, затем сделать рабочими локальными ссылками. External installations не выдавать за относительные ссылки внутри workspace.

### 3. Контракт документов и критерии приёмки

| Критерий | Документ | Проверяемый результат |
|---|---|---|
| DOC-01 | `openspec/PROJECT.md` | Полное inventory ниже, source links, observable inputs/outputs/failures/side effects, две раздельные архитектурные схемы и trust boundaries |
| DOC-02 | `openspec/README.md` | Понятный маршрут нулевого контекста, безопасные команды, видимые незакрытые gates |
| DOC-03 | `openspec/ROADMAP.md` | Все исходные product parent IDs, I0–I7 зависимости, small-task contract, ready docs и blocked runtime различены |
| DOC-04 | `openspec/WORKFLOW.md`, `tasks/todo.md` | Additive навигация и task format, прежние approvals/история не ослаблены |
| DOC-05 | `research.md`, `coverage.md` этого change | Версионные источники, все capabilities/requirements/parent tasks покрыты; scenarios не продублированы, но сверены с audit |
| DOC-06 | `verification.md` этого change | Actual commands/cwd/exits/assertions, preservation checks, semantic findings, границы и проверенный scoped memory refresh |

`openspec/README.md`: обязательны `## Start Here`, `## Current State`, `## Safe Commands`, `## Continue Development`, `## Open Gates`. Порядок чтения: PROJECT → WORKFLOW → ROADMAP → выбранный change proposal/specs/design/tasks → evidence. Quick start содержит только `context`, `list`, `list --specs`, `status`, `instructions apply`, `validate` через `./run-openspec`, без init/install/update/auth/chat/archive. Объяснить, что `instructions apply` читает инструкции, не выполняет задачи. Динамический progress брать через CLI. Ссылки на ORCH-01, OS-06/07/08/09 и MEM-02b ведут к current TODO.

`openspec/PROJECT.md`: обязательны `## Scope`, `## Existing Operations`, `## Tooling and Evidence`, `## Architecture`, `## Data and Trust Boundaries`, `## Constraints and Gaps`. Для каждой операции указать input, output, errors, side effects, source и evidence class. Обязательный inventory:

| Source path | Что отразить после перечитывания, без запуска операции |
|---|---|
| `run-hermes` | `HERMES_WRITE_SAFE_ROOT`, argv forwarding, внешняя установка; не OS sandbox, не запрет всех terminal writes; не приписывать отсутствующий strict mode |
| `backup-hermes-oauth` | Private snapshot, ZIP integrity, umask/permissions; не копировать архивы/credentials, не обещать полный restore по одному unzip |
| `update-hermes-stable` | Release/tag/commit lookup; `--check` использует сеть, но не обновляет; real update зависит от backup/auth/post-checks |
| `configure-hermes-pilot-ssh` | Mutating SSH alias/config setup, backup и private permissions; пользовательские SSH files не читать |
| `configure-codex-sandbox` | Mutating remote provisioning через SSH и embedded operator payload; не inspection command |
| `run-openspec` | Pinned local CLI; побочные эффекты определяются subcommand |
| `run-mempalace` | Local palace/Chroma/embeddinggemma; search отдельно от mine и MCP |

Также покрыть `.hermes/tooling/openspec/`, `.hermes/tooling/browser/`, `.hermes/tooling/mempalace/` и его `provider/README.md`; `.hermes/tooling/telegram-approval-prototype/`, `.hermes/tooling/protected-operation-prototype/`, `.hermes/tooling/mvp1-integration-prototype/`; `.hermes/research/telegram-hermes-codex/native-codex/` и индекс соседних исследований; generated `.hermes/skills/` и `.agents/skills/`; `.hermes/plans/`, `tasks/todo.md`, historical guide. Vendor/node_modules/venv/caches/palace/binary artifacts описать как third-party/generated/state, не собственную продуктовую архитектуру; не обходить их contents для inventory.

Диаграммы: (a) локальные wrappers → external installation/tooling плюс docs/index; (b) proposed Telegram → native Hermes/Kanban → scoped Codex → verification → publication/delivery, с NOT_DEPLOYABLE и неподтверждёнными boundaries. Capability graph не изобретать заново: ссылка на `openspec/changes/telegram-development-workflow/design.md#capability-map`.

Данные: specs, attempts, candidate revision, immutable evidence, owner authority, curated knowledge, private conversation spool, derived index — различить владельцев и ограничения публикации. MEM-02b и broken `test_stock_lifecycle.py` оставить открытыми. Heuristic redaction не гарантирует отсутствие любого секрета. Требования privacy/admission/recovery связать с product specs; не назначать новых лимитов.

`coverage.md`: `## Product Coverage`, затем таблица `Capability/spec path | Requirement IDs | Original task IDs | Current evidence source | Remaining gate | Canonical owner`; отдельные `## Documentation Criteria` и `## Classification`. Все IDs перечисляются явно, без диапазонов. Каждая capability сверяется с полным spec, а не только audit summary. Полный scenario mapping остаётся в существующем audit. Classification отличает current/draft/historical/blocked и evidence class; новый source review не становится новым запуском теста.

`research.md`: `## Sources`, `## Applied Practices`, `## Limitations`. Перенести выводы S1–S9/H1 с датой/версией и последствиями для этого проекта, не копировать полные страницы. Official examples — открытый первоисточник практик; независимый benchmark/council не проводился.

`verification.md`: `## Baseline`, `## Results`, `## Semantic Review`, `## Preservation and Rollback`, `## Handoff`. Для каждого результата: task ID, DOC criterion, command/inspection, cwd, exit/наблюдение, проверенный source, limitations. Expected output не выдавать за receipt. Точный before/after собственных изменений WORKFLOW/TODO хранить здесь, не backup всего home.

### 4. Roadmap — индекс outcomes, а не второй план исполнения

Обязательные headings: `## Increment Rules`, `## Dependency Map`, `## Next Ready Work`, `## Blocked Work`.

| Срез | Исходные product IDs | Outcome / dependencies |
|---|---|---|
| I0 readiness | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6 | Native gates, repo/runner, limits/locks, exact approval. Source discovery допустим в своём scope; canary требует нового разрешения |
| I1 один допущенный intent | 2.1, 2.2, 2.3 | Admission/replay/restart/fencing после нужных I0 gates |
| I2 один scoped candidate | 3.1, 3.2, 3.3, 3.4, 3.5, 3.6 | Изоляция, отмена, memory packet и revision integrity после I1/runtime readiness |
| I3 один verified preview | 4.1, 4.2, 4.3 | Offline guide и независимый pack того же candidate после I2 |
| I4 один controlled PR | 5.1, 5.2, 5.3 | Publication/reconciliation без duplicate effects после I3 и publisher grant |
| I5 доставка и recovery | 6.1, 6.2, 6.3 | Delivery retry без новой разработки и independent bounded recovery; нужные I1/I2/I4 contracts, без цикла intake/transport |
| I6 сохранность и maintenance | 7.1, 7.2, 7.3, 7.4, 7.5, 7.6 | Snapshot/restore/retention/cleanup/drain после нужных I2/I4/I5 dependencies и grants |
| I7 end-to-end acceptance | 8.1, 8.2, 8.3 | Actual journey/faults и exact owner acceptance всех относящихся срезов |

Это индекс существующих задач, не восемь поручений создавать новые changes. ORCH-01 готовится уже при I0, локально проверяется с I2, полностью принимается с доступными dependencies; он не отложенная косметика.

Task contract для ROADMAP и additive вставки в WORKFLOW §6: `ID`, `Outcome`, `Criterion`, `Files`, `Depends on`, `Verify`, `Evidence`, `Size`. Размер — 2–5 минут focused работы; если больше, разбить до исполнения. Для code: meaningful RED → minimal GREEN → regressions; exact test/import/API paths только после discovery manifests/definitions/usages. Для docs: проверка содержания/ссылок/coverage, без dummy tests. API effects требуют отдельного grant и exact readback. Frequent commits допустимы только в выбранном Git repo при разрешении; здесь Git init/commit не входят в scope.

При дальнейшей согласованной декомпозиции product checklist сохранять parent IDs и полный исходный criterion; children `X.Y.1` и далее не закрывают parent частичным успехом. Не дублировать ADDED requirements между umbrella и новым change; перераспределение ownership требует отдельного planning update. `Next Ready Work` указывает разрешаемый docs apply и bounded N-08 discovery из current implementation-readiness; production остаётся BLOCKED, пока paths/runner/approval не определены. Один writer на shared artifacts; read-only исследования можно параллелить. Возможность subagent execution не предполагается автоматически.

### 5. Проверки соразмерны документации

Не создавать test framework. Структурная OpenSpec validation, ссылки, membership coverage, checksums и semantic tabletop вместе проверяют документационный результат; ни одна из них не является продуктовым runtime тестом. Команды V0–V6 приведены в сохранённом плане; ниже заданы конкретные поправки порядка и helpers, чтобы исполнитель не зависел от несуществующих deliverables.

В исходной таблице D12/D13 V4 вызывается до создания ROADMAP. Исполняемый checklist исправляет порядок: сначала `check_product_coverage coverage`, после roadmap — `check_product_coverage all`. Не создавать пустую roadmap ради прохождения проверки и не ослаблять финальный all gate.

Перед D1 переснять baseline. Сохранить hashes неизменяемых sources и product approval/revision; собственные разрешённые WORKFLOW/TODO изменения проверять exact before/after. При обнаружении чужого drift остановить только зависимые записи; не откатывать чужую работу. Финальные числа получать CLI/parser, не переносить исторические counts.

### 6. Memory refresh и граница propose/apply

Сейчас создаются только `.openspec.yaml`, proposal/design/tasks; docs tasks остаются unchecked. Индексирование разрешённых planning docs не выполняет их tasks и не разрешает apply. После предъявления нужен отдельный запрос применить именно этот change.

Во время будущего apply обновлять только `tasks` и `openspec` corpora. После первоначального D21 refresh финальный D22 меняет verification/tasks: повторить scoped refresh после последних Markdown edits и проверить точный source через retrieval. После успешного readback новых правок документов не делать, чтобы не оставлять индекс позади финального checklist. Если refresh/readback не удался, убрать premature completion соответствующей задачи и честно записать `MEMORY_REFRESH_BLOCKED`; не загружать модель из сети и не расширять mining scope.

## Verification Commands

Все команды выполняются из `/Users/s060874gmail.com/coding/projects/hermes-agent`. V0, V1, V3, V5 и V6 полностью приведены в разделе Tests / validation [исходного плана](../../../.hermes/plans/2026-09-21_191959-openspec-project-documentation-seed.md). Это runnable commands, не разрешение на все операции сразу: V6 мутирует только разрешённый локальный индекс; archive/init/update там не выполняются. Git status/branch ожидаемо дают exit 128, пока workspace не стал Git repo; остальные обязательные checks должны дать exit 0.

Для task-specific документационных проверок один раз определить read-only helper в текущей shell:

```sh
check_doc() {
    python3 -c 'from pathlib import Path
import re, sys
from urllib.parse import unquote, urlsplit
root=Path.cwd().resolve()
p=Path(sys.argv[1])
text=p.read_text(encoding="utf-8")
assert sys.argv[2] in text, "missing required section: "+sys.argv[2]
for raw in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text):
    url=urlsplit(raw)
    if url.scheme or url.netloc or not url.path:
        continue
    target=(p.parent/unquote(url.path)).resolve()
    assert target.is_relative_to(root), "link escapes workspace: "+raw
    assert target.exists(), "broken local link: "+raw
print("DOC OK:", p)
' "$1" "$2"
}
```

Expected: exit 0, `DOC OK: <path>`. Это проверка file targets, не anchors или семантики. Python должен поддерживать `Path.is_relative_to`; если установленный `python3` этого не умеет, применить эквивалентный try/except `relative_to` из V2 плана, не ставить зависимость.

Исправленная двухстадийная проверка V4:

```sh
check_product_coverage() {
    python3 -c 'from pathlib import Path
import re, sys
mode=sys.argv[1]
assert mode in ("coverage", "all"), "explicit coverage/all mode required"
base=Path("openspec/changes/telegram-development-workflow")
coverage=Path("openspec/changes/seed-project-documentation/coverage.md").read_text()
audit=Path("openspec/changes/adopt-openspec-workflow/audit.md").read_text()
specs=sorted((base/"specs").glob("*/spec.md"))
assert specs, "product specs missing"
requirements=[]
scenarios=[]
for p in specs:
    relative=p.relative_to(base).as_posix()
    assert relative in coverage, "unmapped capability: "+relative
    text=p.read_text()
    for title in re.findall(r"^### Requirement: (.+)$", text, re.M):
        identifier=title.split()[0]
        requirements.append(identifier)
        assert re.search(r"(?<![A-Z0-9-])"+re.escape(identifier)+r"(?![A-Z0-9-])", coverage), "unmapped requirement: "+identifier
    for scenario in re.findall(r"^#### Scenario: (.+)$", text, re.M):
        scenarios.append(scenario)
        assert scenario in audit, "scenario missing from canonical audit: "+scenario
parents=re.findall(r"^- \[[ xX]\] (\d+\.\d+)\s", (base/"tasks.md").read_text(), re.M)
assert parents, "product tasks missing"
assert len(parents)==len(set(parents)), "duplicate parent IDs"
assert len(requirements)==len(set(requirements)), "duplicate requirement IDs"
for identifier in parents:
    assert re.search(r"(?<![\d.])"+re.escape(identifier)+r"(?![\d.])", coverage), "task missing from coverage: "+identifier
if mode=="all":
    roadmap=Path("openspec/ROADMAP.md").read_text()
    for identifier in parents:
        assert re.search(r"(?<![\d.])"+re.escape(identifier)+r"(?![\d.])", roadmap), "task missing from roadmap: "+identifier
    assert not re.search(r"^\s*[-*]\s*\[[ xX]\]", roadmap, re.M), "roadmap is a second tracker"
print("COVERAGE OK:", mode, len(specs), "capabilities;", len(requirements), "requirements;", len(scenarios), "scenarios;", len(parents), "parent tasks")
' "$1"
}
```

Baseline expected: `COVERAGE OK: coverage 12 capabilities; 25 requirements; 58 scenarios; 33 parent tasks` либо то же с `all`. Это membership check; semantic review отдельно проверяет правильность many-to-many mappings.

Минимальный финальный структурный набор:

```sh
./run-openspec status --change seed-project-documentation --json
./run-openspec instructions apply --change seed-project-documentation --json
./run-openspec validate seed-project-documentation --strict --json
./run-openspec validate --all --strict --json
/bin/zsh -n run-hermes backup-hermes-oauth update-hermes-stable configure-hermes-pilot-ssh configure-codex-sandbox run-openspec run-mempalace
check_product_coverage all
```

Запускать отдельно с записью exit каждой команды либо связывать обязательные проверки `&&`. Expected: все exit 0; specs skipped, ни одной validation ERROR/WARNING; INFO о `skip_specs` допустим; shell stdout пуст; coverage без пропусков. Tasks progress отражает выполненные критерии, а не только наличие файлов. До apply `coverage.md` ещё отсутствует и coverage check не запускать как будто implementation test.

## Migration Plan

1. Propose: explicit skip → proposal → design → tasks по фактическому dependency graph CLI; validate и предъявить владельцу. Дальше stop, не скрытый apply.
2. После разрешения apply: baseline/verification → source research → PROJECT короткими slices → README → coverage → ROADMAP → additive WORKFLOW/TODO. Точный порядок и commands — `tasks.md`.
3. Каждые 2–3 задачи: проверка затронутых ссылок/разделов, запись evidence, сверка scope. Не останавливать разрешённый apply ради промежуточного отчёта.
4. Полные V1–V5, semantic review, targeted docs fixes, V6/readback и final handoff. Archive/commit/push не выполнять.

Rollback без Git: сохранить exact before/after собственных WORKFLOW/TODO вставок в verification; обратный patch только если фрагмент не изменён другим writer. Новые документы не стирать автоматически: при отмене пометить superseded по отдельному решению. Product docs, approvals и historical evidence не использовать как место rollback. Runtime rollback не нужен — runtime не меняется.

## Semantic Review

В `verification.md` составить `Case | Expected route | Actual reference | Finding` по двенадцати tabletop cases из сохранённого плана: zero-context onboarding, docs-only skip, поведенческая feature/TDD, missing implementation repo, historical evidence, PLAN boundary, CLI fallback, R1–R3/OS-07, задача >5 минут, recovery, safe-root limitation, docs completion vs product approval. Итог — Completeness/Correctness/Coherence с CRITICAL/WARNING/SUGGESTION и exact paths. Это source/document review текущего исполнителя, не независимый council или runtime тест.

## Risks / Trade-offs

- [Полнота превращается в копирование всей истории] → Ограниченный inventory и canonical ссылки; vendor/private state не обследуются как собственный продукт.
- [`specs/` пуст, и это принимают за неготовность OpenSpec] → Явно объяснить docs-only/brownfield и separate sync/archive; не создавать фиктивные requirements.
- [Roadmap воспринимают как runnable runtime plan] → N-08/repo/runner/limits остаются BLOCKED; точные code tasks появляются только после discovery и согласования.
- [Новые документы обходят старые approvals] → Protected allowlist, hashes, неизменные product artifacts; scope пользователя не подменяется CLI ready.
- [Нет Git и автоматического rollback] → Только additive patches, exact before/after; Git adoption отдельно.
- [Одни и те же числа/статусы устаревают] → Датированный baseline, динамический CLI и ссылки; не копировать receipts или обещать latest version.
- [Memory refresh отстаёт от финальных task edits] → Последний scoped refresh/readback после финальной записи; при сбое честный blocker.
- [Пять минут недостаточно для сложного чтения] → Разбить focused действие ещё до выполнения; не закрывать parent по частичному результату, не раздувать scope.

## Sources

Привязка к установленной версии, не заявление о latest: tag `v1.13.0`, pinned commit `9d4e5974e5c0d9a09b9c6c1e1eb0975e80ec4461`. S1/S2/S6 повторно получены 2026-09-21 при подготовке proposal. Остальные источники исследованы в исходном плане; будущий `research.md` сохраняет дату и границы этих выводов.

| ID | Официальный источник | Применение |
|---|---|---|
| S1 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/existing-projects.md | Brownfield, delta-first, отказ от массового backfill |
| S2 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/writing-specs.md | Observable behavior, отрицательные scenarios, один intent на change |
| S3 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/workflows.md | Refinement возвращается в artifacts; workflow не новая runtime платформа |
| S4 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/reviewing-changes.md | План review до apply, semantic completeness/correctness/coherence |
| S5 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/team-workflow.md | Один writer; Git рекомендации не являются разрешением commit |
| S6 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/examples.md#recipe-5-a-refactor-with-no-behavior-change | Explicit skip_specs при неизменном поведении |
| S7 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/cli.md | Inspection API; точный JSON проверяется локальным CLI |
| S8 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/supported-tools.md | Разные Hermes/Codex integration paths, existence не равно runtime loading |
| S9 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/concepts.md | Specs/change/archive имеют разные функции |
| H1 | https://hermes-agent.nousresearch.com/docs | Authoritative Hermes docs; runtime APIs этим proposal не переаттестованы |

Локальная версия: `.hermes/tooling/openspec/package.json`; wrapper `run-openspec`; artifact templates/instructions — `.hermes/tooling/openspec/node_modules/@fission-ai/openspec/schemas/spec-driven/schema.yaml` и фактический `instructions`. Эти документы определяют формат, но не выдают runtime полномочия.

## Open Questions

Не осталось нерешённых вопросов, меняющих этот docs scope. Будущий normative as-built baseline, Git adoption, продуктовый repo/runner и runtime grants — отдельные owner decisions вне посева; блокирующие продукт вопросы не маскируются как разрешённые отсрочки.

ORCH-01 / CRITICAL остаётся открытым до явного закрытия владельцем после реальной приёмки независимого контроллера. Документы, OpenSpec и MemPalace его не реализуют.
