## Purpose

Предоставлять долгоживущие контейнеры проектов на общем сервере без расширения доступа к инфраструктуре и без удаления пользовательских данных при обслуживании ресурсов.

## ADDED Requirements

### Requirement: ENV-01 Persistent isolated project environments
Система SHALL размещать на ainetic.tech один переиспользуемый контейнер на проект с воспроизводимым Dev Containers описанием и сохранять его между задачами и ручными SSH-сеансами. Отдельная папка проекта на диске сервера SHALL подключаться через bind mount и сохранять код, Git metadata/worktrees, WIP, полную проектную историю Hermes/Codex, память, спецификации, checkpoints и результаты при удалении/пересоздании технического контейнера. Owner/project identity, mounts, network и CPU/RAM/disk/concurrency limits SHALL применяться до запуска. Изменения base image, host paths и mount permissions SHALL требовать owner approval через Telegram; изменения devcontainer агентом не обходят этот gate. Project code MUST NOT получать host root, privileged mode, управляющий Docker socket или чужие проектные данные. Сохранность файлов SHALL NOT выдаваться за непрерывность процесса после разрушения контейнера.

#### Scenario: Resource admission
- **WHEN** несколько проектов готовы, но их запуск превысит установленный лимит
- **THEN** допущенные проекты работают параллельно в своих границах, остальные ожидают; чужие сервисы сервера не останавливаются

#### Scenario: Untrusted environment change
- **WHEN** изменение devcontainer добавляет host mount или расширяет capabilities
- **THEN** оно не применяется автоматически, пока политика и владелец не разрешили конкретное изменение

#### Scenario: Recreate project container
- **WHEN** технический контейнер удалён и пересоздан в отдельно разрешённой проверке
- **THEN** тот же owner/project получает прежнюю server folder с кодом, Git/worktrees, WIP, историей и checkpoints; стартовый контекст восстанавливается по MEM-12, а прежний процесс не объявляется живым

#### Scenario: Next task reuses environment
- **WHEN** новая задача или ручная SSH-сессия обращается к существующему разрешённому проекту
- **THEN** используется тот же project container и постоянное хранилище, без нового контейнера на каждую задачу; writers получают отдельные worktrees

### Requirement: ENV-02 Ownership-aware cleanup
Система SHALL автоматически удалять только подтверждённо неиспользуемые технические контейнеры, образы, сети, кэши и временные области, принадлежащие системе. Ссылки активных задач, worktrees, rollback и backup SHALL учитываться перед удалением. Проверка и удаление SHALL исключать гонку нового admission. Остановленный контейнер MUST NOT считаться мусором только по статусу. Код, память, спецификации и результаты SHALL удаляться лишь по явному owner approval; исключение retention backups определено BACK-03.

#### Scenario: Unrelated resource
- **WHEN** Docker сообщает reclaimable образ стороннего сервиса
- **THEN** очистка не удаляет его и не запускает глобальный system prune

#### Scenario: New use during cleanup
- **WHEN** ресурс стал нужен задаче между предварительным сканированием и удалением
- **THEN** удаление отменяется при повторной защищённой проверке, активная работа и её данные сохраняются

#### Scenario: Detached manual session is still active
- **WHEN** SSH-соединение закрыто, но ручная сессия продолжает работать
- **THEN** её контейнер, worktree и история остаются используемыми ресурсами; отсутствие SSH-клиента не разрешает cleanup
