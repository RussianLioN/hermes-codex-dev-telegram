# Verification: adopt-openspec-workflow

## Summary

Статус: DOCS_WORKFLOW_APPLIED / OWNER_GATES_PENDING / NOT_ARCHIVE_READY. Разрешение docs apply — отдельный запрос владельца. Product runtime не принимался. Current progress всегда проверять `./run-openspec instructions apply --change adopt-openspec-workflow --json`.

| Измерение | Результат |
|---|---|
| Completeness | Evidence map охватывает 12 capabilities, 25 requirements, все 58 именованных scenarios и все 33 исходных product task IDs; R1–R3 и protected AGENTS write остаются открытыми |
| Correctness | Исторические local/mock/native/canary результаты отделены от NOT_RUN полной production acceptance; receipts сверены без повторного исполнения runtime tests |
| Coherence | WORKFLOW/config/TODO связаны; product clarification packet подготовлен, но исходные product artifacts не переписаны без подтверждения |

## Actual validation

- `context --json`, `--version`: root этого workspace, OpenSpec 1.13.0, exit 0.
- `status --change <each-change> --json`: exit 0, planning complete для обоих; tooling specs skipped.
- `instructions apply --change <each-change> --json`: exit 0; context содержит `openspec/WORKFLOW.md` после config edit. Это реальное использование context injection, не доказательство forced enforcement.
- `instructions tasks --change adopt-openspec-workflow --json`: exit 0; rules содержат requirement/scenario evidence linkage и local/synthetic/native/canary distinction.
- `validate --all --strict --json`: exit 0, два changes valid. INFO о skip_specs не ошибка. Validator не выполняет tests продукта.
- Coverage script: `MAPPING 25 requirements 58 scenarios 33 tasks`; каждый Scenario title присутствует в audit, каждый requirement ID и исходный task ID найден. Это проверка полноты mapping, не тест поведения сценариев.
- Allowlisted product revision digest совпал с recorded `29163c1de50e501a82f85cc72ada9f011520a3a17828ee0027adf006b22c729f`; owner_approved=false. Product 0/33 остаётся без изменений.
- Source_sha256 environment v5 и lifecycle v2 сверены с текущими файлами, SOURCE_DRIFT=[]; receipts file hashes в audit. Никакие transitive dependencies или живой сервер этим не удостоверены.
- `/bin/zsh -n backup-hermes-oauth && ./backup-hermes-oauth`: exit 0, snapshot wrapper выполнил integrity/700/600 checks до configuration edit; payload не читался/не индексировался.
- Первоначальная docs-label assertion завершилась 1: текст уже описывал RED/GREEN, но не содержал буквальную метку TDD. Диагностика `Missing labels: [TDD]`; заголовок уточнён. Это дефект обнаружимости документа, не runtime TDD regression.
- Повторная проверка после исправления: `DOC CONTRACT CHECKS PASS 58 33`, exit 0. Затем `validate --all --strict --json` — exit 0, 2 passed / 0 failed.
- Scoped `mine tasks`, `mine openspec` и search завершились exit 0; поиск вернул текущие TODO/verification с protected-write blocker и pending R1–R3. Последующие изменения progress повторно индексируются перед handoff.

Воспроизводимая компактная повторная проверка docs-контракта из root:

```sh
python3 -c 'from pathlib import Path; import re; p=Path("openspec/changes/telegram-development-workflow"); a=Path("openspec/changes/adopt-openspec-workflow/audit.md").read_text(); s=[x for f in (p/"specs").glob("*/spec.md") for x in re.findall(r"^#### Scenario: (.+)$",f.read_text(),re.M)]; t=re.findall(r"^- \[ \] (\d+\.\d+) ",(p/"tasks.md").read_text(),re.M); assert all(x in a for x in s); assert all("| "+x+" |" in a for x in t); w=Path("openspec/WORKFLOW.md").read_text(); assert all(x in w for x in ("Explore","Propose","Update","Apply","Verify","Sync/archive","TDD","NOT_RUN","E01–E19","ORCH-01")); print("DOC CONTRACT CHECKS PASS",len(s),len(t))'
./run-openspec validate --all --strict --json
```

## Tabletop: семантическая проверка маршрутов

Это прочитанные и разобранные сценарии workflow, НЕ запуски новых engineering tasks, моделей или внешних операций.

| Случай | Маршрут / команды | Проверенный stop condition |
|---|---|---|
| Новая feature с новым behavior | context/list/list --specs → propose/new change → artifact instructions → delta specs → tasks | После propose следующий запрос apply; без него код не пишется |
| Bugfix уже заданного поведения | Найти requirement и подходящий change через list/status; instructions apply; regression RED/GREEN | Не придумывать новое requirement; если реальный scope меняется — update/approval |
| Docs-only typo/config clarification | Малый подходящий change, skip_specs только при неизменном контракте; validate | Нет фиктивных specs и нет разрешения менять runtime под docs scope |
| Architecture drift во время apply | Приостановить затронутый slice, update skill, concrete existingOutputPaths, per-artifact packet | Не урезать требования/подменять runner без подтверждения; независимые задачи продолжаются |
| Plan-only запрос | Только read-only inspection и разрешённый plan file | Ни new change, ни конфиг, ни model calls, ни memory mine без разрешения текущего режима |
| Optional verify skill отсутствует | Проверить файлы; применить установленный verify source template + status/apply/validate | Не заявлять slash invocation или несуществующую openspec verify, не устанавливать silently |
| External effect без approval | Отдельный owner scope/immutable revision и exact target | ready/consilium не grants authority, canary не запускается |
| failed/expectedFailure тест | Сохранить negative evidence и незакрытый acceptance criterion | Никакой галочки за полный product task, нет удаления повреждённого теста ради green |

## Quality/security review

Выполнено ведущим агентом по пяти осям code-review-and-quality и trust-boundary checklist security-and-hardening; это self-review, не fresh-context или независимая модель.

- Correctness: закрытие parent outcomes local fixtures запрещено; coverage mapping полная по именам; полная production acceptance NOT_RUN.
- Readability: одна подробная WORKFLOW, короткий config pointer, текущий TODO отделён от истории. Исторические слова «актуальный» не переопределяют current index.
- Architecture: штатный spec-driven, no extra plugin/schema/daemon/tracker. Product design остаётся самостоятельным; proposed R1–R3 не внедрены.
- Security: единственная попытка protected AGENTS write получила timeout и не повторялась; обхода нет. Данные council/memory не authority. Source reads ограничены docs/synthetic evidence, secret payloads не читались. Authorized private backup выполнен штатным wrapper.
- Performance: нет runtime change; bounded council до трёх волн/трёх параллельных contexts, 180 секунд на попытку. Council в этом ходе не запускался: нет технической неопределённости, разрешаемой голосованием; оставшиеся действия — explicit owner gates.

Scope review основан на фактическом списке tool writes/commands этой сессии, а не полном filesystem attestation: изменены только WORKFLOW, config, TODO и docs текущего change; AGENTS write заблокирован. Generated skills, product code/specs, core/profiles/server не редактировались; новые dependencies/VM/model canary/publication/commit/push/archive не запускались. Утверждение «во всём filesystem ничего не менялось» не делается. Runtime discovery skills в новой model-session остаётся NOT_VERIFIED.

## CRITICAL — до завершения именно этого change

1. Task 2.3: подтвердить R1–R3 из reconciliation.md. Это минимальные уточнения, не новая архитектура.
2. Task 2.4: после подтверждения применить R1–R2 через update workflow и R3 как bookkeeping, пересчитать R1 digest, оставить product approval pending. Пока ничего не применено.
3. Task 3.4: разрешить новую попытку записи AGENTS C.17 и успешно подтвердить protected write. Предыдущая попытка истекла без согласия; AGENTS не изменён, OS-07 открыт.

Эти пункты нельзя закрыть большинством консилиума или успешным validator. Archive запрещён до завершения и отдельного решения.

## WARNING — продукт, не регрессия docs migration

- Product tasks 0/33; CLIENT_ROUTING_GATE_OPEN / NOT_DEPLOYABLE.
- ORCH-01 / CRITICAL не реализован; independent production monitoring/restart не доказан.
- Existing-account metadata probe — FAILED TimeoutError, не отсутствие OAuth.
- test_stock_lifecycle.py — повреждён; реализация не входит в docs change.
- Model routing, live Telegram/PR/backups/updater/restore acceptance и skills runtime discovery не проверены этим ходом.

## Отчёт для handoff

Созданы WORKFLOW, audit и reconciliation; config доставляет инструкцию через штатный CLI context, TODO отделяет текущий индекс от истории. Инструкция: `/Users/s060874gmail.com/coding/projects/hermes-agent/openspec/WORKFLOW.md`. Реализованы все независимые разрешённые docs slices; остаются явные owner gates выше. Доказательства и продуктовые критерии не переписаны задним числом. Следующий пакет владельцу: подтвердить R1–R3 и отдельно разрешить новую protected запись блока C.17 в AGENTS.md. ORCH-01 / CRITICAL открыт. Полное завершение и archive не заявляются.

## Reconciliation execution baseline

2026-09-23, начало исполнения разрешённого плана [reconciliation → coverage → E1 discovery](../../../.hermes/plans/2026-09-23_170149-reconciliation-coverage-e1-discovery.md), ответ владельца «Приступай». Весь предшествующий текст — исторический receipt, не текущие counts/approval. G-DOC и G-DISCOVERY разрешены; отдельный G-AGENTS ещё не получен, новой protected-write попытки нет.

Preflight: V-STATE exit 0 (Git commands по отдельности 128; OpenSpec 1.13.0, correct root, no main specs), V-DIGEST exit 0; `status`/`instructions apply` обоих changes exit 0, 23/26 и 0/44. Strict validation: 3 passed / 0 failed. Первый driver извлечения V-CLI по неверному заголовку завершился IndexError после успешных V-STATE/V-DIGEST; исправлен вызовом настоящих CLI-команд, это не ошибка OpenSpec или runtime. V-BASE exit 0 до любых product edits; ниже его фактический JSON stdout. Не attestation всего filesystem.

<!-- reconciliation-baseline:v1 -->
{
  "fixed": {
    "run-hermes": "e41882100a3742e6d68c4331e44014f7a7e72be4e031f02c34ff987f89d77ba5",
    "backup-hermes-oauth": "2f8b3fa769d2a24e04e5c92beb9535c371ce93ee9b4b66c79dc230cd632b561a",
    "update-hermes-stable": "0a1e84acf25c5deedca0e9b4f054a6e578060884d95e0a587c147df2b681f39f",
    "configure-hermes-pilot-ssh": "571c4282c8655afd079b9813d19b55fd03eef20ce056ee99eae4e54e194fc1f7",
    "configure-codex-sandbox": "27c6053a26f7245206f5dc02f3cdb8899f8e2340285df8300b62d4e4e773be91",
    "run-openspec": "ebe9541604f0605221d1174fdb5ea03ca506932db57ca8d34813a6429db66d7d",
    "run-mempalace": "b573ea2cda207e61138127251b26839c1470688a3b6ffd771d02a8ee7142047d",
    "openspec/config.yaml": "1af1dc4a909a35f28c1327f225efece03bfb4b24b2df6b3073474a6dd80025e1",
    "openspec/WORKFLOW.md": "6b017b835c59fe8bd0406daa8631059aff20c82986e68caaf4e3107dbf082f1a",
    ".hermes/research/telegram-hermes-codex/native-codex/test_stock_lifecycle.py": "faa1b213a4744236e5804731781c63cdef8824e8ed7c846460d4809325f5aa1b",
    ".hermes/research/telegram-hermes-codex/native-codex/environment-run/receipts-v4.json": "8d407ef40388d5a4a0993327cdf2a65bfc2b47d229635aeb35c4ca7735ec5db1",
    ".hermes/research/telegram-hermes-codex/native-codex/environment-run/receipts-v5.json": "bf818443a167b7d89680f2867f5e7707db7a26160ca9fe005434a3fafb756898",
    ".hermes/research/telegram-hermes-codex/native-codex/lifecycle-preparation/receipts-v2.json": "e261a39196a32bdcc699402ef4d21af970c1013bcf93545a42dcb69886559211",
    "openspec/changes/telegram-development-workflow/baseline.md": "8e3d080a8d81783aa6609ad037e69c83f5bd5c36e342155556bedf25392396ea",
    "openspec/changes/telegram-development-workflow/proposal.md": "9c32308bbb38af0035cedaa4fc9c875f334f753aa722d09c9c79fc4176f49cfb",
    "openspec/changes/telegram-development-workflow/interview-decisions.md": "207c794de6f7b14c0810c7c40c131758231d13c9e919c667fa37c26f61fb4222",
    "openspec/changes/telegram-development-workflow/specs/change-publication/spec.md": "095301b8635b5b213f44de3f8f72b4e7d6a45963597827926ecba5aafac7a347",
    "openspec/changes/telegram-development-workflow/specs/code-execution/spec.md": "14db6a6b1194ea6058a3ba68eb2b0962ec59113aef41b169881189a4d8c0f7d3",
    "openspec/changes/telegram-development-workflow/specs/interactive-access/spec.md": "378af91d04d151b47716fc54f6a6306403c2c2afc8888735e47adf588eca7ec9",
    "openspec/changes/telegram-development-workflow/specs/local-preview/spec.md": "2a6675f5e8b359ec706a383f45535cfcff8ca02eb0080532d8dd5f5c8684d43c",
    "openspec/changes/telegram-development-workflow/specs/maintenance-coordination/spec.md": "c5e545d16d232c0b88725cce6ca63f36973de6a232e0d2275bb59296d7dd3565",
    "openspec/changes/telegram-development-workflow/specs/offsite-backup/spec.md": "41a333c80e47eecbf513c0dd8191f127b06a091397b70c9a6a89f9f0cfef62bd",
    "openspec/changes/telegram-development-workflow/specs/portable-memory/spec.md": "4005d77adc99c2d5f801ee297ae4f97b347e16ec5abd09efbcaa62c11689e398",
    "openspec/changes/telegram-development-workflow/specs/project-environments/spec.md": "eea805ab47d3ba31336a6b1250d5148c47c95416fdbd184c6ddc81925aedf8dc",
    "openspec/changes/telegram-development-workflow/specs/specialist-dispatch/spec.md": "4c8b728226257264118438a87eeabb5380c25620203c4141db190f8c22af88f7",
    "openspec/changes/telegram-development-workflow/specs/task-intake/spec.md": "113652336ba4a98718e2dc6563535883a9415d1d6dba04fb3b850fc257cb1c2d",
    "openspec/changes/telegram-development-workflow/specs/task-recovery/spec.md": "323665455bd13d82b309ff79ab90e557be5e403c9a7a6c55b981281e8c0ca256",
    "openspec/changes/telegram-development-workflow/specs/telegram-delivery/spec.md": "3d47924c2a977e81f6d56229dbe9703df3408280f6483a17c6f7a16bb2fba523",
    "openspec/changes/telegram-development-workflow/specs/verification/spec.md": "719b588fe498add1294e0bdad50093a69756e273d853d414595fba7e3ee048dd",
    "openspec/changes/seed-project-documentation/.openspec.yaml": "e67db83f0b45685ae47a30e3dc96b771c8c23d5d8f0776fe792115e9cdb9ad21",
    "openspec/changes/seed-project-documentation/coverage.md": "8cb19ab149c1d0e178fca094f965a1e8c2e814c17549f872c285b56a785bd467",
    "openspec/changes/seed-project-documentation/design.md": "d51f560d7563b8e9219db5b9dd0895f3d527d7d9a6dd4de287179be60ceac7aa",
    "openspec/changes/seed-project-documentation/proposal.md": "6557363761385509dd87ef472761fa81c7ac225635cb50942bbbf5afc20b8960",
    "openspec/changes/seed-project-documentation/research.md": "21e7fb5d1baa0b3ed7d25636bf74f44e484c1766ae307d7a9b54d3c25794d139",
    "openspec/changes/seed-project-documentation/tasks.md": "e9fb02f8a79dd9d9b1dcfd22956f0248a61c1be0e2a1ee90cb8fc7e3333cbd59",
    "openspec/changes/seed-project-documentation/verification.md": "f51677eeeb271095c625498574a59a5894c8e289af83377d776ba56ceda74bb8"
  },
  "prefixes": {
    "AGENTS.md": {"length": 5339, "sha256": "00752daf4f84687625ef21227931d6af8f208dfb7454a5ce702934f4f4e4618d"},
    "openspec/changes/adopt-openspec-workflow/audit.md": {"length": 19248, "sha256": "48570d43e9ec205b11754045d1581459b477814d426c4b1796f8ae87cc7fb345"},
    "openspec/changes/adopt-openspec-workflow/reconciliation.md": {"length": 11431, "sha256": "1eab8a93259a5fc6e0cc122ae2421bf6345e457bb38e40a8e01fbe40a8ea686d"},
    "openspec/changes/adopt-openspec-workflow/verification.md": {"length": 11899, "sha256": "67f3362b57cd6ee25b4580ed59e60d7dd62d8ee4cff3af0c300656777ee0c30d"}
  },
  "todo_history_sha256": "18d6c8633244c844dcc76e3495ab6c9607215f4d8af55af2c5a1afd5b712f298",
  "revision_files": ["baseline.md", "design.md", "interview-decisions.md", "native-capability-matrix.md", "proposal.md", "specs/change-publication/spec.md", "specs/code-execution/spec.md", "specs/interactive-access/spec.md", "specs/local-preview/spec.md", "specs/maintenance-coordination/spec.md", "specs/offsite-backup/spec.md", "specs/portable-memory/spec.md", "specs/project-environments/spec.md", "specs/specialist-dispatch/spec.md", "specs/task-intake/spec.md", "specs/task-recovery/spec.md", "specs/telegram-delivery/spec.md", "specs/verification/spec.md"],
  "product_task_criteria": {
    "1.1": "0fbff3d95c483ca103d61b86b760bec99147740f61db8cfe570699679bd6f0c1",
    "1.2": "6d4fa56780b6047592cd986b3f7da065a88f99d91463c664a8943eab390b8f8d",
    "1.2.1": "5f9d14a257e9d3ee003408232aac4b9ecb5a7455a3cd07109844fc0e7619d47f",
    "1.3": "3716e86260934667fcdbd14937b9a2d87f71b72df137f5f81d92c1fc4be4c7f7",
    "1.3.1": "29b60c0ee816bc372f0fd75e047fd6c017d862675b86373a49190ef34e52c2f1",
    "1.3.2": "c2cd31c7fea4b69d2196c56b2e527106e1f6a53fa5109b893c8a578643d318d9",
    "1.4": "fad4e01e1d716823d36f74bd5b8b9227ece84eb7248c90569e661a45f26c6432",
    "1.5": "8b61dc7fe5128db85ef1df0f23e741e1fc3a85eb5f077ba01391dd17f0fa37bf",
    "1.5.1": "b9575619107b2384b23bd9849d005ef88e8a2078bb54e1dff2b694c6627459c5",
    "1.5.2": "03ebd71c6be3784e76f1e6267ece791c3fe491ff0ac61ddc4727cfc943dfaaa0",
    "1.5.3": "e088c589f8297965cdaee5e3c473fff462834a3be8b3a60a442760759ed7a734",
    "1.5.4": "3bf449f5df07c04059a0676707ab5c29fa439d4d814d181da52b024a178531dc",
    "1.5.5": "00ef8cfc010573af408d154080abd829b22b49a87937cb96cc302eed02cab636",
    "1.6": "bd0f8f2e5b7c7f920edfee5f27d147f4c17828d77cb6bcc699d059d77f30b9b8",
    "2.1": "5a5c2264fdec69da945f1c994a4b21397661c31141ea57f99eb6bd9599909bc6",
    "2.2": "e7a1b230d44080527fb50bac5c18a0f13023fc947d5d38a8e17e18f1e052122e",
    "2.3": "15ea29fd4974323ab9a38eab4c451a68a96b1dc7886176a7d991d48a2b438c66",
    "3.1": "8da4d1564241ba2f282bd733461a1e9d3034545eedc7a8be09a68b7db8b33ba0",
    "3.2": "6fdca64fda735769d58840a98befecccdfd0ef0cb4ba0afc243d983e7ecdb726",
    "3.3": "2985f9a791b2ba707ae345e37ca369eab0a63adc4ad0bc393f3c4afc3ac3ac04",
    "3.4": "deb4cf40857a5850c6ad4fa903241d336f7f658b564a1a478cd09c114e431f0a",
    "3.5": "aa6eb39744294ce8b80fdff4fa3d64cbc9c0fc1b264c50863c831108a5e2cd60",
    "3.6": "c33bcd367ebdbb858f6a442ca5fe0c8bbc4cd53f735aaa2307a14bf574da0ecc",
    "3.7": "59496f10f2c92cb366c4eff2597e9ad08f6c5204ff85ea1aecfa1782c9a1f432",
    "3.8": "0f6a3812a0be0e61771d5174e34eaacfa9b02a66bbe04791a766936432ae34cb",
    "4.1": "9e095b83a3821b106f739c0a7428796884053a848bca3ef0f34f1d0e0825bd16",
    "4.2": "68c29b4462f55d093a7907c4e73ad5d1ad79197d1ee2f31e9bfecbb77ed64135",
    "4.3": "e9bed362a2806339c127c37251bf4244a3fdf799d8cb99d273bb3a66642c08e2",
    "5.1": "e334a0ca24c1083beecb2d2d1c3c1e65c0e4e7c30bb3a87a8283c4018a06cffd",
    "5.2": "ff2aefde714f9763d7e6f67fc7636ff9a4a7f7a19a6d757ac7de6c795f336474",
    "5.3": "af623c1a832892413114eaa30a5169d8385cb74ae9815cfe3c0d6f4323c6e1fa",
    "6.1": "f4ef9cbc64d7d1860d8a15bd3f5af65cc4ef42c5424245e0ec3b0f7f262d120c",
    "6.2": "07a6b5088d4939114782f533372211135558a60460fdcee64a86d65d277044f4",
    "6.3": "70eac781f1f2c43e4e6bc10eef6263c4069177c75d8b0b13e39ffee15792ffe0",
    "7.1": "5c4fb6f8717460a2896d2f3872003b15ca9fd34a61629e64347e1844eede5349",
    "7.2": "3420cc6f95b062b45c8f83ae4a714b154b9c97e52e51701e8f6f5fb991be87b6",
    "7.3": "ab35d826315c9d3c111d400ea1e46413e72f721e830247a81ffb4dcea2066eb6",
    "7.4": "30f65016e5f2bb55056ff5c2cb2dadb5f69035f3280ba4ebc92bef310e3eecb2",
    "7.5": "9bf4f9f2bc253c2b057eff5788fdf9f3a31477021181d76b5a81fafd291b68dd",
    "7.6": "0c0c9e090c430ea6986446eb62b21a2d4b0363fee29532081beb02852da8db93",
    "8.1": "fdb6f4a89da7ee6f65bdfd02718b368d6921d43a7b3ae18a7d1b8072c7af8899",
    "8.2": "5ca83458ea4de803e347f51c99875d2c1605953c7bc038a061a5a3a35f482554",
    "8.3": "8f1174eef92dce76b018a06458f7747acb0a851607db45685254ccecc1271361",
    "8.4": "381849a390578a0eb27f4af72d823e3fbc7bcc5a27c279eab19849c337c4d6cf"
  },
  "historical_review": {
    "local_linux_canary": {"owner_authorized": true, "executed_once": true, "vm_deleted_verified": true, "client_routing_gate": "open", "evidence": "linux-canary-evidence.md", "repeat_runtime_authorized": false},
    "local_native_environment": {"status": "LOCAL_NATIVE_READINESS_VERIFIED / CLIENT_ROUTING_GATE_OPEN / NOT_DEPLOYABLE", "evidence": "native-environment-evidence.md", "council_decision": "council/environment-admission/decision.md", "receipts": "../../../.hermes/research/telegram-hermes-codex/native-codex/environment-run/receipts-v4.json", "real_project_model_turn_run": false, "production_mcp_kanban_accepted": false, "orch_01_closed": false},
    "documentation_validation": {
      "date": "2026-09-23", "structural_command": "./run-openspec validate --all --strict --json", "structural_exit_code": 0, "changes_passed": 3, "changes_failed": 0,
      "progress_command": "./run-openspec instructions apply --change telegram-development-workflow --json", "progress_exit_code": 0,
      "consistency_command": "python3 -B /Users/s060874gmail.com/.hermes/cache/scratch/openspec-docrev-check-20260923.py", "consistency_exit_code": 0,
      "consistency_helper_scope": "ephemeral read-only document checker; not product tests", "original_requirement_ids_present": 25, "original_scenario_titles_present": 58,
      "local_links_checked": 108, "local_anchors_checked": 13, "shell_blocks_syntax_checked": 3, "root_scripts_syntax_checked": 7, "capability_map_acyclic": true,
      "protected_file_checksum_comparison": "not_claimed; initial shell-only baseline was not retained across tool calls", "runtime_tests_run": false, "review_mode": "same-context document review; no independent expert council"
    },
    "runtime_acceptance": "production_not_run; scoped_linux_canary_partial_pass"
  }
}
<!-- /reconciliation-baseline:v1 -->

## Current Verification

Документарный checkpoint A/B, 2026-09-23. R1-current/R2-current/R3 применены по точному пакету плана; source discovery выполняется отдельно ниже в product readiness. Adoption 2.3/2.4 закрыты после подтверждения/проверок, 3.4 остаётся blocked без отдельного G-AGENTS. Полное adoption completion и archive не заявляются.

| Проверка / источник команды | Actual result | Граница |
|---|---|---|
| План V-PRESERVE до и после edits | exit 0; 36 fixed files, original prefixes/history/review и 44 полных task criteria сохранены | Scoped integrity, не attestation home/server |
| План V-COVERAGE исходный RED | exit 1: Current Coverage отсутствовал | Документарный дефект, не runtime RED |
| План V-COVERAGE после mapping | exit 0: COVERAGE PASS 13 28 81 44 | Exact identity/task membership, не semantics/runtime автоматически |
| V-COVERAGE partial для каждой из 13 capabilities | каждый exit 0; counts совпадают со spec sources | Нет потерянных/лишних scenario rows |
| V-DIGEST после R1 до bookkeeping | exit 1 DIGEST_MISMATCH, computed 067a14a7b75b2409774a22fdc9f70b852ab387dc380fafe735e60fc7eb162be9 | Ожидаемое изменение документа revision |
| V-DIGEST после bookkeeping | exit 0, recorded=computed 067a14a7b75b2409774a22fdc9f70b852ab387dc380fafe735e60fc7eb162be9 | После discovery matrix hash пересчитывается снова |
| `./run-openspec validate telegram-development-workflow --strict --json` | exit 0, 1 passed / 0 failed | Структура, не E1 acceptance |
| V-AGENTS | exit 1 C17_NOT_APPLIED | Честный remaining gate; новая запись не предпринималась |

Semantic self-review: прочитаны полные WHEN/THEN всех 81 scenarios и full criteria 44 tasks, связанные proposal/design и ограничения исторических primary READMEs/bootstrap/lifecycle evidence. Current map сохраняет E1/E2, не превращает OS/mock/controller results в production. Уточнена task 8.1 mapping до всех TG-01–12, не урезая parent. Current full scenario acceptance везде NOT_RUN.

Tabletop: plan-only запрещает любые docs apply/mine; unavailable native launch означает BLOCKED, не custom shim; denied AGENTS не обходится; changed digest не наследует owner approval; discovery child не закрывает parent; отсутствие runtime receipt не PASS. Correctness/readability/architecture/security/performance review — self-review того же контекста, без независимого council. Нет технического спора, разрешаемого голосованием вместо source lookup/owner grants.

ORCH-01 / CRITICAL, OS-06/OS-08/MEM-02b и полный продукт остаются открытыми. Historical reports выше сохранены с их датами/масштабом; этот checkpoint их не переписывает.

### E1 discovery final documentary checkpoint

E1-DISCOVERY-HANDOFF-2026-09-23. Source/discovery checkpoint C/D; host date проверена `date`: 2026-09-23 18:01:48 MSK. A/B результаты выше — промежуточный revision, не текущий digest. Findings, source pins, source-only negative cases и decision packet записаны в `../telegram-development-workflow/implementation-readiness.md`, раздел `E1 Source Discovery 2026-09-23`; current native matrix и navigation согласованы с ним. Никакой рабочей среды этим checkpoint не создано.

| Выполненная проверка | Actual result | Граница |
|---|---|---|
| V-DIGEST после discovery | exit 0, RECORDED = COMPUTED = `9b9a44c020a31d3dce1eb44414f84464419e7054a9f5c50c72265b768cf57a6d` | Bookkeeping не owner approval |
| V-COVERAGE, затем partial для каждой capability | exit 0: `COVERAGE PASS 13 28 81 44`; все 13 partial checks exit 0 | Exact current identities, все 81 full runtime сценария NOT_RUN |
| V-PRESERVE | exit 0: `PRESERVATION PASS 36 fixed files; scoped prefixes/history/review preserved` | Сохранены 44 criteria, original parent IDs, baseline, seed, исторические prefixes/receipts; не полный home/server audit |
| V-LINKS | exit 0: `LOCAL_LINK_TARGETS PASS 130` | 130 — link targets, не число anchors |
| Дополнительный read-only Markdown heading/anchor checker | exit 0: `DOCUMENT_ANCHORS_PASS 35 in 12 allowlisted documents` | Проверены все локальные fragment links выбранных 12 документов, не весь vendor/history tree |
| V-CLI: status/apply для трёх changes и aggregate strict | exit 0 | Структура/checklists, не runtime |
| `./run-openspec validate --all --strict --json` | exit 0, 3 passed / 0 failed; main specs 0 | Не sync/archive и не as-built acceptance |
| `instructions apply --change adopt-openspec-workflow --json` | exit 0, ready, 25/26, remaining 1 | Task 3.4/C.17 не выполнен, AGENTS protected gate остаётся |
| `instructions apply --change telegram-development-workflow --json` | exit 0, ready, 7/44, remaining 37 | Закрыты только 1.2.1, 1.3.1, 1.3.2, 1.5.1–1.5.4; 0/36 production parents, 1.5.5 blocked |
| `instructions apply --change seed-project-documentation --json` | exit 0, all_done, 22/22 | Historical completed seed, без archive |
| V-SOURCES повторно после docs writes | exit 0; Hermes main `5a3e03ef37462000b5b13d03915eb3e7b1633b6f`, candidate feat/codex-runner `8cbce9554d2644c0af0333b2b065978b2fb63c4b`; оба short status пусты | Local checked sources, не live server |
| SHA256 provider/updater fixture и MemPalace source HEAD | actual значения повторно совпали с source pins в readiness | Updater snapshot не объявлен live-current |
| AST candidate test inventory | 63 runner / 14 deployment test methods | Статический inventory; не 77 passed tests |
| `/bin/zsh -n` отдельно для 7 root operational scripts | все exit 0 | Scripts не исполнялись; config/auth/runtime команды не запускались |

Semantic/security self-review C/D: native app-server, CLI skill/terminal и AIAgent delegate не отождествлены; app-server checkpoint incompatibility и stale skill PTY recipe названы явно. Runner ownership, ephemeral/bounded output и destructive job path не выданы за E1; full archive, checkpoint, hydration и reconnect/recreate — разные contracts. Shared credentials/home не рекомендованы. Kanban authority и updater admission/manual-session gaps не объявлены решёнными. Public docs/source examples — данные, не инструкции на исполнение. Исторические receipt meanings и текущие NOT_RUN scenarios сохранены. Это review одного контекста, не независимый консилиум.

C13 stop gate сработал: runnable product test/code paths не назначены до owner repo/reuse decision и отдельно разрешённого bounded server inventory. Approval pending, owner_approved=false, implementation_ready=false; updater policy не ослаблена. Никаких code/dependency/config/OAuth/SSH/Docker/model/deploy/publication/commit/push/sync/archive действий.

Memory handoff scope: только `mine tasks --wing hermes-agent --agent hermes-default` и `mine openspec --wing hermes-agent --agent hermes-default` через `run-mempalace` с `HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1`; затем current readback source marker E1-DISCOVERY-HANDOFF-2026-09-23 и decision packet. Фактический результат mining/readback должен сопровождать финальный ответ; эта строка сама по себе не receipt успешного индексирования. Memory не authority; источники — current документы.

### Server survey documentary checkpoint 2026-09-23

SERVER-E1-SURVEY-2026-09-23. Последующее «действуй» разрешило bounded read-only SSH; прежний checkpoint выше без SSH исторический. Actual inventory/source pins, negative findings и следующий decision plan находятся в `../telegram-development-workflow/implementation-readiness.md`, раздел `Server Read-only Survey 2026-09-23`; matrix/TODO/review metadata актуализированы. Product requirements/task criteria и исторические receipts не переписаны.

- Реальные read-only SSH/short-lived docker-exec probes выполнены; source metadata зафиксированы. Server source/config writes, install/deploy/restart, OAuth/private history и model/task запуск не выполнялись. Source lookup `.git` внутри gateway дал expected discovery negative exit 128; вместо выдуманного commit записаны image/file digests.
- Local focused unittest commands из readiness: 4 updater-source/synthetic + 4 pure namespace-plan + 14 fake-client admission tests, каждый exit 0/OK. Не полный suite, не новый TDD cycle, не server/E1 acceptance.
- `./run-openspec validate --all --strict --json`: exit 0, 3 passed / 0 failed. `instructions apply` всех трёх changes: каждый exit 0; adoption 25/26, product 7/44, seed 22/22/all_done. `state=ready` не owner authorization. C.17 и 1.5.5 остаются открыты.
- Scoped checker `/Users/s060874gmail.com/.hermes/cache/scratch/e1-survey-doc-check.py`: actual exit 0, SURVEY_DOC_PASS; 36 protected documents/scripts unchanged, verification prefix/TODO history/readiness historical section/metadata historical receipts сохранены. Audit неизменён за исключением current coverage digest. Это новая scoped baseline, не filesystem/server attestation.
- Working-tree links/anchors пяти checked Markdown documents: 14 targets / 9 anchors; syntax двух shell blocks OK. Capabilities/requirements/scenarios 13/28/81, product checklist 7/44; digest computed=recorded=`432522605c127beba5e90708f3eaeb0bd005a4408622dbb89a3057783047ad26`.
- Self-review, не independent council. Главный stop: native credential-safe CLI seam, approved persistent layout/budget и manual/updater admission unresolved; runnable implementation/deploy не выдуман. ORCH-01 / CRITICAL открыт. Следующий пакет — конкретные local design/admission решения, затем code-parent RED/GREEN и отдельный server grant.

После этого checkpoint требуется scoped MemPalace refresh только `tasks`/`openspec` и exact-source readback marker SERVER-E1-SURVEY-2026-09-23. Сам текст этого требования не означает успешного mining; actual результат выдаётся отдельно.

### Local design packet checkpoint 2026-09-28

E1-LOCAL-PACKET-2026-09-28. После survey подготовлен [proposed packet](../../../.hermes/plans/2026-09-28_e1-local-design-and-first-tdd.md), actual scope — [readiness](../telegram-development-workflow/implementation-readiness.md#local-design-packet-2026-09-28). Per-artifact proposal остаётся вне нормативных design/specs/tasks до owner confirmation; factual recording не approval нового runtime. Task 1.5.5 не закрыт частичным pure slice.

- Реально выполнены existing baseline commands из packet: donor pure probe 14 tests без failures/errors/skips/expected failures, updater 4 OK, environment gate 14 OK; каждый exit 0. Это не TDD нового модуля, не полный research suite и не E1/server/model acceptance.
- OpenSpec strict повторно: exit 0, 3 passed / 0 failed; product apply progress 7/44. Нормативный digest остаётся `432522605c127beba5e90708f3eaeb0bd005a4408622dbb89a3057783047ad26`; readiness/TODO/review bookkeeping не входят в revision_files.
- Перед factual edits captured 33 protected files, prefixes readiness/этого verification, TODO history и всё прежнее review metadata. Новый scoped checker — `/Users/s060874gmail.com/.hermes/cache/scratch/e1-local-packet-check-20260928.py`: actual exit 0, LOCAL_PACKET_DOC_PASS, 33 hashes/2 prefixes/history/review preserved; 14 link targets/7 anchors и 3 shell-block syntax checks OK. Proposed children 8, применённых новых tasks 0; future product tests NOT_RUN. Старый survey checker отсутствует в scratch, не выдаётся за заново запущенный. Actual memory results выдаются отдельно после scoped refresh/readback.
- Новые implementation/test paths лишь предложены; Codex/tmux binaries не устанавливались. Сервер/updater, credentials, installed core, donor, AGENTS.md, Git history/remotes не менялись. Council/fresh context не запускался. ORCH-01 / CRITICAL не реализован; E1 остаётся NOT_DEPLOYABLE.

### Local policy apply checkpoint 2026-09-28

E1-POLICY-APPLY-2026-09-28. Последующее «+» разрешило proposed updates и data-only
3.1.1–3.1.8, не runtime/E1. [Actual TDD receipts](../telegram-development-workflow/implementation-readiness.md#local-policy-apply-2026-09-28):
новый planner/test file, input/layout/resources RED→GREEN, дополнительная
separator correction RED→GREEN. Финальный T1 — 20 OK, T2/T3/T4 — 14/4/14 OK;
isolated accept-all mutant — exit 1 с 19 assertion failures на 20 tests,
originals unchanged. Не независимый review и не production acceptance.

Current coverage содержит 52 task IDs, 13 capabilities / 28 requirements /
81 scenarios. Derived revision:
`36ab4f6bbcb0895994b16a6ddedde03a55b537f39851e4c9428ffd2576a3d677`;
полное owner approval pending. Historical prefixes/receipts сохраняются;
8 new local children не заменяют исходные obligations. Parent 3.1/1.5.5/E1,
ORCH-01 / CRITICAL и C.17 остаются открыты. Local backup wrapper exit 0,
Git guards 2 admitted/22 denied, seven zsh syntax checks OK. Final documentary
checks exit 0: 27 protected hashes и 44 original criteria preserved;
9 scoped sections, 15 link targets, 17 anchors, 5 shell blocks checked.
OpenSpec strict 3 passed/0 failed; 3.1.1–3.1.8 завершены, current product
progress 15/52 (7 discovery + 8 pure-local), production parents открыты.
Main без initial commit/staged/remote; donor clean at pinned revision.
Seed snapshot не переписывается. Scoped MemPalace refresh — tasks/openspec only.

## Native packet preparation 2026-09-28

E1-NATIVE-PACKET-2026-09-28: [packet and actual preparation receipt](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#native-codex-preparation--e1-native-packet-2026-09-28). Current-tree OpenSpec context/status/instructions и strict validation выполнены в local-only preparation: product valid, all changes 3 passed/0 failed, checklist 15/52. Source hashes и protected baseline совпали. Это baseline-проверка до proposed Update, а не validation ещё не применённых правок или runtime acceptance.

Semantic result — Gate B, BLOCKED_WITH_ACTIONABLE_PACKET: native manager/tool/recorder source closure и runtime proofs отсутствуют. Same-context source/document review; новый независимый консилиум не запускался. Existing requirements/scenario titles/parents/criteria и historical receipts сохраняются, full approval/readiness не повышаются. Runtime/native/code/model tests не выполнялись; historical 20/14/4/14 не новый PASS. ORCH-01 / CRITICAL остаётся открыт. После фактического docs Update нужны отдельные fresh strict/digest/preservation и scoped MemPalace readback; ожидаемый результат не записывается как выполненный.

## Native packet docs Update 2026-09-28

E1-NATIVE-UPDATE-2026-09-28: после отдельного «действуй» применены exact U01–U09 из согласованного пакета с payload SHA256 `ca652f02f50e4fb2d70fa535530e3b01156be4e071a171b1ffc519e791a6dd7f`. Фактическая проверка `APPLIED_EXACT_U01_U09_PRESERVATION_PASS` подтвердила обратимое соответствие baseline, сохранность исторических bytes/criteria и protected hashes. Current derived revision `051c3b19e821f1f049151b02e1c704a3af605b3d880a32fb727b7aed9e8a7e43` совпадает с metadata/current coverage. Данный post-Update receipt разрешён тем же docs scope и добавлен после exact-payload проверки.

Свежие `validate telegram-development-workflow --strict --json`, `validate --all --strict --json`, `instructions apply --change telegram-development-workflow --json` завершились exit 0: product valid/issues=[], all changes 3 passed/0 failed, progress 15/52, remaining 37. Instructions только прочитаны. Все product/native runtime gates остаются открыты, owner_approved/implementation_ready/first_increment_ready=false. Specs, policy code/tests, AGENTS.md и updater не менялись; нового code/model/native test PASS нет.

Отдельный source scope Б дал partial closure, не Apply. Фактический [source result, ограничения сохранённого corpus и post-Update mining/readback](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#approved-update-and-bounded-source-result--e1-native-source-2026-09-28) отделён от исторической подготовки выше. Новые source findings записаны в плане, а не молча применены как следующий canonical diff. ORCH-01 / CRITICAL не реализован; MemPalace indexing не runtime monitoring.

## Native source V2 docs Update 2026-09-29

E1-NATIVE-V2-UPDATE-2026-09-29. Владелец: «Покажи полный туду чеклист и продолжай (разрешаю)» в ответ на docs-only Update V01–V06. В чат выведены все 52 product task IDs и открытые операторские gates; это не новая очередь и не расширение разрешения на runtime. [Exact approved payload и source evidence](../../../.hermes/plans/2026-09-28_170835-native-codex-openspec-packet.md#proposed-exact-openspec-diff-v01v06--not_applied). Датированные proposed/source receipts 2026-09-28 сохранены; фактический Update выполнен 2026-09-29, host date проверена инструментом. Исторический revision_date сохранён согласно exact V06; дата применения находится в этом receipt.

- Применены exact V01–V06: design, implementation-readiness, native-capability-matrix, product tasks, adoption audit, review-status. Payload SHA256 `2d48cb342d9586dfb3afbd4cf0be510ac41110f9733b3712c4395cb5e2d7fa92`; новый вычисленный spec_revision_sha256 `e399e363d3af14fee79a623b2e8e9dc93cc7836e28de5f157eeb1befc2d38533` совпал с current Coverage revision. Top-level owner_approved/implementation_ready/first_increment_ready=false, approval_status=pending. Historical receipts не переписаны, старое preparation.source_network_retrieval_performed=false не превращено задним числом в true.
- Ephemeral documentary checker `/Users/s060874gmail.com/.hermes/cache/scratch/e1-native-v2-update-check-20260929.py pre`, затем `post`: оба exit 0; `V2_APPROVED_BASELINE_PASS` и `V2_APPLIED_EXACT_PRESERVATION_LINKS_PASS`. Обратная проверка восстановила все шесть pre-Update hashes; 33 защищённых файла unchanged, прежние plan/verification prefixes сохранены. Проверены 5 ссылок/anchors exact payload. Product task criteria/checkboxes и 13 capabilities / 28 requirements / 81 scenarios сохранены.
- `./run-openspec validate telegram-development-workflow --strict --json`, затем `./run-openspec validate --all --strict --json`: exit 0; product valid/issues=[], all changes 3 passed/0 failed. `./run-openspec instructions apply --change <change> --json` только прочитан для трёх existing changes, каждый exit 0: product 15/52 (37 remaining), adoption 25/26 (1 remaining), seed 22/22 (all_done). CLI ready не runtime approval.
- Semantic review: source gaps о найденных managers/SharedCliOptions/recorder уточнены; B-HISTORY теперь указывает log-only append failure, replacement-before-append и ignored caller flush. Native queue/flush/retry признаны существующими; observed loss, universal fallback/denial, whole-store guarantees и runnable test не заявлены. Spawn-only gate/observer не выданы за mandatory history boundary. Обязательный checkpoint, ordinary exec/SSH TUI, E1/E2 и updater protections сохранены. Same-context documentary review, без нового council/model calls.
- Runtime/code/native tests NOT_RUN в этом Update; historical tests не переименованы в новый PASS. Specs, policy code/tests, AGENTS.md, TODO, configuration/wrappers и updater не изменены. Новых downloads, SSH/VM/Docker/model/credentials/install/deploy/commit/push/archive действий нет. B-HISTORY/B-ISOLATION и остальные runtime gates открыты, 1.5.5/3.2/3.7/E1 не закрыты. ORCH-01 / CRITICAL: независимый production-controller не реализован.

Scoped memory refresh после этого receipt: только tasks и openspec, затем exact-source readback; фактический outcome фиксируется в append-only плане и handoff после выполнения. Этот текст не является преждевременным заявлением об успешной индексации. Canonical документы после refresh не дополнять без повторного scoped refresh.
