## Why

The repository currently has no GitHub Actions workflow for basic code-quality gates, so syntax errors or formatting drift can slip into pull requests unnoticed. The project already uses `uv` for local development, which makes this a good time to add a small, repeatable CI check that matches the existing tooling.

## What Changes

- Add a GitHub Actions workflow that runs on `push` and `pull_request` and checks Python syntax plus code formatting.
- Introduce the minimal formatter support needed to run the formatting check through the repository's existing `uv`-managed development workflow.
- Pin every GitHub Action reference in the workflow to a full commit SHA instead of floating version tags.

## Capabilities

### New Capabilities
- `repository-quality-automation`: Defines automated syntax and formatting verification for repository changes, including immutable pinning for workflow actions.

### Modified Capabilities
- None.

## Impact

- Affects repository automation under `.github/workflows/`.
- Adds formatter support to the development dependency set and refreshes `uv.lock`.
- May reformat existing Python files if the formatter finds drift.
- Does not change the package's public API or runtime behavior.
