# repository-quality-automation Specification

## Purpose
TBD - created by archiving change add-syntax-and-format-ci. Update Purpose after archive.
## Requirements
### Requirement: Repository changes are checked for Python syntax and formatting
The repository SHALL run automated validation for Python syntax and code formatting on both pull requests and pushes.

#### Scenario: Workflow runs for proposed and pushed changes
- **WHEN** a contributor opens or updates a pull request, or pushes commits to the repository
- **THEN** GitHub Actions runs a workflow that executes both syntax validation and formatting validation before reporting status

#### Scenario: Syntax errors fail the workflow
- **WHEN** Python source or test files contain syntax errors
- **THEN** the syntax validation step fails and the workflow reports the change as not passing

#### Scenario: Formatting drift fails the workflow
- **WHEN** tracked repository files are not formatted according to the repository formatter
- **THEN** the formatting validation step fails and the workflow reports the change as not passing

### Requirement: Workflow action references are immutable
The repository SHALL reference GitHub Actions by full commit SHA instead of floating version tags.

#### Scenario: Workflow uses full commit SHAs
- **WHEN** a maintainer inspects the workflow definition
- **THEN** every `uses:` entry references a full 40-character commit SHA rather than a tag such as `@v4` or `@v5`

