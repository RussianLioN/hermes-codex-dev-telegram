## Purpose

Доставлять пользователю в правильный Telegram chat/topic проверяемый прогресс и артефакты разработки, независимо восстанавливая уведомления после сбоев транспорта.

## ADDED Requirements

### Requirement: TG-11 Route-bound observable results
Система SHALL использовать доверенную исходную привязку user/chat/topic/project для статуса и артефактов. Пользователь MUST различать исполнение, verification, approval, публикацию и доставку; локальный путь к файлу SHALL NOT выдаваться за успешно отправленное вложение. Отчёт первого этапа SHALL содержать task/session identity, project/worktree/branch, base/candidate revision либо явный WIP, реальные команды/результаты проверок, ссылки на сохранённые артефакты и blockers. PR, preview и offsite backup SHALL отмечаться not_provisioned/not_run, если соответствующий инкремент не реализован, а не выдумываться ради полноты отчёта.

#### Scenario: Gateway cannot access artifact
- **WHEN** screenshot существует только в container path, недоступном отправляющему gateway
- **THEN** доставка отмечается неуспешной, а пользователь не получает ложное подтверждение вложения

#### Scenario: Ambiguous owner reply
- **WHEN** ответ владельца нельзя однозначно связать с ожидаемой спецификацией, merge или инфраструктурным действием
- **THEN** Hermes запрашивает уточнение в обычном диалоге и не выполняет действие; собственные кнопки/approval service не создаются

#### Scenario: Working environment report without PR
- **WHEN** разрешённая задача первого этапа завершила реальные изменения и проверки без GitHub publication и preview
- **THEN** исходный Telegram route получает проверяемый отчёт о коде/тестах и состоянии проекта; отсутствие PR/preview явно обозначено и не превращает успешно проверенную локальную работу в заявленную полную готовность MVP1

### Requirement: TG-12 Delivery retries do not rerun development
Система SHALL восстанавливать доставку по сохранённым результатам и отдельным delivery receipts. Ошибка Telegram MUST NOT перезапускать Codex, тесты или публикацию. При неоднозначном сетевом ответе допускается ограниченный повтор уведомления, но не новая инженерная задача.

#### Scenario: Transport restart
- **WHEN** gateway перезапускается после выполнения задачи до подтверждения доставки
- **THEN** восстанавливается отправка прежнего результата в исходный маршрут, без нового run

#### Scenario: Local preview delivery
- **WHEN** проверенный статический preview опубликован в ветке задачи
- **THEN** бот сообщает repo, branch, точный commit, PR, результаты проверок и путь preview/index.html; владелец получает файлы обычным Git, без серверного preview, нового сервиса синхронизации и автоматического исполнения на локальной машине
