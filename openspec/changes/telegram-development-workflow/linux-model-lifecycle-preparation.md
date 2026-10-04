# Подготовка guest lifecycle и сохранения результатов

Статус: LOCAL_PREPARATION_ONLY / NOT_RUNTIME_ADMISSION. ORCH-01 / CRITICAL открыт.

## Фактическая локальная проверка

`native-codex/lifecycle-preparation/receipts-v2.json`: 14 unittest — 4 для command-plan и 10 для настоящего файлового экспорта на принадлежащих тесту временных файлах. Receipt содержит фактические transcripts, exit codes, SHA256 и полный текст только этих публичных локальных исходников. Исторический v1 сохранён. Это дополнение к environment receipts-v5, не Linux runtime receipt.

`guest_namespace_plan.py` только строит argv: не создаёт VM/пользователя/cgroup/firewall, не запускает процесс и никогда не выдаёт model admission. Кандидат требует снижения внешнего UID до user namespace, отдельной проверки UID снаружи namespace, exec-server как PID 1, очищенного environment, loopback и отказа от registration/Agent Identity. `bwrap --uid` сам по себе НЕ свидетельствует о смене внешнего UID для owner-based network rules.

Source-reference bubblewrap v0.12.0: commit `2a76602a8c71f36c1527cf9fc3417d9149822e0c`, `bwrap.xml` и `bubblewrap.c`. Проверены требования `--as-pid-1`/`--unshare-pid`, несовместимость с lock-file, поведение sync-fd и назначение uid mapping. Это НЕ утверждение о версии bundled bwrap и не разрешение её устанавливать. Реальный guest binary/options ещё предстоит проверить. Stock setpriv flags взяты также из ранее выполненного `linux_probe.py`; новая комбинация namespace/UID/listener пока не испытана.

## Экспорт

`safe_canary_export.py` действительно копирует и перечитывает bounded regular files, считает SHA256, создаёт назначения 700/600 и ничего не удаляет. До чтения содержимого отклоняются symlinks, hardlinks, FIFO/необычные типы, несоответствие UID/device, credential/environment/archive filenames. Existing destination не перезаписывается. Зафиксирован RED → GREEN для обхода общего лимита пустыми подкаталогами: теперь бюджет entries глобальный, обход не использует неограниченный listdir.

Это НЕ credential scanner, authorization boundary или snapshot активного дерева. Quiescence — обязательный контракт доверенного caller, НЕ независимое наблюдение. Нужны настоящий external cgroup-empty readback и фиксированный scope source/destination. Ошибка оставляет источник и частичное назначение; она запрещает удаление VM под видом успешного экспорта.

## Deadline и данные

Только volatile tmpfs для результатов конфликтует с обязательной остановкой VM при неуспешном экспорте. Кандидат изменён через RED → GREEN: оба writable дерева project и tmp должны иметь ограниченное persistent backing, а корень view — read-only. Реальные size/inode limits, fsync и сохранность после VM stop ещё не реализованы/не проверены. Нельзя объявлять сам bind disk-backed quota.

Будущий controller должен уметь остановить вычисление и сохранить диски при непроверенном экспорте, не теряя project results и не продолжая исследование бессрочно. Неизвестная ownership не разрешает остановку/удаление чужого профиля. Native technical symlinks/cache требуют отдельной классификации; нынешний строгий exporter не разрешает их молча исключить вместе с возможными изменёнными результатами.

## Оставшийся объём

Физический lifecycle harness, root-owned control pipe и независимый deadline, cgroup placement/kill/empty readback, IPv4/IPv6 positive/negative controls, listener anti-replacement, persistent quota/sync, safe host transfer и reconciliation при failure ещё не закрыты. Host bootstrap/config admission отдельно остаётся закрывающим gate (`native-bootstrap-evidence.md`). Новый scope B не предъявляется как готовый и не запускается по старому разрешению.
