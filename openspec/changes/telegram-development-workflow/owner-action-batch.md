# Пакет действий владельца

## Однократная Linux test-среда: разрешена, выполнена, удалена

Публичное чтение Codex/GitHub и оставшаяся local работа подтверждены; повторно
не запрашиваются. Integration44OK/current updater fixture+4source tests сохранены;
три полные волны live-boundary E01–E19 приняли C2 только как canary candidate.
Отдельный native app-server macOS readiness test остаётся FAIL (nested sandbox).
Linux client/profile и C2 containment probe прошли; missing/exited selected helper
не блокирует thread/start: readiness gate остаётся FAIL, fallback execution не доказано.
Рабочий deploy/rollback diff не готов. Evidence: `linux-canary-evidence.md`.

Последующее local обновление: `native-environment-evidence.md`. Штатные info/status реально проверены без VM/авторизации; local-only FS/command/shell endpoints отвергаются с exact -32603 при include_local=false. Отдельный clean-config probe воспроизводит unsafe MCP merge и late-untrust. Эти работы не требуют нового owner действия и продолжаются автономно; runtime/model scope ещё не запрашивается вместо доступных local проверок.

Владелец подтвердил `+` весь `local-linux-canary-scope.md` — одна новая временная
Colima VM hermes-boundary-canary,1CPU/2GiB,data8GiB/root10GiB,без host mounts,
SSH-agent/context/default VM изменений; native Codex0.153.4 Linux bundle с exact
release digest,synthetic no-auth/no-model probes,экспорт результатов и owned cleanup.
VM и её данные удалены с независимым readback за1752s; default VM/context сохранены.
Однократное разрешение исполнено, не разрешает повторный VM launch, server/бот,
ordinary model tasks,GitHub publication или финальную spec revision.

Все будущие server/Telegram/model/PR/backup-key/restore/merge gates перечислены в
`integration-live-gates.md`; нельзя выдавать неизвестные будущие hashes за готовый
общий deployment пакет. ORCH-01 / CRITICAL по-прежнему открыт. Ниже — история.

Статус: **LOCAL_EXECUTOR_AUTHORIZED / NEXT_BATCH_IN_PREPARATION**. Владелец подтвердил `protected-executor-scope.md` и потребовал собрать все остальные необходимые согласования в следующую единую эскалацию. Локальный протокол разрабатывается автономно, без core/profile/bot/server изменений и production credentials. Transport/PTB и этот local scope повторно не запрашиваются. Консилиум — полный состав E01–E19; технические вопросы решаются без владельца. Ниже сохранена история предыдущих этапов, не текущий запрос повторных разрешений.

Актуальное основание: 40 tests, `OK (expected failures=1)`; generic selected-transport requirement не проходит. Real hook missing/error/unload не даёт обязательного veto. Transport-only не закрывает полный N-01. Независимые Kanban/crypto/runner probes и read-only server/source checks выполнены; детали в `../../../.hermes/research/telegram-hermes-codex/readiness-probes-2026-09-11.md`. OS isolation/live auth/deployment gates не подменяются local probes. ORCH-01 / CRITICAL открыт.

## Блокирующее решение N-01

Текущее обновление: A выполнен и verified; прежние auth проверки не требуют повторного local login. Владелец подтвердил весь `integration-readiness-scope.md`: AUTHORIZED_LOCAL_INTEGRATION. Связанный локальный стенд реализован и проверен: 33 tests OK, две полные волны E01–E19, без server/runtime изменений. Точный deploy diff ещё технически заблокирован; `integration-live-gates.md` содержит оставшиеся live gaps и rollback constraints. Не запрашивать повторно local scope и не авторизовывать server root по одному лишь прежнему gh exit4. ORCH-01 / CRITICAL открыт.

Пакет `next-owner-gates.md` хранит выполненный точный OS canary A и реестр B–I с зависимостями и трассировкой к tasks/specs. Local regression 23 tests PASS; server receipt отдельно в server-evidence.md. Повторные transport/PTB/local-marker permissions не требуются. Старые разделы ниже — история.

Штатный exec approval Telegram в latest stable и исследованном main не передаёт request_id. Extracted actual callback воспроизводит B button → A. Штатный /approve также не передаёт ID. Другая native интеграция ещё не доказана; обновление на latest само по себе не решение.

Владелец отклонил любые изменения Hermes Agent. Прежнее предложение core patch отменено: не создавать fork, monkey patch или подмену adapter. Выполнено трёхфазное исследование OSS альтернатив: `.hermes/research/telegram-hermes-codex/no-core-alternatives/04-phase3-finalists.md`, шесть архитектурных финалистов, ни один не принят как runtime-ready.

Владелец явно ОТКЛОНИЛ ручное выполнение infrastructure/merge. Это больше не вопрос для эскалации и не fallback. Обязательно автоматическое выполнение после точного owner confirmation в Telegram. UX/CX консилиум поддержал карточку конкретной неизменной операции, автоматическое исполнение и проверяемый результат в Telegram; отчёт `.hermes/research/telegram-hermes-codex/no-core-alternatives/08-ux-cx-telegram-automatic.md`. Framework ещё не выбран, runtime не проверен. Следующий gate: готовый OSS Telegram confirmation-to-execution path без изменений Hermes и без молчаливого создания custom approval service. Whitelist не исправляет FIFO binding. Авторизации/развёртывание запрашивать только после доказанного ограниченного технического scope.

## N-01: результат исполнения плана 2026-09-11_155538

Проверка StackStorm pack не дала готовой owner → inquiry → exact execution интеграции. Найден более прямой native extension path: в stable Hermes `2237be355906fbe6065ce1815711eee52b2d646e` есть `register_approval_transport` и `register_telegram_handler`; наличие API подтверждено read-only в серверном контейнере. Изолированный host transport module прошёл 11 tests. Это не Telegram integration: generic action gate имеет transport=False; sender, exact commit, bypass, restart и полный effect→result ещё не доказаны. Built-in FIFO defect не объявляется исправленным.

Владелец разрешил НОВЫЙ локальный transport plugin prototype на штатных API. Разрешение G4 на код получено и повторно не запрашивается. Реализован план `.hermes/plans/2026-09-11_162951-native-telegram-transport-prototype.md` в доступной части: plugin + 20 tests PASS, включая actual host contract/sentinel и отдельный subprocess. Статус LOCAL_PROTOTYPE_PARTIAL: PTB отсутствует в Hermes venv и системном Python, actual routing/plugin loader ещё не проверены. Код/результаты: `.hermes/tooling/telegram-approval-prototype/`.

Dependency scope разрешён владельцем и выполнен: project-local `.hermes/tooling/telegram-approval-prototype/.venv`, Python 3.11.15, PTB 22.8, полный hash lock и license metadata/header review. Штатный backup wrapper прошёл до установки. Actual SDK offline routing suite: пять новых tests PASS; общий suite 25 PASS, socket/DNS guard включён. Статус LOCAL_SDK_VERIFIED / NOT_INSTALLED. Отсутствие SDK больше не blocker, разрешение повторно не запрашивать. Hermes runtime venv/профили/сервер не менялись. Следующий непроверенный технический этап — изолированный full PluginManager loader/lifecycle и coverage/permission review; live bot scope отдельно после точного canary diff. Это не разрешение live Telegram и не закрытие N-01 в целом.

Доказательства: `.hermes/research/telegram-hermes-codex/n01-ready-telegram/11-readiness.md`. Точный scope: `09-owner-batch.md` в том же каталоге. Полная интеграция BLOCKED; runtime/сервер не менялись. Разрешение на обычное read-only исследование повторно не требуется.

## Последующий локальный loader/lifecycle этап

Проверен targeted настоящий PluginManager с временным home/config, без discovery чужих плагинов и без установки в рабочий профиль. Исправлен реальный дефект prototype: после unload старый SDK handler разрешал pending запрос. Теперь on_unload закрывает Bridge, удаляет handler и отменяет ожидания; loop/thread/reload tests пройдены. Полный regression 30 PASS. Доказательства: `.hermes/tooling/telegram-approval-prototype/lifecycle-evidence.md`.

Новые границы: host сохраняет inert factory при targeted unload (unload-all очищает); отзыв уже выданного verdict и полный drain при shutdown не доказаны. Следующий технический шаг — coverage/privileged boundary для exact protected operations, не преждевременное подключение live bot. Новое разрешение на уже согласованные локальные tests не требуется. ORCH-01 / CRITICAL открыт.

## Остальное — пока не запрашивать преждевременно

- Exact spec revision approval после закрытия технических решений.
- Container/canary scope с exact resources/rollback после N-04/N-08.
- ChatGPT/GitHub authorization после безопасного credential design; не до него.
- Local private decrypt key и restore только по готовой процедуре, без overwrite/exec.
- Live Telegram owner/stale/restart и local preview по готовым безопасным тестам.

Не объединять в один преждевременный blanket approval неизвестные diff/credentials/production actions. ORCH-01 / CRITICAL открыт.
