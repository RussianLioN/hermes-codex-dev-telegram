## Purpose

Согласовать существующее ежедневное обновление Hermes с разработкой проектов, не вводя второй updater и не прерывая активную работу ради автоматического обслуживания.

## ADDED Requirements

### Requirement: UPD-01 Drain before existing updater disruption
Система SHALL использовать существующий updater на ainetic.tech и его окно обслуживания; штатные ежедневные stable updates SHALL сохранять согласованную автоматическую политику без нового approval каждого обычного обновления. Изменение самого инфраструктурного скрипта или его policy SHALL требовать owner approval через Telegram. Перед disruption SHALL закрываться admission новых задач/ручных сессий и завершаться активные в пределах заданного timeout. Ручная сессия, в том числе detached после SSH disconnect, SHALL учитываться как активная до подтверждённого завершения; отсутствие подключённого клиента не означает drain. При превышении timeout обновление SHALL откладываться без принудительной остановки задач/сессий, с уведомлением владельца. Lock ordering и cleanup SHALL не создавать deadlock и гонку запуска после drain.

#### Scenario: Active task exceeds maintenance wait
- **WHEN** активная задача не завершилась до deadline ожидания
- **THEN** обновление не останавливает gateway/workers, фиксируется defer и admission возвращается в допустимое рабочее состояние

#### Scenario: Manual session survives servicing deadline
- **WHEN** ручная Codex-сессия всё ещё активна после deadline обслуживания
- **THEN** updater откладывает disruption, не убивает сессию ради обновления и безопасно возвращает admission; это проверяется отдельно от одной только автоматической задачи

### Requirement: UPD-02 Verified update and recovery
В полном MVP1 перед разрешённым обновлением система SHALL получить согласованный snapshot и дождаться подтверждённого завершения изменившегося off-host backup с readback точного удалённого объекта; для неизменившегося набора SHALL подтверждаться покрытие существующей удалённой копией. Pending, unknown или failure обязательного backup SHALL откладывать обновление с blocker. Ручная restore attestation не требуется перед каждым обновлением и остаётся отдельным условием retention. Первая приёмка рабочей среды SHALL явно оставлять BACK-01–03 и полный off-host gate UPD-02 незавершёнными; это SHALL NOT разрешать отключение существующих backup/auth/snapshot/candidate-validation/rollback/pinned-image защит updater. Admission SHALL открываться только после проверок работоспособности и восстановления task/session state; ошибка восстановления SHALL оставлять его закрытым с объяснением.

#### Scenario: Candidate fails health checks
- **WHEN** обновлённый Hermes не проходит обязательную проверку
- **THEN** используется проверенный rollback/recovery путь существующего updater, пользовательские данные сохраняются, новые задачи не запускаются до подтверждённого восстановления

#### Scenario: First increment is not backup acceptance
- **WHEN** рабочая среда принимается до внедрения offsite backup/restore
- **THEN** отчёт не заявляет off-host protection или полный UPD-02; существующий updater и его защиты не ослабляются, изменение координации требует отдельного scope и проверок
