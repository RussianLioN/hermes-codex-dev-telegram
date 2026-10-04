# hermes-agent — project integration workspace

Локальный репозиторий проекта: `/Users/s060874gmail.com/coding/projects/hermes-agent`.
Владелец выбрал его для дальнейшей реализации 2026-09-23. Это **не upstream
NousResearch/hermes-agent** и не установленный runtime `~/.hermes/hermes-agent`.
Существующие operations scripts, OpenSpec и проектные правила остаются здесь;
будущая интеграция Telegram → Hermes → Codex также принадлежит этому repo.

## Start here

- [OpenSpec navigation](openspec/README.md), [project map](openspec/PROJECT.md).
- [Current tasks and critical gates](tasks/todo.md).
- [Repository decision and selective reuse](openspec/changes/telegram-development-workflow/implementation-readiness.md#repository-decision-2026-09-23).
- [Workflow](openspec/WORKFLOW.md) and [agent rules](AGENTS.md).

Product status: NOT_DEPLOYABLE. Repository selection is not approval of the
exact product revision, runtime implementation, SSH, deployment or publication.
ORCH-01 / CRITICAL remains open: MemPalace does not supervise or restart agents.

## Local project policy slice

Owner-approved scope E1-POLICY-APPLY-2026-09-28 adds
`scripts/project_environment.py:plan_project_environment(document)` and
`tests/test_project_environment.py`. This is a pure Python standard-library
function, not a CLI launcher, scheduler, Docker adapter or authorization gate.
It validates the seven-field policy, describes stable owner/project paths and
compact/large resource limits, and always returns `runtime_admitted=False`.
Each result is independent; input values are not normalized or modified.

Input contract: exact fields `schema_version`, `owner_id`, `project_id`,
`image_ref`, `worker_uid`, `worker_gid`, `resource_class`; plain dict/scalars only.
Schema is integer 1; worker IDs are integers 1000..65533, never bool. Opaque
owner/project IDs match `[a-z][a-z0-9]{0,15}`. Image syntax is a lowercase
repository (up to 255 characters) plus `@sha256:` and 64 lowercase hex digits;
optional registry port is canonical decimal 1..65535. Tags, URL/userinfo,
IPv6 registry syntax and noncanonical segments are not supported by this narrow
policy; values are rejected, not repaired. This validates syntax, not image
provenance. Resource class must explicitly be `compact` or `large`.

Run from this repository root (tested with Python 3.13.3; uses 3.10+ syntax):

```sh
PYTHONPATH=scripts python3 -B -m unittest discover -s tests -p test_project_environment.py -v
```

Focused runs append `-k rejects`, `-k layout` or `-k resources`.
No install, network, Docker or credentials are needed. Test image digests and
UIDs are synthetic, not approved resources. The function does not create paths,
reserve pool capacity, enforce quotas, inspect symlinks/ACLs, save history or
launch Codex. A future trusted runtime must verify all those boundaries afresh.
See [local contract](openspec/changes/telegram-development-workflow/design.md#approved-local-policy-slice-2026-09-28)
and [evidence](openspec/changes/telegram-development-workflow/implementation-readiness.md).

## Git boundary

Git was initialized locally on `main`, without a first commit, staged files or
remote. These are bootstrap facts, not a promise of future Git state; inspect
`git status --short` and `git branch --show-current` before changes. No GitHub
repository was created. Commits, remote provisioning and pushes need separate
permission. Worktree/candidate-commit workflows require an initial reviewed commit.

The older statement in AGENTS.md that this directory is not a Git repository
is a historical baseline. AGENTS.md was not edited: its protected-write gate
remains separate from the authorized Git initialization.

`.gitignore` uses a reviewed root-path allowlist. Existing root scripts,
OpenSpec/tasks and project skill adapters are eligible; new root source paths
must be admitted deliberately when their implementation slice is designed.
Credentials, environment files, private state, raw history, archives, caches,
installed tooling, research dumps and council transcripts are excluded.
Nothing was staged. Ignore rules are not a secret scanner or an access-control
boundary: review exact contents before any initial commit; never use blanket
`git add -f` to bypass exclusions.

Ignored local research/tooling/plans remain on disk. Some documentary links
refer to those local resources; this is not yet a self-contained clone/install
package. Do not copy whole runtime homes, private evidence or dependency trees
to make a future clone appear complete.

## Reuse boundary

`../hermes-remote-migration` is a read-only source donor, not the implementation
repository or a runtime dependency. The pinned source/test map and selected
regression cases are recorded in the repository decision above. Its scheduler,
GitHub App publisher, separate updater and ephemeral/destructive job lifecycle
are not imported. No executable runner code was copied at bootstrap; import
only needed, reviewed seams with their tests in the corresponding code slice.
