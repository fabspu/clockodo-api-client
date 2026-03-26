## ADDED Requirements

### Requirement: ClockodoClient declares its supported top-level resource attributes
The library SHALL define the supported top-level `ClockodoClient` resource attributes in its type surface so static analysis tools can recognize valid access patterns without executing the client constructor.

#### Scenario: Top-level resource attributes are statically discoverable
- **WHEN** a consumer writes code against `ClockodoClient`
- **THEN** supported attributes such as `clock`, `customers`, `entries`, `projects`, `users`, `user_access`, `aggregates`, and `work_times` MUST exist in the declared client type surface

#### Scenario: Declared resource attributes remain concrete
- **WHEN** a consumer accesses a declared top-level resource attribute after constructing `ClockodoClient`
- **THEN** the attribute MUST resolve to its concrete resource-group type rather than an unknown member or untyped dynamic value

### Requirement: Nested resource groups remain discoverable through the typed client surface
The library SHALL preserve the current nested client grouping model while making those nested paths available through the typed top-level client attributes.

#### Scenario: User access nested resources stay discoverable
- **WHEN** a consumer accesses `client.user_access`
- **THEN** static analysis MUST recognize nested members such as `customer_projects` and `services`

#### Scenario: Work time nested resources stay discoverable
- **WHEN** a consumer accesses `client.work_times`
- **THEN** static analysis MUST recognize nested members such as `change_requests` in addition to the existing work time operations

### Requirement: Typed client declarations stay aligned with runtime resources
The library SHALL keep the declared `ClockodoClient` resource surface consistent with the runtime resources installed by default construction.

#### Scenario: Declared client attributes match default resource installation
- **WHEN** the default client resource set is built for `ClockodoClient`
- **THEN** every supported public resource path exposed at runtime MUST have a corresponding declared attribute path in the typed client surface
