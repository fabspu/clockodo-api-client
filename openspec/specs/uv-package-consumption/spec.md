# uv-package-consumption Specification

## Purpose
TBD - created by archiving change support-uv-package-consumption. Update Purpose after archive.
## Requirements
### Requirement: Downstream `uv` installation workflows are documented
The project SHALL document the supported ways for a downstream Python project to install this library with `uv`, and SHALL distinguish those consumer workflows from contributor setup commands.

#### Scenario: README shows supported consumer installation commands
- **WHEN** a downstream developer reads the package installation guidance
- **THEN** the documentation includes copy-paste `uv` commands for local path installation, editable local path installation, and installation from a built wheel

#### Scenario: README separates consumers from contributors
- **WHEN** a developer reads the README
- **THEN** the document distinguishes "use this package in another project" guidance from "develop this package locally" guidance

### Requirement: Distribution artifacts remain installable in downstream `uv` projects
The project SHALL produce package artifacts and local package metadata that allow an isolated downstream `uv` project to install the library without changing its public package name or Python import path.

#### Scenario: Built artifact installs into a clean consumer project
- **WHEN** a clean `uv` project adds the built wheel for this library
- **THEN** the installation succeeds and the package remains importable as `clockodo_api_lib`

#### Scenario: Local path install preserves the package contract
- **WHEN** a clean `uv` project adds the repository as a local path dependency
- **THEN** the installation succeeds and consumer code imports the library with `from clockodo_api_lib import ClockodoClient`

### Requirement: The supported consumer install contract is validated
The project SHALL provide a repeatable validation step for the documented downstream install workflows so packaging regressions are detected before release or handoff.

#### Scenario: Validation covers artifact-based consumption
- **WHEN** maintainers run the package-consumption validation flow
- **THEN** it verifies at least one built-artifact installation path in an isolated `uv` consumer environment

#### Scenario: Validation covers local development consumption
- **WHEN** maintainers run the package-consumption validation flow
- **THEN** it verifies at least one local path-based installation path in an isolated `uv` consumer environment

