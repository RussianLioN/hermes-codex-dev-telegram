# Экспертные решения автономного этапа

## DEC-N01-001 — не подменять адресность сериализацией

Статус: принято техническое решение BLOCKED_FOR_PROTECTED_ACTIONS; gate N-01 не закрыт. Это не owner approval и не нормативное изменение требований.

### Фактические консультации

Запущены три отдельных `codex exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox read-only --color never` с packet через stdin, без разрешения tools. E03 Hermes integrator, E05 distributed systems, E07 security architect. Все процессы exit 0, timeout 180 секунд не достигнут. Передавались только source findings и ограничения, без credentials. Отдельные контексты одной модели, не независимые модели. Cross-model не проводился в автономном этапе.

Пакет: stable v2026.9.7 adapter:3795–3818 сохраняет approval_id→session_key; :4297 вызывает resolver без request_id; approval.py:137–168 имеет адресный аргумент, но по умолчанию FIFO; isolated resolver probe; обязательны native-only и exact protected-action approval. Вопросы: достаточна ли сериализация, можно ли считать slash confirm альтернативой без caller trace, минимальная следующая проверка.

Краткие выводы, не дословные стенограммы:
- E03: сериализация уведомлений не доказывает единственный live запрос или защиту от устаревшей кнопки; нужен настоящий callback с fake transport.
- E05: A expired → B pending → tap A может разрешить B даже без одновременных pending; проверить повтор, cancellation и session boundary.
- E07: не использовать недоказанную привязку для инфраструктуры/merge; slash path требует source trace, разрешение владельца не заменяется council.

Разногласий по запрету считать FIFO точным подтверждением нет. Это не три независимых доказательства: общий packet и модель создают корреляцию.

### Проверка и reconciliation

После консультаций исполнены extracted callback, claim-state и resolver из pinned upstream `cbd03e6e4ca143c1d5c2db881320afb85783c30b` через локальный probe. Подтверждён сценарий B-button → A, а также retained-A-map → B при синтетическом начальном состоянии. Production timeout cleanup не проверен. Контрпример про повтор уже consumed кнопки уточнён: actual state.pop предотвращает повторное разрешение без восстановления/collision mapping; в probe повтор не разрешил B. Не объявлять все повторы уязвимыми.

`gateway/slash_commands.py` stable:1128–1145 вызывает resolver только с session_key/choice/resolve_all, не request_id. `/approve <id>` как адресный интерфейс не подтверждён и по этому parser не реализован; не предлагать эту команду владельцу. `send_slash_confirm` — отдельный механизм; наличие confirm_id не доказывает подключение к exec approvals.

### Решение

Не менять core, не строить custom approval service, не включать global YOLO и не принимать сериализацию как доказанное исправление. Не выполнять защищённые infrastructure/merge действия через исследованный FIFO путь. Независимые read-only readiness задачи продолжаются. Если другого штатного пути не найдётся, владельцу нужен выбор изменения scope либо разрешение отдельно ограниченной работы над исправлением; unsafe rollout не является вариантом.

ORCH-01 / CRITICAL остаётся открытым. Его реализация не устранит ошибку адресации разрешений.
