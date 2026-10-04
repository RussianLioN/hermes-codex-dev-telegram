# Решения интервью MVP1

Источник исходного интервью: явные ответы владельца, собранные в `.hermes/plans/2026-09-11_002258-telegram-hermes-codex-mvp1.md`. Таблица D-01–D-26 ниже сохранена как история. Уточнения 2026-09-23 имеют приоритет в указанных областях; точная новая spec revision и deploy ещё не утверждены. Нормативные требования — specs/*/spec.md; найденное противоречие возвращается владельцу, а не разрешается по памяти агента.

| Решение | Подтверждённый результат | Контракт |
|---|---|---|
| D-01 Shared tooling | Общие знания/проектные файлы/совместимые skills с адаптерами Hermes и Codex, credentials отдельно | MEM-10–11, TG-04–05 |
| D-02 Owner | Один владелец сейчас, будущие отдельные owner/project scopes | TG-01, ENV-01 |
| D-03 Autonomy | YOLO внутри проекта; infrastructure только по запросу владельцу | TG-05 |
| D-04 Container lifecycle | Persistent container на проект, адресная cleanup без удаления пользовательских данных | ENV-01–02 |
| D-05 SSH | Managed SSH + Dev Containers база, интерактивный доступ MVP2; перед его реализацией app-server comparison | proposal Non-goals |
| D-06 Preview | Только локальный interface с demo data, обычный Git, без server preview/framework/paid service | PRE-01–02 |
| D-07 GitHub | Отдельные private project repos в аккаунте RussianLioN, настраиваемом для будущих owners | TG-01, TG-09 |
| D-08 Publication | Auto repo/task branch push/PR после spec agreement; merge main и visibility/rights/delete только owner | TG-09–10 |
| D-09 Parallelism | Несколько проектов и субагенты; separate writer worktrees, serial integration, конфигурируемые limits | TG-03, ENV-01 |
| D-10 ORCH-01 | Минимальный независимый controller в MVP1, bounded retry, unknown effects reconcile | REC-01–02 |
| D-11 Codex auth | ChatGPT subscription, без API fallback | TG-05 |
| D-12 Memory | Вариант 3: Markdown/Git sources + MemPalace index + context packets; full persona exchange позже | MEM-10–11 |
| D-13 Fixture | contemporary-dance-guide: русский guide + вымышленная студия, HTML/CSS/JS, file://, no backend | PRE-01–02 |
| D-14 Maintenance | Existing updater ждёт задачи с timeout; defer вместо принудительного прерывания | UPD-01–02 |
| D-15 Shared installs | Общие tools/skills — owner approved pinned updates; project dependencies автономны | TG-04 |
| D-16 Approvals | Только штатный Hermes/диалог Telegram, без собственных кнопок и approval service | TG-01, TG-09, TG-11 |
| D-17 Host | Codex на том же ainetic.tech, лимиты и защита существующих сервисов | ENV-01 |
| D-18 Preview revision | Просмотр task branch/commit до merge, не отдельная preview branch | PRE-02 |
| D-19 Knowledge repo | RussianLioN/agent-knowledge; предложения знаний через PR, owner merge, raw/checkpoints вне Git | MEM-10–11 |
| D-20 GitHub auth | Отдельная GitHub CLI авторизация только у этапа публикации | TG-09 |
| D-21 Off-host backup | GitHub обязателен; agent-backups, public-key encryption, private key вне host/GitHub, credentials исключены | BACK-01–02 |
| D-22 Cheap backup | Не hourly full: changed projects, milestones/pre-maintenance и daily fallback; не дублировать доступный код | BACK-01 |
| D-23 Retention | 30 дней; удалять только при более новой verified-on-restore copy; последняя verified/dependencies защищены | BACK-03 |
| D-24 Restore | Ручная локальная команда в отдельный каталог, без исполнения/перезаписи; owner report через Telegram с ID/checksum | BACK-03 |
| D-25 Detection | До пяти минут при живом controller; quiet process не dead, stage timeouts отдельно | REC-01 |
| D-26 Outage | Внешнего host monitoring нет; после возврата сообщить прерывание и reconcile | REC-02 |

## Уточнения 2026-09-23

Интервью завершено; владелец подтвердил итог знаком «+» как согласованное намерение, затем разрешил пакет словами «Обновляй OpenSpec по этому пакету». Это разрешение только на документы, не approval получившегося digest и не запуск реализации. План интервью: `../../../.hermes/plans/2026-09-23_133530-ephemeral-codex-sdd-interview.md`; слово ephemeral в имени не означает контейнер на задачу.

| Решение | Подтверждённый результат и причина | Связь с историей / контракт |
|---|---|---|
| D-27 Project lifecycle | «Б. Одинконтейнер на проект! Причем крайне важно сохранять весь контекст по проекту через мапиинг на папку диск сервера!» Один переиспользуемый контейнер, отдельная постоянная server folder через bind mount; не контейнер на задачу или SSH-сеанс | Уточняет D-04; ENV-01–02 |
| D-28 Full history | «нужна полная сохраняемая история, а при запуске агент автоматически получает актуальный контекст из неё». Полная история отдельно от ограниченного стартового контекста; compression/index rebuild не удаляют оригиналы | Расширяет D-12; MEM-10–12 |
| D-29 Independent SSH | Ответ «А»: отдельный обычный интерактивный Codex CLI в контейнере проекта, с его контекстом, не перехват Hermes-задачи | Заменяет перенос SSH в MVP2 из D-05; SSH-01 |
| D-30 Parallel writers | Ответ «Б»: ручная и автоматическая работа параллельно, отдельные Git branches/worktrees, отдельная последовательная интеграция с повторными тестами | Уточняет D-09; TG-03, SSH-01 |
| D-31 Extension levels | «+»: общие OpenSpec/MemPalace/skills/rules с проверенными адаптерами Hermes/Codex; проектные зависимости, инструменты и skills изолированы | Уточняет D-01/D-15; TG-04 |
| D-32 Authority | «+»: внутри разрешённого проекта code/dependencies/tests автономны; shared tools/skills, base image, server settings, SSH access и mount permissions — после approval через Telegram. Существующие ежедневные stable updates Hermes продолжают свою согласованную автоматическую политику | Уточняет D-03/D-14/D-15/D-16; TG-01, TG-04–05, UPD-01–02 |
| D-33 First acceptance | Ответ «А»: сначала рабочая среда Telegram → Hermes/Codex → изменения/tests → отчёт, SSH/worktrees и восстановление истории/контекста. Private PR, contemporary-dance-guide и encrypted offsite backup/restore — последующие инкременты полного MVP1, не отменённые требования | Меняет порядок D-07/D-08/D-13/D-21–24, не их критерии; TG-08 |
| D-34 SSH disconnect | Ответ «А»: ручная сессия продолжает работать при разрыве SSH; reconnect возвращает в ту же сессию. Разрушение контейнера не обещает сохранение живого процесса, только восстановление данных/контекста | SSH-02, MEM-12, REC-01–02 |

Варианты контейнера на задачу, перехвата Hermes-сессии и обязательного последовательного ручного/автоматического исполнения отвергнуты. Общий writable home с credentials не выбран. Предварительное сравнение с app-server из D-05 более не является продуктовым prerequisite обычного интерактивного CLI; точный штатный launch/session interface всё равно требует source discovery. ORCH-01 / CRITICAL остаётся обязательством полного MVP1, не закрывается первым промежуточным результатом, историей или surviving SSH session.

## Не выбрано и не следует считать разрешённым

- Реальный implementation repo, exact APIs и доступный ресурсный бюджет.
- Конкретный механизм безопасной подписочной авторизации нескольких Codex процессов.
- Развёртывание server memory и настройки GitHub credentials.
- Использование Releases для backup до проверки условий/лимитов.
- Новый Telegram bot token, внешний embedding service, публичные preview endpoints.

Численные согласованные параметры: пять минут detection и 30 дней retention. Остальные лимиты не назначаются молча. План обновления docs не даёт полномочий изменить root host или создать перечисленные GitHub repos.
