## ADDED Requirements

### Requirement: Consumer documentation explains client setup and configuration
The project SHALL document how a downstream consumer constructs `ClockodoClient`, including the required authentication inputs and the optional configuration values that affect request behavior.

#### Scenario: README explains required and optional client inputs
- **WHEN** a developer reads the consumer usage guide
- **THEN** the documentation identifies the required `api_user`, `api_key`, `application_name`, and `application_contact` inputs and explains optional settings such as `base_url`, `timeout`, and `language`

#### Scenario: README shows a valid client construction example
- **WHEN** a developer follows the documented setup example
- **THEN** the example imports `ClockodoClient` from `clockodo_api_lib` and shows a complete client construction pattern that matches the current public API

### Requirement: Consumer documentation explains how to navigate the public API surface
The project SHALL document how endpoint groups are exposed on the client so consumers can discover top-level and nested resources without inspecting the implementation.

#### Scenario: README lists public resource entry points
- **WHEN** a developer needs to find an endpoint group
- **THEN** the documentation describes the public client attributes for representative top-level resources and nested groups such as `user_access`, `aggregates`, and `work_times.change_requests`

#### Scenario: README explains model import conventions
- **WHEN** a developer needs request params or request body types
- **THEN** the documentation shows that typed request and parameter models are imported from `clockodo_api_lib.models` and used directly in client calls

### Requirement: Consumer documentation includes representative usage workflows
The project SHALL include copy-paste examples for common library workflows so first-time consumers can adapt them without reverse-engineering tests or source files.

#### Scenario: README shows a list workflow
- **WHEN** a developer wants to query Clockodo data
- **THEN** the documentation includes an example that performs a list call with a typed parameter model and shows how to read the returned items or pagination data

#### Scenario: README shows a create or nested-resource workflow
- **WHEN** a developer wants to perform a write or nested-resource call
- **THEN** the documentation includes at least one example that creates a resource or calls a nested resource group using the current public API

### Requirement: Consumer usage guidance remains distinct from contributor guidance
The project SHALL separate "use the library" documentation from "develop the library" instructions so consumers can find the right guidance quickly.

#### Scenario: README separates usage from development tasks
- **WHEN** a developer reads the README
- **THEN** consumer installation and usage guidance appears separately from contributor commands such as dependency sync, tests, and validation
