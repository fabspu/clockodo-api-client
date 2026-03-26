## Context

The project is a Python library managed with `uv`, with tests already configured in `pyproject.toml`, but it does not yet have GitHub Actions automation or a formatter in the development toolchain. The requested change is narrow: add a workflow that catches syntax errors and formatting drift while keeping the implementation aligned with the repository's existing `uv`-based setup and avoiding floating GitHub Action refs.

## Goals / Non-Goals

**Goals:**
- Run a fast repository-level quality workflow for pull requests and pushes.
- Fail CI when Python files contain syntax errors.
- Fail CI when the repository is not formatted according to an enforced formatter.
- Keep the formatter command reproducible through the same `uv` workflow the repo already uses locally.
- Pin every GitHub Action reference to a full commit SHA.

**Non-Goals:**
- Adding broader linting, type-checking, release automation, or packaging validation to this workflow.
- Replacing the existing test workflow or release process.
- Introducing multiple workflows when a single job is sufficient for the requested checks.

## Decisions

### Use one lightweight quality workflow

The repository only needs one small workflow for this change, so implementation should add a single workflow file that runs on both `push` and `pull_request`. This keeps the status surface simple and makes the repository's baseline quality gate obvious.

Alternatives considered:
- Split syntax and formatting into separate workflows: rejected because it adds more files and status checks without improving clarity for this scope.
- Run only on the default branch: rejected because the user asked for a workflow that watches the repository and should therefore catch problems in pull requests before merge.

### Manage formatting through the repo's `uv` dev dependency workflow

The repo already commits `pyproject.toml` and `uv.lock`, so the formatter should be added as a development dependency and run with `uv`. This keeps the command reproducible in both CI and local development without introducing an action-specific tool install path that bypasses the repository's dependency management.

Alternatives considered:
- Use `astral-sh/ruff-action`: rejected because it adds another third-party GitHub Action and makes local reproduction less direct.
- Use `uvx` or `pip install ruff` only inside CI: rejected because the formatter version would live in workflow logic instead of the repo's normal dependency contract.

### Use `python -m compileall` for syntax validation

Syntax checking should use the standard library's compile step across `src` and `tests`. It is fast, does not require another lint rule set, and matches the user's explicit requirement to watch for syntax errors.

Alternatives considered:
- Use `pytest` alone to surface syntax problems: rejected because import coverage is indirect and slower than a direct compile pass.
- Add a broader linter rule set for syntax: rejected because formatting and syntax are the requested scope, not general lint policy.

### Minimize external action usage and pin immutable refs

The workflow should only use the official actions required to check out the repository and provision Python, with each `uses:` entry pinned to a full commit SHA. `uv` can then be installed with a normal shell command, which avoids adding more GitHub Actions than necessary while still satisfying the immutable pinning requirement.

Alternatives considered:
- Use setup actions for every tool: rejected because it increases the number of pinned external dependencies for little benefit in this small workflow.

## Risks / Trade-offs

- [Formatting may rewrite some existing files] -> Mitigation: run the formatter locally during implementation and include any required file updates in the same change.
- [A new dev dependency changes the lockfile] -> Mitigation: keep the addition limited to the formatter and validate the test suite after refreshing the lock.
- [CI depends on a specific Python/tool bootstrap sequence] -> Mitigation: match the repository's current Python version target and keep the workflow commands short and explicit.

## Migration Plan

1. Add the formatter to the dev dependency group and refresh `uv.lock`.
2. Run the formatter locally and apply any required file changes.
3. Add the GitHub Actions workflow with SHA-pinned actions and the syntax/format commands.
4. Validate the new commands locally before considering the change complete.

Rollback is straightforward: remove the workflow and the formatter dependency updates if the quality gate proves too noisy or misaligned.

## Open Questions

- None.
