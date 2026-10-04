## Purpose

Публиковать только точно проверенный и разрешённый результат разработки, сохраняя явную неопределённость при гонках отмены и потерянных ответах внешней площадки.

## ADDED Requirements

### Requirement: TG-09 Scoped autonomous publication and owner-controlled merge
После согласования проекта и spec revision система SHALL автономно создавать отдельный приватный repo под настроенным GitHub owner, отправлять проверенный candidate в task branch и создавать PR. Дополнительное подтверждение каждого push/PR SHALL NOT требоваться в согласованной области. Merge main SHALL требовать решения владельца для точного repository/PR/head commit и актуальных проверок штатными средствами Hermes/диалогом Telegram. Удаление repo и изменение прав/видимости SHALL требовать отдельного подтверждения. GitHub CLI авторизация SHALL быть отдельной от ChatGPT и доступной только этапу публикации; production deploy не входит в MVP1.

#### Scenario: Merge approval does not match
- **WHEN** изменён head commit или целевой repo/PR после подтверждения merge
- **THEN** слияние отклоняется, проверки выполняются для нового candidate и требуется новое решение владельца

#### Scenario: Approved task publication
- **WHEN** verified candidate относится к согласованному проекту и revision
- **THEN** publisher создаёт или обновляет соответствующий PR без дополнительного approval, читает обратно точные repo/branch/commit/PR и не выполняет merge автоматически

#### Scenario: Worker tries to publish directly
- **WHEN** инженерный исполнитель обращается к публикационным credentials или пытается создать PR вне доверенного интерфейса
- **THEN** операция отклоняется и не считается разрешённым результатом задачи

### Requirement: TG-10 Cancellation and ambiguous side effects
Система SHALL сериализовать допуск sending с отзывом generation. Отмена до допуска MUST запрещать отправку; отмена после допуска SHALL сообщать о возможном внешнем эффекте. Пустой поиск PR MUST NOT считаться доказательством отсутствия ещё выполняющегося запроса.

#### Scenario: Cancel wins admission race
- **WHEN** отмена зафиксирована до допуска sending
- **THEN** соответствующий внешний запрос не отправляется

#### Scenario: Response lost after sending
- **WHEN** ответ потерян или прежний запрос может завершиться позднее, даже при пустом lookup
- **THEN** система сохраняет unknown и не создаёт второй PR автоматически; поздний эффект сопоставляется с исходным intent
