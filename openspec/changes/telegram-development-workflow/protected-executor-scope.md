# Следующий owner scope: локальный протокол ограниченного исполнителя

Статус: **AUTHORIZED_LOCAL_ONLY**. Владелец подтвердил текущий запрос словами «Текущи запрос подтверждаю и продолжай далее автономно». Разрешён только перечисленный local implementation scope; transport/PTB повторно не согласуются. Production implementation/spec approval этим подтверждением не выданы.

## Причина

Новые реальные native probes показали, что transport не вызывается для generic actions и не является обязательным veto при отсутствующем/упавшем hook. Без отдельного ограничения полномочий нельзя честно обещать «подтверждение именно этой операции → автоматическое исполнение без обхода». Менять ядро или выполнять защищённые действия вручную не предлагаем.

Evidence: `../../../.hermes/tooling/telegram-approval-prototype/boundary-evidence.md`; technical reconciliation: `boundary-council.md` в том же каталоге. Независимые пробы N-02–08: `../../../.hermes/research/telegram-hermes-codex/readiness-probes-2026-09-11.md`.

## Разрешение, которое требуется сейчас

Разработать только project-local прототип протокола ограниченного исполнителя в предлагаемом каталоге `.hermes/tooling/protected-operation-prototype/`, без установки в Hermes или рабочую систему. Использовать имеющиеся Python/stdlib и изолированный transport harness; новых dependency installs не разрешать по умолчанию.

Прототип не серверный сервис и не автономный daemon. Только запускаемые тестами короткоживущие процессы и temporary synthetic resources. Он моделирует границу исполнения; до отдельного испытания OS isolation НЕ считается границей полномочий против процесса того же UID.

## Ограниченный функциональный контракт

1. Typed operation вместо произвольного shell: единственная первая операция — создание заранее ограниченного безвредного synthetic marker во временном стенде. Никаких SSH/GitHub/Docker/merge/infra effects.
2. Immutable manifest связывает owner/project/native task ID/run ID/operation ID/type/target/revision/arguments/deadline. Credential values не входят в manifest; в текущем стенде credentials отсутствуют.
3. Точное once/deny решение приходит через уже проверяемый transport harness. Изменение любого связанного поля, другой owner, истечение времени и повтор отклоняются. Synthetic updates не называются настоящим Telegram.
4. После допуска marker создаётся автоматически и читается обратно. До допуска effect отсутствует. Повтор/конкурентное предъявление не даёт повторного исполнения.
5. Technical SQLite journal хранит только operation admission/attempt/unknown/result. Не создаёт пользовательскую очередь, не выбирает следующую Kanban task и не подменяет ORCH.
6. Сбой/потеря ответа после возможного эффекта сохраняют unknown. Reconciliation использует точный marker/operation ID/revision; отсутствие доказанного результата не превращается в слепой повтор. Checkpoints/restart проверяются новыми процессами на synthetic journal.
7. Native Kanban остаётся task authority. Local fixture run fencing можно использовать как протокол, но перед production нужна проверка actual server revision и stale-effect fencing у конечного ресурса.

## Проверки и честные границы приёмки

После разрешения сначала отдельный implementation plan и TDD для protocol code; tests negative owner/revision/expiry/replay/concurrent approval/stale run/unknown after crash. Результат — работающий локальный protocol artifact, не production N-01 acceptance.

OS boundary остаётся отдельным последующим gate: новый непривилегированный процесс не должен иметь прямого доступа к защищённому resource/code/policy/journal/credentials. Два процесса одного UID этого не доказывают. Создание users, изменение sandbox/permissions/SSH и рабочая установка требуют своего точного scope и rollback; данный запрос их НЕ включает.

## Явно не разрешается этим scope

- Core/fork/monkeypatch или изменение Hermes installation/active profiles.
- Подключение рабочего бота, чтение/копирование OAuth и других настоящих credentials.
- Создание контейнеров/пользователей, изменение сервера/updater/SSH/permissions.
- Новый daemon/server service/task queue/updater.
- GitHub repo/push/PR/merge/upload, публикация и deployment.
- Объявление ORCH-01 выполненным. **ORCH-01 / CRITICAL открыт.**

## Одна формулировка подтверждения

«Разрешаю локальный прототип ограниченного исполнителя в указанном scope, без изменения ядра Hermes, установки в рабочие профили, подключения бота и изменений сервера».

Такое подтверждение разрешит только перечисленную local protocol работу. Оно не одобряет финальную OpenSpec revision или production effects.
