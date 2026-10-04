## Purpose

Превратить авторизованный запрос из Telegram в однозначно привязанную к проекту и версии спецификации задачу, сохраняя эту идентичность при повторах и перезапусках.

## ADDED Requirements

### Requirement: TG-01 Authorized and revision-bound intake
Система SHALL принимать запрос только от разрешённого пользователя в разрешённом chat/topic и связывать его с owner_id, project_id, change_id, spec_revision, областью принимаемого инкремента и criterion IDs. MVP1 SHALL обслуживать одного владельца с настраиваемым GitHub account RussianLioN, не зашитым в код. На первом этапе рабочей среды допуск локального проекта SHALL согласовывать project identity, постоянную server folder и границы действий; remote repository SHALL оставаться явно not_provisioned до publication-инкремента. Перед созданием отдельного приватного repo SHALL согласовываться его имя и owner binding вместе со спецификацией; контракт TG-09 применяется в согласованной publication-области, не вызывает раннее создание repo ради локального запуска. Неутверждённая revision SHALL блокировать исполнение. Подтверждения SHALL использовать только штатные средства Hermes и обычный диалог Telegram; неподдерживаемый обязательный gate SHALL блокировать действие, не создавать собственный approval service.

#### Scenario: Unknown project
- **WHEN** пользователь ставит задачу без однозначного проекта
- **THEN** система запрашивает выбор проекта и не запускает worker

#### Scenario: Revised specification
- **WHEN** требования меняются после approval
- **THEN** прежний approval становится недействительным и исполнение новой revision остаётся заблокированным

#### Scenario: Unauthorized sender
- **WHEN** запрос отправлен пользователем вне allowlist
- **THEN** задача не создаётся и данные проекта не раскрываются

#### Scenario: New project agreement
- **WHEN** владелец согласует новую спецификацию и предложенное свободное имя репозитория
- **THEN** система сохраняет owner/project/repository binding и не подменяет его другим аккаунтом при последующей публикации

#### Scenario: Native approval unavailable
- **WHEN** штатный механизм не может надёжно связать решение владельца с конкретным защищённым действием
- **THEN** действие остаётся blocked с описанием пробела; собственные кнопки и альтернативный approval service не создаются

#### Scenario: Local environment before remote publication
- **WHEN** владелец одобрил exact revision и local-project scope первого этапа без publication
- **THEN** задача связывается с project folder и локальной Git history для worktrees; отсутствие remote repo/PR не блокирует разрешённую локальную работу и не выдаётся за созданный GitHub repo

### Requirement: TG-02 Replay-safe admission
Система SHALL связывать все доставки одного Telegram update с одним устойчивым intent и native task mapping. Worker MUST NOT стартовать до сохранения mapping и проверки актуального поколения; неизвестный исход прежнего create SHALL блокировать повторное создание до сверки.

#### Scenario: Concurrent repeated delivery
- **WHEN** одно обновление одновременно доставлено повторно, в том числе после restart
- **THEN** существует одна логическая задача, один native mapping и не более одного разрешённого запуска попытки

#### Scenario: Crash before mapping
- **WHEN** карточка создана, но процесс завершился до сохранения mapping
- **THEN** карточка остаётся недоступной для dispatch и восстановление сверяет прежний intent до любых новых запусков

#### Scenario: Ambiguous previous producer
- **WHEN** поиск не нашёл карточку, но завершение предыдущего producer не подтверждено
- **THEN** система сохраняет блокировку вместо нового create
