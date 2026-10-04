# Проверка документов MVP1

Проведено docs-only ревью через отдельный ephemeral read-only процесс Codex CLI, exit 0. Ревьюер получил proposal/design/tasks/specs через stdin без инструментов и без доступа к credentials. Это отдельный контекст, не независимая модель; interview-decisions/baseline не передавались, поэтому reviewer не подтверждал историческое согласование владельца.

Выявлено и исправлено:
- BACK-03: новая копия B не разрешает удалить последнюю восстановимую A; replacement coverage и dependencies проверяются по owner/project scope.
- UPD-02: ждать завершения off-host backup и exact readback; pending/unknown блокируют update. Для неизменившегося набора проверить существующее покрытие. Ручная restore attestation не нужна на каждое update.
- tasks: 1.1–1.5 перед approval 1.6; side-effect canary требует отдельного ограниченного разрешения.
- BACK-01: негативный сценарий с credential внутри checkpoint; фильтрация имён auth-файлов недостаточна. Эвристическая редакция не гарантирует обнаружение любого секрета.

После правок выполнены:
- `./run-openspec validate --all --strict --json`: 1 passed, 0 failed.
- `./run-openspec status --change telegram-development-workflow --json`: isPlanningComplete true.
- `./run-openspec instructions apply --change telegram-development-workflow --json`: total 33, complete 0, remaining 33.
- Программно подсчитаны 12 capabilities, 25 уникальных requirement IDs и 58 сценариев.

Не выполнены: runtime tests, deployment, создание GitHub repos, live Telegram approvals, server memory lifecycle canary, backup upload/restore. Это не завершённая реализация и не закрытые N-01–08. ORCH-01 / CRITICAL открыт. Статус exact revision — review-status.json, owner_approved false. Этот отчёт не входит в spec digest и не выдаёт полномочий.
