# Integration: единый пакет незакрытых live gates

Статус: DEPLOY_PACKET_BLOCKED, NOT_AUTHORIZED_FOR_LIVE.
Local scope подтверждён и не запрашивается повторно. Связанный artifact:
`.hermes/tooling/mvp1-integration-prototype/README.md`, 44 tests OK.
Это не ready-to-apply diff, не blanket разрешение и не final spec approval.

2026-09-14: `live-source-evidence.md`, `codex-boundary-decision.md`,
`execution-authority-contract.md` и три волны `council/live-boundary/` сохранены.
Exact current updater fixture получена и проверена4source/guard tests, но shared
admission/production patch не реализованы. Native shell/exec-server smoke прошли;
отдельный native app-server macOS test FAIL на nested sandbox helper. C2 выбран
только кандидатом следующего Linux canary. Additional runtime scope собран в
`local-linux-canary-scope.md` (PROPOSED, NOT_AUTHORIZED); existing Colima/default VM
не запускалась. Read-only источник GitHub разрешён, повторного разрешения не требует.
Direct client/session hashes local/server совпали; model_tools отличается также по
AST. Старый gateway image/start заменён свежим receipt, не нашей server mutation.

## Технические blockers перед точным deployment diff

| Gate | Уже проверено локально | Что отсутствует |
|---|---|---|
| N-01 / credentials | Bridge→immutable synthetic effect, OS canary A исторически пройден | Обязательная OS authority для ВСЕХ реальных code/API/MCP/merge путей. Generic gate по-прежнему bypasses selected transport; transport expectedFailure не скрыт |
| Native server compatibility | Pinned локальный Kanban и cooperative intake, stale run fencing | Source local/server ранее различался; реальный серверный native lifecycle+cancel+external authority не доказан одной транзакцией |
| Codex | Native task + настоящие toy subprocess death/restart | Настоящий Codex project process в credential-isolated boundary; CLI на сервере не найден в предыдущем обследовании; Hermes provider login ≠ CLI setup |
| ORCH-01 / CRITICAL | Независимый toy controller, retry budget, waiting approval, reopen | Рабочий controller, crash/provider outage/descendants, Telegram alerts, detection ≤5 min, coordination с одним updater |
| Updater | Просмотренные исторические pure helpers; отдельная local drain/backup fixture | Точный patch нынешнего server updater с общей admission boundary. Исторический source нельзя подменить server source; existing recovery wiring не crash acceptance |
| Publisher/backups | MOCK PR/upload receipts, реальные age/filesystem roundtrips, pure retention policy | Изолированный publisher context, private remote objects, Git reachability/readback, offserver private key и действительное восстановление |
| Memory | Synthetic scope-before-read, checkpoint CAS/failure | Курируемый Git source и project scope в рабочем entrypoint; credentials/raw histories не source |

## Единая последовательность будущего live пакета

1. Read-only определить поддержанный real Codex execution boundary без core patches,
   publisher identity и server source compatibility. Если штатный интерфейс не даёт
   нужной границы, зафиксировать unsupported, не устанавливать небезопасную замену.
2. Только после технической готовности составить exact файлы/хеши/paths/limits,
   optional short-lived canaries и единственный updater diff; не выпускать
   placeholder compose, который выглядит применимым. Нынешний local scope разрешает
   подготовку этих текстов, но не запуск реальных Codex задач/новых server effects.
3. Одной owner batch согласовать необходимые изменения runtime/инфраструктуры,
   минимальную publisher authorization, custody тестового/private backup key и
   одну сессию live Telegram→Codex→tests→PR→Telegram, preview и restore.
   Не требовать повторного входа в local Codex/GitHub без ошибки текущей проверки.
4. Readback exact применённых targets, immutable operation revision и receipts;
   negative cases owner/chat/request/revision/late/duplicate/restart/unknown.
5. Только после реальных commit/results запросить exact merge и итоговую приёмку;
   будущий неизвестный commit нельзя заранее считать подтверждённым.

## Rollback-пакет: обязательные условия, не выдуманные команды

- До изменений: private verified backup штатным существующим механизмом; нельзя
  печатать/индексировать archive или auth.json. Сохранить hashes текущих НЕсекретных
  изменяемых файлов и exact container/image/runtime metadata.
- Сначала закрыть admission, дождаться bounded drain. Waiting approval не убивать
  как stalled, unknown external effects сверить с провайдером, не повторять слепо.
- Rollback менять только перечисленные будущим exact diff targets. Существующее
  current OAuth state не восстанавливать из старого archive: проверенная pure policy
  исключает auth.json; реальные release/recover механизмы остаются единственными.
- Canary cleanup только по сохранённому ID созданного ресурса; никакого global prune,
  удаления project code/memory/spec/results или чужих контейнеров.
- Уже созданные remote effects не «отменять» локальным rollback. Сначала exact remote
  readback, затем отдельная owner-authorized компенсация при необходимости.
- Для незавершённого local backup preparing/unknown fail-closed; автоматическое
  восстановление пока не доказано. Нельзя обещать production maintenance-ready.
- После rollback: gateway/auth/config/version и отсутствие только созданных canaries
  проверить реальными read-only командами. Не перезапускать ничего в рамках нынешнего
  local разрешения и не применять исторические shell snippets к новому server source.

Все mock, local и historical результаты отделены от live acceptance.
Рабочий deployment diff пока отсутствует по техническим причинам, а не потому,
что нужно заново согласовать очередной локальный компонент.
