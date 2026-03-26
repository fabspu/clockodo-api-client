## 1. Formatter setup

- [x] 1.1 Add Ruff to the `dev` dependency group and refresh `uv.lock` so formatting checks run through the repository's existing `uv` workflow
- [x] 1.2 Run the formatter locally and keep any necessary source-file normalization in this change

## 2. Workflow implementation

- [x] 2.1 Add a GitHub Actions workflow that runs on `push` and `pull_request`, provisions Python 3.12, installs `uv`, and executes syntax plus formatting checks
- [x] 2.2 Pin every `uses:` reference in the workflow to a full commit SHA

## 3. Validation

- [x] 3.1 Run the syntax and formatting commands locally and fix any failures
- [x] 3.2 Run the existing test suite after the dependency and workflow updates
