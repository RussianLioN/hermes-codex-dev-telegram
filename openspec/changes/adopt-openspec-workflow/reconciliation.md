# Reconciliation: точный пакет продуктовых уточнений

## Статус

Docs apply разрешён: «Применяй adopt-openspec-workflow». Это разрешает реализовать описанный workflow, но по tasks 2.3–2.4 не подменяет ещё не предъявленное per-artifact confirmation изменений product change. Ни один product файл этим этапом не изменён. Ниже пакет R1–R3: PENDING_OWNER_CONFIRMATION. Отказ от пакета не отменяет уже разрешённый WORKFLOW/AGENTS/config/TODO этап.

## R1 — product design.md: исследование отдельно от решения

Файл `openspec/changes/telegram-development-workflow/design.md`.

Before: после пункта Decisions 5 отсутствует явная классификация поздней app-server research. Существующие Non-Goals `app-server/интерактивный SSH до MVP2` и пункт `CLI прежде remote TUI` сохраняются ДОСЛОВНО.

After: добавить после пункта 5 отдельный абзац:

> **Исследовательский кандидат, не изменение MVP1:** последующие app-server/exec-server/environment probes описаны в native-environment-evidence.md, native-bootstrap-evidence.md и linux-model-lifecycle-preparation.md. Их результаты ограничены local/native/synthetic и одноразовым разрешённым Linux canary; CLIENT_ROUTING_GATE_OPEN / NOT_DEPLOYABLE сохраняется. Они не отменяют CLI-first и Non-Goals выше. Выбор иного production runner требует отдельного согласования design/spec revision и его точного runtime scope. Трассировка исторической работы: ../adopt-openspec-workflow/audit.md.

Rationale: убрать неоднозначность без выбора новой архитектуры. Effect: меняется digest design revision, owner_approved остаётся false. Никакое новое исполнение не разрешено.

## R2 — product tasks.md: уточнение статуса исследований

Файл `openspec/changes/telegram-development-workflow/tasks.md`.

Before: после первого вводного абзаца нет ссылки на полную evidence map; task 3.2 описывает подключение CLI без ссылки на текущий unresolved runner choice.

After: добавить после вводного абзаца:

> Историческая локальная подготовка и её пределы сведены в ../adopt-openspec-workflow/audit.md. Наличие локального прототипа, source probe или mock результата не закрывает перечисленные production outcomes; разрешённые local scopes остаются действительны только в своих границах. Исходные task IDs сохранены, локальные результаты не засчитываются вместо полного критерия.

После неизменённой строки checkbox 3.2 добавить отдельный абзац:

> Уточнение к 3.2: исследованный app-server/client-executor путь пока является кандидатом, не утверждённой заменой Codex exec. До подключения требуется согласованный выбор runner и доказательство model routing/credential boundary; native environment readiness не закрывает этот пункт.

Rationale: показать реальные local результаты, не менять условия приёмки. Effect: все исходные checkbox/IDs остаются неизменными; tasks исключены из spec digest, но семантическое scope approval всё равно обязательно.

## R3 — product review-status.json: дополнительные evidence, не переписывание baseline

Файл `openspec/changes/telegram-development-workflow/review-status.json`.

Before: local_native_environment.receipts указывает на v4; это корректный historical baseline, но не полный индекс последующих исследований.

After: сохранить весь local_native_environment объект, включая v4, и добавить отдельный sibling объект:

```json
"subsequent_local_evidence": {
  "bootstrap_evidence": "native-bootstrap-evidence.md",
  "bootstrap_receipts": "../../../.hermes/research/telegram-hermes-codex/native-codex/environment-run/receipts-v5.json",
  "lifecycle_evidence": "linux-model-lifecycle-preparation.md",
  "lifecycle_receipts": "../../../.hermes/research/telegram-hermes-codex/native-codex/lifecycle-preparation/receipts-v2.json",
  "status": "LOCAL_PREPARATION_ONLY / NOT_RUNTIME_ADMISSION",
  "existing_account_metadata_probe": "FAILED: TimeoutError; not evidence of absent OAuth",
  "stock_lifecycle_test": "BROKEN_SOURCE / NOT_RUN",
  "runtime_permission_granted": false
}
```

Если R1 принят: пересчитать spec_revision_sha256 только по существующему алгоритму и неизменённому revision_files. Не менять approval_status=pending, owner_approved=false, implementation_ready=false, runtime_acceptance или orch_01_closed. R3 — bookkeeping, не штатный planning artifact update.

## Что не предлагается изменять

Product proposal.md, все specs, native-capability-matrix.md, source и receipts остаются неизменными: для docs workflow это не нужно. Полное изменение architecture не включено в пакет. Нет новых требований, отмены безопасности, публичного repo, model canary, server effect или archive. ORCH-01 / CRITICAL остаётся открыт.

## Сверка revision и receipts

Actual computed и recorded SHA256 совпали: `29163c1de50e501a82f85cc72ada9f011520a3a17828ee0027adf006b22c729f`; owner_approved=false. Receipt v4/v5/lifecycle v2 hashes и coverage — audit.md. Source_sha256 v5 и lifecycle v2 сверены с соответствующими текущими файлами: SOURCE_DRIFT=[] для обоих, unresolved paths не было. Это integrity check выбранных sources, не новый запуск tests или attestation всех transitive dependencies.

## Открытый отдельный дефект

`.hermes/research/telegram-hermes-codex/native-codex/test_stock_lifecycle.py:4` буквально содержит `from guest_namespace_plan import ...[truncated]`. Не реализовывать stock_lifecycle.py и не ремонтировать тест в docs change. Отдельная последующая code task должна восстановить настоящий behavior test и пройти meaningful RED/GREEN по согласованному runtime scope. Старый syntax failure не засчитывать как RED; файл и receipts сохранены.

## Подтверждение

| Изменение | Статус | Основание |
|---|---|---|
| WORKFLOW + AGENTS блок C.17 + config linkage + TODO index | AUTHORIZED_DOCS_APPLY | Текущий запрос применить конкретный docs change |
| R1 design addition | PENDING | Предъявляется впервые в этом документе |
| R2 tasks clarification | PENDING | Предъявляется впервые в этом документе |
| R3 additive receipt bookkeeping / R1 digest refresh | PENDING | Предъявляется впервые в этом документе |
| Product runtime/canary/deployment/archive | NOT_AUTHORIZED_BY_THIS_CHANGE | Вне scope |

Однозначный следующий ответ для оставшейся работы: «Подтверждаю R1–R3 из reconciliation.md». Перед записью перечитать existing files: при drift повторно предъявить изменённый diff. Это не запрос согласовать заново local integration scope.

## Собственные docs edits и rollback

AGENTS.md: предполагалось добавить только новый `## Required OpenSpec workflow` блок C.17 после существующего текста. Фактическая попытка BLOCKED: protected-write approval timeout. По read-only проверке раздел отсутствует; запись не повторялась другим способом. Task 3.4/OS-07 остаются открытыми. Нужно отдельное разрешение владельца на повторную защищённую запись, затем успешное подтверждение инструмента. Никакого rollback AGENTS не требуется, поскольку изменения не применились.

openspec/config.yaml:

```diff
   Read .hermes/research/telegram-hermes-codex/08-target-concept.md and 10-implementation-plan.md for background.
+  Follow openspec/WORKFLOW.md for every feature, fix, refactor, documentation, configuration, and tooling change.
@@
     - Leave implementation and owner approval checkboxes unchecked until verified.
+    - Link each task to a requirement/scenario or a docs criterion and exact verification evidence.
+    - Distinguish local/synthetic/native/canary evidence from full live acceptance; do not close a parent task for a partial result.
```

Rollback: удалить только эти три добавленные строки; context/rules/operations approvals не менять. Private backup выполнен до configuration edit; payload не копируется в workspace.

tasks/todo.md: добавить новый текущий операторский индекс сразу после заголовка, затем heading `## Исторические checkpoints до OpenSpec reconciliation`. Всё старое содержимое сохраняется, включая старый незакрытый OS-07 как historical record. Rollback: удалить только добавленный индекс и historical separator при отсутствии конкурентных изменений. Не удалять исторические checkpoints.

Новые WORKFLOW/audit/reconciliation/verification не удаляются автоматически при rollback: они являются результатом работы; при отмене пометить superseded по согласованию. При изменённом чужим writer фрагменте rollback остановить, не применять blind replacement. Workspace не Git repo, git reset/checkout/init не используются.

## Current Reconciliation

2026-09-23. Весь текст выше — historical packet/receipts. Старый R1 с сохранением «SSH до MVP2» **SUPERSEDED**, не текущая инструкция. Действуют решения D-27–34 и E1/E2 текущего product design. История сохранена, а не исправлена задним числом.

Владелец ответил «Приступай» на предъявленный [план с exact R1-current/R2-current/R3](../../../.hermes/plans/2026-09-23_170149-reconciliation-coverage-e1-discovery.md#exact-reconciliation-packet-для-подтверждения) и предложение выполнить документационный пакет/source discovery. Это подтверждение перечисленных edits и G-DISCOVERY, не approval resulting product revision или runtime. Для C.17 было явно оговорено отдельное подтверждение: G-AGENTS остаётся PENDING, новой попытки записи нет.

| Пакет / файл | Before текущей revision | Подтверждённый after | Approval impact |
|---|---|---|---|
| R1-current / product design.md | Decisions 5 уже задаёт два CLI пути; поздние probes не классифицированы отдельным абзацем | Exact абзац из плана после Decisions 5: app-server research — кандидат; ordinary SSH остаётся E1; ссылка на current coverage | Docs edit AUTHORIZED; digest пересчитывается, owner_approved=false |
| R2-current / product tasks.md | Нет current map link и clarification после 3.2 | Два exact абзаца из плана; parent IDs/checkbox criteria сохранены | Docs edit AUTHORIZED; tasks вне spec digest; runtime не разрешён |
| R3 / product review-status.json | v4 historical baseline без отдельного индекса последующих receipts | Additive subsequent_local_evidence с v5/lifecycle v2, FAILED metadata probe и BROKEN_SOURCE; старые объекты неизменны | Bookkeeping AUTHORIZED; никаких новых canary permissions |
| Current coverage/navigation | Historical 12/25/58/33; TODO N-01–08 | Отдельные current sections в audit, 13/28/81/44, N-01–N-11; historical receipts сохраняются | Docs-only AUTHORIZED |
| E1 source discovery | Current interfaces/storage/SSH/history не установлены | Source-pinned findings и blockers в existing matrix/readiness, без runtime исполнения | G-DISCOVERY AUTHORIZED; source-only не закрывает gates |
| C.17 / AGENTS.md | Required OpenSpec workflow отсутствует | Append exact C.17 только после отдельного разрешения и successful protected confirmation | PENDING; adoption 3.4 / OS-07 остаются open |

Исходный проверенный digest: `76c3d8d476e2267ce2f76acefb85cf3d630cc9a81066dee3285c5b8398f829a7`. Progress и actual final checks — [Current Verification](verification.md#current-verification); актуальная revision — product review-status.json. Seed, specs, historical receipts и полные task criteria защищены baseline в verification.md.

При новом normative finding исполнитель предъявляет отдельный diff, не меняет specs/architecture под видом discovery. Private credentials/history не читаются, candidate repo/upstream/server не редактируются; sync/archive/commit/publication не разрешены. ORCH-01 / CRITICAL открыт.
