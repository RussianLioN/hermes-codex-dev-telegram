# Источники первичного посева

## Sources

Версионная основа: установленный `@fission-ai/openspec` 1.13.0, schema `spec-driven`, [manifest](../../../.hermes/tooling/openspec/package.json), [wrapper](../../../run-openspec). Это не утверждение о latest release. Tag `v1.13.0` при планировании разрешён в commit `9d4e5974e5c0d9a09b9c6c1e1eb0975e80ec4461`; raw GET S1/S2/S6 по этому commit повторён 2026-09-22, exit 0. Остальные страницы прочитаны при планировании 2026-09-21; в текущем apply их содержание заново не аттестовано.

| ID | Официальный открытый источник | Вывод и применение |
|---|---|---|
| S1 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/existing-projects.md | Brownfield/delta-first; «Resist the urge to back-fill everything». Описываем весь поддерживаемый inventory, но не создаём фиктивных normative specs для неизменяемого runtime |
| S2 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/writing-specs.md | Одно наблюдаемое поведение на SHALL/MUST; WHEN/THEN и важные отказы; один intent на change. Implementation details остаются в design |
| S3 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/workflows.md | Refinement возвращается в артефакты; independent intent получает отдельный change; workflow не заменяет runtime |
| S4 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/reviewing-changes.md | Review proposal/specs/tasks до apply; после исполнения отдельно completeness, correctness, coherence, а не только validator |
| S5 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/team-workflow.md | Один writer shared change, specs и code версионируются вместе. Здесь Git отсутствует; рекомендация не разрешает git init/commit |
| S6 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/examples.md#recipe-5-a-refactor-with-no-behavior-change | Explicit `skip_specs: true` для работы без изменения specified behavior; отсутствие deltas обозначено, не забыто |
| S7 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/cli.md | `context`, `status`, `instructions`, `validate` — разные inspection вопросы; точные flags/JSON сверяются с installed CLI |
| S8 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/supported-tools.md | Hermes и Codex имеют разные integration paths; файл skill, его runtime loading и вызов — разные факты |
| S9 | https://github.com/Fission-AI/OpenSpec/blob/v1.13.0/docs/concepts.md | Main specs, in-flight changes и archive имеют разные роли; переход baseline нельзя имитировать переносом неподтверждённого продукта |
| H1 | https://hermes-agent.nousresearch.com/docs | Авторитетная документация Hermes; конкретные runtime APIs этим docs apply не проверяются и не выбираются |

Локальный authoritative формат: [schema](../../../.hermes/tooling/openspec/node_modules/@fission-ai/openspec/schemas/spec-driven/schema.yaml), фактические `status --json` / `instructions apply --json`, [propose skill](../../../.hermes/skills/openspec-propose/SKILL.md), [apply skill](../../../.hermes/skills/openspec-apply-change/SKILL.md). Эти источники описывают workflow, но не выдают права на runtime/deployment.

[Task parser](../../../.hermes/tooling/openspec/node_modules/@fission-ai/openspec/dist/utils/task-progress.js) учитывает вложенные checkbox и примеры внутри fences. Поэтому ROADMAP не содержит checkbox, а checklist — только реальные задачи. [Numbering validator](../../../.hermes/tooling/openspec/node_modules/@fission-ai/openspec/dist/core/validation/task-numbering.js) проверяет IDs и numbered groups. Semantic review опирается на [штатный template](../../../.hermes/tooling/openspec/node_modules/@fission-ai/openspec/dist/core/templates/workflows/verify-change.js); отдельной CLI-команды `openspec verify` не предлагается.

## Applied Practices

1. S1/S6: docs-only посев в собственном change; product deltas и main specs не меняются. Полнота — карта компонентов, источников и gaps, не backfill всей истории.
2. S2/S3: один intent, исходные parent task IDs сохранены. Для будущего кода exact source/test paths сначала проверяются по manifests/definitions/usages; неизвестные пути остаются BLOCKED_PATH_DISCOVERY.
3. S4: структурная проверка, membership coverage, source review и runtime acceptance различаются. Фиксируются реальные command/cwd/exit, expected outputs не называются receipts.
4. S5: один writer общих документов; параллельны независимые read-only исследования. Нет нового tracker рядом с change/tasks и Hermes Kanban. Git adoption и commits требуют отдельного решения.
5. S7/S8: используем существующий wrapper и installed skills; init/update/install ради документации не нужны. CLI fallback не выдаётся за исполнение отсутствующего slash tool.
6. S9: sync/archive отдельно разрешаются после подходящей приёмки. Завершение docs tasks не меняет product owner_approved и не закрывает ORCH-01.
7. Локальная адаптация [WORKFLOW](../../WORKFLOW.md): задачи по 2–5 минут focused работы, checkpoints каждые 2–3 задачи; docs проверяются без dummy TDD, code — RED/minimal GREEN/regression. Оценка не является SLA сетевого ожидания.

## Limitations

Исследованы официальные документы и публичные recipes, не проведены независимый benchmark, cross-model review или новый council. Historical guides сохраняются как background, не requirements и не permissions. Документация не усиливает OS isolation.

Восстановление индекса 2026-09-22 выполнено штатным scoped mine без переустановки/изменения конфигурации. Предыдущий timeout был отказом запуска проверки, не доказанной corruption. Отдельный MCP stdio disconnect диагностирован через рабочие CLI status/search; последующий exact-source MCP search/readback доступен. Подробные actual результаты — в [verification](verification.md), operational маршрут — в [PROJECT](../../PROJECT.md#existing-operations) и [WORKFLOW](../../WORKFLOW.md#11-handoff-и-память).

Ни OpenSpec, ни MemPalace не мониторят и не перезапускают stalled agents. ORCH-01 / CRITICAL остаётся открыт.
