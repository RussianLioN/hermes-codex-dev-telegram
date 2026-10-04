# Единый следующий пакет участия владельца

Статус: **A AUTHORIZED_AND_EXECUTED / LOCAL_INTEGRATION_AUTHORIZED / B–I LIVE PENDING**. Владелец подтвердил A; exact hash проверен, реальный canary exit 0 и независимый readback подтвердил отсутствие контейнера. Receipt: `.hermes/tooling/protected-operation-prototype/server-evidence.md`. Local executor и весь `integration-readiness-scope.md` уже разрешены; 33 integration tests OK. Технические blockers рабочего deployment diff и rollback constraints — `integration-live-gates.md`. Ниже сохранён точный scope выполненного A; повторный запуск этим однократным разрешением не покрыт. B–I — реестр последующих live участий, не blanket approval неизвестных diff. Локальные компоненты повторно не согласуются.

## Ближайшее необходимое разрешение A — ограниченный OS canary

Следующий эксперимент выходит за local-only scope: один короткоживущий Docker container на ainetic.tech. Не установка рабочей системы и не новый сервис. Цель — подтвердить базовую OS разницу между UID executor и недоверенным worker на synthetic ресурсах. Это не полная изоляция управляющего Hermes и не production N-01.

Точный предлагаемый scope:
- Новый контейнер с фиксированным именем `hermes-protocol-canary`, label `hermes.scope=protocol-canary`; если имя занято, отказ без удаления существующего.
- Только уже имеющийся image `sha256:c36a3717b18b07b4e61c7cd3f2a0a08c32e7823525179a9e4d57fd248f4a83ae` (read-only lookup подтвердил amd64/linux). Никаких pull/build/install.
- Проверенный в контейнере путь Python `/opt/hermes/.venv/bin/python3`; `/usr/bin/env` также проверен. ENTRYPOINT принудительно заменяется на `/usr/bin/env -i`, Python запускается с `-I -B`; image HEALTHCHECK отключён, pull/restart запрещены. Контроллер подаётся по SSH stdin, body передаётся Python как аргумент `-c`. Никаких Hermes imports/plugin/OAuth/LLM/сети; данные синтетические. Локальный script уже подготовлен и проверен ДО запроса серверного разрешения.
- `--network none --read-only --pids-limit 32 --memory 128m --cpus 0.25 --security-opt no-new-privileges --cap-drop ALL`; лишь `SETUID`/`SETGID` для перехода дочернего процесса на numeric UID/GID 65534. Главный процесс UID 0 остаётся только внутри этого контейнера, не управляющим Hermes.
- Только tmpfs `/work` (16 MiB, mode=0711), `/tmp` (16 MiB, mode=1777), `/opt/data` (1 MiB, mode=0700), все nosuid,nodev,noexec; shm 1 MiB, memory+swap 128 MiB. Read-only image lookup обнаружил объявленный VOLUME `/opt/data`: он явно перекрыт пустым tmpfs, actual mounts проверяются до start, volume/bind приводит к отказу. Родительские каталоги проходимы worker; protected files 0600 проверяются раздельно, доступный projects каталог даёт положительный control. Никаких host binds/Docker socket/host namespaces/ports/production credentials.
- Synthetic files code/policy/journal/credential-marker с owner-only режимами; worker должен получить EACCES на read/write/replace, но писать в свой synthetic project каталог. Parent разрешает единственный marker только после synthetic exact decision; readback проверяет эффект.
- Бюджет SSH 120 секунд, start/wait 60 секунд, явный SIGALRM handler body завершает PID1 через 30 секунд; ограниченные отдельные Docker calls. `--rm`; при сбое после получения ID очистка только exact созданного ID после сверки image+label. Admission отказывает при MemAvailable ниже 512 MiB или load1 выше 2. Никаких global prune/чужих ресурсов; gateway/updater/compose не меняются. При потере ответа create/SSH или недоступности Docker отсутствие ресурса не объявляется доказанным: read-only reconciliation по имени/image/label, без слепого повторного create или удаления неизвестного ID. Это не гарантия восстановления при потере host.
- Rollback: завершить только созданный ID и убедиться в его отсутствии; tmpfs удаляется вместе с контейнером. На хосте проектные данные не записываются.

Готовый script: `.hermes/tooling/protected-operation-prototype/os_canary.py`.
SHA256 файла: `84b3597a2956c6256a93c6869999b4ab3cdc5c05bb46bd4e922847097acfa975`.
SHA256 развёрнутого remote source: `3abdc6917b4ea1be5a39dec6db9f9f6cacd12033bebe3dc39845928a05e6ef01`.
Offline `--check` не вызывает subprocess; пять preparation tests проверяют argv, occupied name, unexpected volume и cleanup after timeout с явно mock Docker. Реального Docker canary ещё не было. Точная команда ПОСЛЕ разрешения из каталога прототипа: `../telegram-approval-prototype/.venv/bin/python -B os_canary.py --run-approved`. Разрешение A — только однократное описанное испытание этого script/hash; несовпадение image/limits/path запрещает автоматическое расширение scope.

## Последующие необходимые участия — собрать в ту же согласованную программу

B. Точная OpenSpec/design revision после закрытия readiness 1.1–1.5. Сейчас owner_approved=false. Local prototype не утверждает итоговый production дизайн. Контроллер ORCH-01 / CRITICAL обязателен, не реализован.

C. Рабочая инфраструктура и установка: отдельный exact diff/mounts/identities/rollback для проектного контейнера, ограниченного исполнителя, native transport/provider и независимого controller, а также изменения существующего updater для drain/admission/backup. Без нового updater, внешнего preview service, global YOLO или core patch. Сейчас diff не подготовлен, разрешение на его выполнение не запрашивается авансом. Готовые изменения должны быть представлены одним пакетом, а не по одному компоненту.

D. Авторизации: владелец выполняет отдельные browser/device authorization ChatGPT/Codex и GitHub только в готовой проверенной модели credential ownership. Tokens/пароли не передаются в чат. Наличие passwordless admin SSH не разрешает выдавать его worker. OAuth refresh lifecycle и subscription concurrency должны быть проверены, не замещены API key.

E. Backup key и restore: локальное создание/выбор age private identity у владельца; на сервер только public recipient. Подготовленная команда скачивает synthetic/первый реальный backup в новый локальный каталог и проверяет без исполнения кода/overwrite. Владелец подтверждает точные backup ID/checksum/result. Это owner attestation, не независимая серверная проверка. После готовности выполняется в одной сессии с D/F, без сообщения ключа агенту.

F. Живые ручные проверки: owner numeric identity/chat binding без извлечения секретов; Telegram exact once/deny/nonowner/stale/restart, доставка проверенного результата; локальный file:// preview; restore attestation. Полный сценарий и безопасные fixtures подготовить до просьбы владельцу нажимать кнопки. Нет подключения рабочего бота по разрешению A.

G. GitHub scope: согласованный private `RussianLioN/contemporary-dance-guide`, `RussianLioN/agent-knowledge`, `RussianLioN/agent-backups`, publisher-only credentials, проверка privacy/readback. После утверждения проекта/spec task branch push/PR автоматические — повторные approvals каждого push не нужны. Merge требует exact repo/PR/head commit. Их ещё нет, поэтому сегодняшний ответ не может быть разрешением будущего merge. Изменение visibility/прав, удаление repo/проектных данных также остаются exact owner actions.

H. Допустимость backup storage: Releases assets остаются кандидатом до N-07. При непригодности сначала консилиум ищет бесплатный совместимый способ без лишнего сервиса; только необходимость изменить пользовательское ограничение требует решения владельца. Не запрашивать оплату или blanket upload.

I. Итоговая runtime acceptance: после реального E2E и fault tests владелец принимает результат; закрытие ORCH-01 только явно. Предварительное разрешение программы не означает успешную приёмку ещё не выполненных тестов.

## Трассировка участия к текущим требованиям

| Источник | Пункт пакета | Результат участия |
|---|---|---|
| tasks 1.1–1.5, ENV-01, TG-05 | A/C/D | bounded canary receipts; доказанная OS/auth/native readiness, не source presence |
| tasks 1.6, TG-01 | B | owner approval exact spec/design digest |
| tasks 2.1/3.6 | B/C/F | project/owner binding и согласованный shared tool revision |
| tasks 4.1–4.3, PRE-01–02 | F | file://, mobile без горизонтального overflow, keyboard/focus, demo labels |
| tasks 5.1–5.3, TG-09–10 | D/G | private repo readback, PR, exact merge receipt; автоматические task push/PR |
| tasks 6.1–6.3, TG-11–12, REC-01–02 | C/F/I | единственный route owner, старый handler не потребляет новую кнопку; rollback/restart, heartbeat/quiet build/unknown |
| tasks 7.1–7.4, BACK-01–03 | E/H | exact encrypted object/restore attestation, проверенные зависимости и ключи; 30d только с newer verified same-scope copy, last/dependencies retained |
| tasks 7.5, ENV-02 | C/G | ownership-only technical cleanup; проектные данные только по exact approval |
| tasks 7.6, UPD-01–02 | C | exact updater diff и backup/drain/defer/rollback evidence |
| tasks 8.1–8.3 | F/I | реальные E2E/fault receipts и owner acceptance |

Для D до авторизации обязателен один refresh-owner, известные allowed readers/storage, проверки concurrent refresh/revoke/re-auth и subscription limits. Для E до restore нужны format/tool revisions, reachable dependencies и сохранение decrypt identities при ротации. Старые снимки журнала данного прототипа НЕ поддерживаются как anti-rollback recovery. Трассировка сверена ведущим с прочитанными tasks.md и specs/change-publication/spec.md, specs/offsite-backup/spec.md; третья волна не получила эти тексты повторно и не выдала независимый completeness proof.

## Технические решения без владельца

Технические алгоритмы, имена внутренних функций, defaults численных бюджетов, выбор тестов, source lookup, локальная разрешённая реализация, исправления по review, подготовка diff/procedures и scoped memory refresh. Решения через консилиум полного состава E01–E19, максимум 3 одновременных контекста, до 3 волн при споре. Изменять Hermes settings для такого исполнения не требуется.

## Как избежать повторных промежуточных остановок

A выполнен; не запрашивать его повторно. B–I — оставшийся реестр с зависимостями. Локальные Codex и GitHub авторизации подтверждены; server Hermes openai-codex logged in, recovery wiring найден. Server root gh exit4 требует login именно в этом контексте, но авторизация root не предлагается: сначала isolated publisher. Следующая объединённая локальная реализация готовится по `integration-readiness-scope.md`, а рабочие C/D–F — одним подготовленным пакетом. Exact merge, restore attestation и итоговая приёмка требуют уже существующих объектов/результатов и не выдаются заранее.
