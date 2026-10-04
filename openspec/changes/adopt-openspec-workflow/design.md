## Context

Мотивация и scope — proposal.md. Исходный план: `.hermes/plans/2026-09-16_193737-openspec-workflow-reconciliation.md`. Текущий этап — proposal, не apply.

Проверено CLI: OpenSpec 1.13.0, root текущего workspace, основной product change имеет 0/33 выполненных задач; structural validation проходит. Основных specs ещё нет: это допустимо для незавершённого первого change. Workspace не под Git, автоматические commits запрещены. Инструкция установленного `.hermes/skills/openspec-propose/SKILL.md` отделяет создание planning artifacts от следующего запроса apply.

## Goals / Non-Goals

**Goals:** единый понятный маршрут изменения; сохранённая связь требования, задачи, реализации и доказательства; различимые planning/progress/validation/acceptance/approval статусы.

**Non-Goals:** технический sandbox или enforced authorization из Markdown; изменение product behavior; новая схема, daemon, plugin или runtime runner; переписывание истории и ретроспективные approvals. Ограничения proposal сохраняются.

## Decisions

### 1. Штатная схема и отдельный docs change

Использовать `spec-driven` и обоснованный `skip_specs: true` здесь; product delta specs остаются в `telegram-development-workflow`. Альтернативы — новая schema или разбиение всех исторических исследований на changes — создают лишнюю миграцию и конфликтующие requirements. Пустой основной `openspec/specs` не заполнять незавершённым продуктом ради статистики.

### 2. Источники истины

| Объект | Авторитетный источник | Не заменяется |
|---|---|---|
| Product requirements | Product specs и согласованная revision | Советами экспертов, памятью |
| Архитектурный замысел | Соответствующий design.md | Последним research-отчётом |
| План результатов | Соответствующий change/tasks.md | Операторским TODO |
| Реальные попытки выполнения | Штатный Kanban там, где реально задействован | Второй очередью в Markdown |
| Исполнение проверки | Actual receipts с coverage/revision | Checkbox или exit чужой команды |
| Полномочия | Явное решение владельца для конкретного scope | state=ready, council, config guidance |
| Память | Перечитываемый current source | Производным MemPalace index |

`audit.md` — таблица доказательств, не tracker. Поля: requirement/scenario, original task ID, implementation path, evidence path/revision, класс, выполненные/оставшиеся критерии, источник разрешения. Классы: SOURCE_ONLY, LOCAL_SYNTHETIC, NATIVE_LOCAL, AUTHORIZED_CANARY, LIVE_ACCEPTANCE, FAILED, NOT_RUN. Старые receipts не изменяются под текущие файлы; несовпадение отмечается stale.

### 3. Согласование вместо заднего числа

`reconciliation.md` содержит proposed per-file revisions, before/after, rationale и подтверждение либо pending. Product design с CLI-first/non-goals не заменяется app-server-кандидатом без решения владельца. Product task 3.2 остаётся открытым до полного критерия. Product IDs сохраняются; local readiness subtasks допустимы только с отдельным ограниченным критерием и без закрытия parent.

Штатный update workflow правит существующие planning artifacts после подтверждения. Допустим единый пакет с однозначным перечнем revisions. New evidence files создаются в docs apply, а не через ложное расширение update skill. Смена поведения требует product delta и отдельного approval; docs change не может её легализовать.

### 4. Один WORKFLOW вместо копий инструкций

`openspec/WORKFLOW.md` описывает контур: root/list → explore при неопределённости → propose → отдельное apply разрешение → tasks/test/evidence → verify → отдельно разрешённые sync/archive. При architecture drift — update planning artifacts, а не незаметное расширение реализации.

AGENTS содержит короткий обязательный блок из пункта C.17 плана. Config добавляет ссылку, traceability и local/live distinction, сохраняя текущие approvals. Не копировать generated skills; читать текущие instructions от CLI. Перед configuration work выполнить предусмотренный AGENTS private backup после проверки shell syntax; не раскрывать payload и credentials.

Каждая feature/fix/refactor/docs/config/tooling доработка выбирает подходящий change. Новое самостоятельное намерение — новый change, продолжение той же задачи — существующий. Для неизменного поведения применим skip_specs; нельзя выдумывать требования ради валидатора. TDD применяется к последующим code tasks; здесь нужны проверяемые docs/CLI контракты, а не фиктивные unit tests.

### 5. Verification и интеграции

Переиспользовать installed Hermes/Codex skills; проверить файлы и runtime discovery раздельно. Optional verify skill не предполагать установленным: использовать source template `dist/core/templates/workflows/verify-change.js` локального OpenSpec. Терминальной команды `openspec verify` не заявлять.

`verification.md` оценивает Completeness, Correctness, Coherence. `validate` проверяет структуру, `status` — planning artifacts, `instructions apply` — task progress. Каждый task completion требует своего evidence, а итог docs acceptance не является product acceptance.

### 6. Bounded council

При спорном решении/низкой уверенности после source lookup — три волны полного E01–E19: варианты → контрпримеры → исправленное решение. Роли из плана `2026-09-11_114507-autonomous-mvp1-expert-council.md`; его старые правила меньшего состава/двух волн не применять. Каждый эксперт — отдельный контекст; одна модель не называется независимыми моделями. До трёх параллельных запусков, timeout 180 секунд на попытку; запрещены вложенные агенты и tools. Фактические packets/results/manifests сохранять только при запуске; отсутствие ответа не считать голосом.

Сначала проверить доступный штатный механизм. Hardcoded lifecycle_council.py не использовать для новой темы. Если capability недоступна — честный blocker, не самописный runner внутри docs change. После трёх волн неразрешённый существенный конфликт эскалировать одним пакетом владельцу; независимую безопасную работу продолжать. Никакое голосование не выдаёт разрешение внешних эффектов.

## Risks / Trade-offs

- [Ложный прогресс] → не закрывать product tasks за synthetic/native-only результаты; сохранять FAILED/NOT_RUN.
- [Разрастающаяся документация] → один WORKFLOW, один audit, один reconciliation; canonical artifacts со ссылками, без нового tracker.
- [Нежелательные микросогласования] → единый per-artifact пакет, но обязательные propose/apply и update confirmations сохраняются.
- [Недоказанная безопасность] → guidance явно advisory; не обещать enforced boundary.
- [Потеря контекста] → ORCH-01 / CRITICAL открыт и упоминается при handoff; MemPalace не controller.
- [Отсутствующий optional plugin] → использовать проверенный source workflow без автоматической установки.

## Migration Plan

1. Создать/проверить proposal, design, tasks. Остановиться на границе A.8, не начинать apply в этом же ходе.
2. После отдельного apply: audit, mapping всех product tasks/scenarios, proposed reconciliation. Создать WORKFLOW и подготовить точные edits AGENTS/config/TODO; product revisions подтверждать отдельно.
3. Проверить CLI и tabletop кейсы. Зафиксировать semantic review, реальные ограничения, безопасно обновить только tasks/openspec MemPalace corpora.
4. Для rollback перед каждым существующим docs edit сохранить исходный фрагмент и точный diff в reconciliation, без secrets. Обратный patch применять только к своему неизменённому после записи фрагменту; при конкурентном изменении остановить rollback и согласовать конфликт. Не удалять research/receipts или новые пользовательские данные.
5. Итоговый отчёт отделяет docs completion от product readiness. Архивация отдельно разрешается; product change и ORCH-01 остаются открытыми.
