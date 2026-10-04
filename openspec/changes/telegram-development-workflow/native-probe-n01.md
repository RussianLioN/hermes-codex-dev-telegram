# N-01: статическое исследование штатных approvals

Статус: SOURCE_REVIEW_ONLY; gate не закрыт. Проверена установленная серверная копия `/opt/hermes` через read-only SSH/docker exec python. Функции не импортировались и не исполнялись; исходники читались как текст. Live Telegram requests, auth и restart не выполнялись. Это дополнительное evidence, не изменение нормативной spec revision.

## Наблюдения

1. `/opt/hermes/tools/approval.py:799–865`: `_run_approval_gate` явно обрабатывает YOLO bypass (817–818) и session-cache (820–821) до интерактивной ветки. `request_tool_approval` (930+) использует этот же gate. Следовательно, глобальный Hermes YOLO нельзя считать безопасным механизмом сохранения обязательного infrastructure approval. Это не утверждение о включённом YOLO на сервере: конфигурация не проверялась.
2. `tools/approval.py:887–901`: `_floor_block` содержит hardline и user deny checks до YOLO в соответствующем command path. Это блокировка некоторых команд, не доказательство универсальной изоляции всех tool/API действий.
3. `gateway/slash_commands.py:1128–1145`: штатный `/approve` существует; варианты once/session/always/all. Handler вызывает `resolve_gateway_approval(session_key, choice, resolve_all=...)` без request_id. `tools/approval.py:137–169` умеет request_id, но при его отсутствии выбирает FIFO. Поэтому при нескольких pending requests нельзя предполагать точное адресное подтверждение по тексту ответа.
4. `tools/approval.py:116–117`: очередь и notify callbacks — in-memory dictionaries. `approval_gateway_wait.py:25–36`: ожидающий entry содержит threading.Event. `gateway/slash_commands.py:1116–1126` сбрасывает stale prompt при отсутствии blocked thread. Эти места сами по себе не обеспечивают durable продолжение approval после смерти процесса; сквозной recovery требует проверки.
5. `approval_gateway_wait.py:39–67`: ожидание имеет deadline, interruption и heartbeat. Ожидание владельца не следует классифицировать как dead worker только из-за отсутствия обычного progress. `105–167`: notify failure возвращает unresolved, interrupted приводит к deny; identical requests coalesce, once не переиспользуется для follower без свежего prompt.
6. Поиск calls обнаружил shared gateway slash handler, relay adapter, API server, WhatsApp и QQ. Предполагаемый `gateway/platforms/telegram.py` и верхнеуровневое имя с telegram не обнаружены. Это не доказательство отсутствия Telegram: adapter может быть вне просмотренных каталогов/внешним пакетом. Owner authentication route и фактическая доставка пока не прослежены.

## Выводы для MVP1 (не новая реализация)

- Сохранить принятое разделение: YOLO только Codex/project execution, не глобальный управляющий Hermes.
- Не создавать собственный approval service. Сначала проверить возможность штатного одноразового approval при единственном ожидающем защищённом действии в маршруте.
- session/always и параллельные requests требуют отрицательных тестов для exact merge/infrastructure decision.
- После restart старое ожидание нельзя считать разрешённым. Требуется сверка pending task и новое штатное подтверждение, если исходное разрешение недоказуемо.
- Без проверки owner route и реального canary N-01 не считается пройденным. При несовместимости — blocker владельцу, не обход.
- ORCH-01 / CRITICAL должен отличать human wait от зависания; он не реализован.

## Следующие ограниченные проверки

Read-only: найти фактическую регистрацию Telegram adapter и pre-dispatch owner filter, проверить конфигурационные возможности once-only/YOLO scope без печати secrets. Canary: разрешённое безопасное действие, отказ, timeout, параллельные requests и restart на изолированной тестовой среде. Canary пока не запускался: потребуются отдельный scope и безопасная площадка, не restart рабочего gateway.
