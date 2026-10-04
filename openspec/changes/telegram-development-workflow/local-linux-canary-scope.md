# Local Linux canary — единый дополнительный scope

Статус EXECUTED_ONCE / VM_DELETED / PARTIAL_PASS / CLIENT_ROUTING_GATE_OPEN. Владелец подтвердил весь пакет ответом «+» после его предъявления. VM создана и удалена за 1752s; evidence: `linux-canary-evidence.md`. Повторное создание не разрешено автоматически. Это только исследовательская Linux-среда, НЕ production deployment packet. ORCH-01 / CRITICAL открыт.

## Почему требуется отдельное разрешение

На Mac установлена Colima0.10.3, но единственная existing default VM остановлена. Native app-server probe под внешним macOS sandbox остановился на nested filesystem helper (sandbox_apply Operation not permitted); Linux containment/cgroup невозможно проверить одним macOS source test. Чтение GitHub уже разрешено; новый запрос не о повторном исследовании, а о создании временной инфраструктуры/распаковке Linux test binaries.

Выбран минимальный scope без касания ainetic.tech/default VM: отдельная `hermes-boundary-canary`. ARM capability Mac подтверждён, shell работает под translation; VM будет aarch64. Это Linux canary, НЕ финальная amd64/server acceptance.

## Что разрешает подтверждение этого файла целиком

1. Создать/запустить одну новую временную Colima VM `hermes-boundary-canary` штатным уже установленным Colima0.10.3. До старта name must-not-exist; существующую VM с таким именем не использовать и не удалять.
2. Limits:1vCPU,2GiB RAM,data disk8GiB,root disk10GiB (sparse virtual limits, не обещание фактического расхода). Никаких user-home/project mounts, SSH-agent forwarding, SSH config modification, Kubernetes, Rosetta/binfmt или смены active Docker context. Не запускать existing default VM.
3. При cold bootstrap разрешить штатную загрузку base Linux image/runtime Colima из его официальных источников; зафиксировать фактические URLs/version/checksums до тестирования. Это НЕ transitive supply-chain acceptance. Никаких host Homebrew/npm/pip upgrades. В VM использовать штатные Docker/Python3/util-linux; если их нет — не добавлять неизвестные зависимости и зафиксировать ограничение.
4. Скачать и проверить один официальный test bundle Codex0.153.4 для aarch64 Linux, распаковать ТОЛЬКО внутри новой VM после проверки archive paths/symlinks. Не устанавливать в macOS PATH или Hermes. URL: https://github.com/openai/codex/releases/download/rust-v0.153.4/codex-package-aarch64-unknown-linux-musl.tar.gz . Release API сообщает size117238842 и SHA256 `fc395cb043a1093ab0db34f44aba3199bfaa9ce640cd9be7fd588f44b0da64a4`; это metadata, байты ещё не скачаны/не проверены. Несовпадение hash — остановка до распаковки/исполнения.
5. Выполнить только synthetic no-auth/no-model Linux probes из `codex-canary-contract.md`: native handshake/FS/process/profile, отрицательные file/env/FD/fallback checks и descendants/containment. Никакого `turn/start` реальной модели, Telegram/GitHub writes, новых OAuth flows или credentials mounts/copies. Network bootstrap разрешена ДО project execution; при probes worker network изолируется и проверяется, не допускаются outbound project запросы.
6. Сохранить source/test receipts в workspace, затем остановить/удалить только созданную VM и её технический runtime disk. До удаления экспортировать ВСЕ результаты; project code/memory/spec/results не удалять. Не удалять общие Colima caches/default VM. Проверить отсутствие exact profile и неизменность default/status/context.

## Проверенная по installed help команда старта (разрешена этим scope)

```sh
colima start hermes-boundary-canary --arch aarch64 --vm-type vz --cpus 1 --memory 2 --disk 8 --root-disk 10 --runtime docker --mount none --activate=false --ssh-agent=false --ssh-config=false --kubernetes=false --network-address=false --network-host-addresses=false --port-forwarder none --template=false --vz-rosetta=false --binfmt=false
```

Перед стартом: `colima list`, `docker context show`, resource/free-disk check, current version; `./backup-hermes-oauth` перед configuration/dependency work согласно AGENTS, не читать/индексировать private archive. Не соглашаться автоматически на непредусмотренный sudo/system-extension prompt. Startup timeout600s; если tool переносит в background — poll/wait, не запускать дубликат. После успеха actual readiness: `colima --profile hermes-boundary-canary status` и `colima --profile hermes-boundary-canary ssh -- uname -sm`.

Каждый probe timeout≤60s, общий investigative window≤30min после readiness; limit output≤1MiB на процесс. При timeout остановить только owned process/VM; сохранить диагностический FAIL, не расширять limits молча. Root в новой VM допустим только trusted test setup/controller; worker — отдельный UID/namespace без host mounts/socket/credentials. Синтетические писатели имеют собственный deadline, не бесконечные daemons.

## Cleanup / rollback

После сохранения receipts и проверки ownership вновь сверить `colima list`; использовать только явно созданное имя:

```sh
colima --profile hermes-boundary-canary stop
colima --profile hermes-boundary-canary delete --data --force
colima list
docker context show
```

Команды delete подтверждены installed help; применять только если creation receipt доказывает владение новым профилем. При неоднозначном/частичном создании — status/inspect и остановка, не global cleanup. Cold bootstrap может сохранить shared download cache; его не чистить автоматически.

## Остальные согласования — здесь НЕ выдаются

Рабочая установка controller/plugin/updater, серверный canary на текущем amd64 image, ordinary Codex task, publisher auth context, private GitHub creation/PR, backup key custody/live restore, Telegram/manual preview и exact merge остаются в `integration-live-gates.md`. Имеющегося exact deployment diff нет: подменять его этим VM scope запрещено. После Linux evidence готовится один действительно применимый live пакет; повторный login без ошибки auth status не запрашивается.
