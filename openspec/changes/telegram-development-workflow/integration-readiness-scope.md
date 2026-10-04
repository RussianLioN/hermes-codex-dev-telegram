# Единый оставшийся integration-readiness scope

Статус: **AUTHORIZED_LOCAL_INTEGRATION**. Владелец ответил «разрешаю» на весь этот scope. Все шесть направлений реализуются без дополнительных микросогласований в перечисленных границах. Предыдущий scope A выполнен, receipt: `.hermes/tooling/protected-operation-prototype/server-evidence.md`. Production installation, новые server effects и итоговая spec approval остаются вне разрешения.

## Причина нового объёма

Разрешённые transport, local marker protocol и одно OS испытание завершены. Они не разрешают реализацию остальных частей MVP1, установку Codex в рабочую серверную среду или настройку publisher. Незакрытые readiness 1.1–1.5 нельзя превращать в approved exact production spec по локальному успеху. Чтобы не останавливаться на каждом новом компоненте, предлагается один локальный интеграционный объём для всех оставшихся интерфейсов.

## Что разрешить одним решением

Разработать и испытать связанный локальный стенд `.hermes/tooling/mvp1-integration-prototype/` по существующим требованиям:
1. Native Kanban task/run → immutable operation → существующий Bridge/protocol → проверяемый synthetic result, включая restart/replay/cancel/unknown; без новой пользовательской очереди.
2. Минимальный независимый ORCH controller в тестовом процессе: heartbeat, quiet build, bounded retries, restart и отсутствие повторного external effect. Это только прототип требуемого controller; systemd/cron/новые profiles не устанавливаются, ORCH-01 не закрывается автоматически.
3. Границы переносимой памяти: synthetic owner/project scope до retrieval, checkpoint/readback/failure; без индексации реальных credentials/историй и без изменения установленного memory provider.
4. Fixture существующего updater на просмотренном source: task admission/drain/defer/backup failure и сохранение current auth state; никакого вызова apply/recover рабочего updater и никакой загрузки реального auth.json.
5. Publisher/backup state machines на явно mock GitHub responses и synthetic age data: lost response/reconciliation, reachable dependencies/restore/retention. Mock API не выдаётся за live acceptance; существующая локальная GitHub авторизация не копируется.
6. Подготовка точных deploy/canary diffs и общего rollback-пакета для оставшихся server/live gates после этих проверок. Только текст/локальные файлы, без исполнения deployment.

Существующие Python stdlib, разрешённый transport venv и installed age; новые установки/обновления зависимостей не входят. Для всех новых slices сначала source discovery и TDD, bounded review полного E01–E19. Точные API/команды берутся из source/help, не придумываются. Процессы короткоживущие с timeout и проверкой cleanup, данные во временных каталогах. Existing project files только разрешённые docs/prototype, не исторические runtime repositories.

## Что не разрешается

Core/fork/monkeypatch; установка в Hermes или другие profiles; новые server containers/users/services; изменения compose/updater/SSH; real GitHub create/push/PR/merge/upload; чтение/копирование токенов; новая авторизация; исполнение проектного кода с доступом к реальным credentials. Реальные Codex model tasks кроме уже разрешённого read-only консилиума этим scope не добавляются. Это не разрешение production реализации и не owner approval будущей spec revision.

## Авторизация и участие владельца

- Локальные Codex/ChatGPT и GitHub RussianLioN подтверждены; повторный вход не нужен.
- Hermes openai-codex на сервере logged in; persistence/recovery wiring найден. Существующий вход не заменять и не восстанавливать токены из backup.
- Серверный host-root gh требует login; gateway gh/Codex CLI отсутствуют в PATH. Не предлагать login в root: сначала подготовить изолированный publisher scope. Будущий единый рабочий пакет включает настройку publisher, только действительно необходимые authorization steps, live Telegram и restore/preview проверки.
- До этого этапа пароль/ручной тест от владельца не требуется — нужен только явный scope реализации перечисленных остальных компонентов, который нельзя получить голосованием консилиума.

## Критерий завершения

Фактический результат реализации: `LOCAL_INTEGRATION_VERIFIED / DEPLOY_PACKET_BLOCKED`. Связанный прототип и fault regressions — `.hermes/tooling/mvp1-integration-prototype/README.md`, 33 tests OK. Transport regression сохраняет 1 expected failure из 40 tests; protected protocol 23 tests OK. Направления проверены только в явно обозначенных local/mock/historical пределах; updater не интегрирован с рабочей системой. Шестой пункт (точный рабочий deploy diff) не завершён: неподдержанные/непроверенные native и credential boundaries перечислены в `integration-live-gates.md` вместе с общими rollback/authorization/acceptance процедурами. Это технический blocker, не отзыв разрешения локального scope и не запрос согласовать компоненты повторно.

Реальный связанный локальный artifact с tests/fault receipts, таблица оставшихся именно live gates, подготовленный единый рабочий diff/rollback и процедуры авторизации/приёмки. Никаких промежуточных остановок между шестью направлениями; blocker одного направления не останавливает независимые разрешённые задачи. Неподдержанный native API фиксируется как blocker, не обходится правкой Hermes.

Разрешение формулируется: «Разрешаю весь локальный integration-readiness scope без установки в рабочую систему и реальных внешних эффектов». После него новые локальные компоненты из этого списка не согласуются по одному.

ORCH-01 / CRITICAL остаётся открытым до согласованной реальной приёмки.
