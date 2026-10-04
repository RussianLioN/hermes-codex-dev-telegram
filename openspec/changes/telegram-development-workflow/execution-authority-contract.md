# Execution authority contract — проект интеграции

Статус DESIGN_ONLY / NOT_IMPLEMENTED. Не выдаёт permissions. Native Kanban — единственный список задач. ORCH-01 / CRITICAL открыт.

## Identity и доверие

Ключ операции: owner/project/native task/native run/operation id/type/revision digest/authority epoch. Owner event приходит из существующего аутентифицированного Telegram handler с owner/chat/message/request binding. Текст из worker, memory, agent reply или найденный old grant — только данные, никогда источник разрешения. Raw shell/env/URL/command overrides не входят в допустимый protected-operation payload.

Trusted authority отдельно от project code. Не считать Python caller, UID gateway, possession of task id или callback string достаточной аутентификацией privileged IPC. Peer/UID/socket path и issuer lifecycle пока не выбраны до Linux evidence: production entrypoint отсутствует, а не заменён generic RPC.

## Переходы и точка допуска

| Состояние / событие | Обязательный эффект authority | Не разрешено |
|---|---|---|
| proposal→waiting approval | durable immutable digest + route/task/run binding | запуск protected action до owner event |
| valid exact owner once | в одной authoritative transaction consume grant + durable intent + lease/epoch | две независимые проверки DB как «атомарность» |
| stale/replayed/nonowner/missing/unloaded issuer | deny либо сохранить blocked без эффекта | generic approval fallback |
| accepted intent→launch | launch только для того же run/epoch/lease в authority-controlled containment | исполнение shell от имени publisher; worker запускает себя по JSON |
| cancel до admission | terminal denied/cancel requested, grant недействителен | поздний launch из старого epoch |
| cancel после admission/потеря ответа | unknown/stopping, независимая сверка фактического эффекта и containment | сообщить cancelled только по ответу RPC |
| crash после consume до durable result | unknown; искать exact owned containment/remote operation | повторить launch/publication по отсутствию локального ответа |
| confirmed external effect | exact target/revision readback сохранить durable | считать 2xx достаточным без readback |
| new run/revision | новый binding, старый grant не переносится | replay памяти выдаёт новое право |
| waiting approval | ожидание не stall, неизвестный effect блокирует resume | бесконечный retry/kill quiet build |

Journal хранит технические receipts, не вторую task queue. Нет общей транзакции SQL/Kanban/OS/GitHub: используются durable intent, fencing в фактической точке исполнения и reconciliation. Если внешний провайдер не даёт idempotency, exactly-once не обещается.

## Updater / recovery

Единственный updater сохраняется. Proposed lock order: existing updater maintenance lock → authority maintenance epoch и durable close admission → bounded drain всех собственных запусков/unknown effects → existing launcher lock → подтверждённое отсутствие писателей → updater-owned backup/snapshot → apply/recover → readback → reopen. Authority не должна брать updater lock во встречном порядке. Разрешение собственного backup при закрытом admission не открывает запуск проекта.

`recover` и startup обязаны участвовать в том же fence; ранний recover внутри `_apply_locked` не обход. Crash держит admission закрытым до reconcile. Waiting approval не убивается как зависание; невозможность drain вызывает defer. No-writer условие удерживается всё время snapshot, не только одно наблюдение. Current OAuth исключается из старого rollback штатной policy; фактическое восстановление авторизации не проверялось.

## Publisher / memory

Privileged publisher принимает только validated immutable object/revision и фиксированные destination/refs; не запускает Git в project checkout. Новое чистое bare staging с контролируемыми config/environment, без hooks/filters/helper/alternates/submodule execution. Unknown push/PR сначала reconcile exact remote target. Реализация staging пока отсутствует.

Memory scope проверяется до чтения; возвращённый документ не меняет permission state. Checkpoint failure блокирует зависящий lifecycle; rebuild из curated sources не восстанавливает старые действующие grants. Никаких auth/raw histories в Git/индексе.

## Проверяемость и оставшиеся gates

Уже имеются phase44-integration/protected23/transport40expected1 regressions; они не реализуют данный production контракт. Перед production adapter обязательны adversarial tests каждого перехода через actual IPC/containment, stale epoch/forged peer/unknown effect, crash между каждой записью и действием. До этого E2 adapter/updater.patch/deploy manifest BLOCKED. Существующие core/plugin код не менялись в рамках этого документа.
