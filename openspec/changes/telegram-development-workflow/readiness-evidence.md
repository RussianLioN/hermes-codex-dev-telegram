# Readiness evidence — автономное продолжение

## N-01: latest/upstream и callback probe

GitHub releases/latest вернул tag `v2026.9.7`, published_at `2026-09-07T22:17:01Z`:
https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.7

Main SHA получен отдельно из GitHub API: `cbd03e6e4ca143c1d5c2db881320afb85783c30b`. Первое сравнение читало moving main; воспроизводимый probe затем загрузил exact SHA.

Команда:

    python3 .hermes/research/telegram-hermes-codex/probe_n01_callback.py

Фактический exit 0. Загрузки по HTTPS raw.githubusercontent.com, никаких live gateway imports или auth files. Из исходника AST извлечены только resolver и два callback methods; annotations удалены, тело функций сохранено. Auth implementation и Telegram transport stubbed. Это исследовательский probe установленного класса проблемы, не реализация платформы и не TDD fix.

Source hashes SHA256:
- tools/approval.py: e48f1909968b253907fca01e9dad0593bee7a2bf7cf5278470c6d15a5150359f
- plugins/platforms/telegram/adapter.py: 715464f07c46fe3b7aea834f16b2c46988aabd6f6cfc763de99a342181eaa53d

Фактические проверки:
1. B button при A/B pending разрешает A — риск воспроизведён.
2. Сохранённый mapping A при только B pending разрешает B — риск воспроизведён при synthetic prerequisite; production timeout cleanup не исследован этим тестом.
3. Auth callback возвращает False: очередь/mapping остаются — passed, реальная sender authorization не проверена.
4. Повтор уже использованной кнопки при следующем B не разрешает B — passed.
5. Неизвестный ID не разрешает B — passed.

Stable и исследованный main сохраняют session-only exec callback. Stable slash_commands.py:1128–1145 не передаёт request_id; /approve parses all/session/always, не ID. Источник:
https://raw.githubusercontent.com/NousResearch/hermes-agent/v2026.9.7/gateway/slash_commands.py

Нельзя вывести «update исправляет проблему». Gate остаётся BLOCKED_FOR_PROTECTED_ACTIONS; live Telegram E2E, restart collision и полный caller policy не выполнены.

## N-08: предварительный discovery, не окончательный выбор

Read-only Git в `/Users/s060874gmail.com/coding/projects/hermes-remote-migration`:
- status --short: пустой вывод, clean на момент вызова;
- branch: feat/codex-runner;
- HEAD: 8cbce95, «fix: блокировать новые задания во время обновления Runner».

Найден `deploy/codex-runner/README.md`, описывающий controller/executor/publisher, собственный updater и GitHub App. Это историческая архитектура, не автоматически согласованный current MVP1: текущие native queue, project-lifetime containers, один updater и publisher auth требуют сравнения. Репозиторий не переключался и не изменялся; deployment не доказан README.

## Документарная проверка

`./run-openspec validate --all --strict --json`: valid true, issues [], 1 passed, 0 failed. Нормативные specs/revision_files не изменены этими research records. owner_approved не изменён. ORCH-01 / CRITICAL не реализован.
