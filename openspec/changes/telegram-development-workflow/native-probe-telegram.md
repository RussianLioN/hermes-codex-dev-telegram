# N-01 продолжение: найден Telegram adapter и риск FIFO

Статус: source trace + isolated function probe, не live Telegram acceptance. Дополняет native-probe-n01.md; отсутствие adapter по старому пути разрешено обнаружением plugin path. Нормативная revision не изменялась.

## Источники установленного сервера

- `/opt/hermes/plugins/platforms/telegram/adapter.py:6518–6525`: register(ctx) регистрирует telegram, allowed_users_env и allow_all_env.
- `:5687–5699`: входящий текст проверяет `_is_user_authorized_from_message` до batching/agent. `:746–781` и `:4230–4238`: inline callback проверяет отправителя через injected auth callback, legacy runner или env fallback.
- `/opt/hermes/gateway/authz_mixin.py:473–544`: цепочка разрешений включает chat grants, platform allow-all, pairing, allowlists/global и default deny. Наличие TELEGRAM_ALLOWED_USERS само по себе не доказывает единственного owner: другие разрешения могут расширять доступ. Фактические credentials/env/pairing store не читались; текущий owner-only режим не подтверждён.

## Штатные кнопки действительно существуют

`adapter.py:3795–3818` send_exec_approval уже создаёт Allow Once, Session, Always, Deny. Параметры allow_session/allow_permanent управляют отображением широких вариантов. Это штатные кнопки Hermes, не отвергнутый собственный UI. Ограничение отображения не доказывает запрета `/approve session` или other path: нужна полная проверка policy.

## Конкретный риск адресации

- `:3803–3815`: локальный approval_id сохраняет только session_key в `_approval_state`.
- `:4273–4297`: callback извлекает этот session_key и вызывает `resolve_gateway_approval(session_key, choice)` без request_id.
- `tools/approval.py:137–169`: без request_id resolver выбирает FIFO.

Следствие по source: если в одной session pending A и B, кнопка B может разрешить старейшее A. Нажатие устаревшей кнопки также нельзя считать безопасным только потому, что её исходный wait истёк: если появился другой pending той же session, этот путь не проверяет исходный request_id. Live exploit/canary не выполнялся. Counter/map in-memory требует отдельной проверки stale callbacks после restart; не утверждается, что вся система лишена иных защит.

## Изолированная проверка resolver

Через SSH прочитан только исходник tools/approval.py. Локально AST извлёк ровно функцию resolve_gateway_approval без imports/runtime initialization; аннотации удалены для исполнения в изолированном namespace. Synthetic queue entries A/B и lock созданы только в памяти отдельного Python процесса. Реальная очередь gateway не затронута.

Фактический результат:

    PASS no request_id resolves oldest A, not B
    PASS explicit request_id B resolves B
    SCOPE local isolated function execution; synthetic entries; no Telegram call, no live queue access

Проверен сам server-source resolver, а не сетевой Telegram callback и не авторизация владельца. Две assertions прошли, exit 0.

## Решение gate

N-01 остаётся открытым с конкретным blocking risk для exact protected actions. Одного совета «не запускать два запроса сразу» недостаточно без проверки stale buttons и restart. Не создавать собственный approval service и не патчить работающий Hermes без разрешения. Дальше read-only проверить актуальное upstream исправление/штатную альтернативу и caller policy; если решения нет — представить владельцу ограничение до rollout.

Глобальный Hermes YOLO не включать как замену проектного Codex YOLO. ORCH-01 / CRITICAL не реализован; human wait не равен dead worker.
