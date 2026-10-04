## Purpose

Доставлять владельцу проверенный статический интерфейс через GitHub для локального просмотра обычным браузером, без дополнительных сервисов на ainetic.tech.

## ADDED Requirements

### Requirement: PRE-01 Contemporary dance acceptance project
Первый проект SHALL быть отдельным приватным RussianLioN/contemporary-dance-guide: русский информационный гид о современном танце с явно вымышленной студией. Страница SHALL содержать объяснение современного танца, направления, советы начинающим и демонстрационные сведения студии. Факты SHALL иметь проверенные источники, вымысел SHALL быть помечен. HTML/CSS/JavaScript SHALL работать без framework/build, backend, БД, регистрации, платежей и сбора заявок.

#### Scenario: Demo is not presented as real service
- **WHEN** владелец просматривает раздел студии
- **THEN** преподаватели/расписание помечены как демонстрационные, нет действующей отправки персональных данных или оплаты и нет утверждения о реальных занятиях

### Requirement: PRE-02 Offline exact-revision delivery
preview/index.html SHALL открываться через file:// с относительными локальными assets, без обязательного CDN, fetch, JS modules и API. Страница SHALL поддерживать мобильный и desktop viewport и клавиатурную навигацию. Preview SHALL находиться в той же task branch и commit, что проверенный candidate, до merge main. Владелец SHALL получать его обычными git clone/fetch/pull --ff-only и выбором ветки; автоматический запуск кода, собственный синхронизатор и server preview исключены.

#### Scenario: Offline local opening
- **WHEN** владелец получил точную ветку/commit и отключил сеть
- **THEN** открытие preview/index.html показывает интерфейс с демонстрационными данными без ошибок загрузки обязательных ресурсов

#### Scenario: Local modifications
- **WHEN** получение новой версии конфликтует с локальными правками или разошедшейся историей
- **THEN** обновление не выполняет force/reset и не стирает правки; владелец получает понятное указание разрешить конфликт обычным Git
