## ADDED Requirements

### Requirement: Configured Clockodo client
The library SHALL provide a reusable Clockodo API v2 client that accepts validated configuration for authentication, base URL, and transport behavior.

#### Scenario: Create a client with valid configuration
- **WHEN** a consumer constructs the client with all required Clockodo authentication inputs and optional transport settings
- **THEN** the library returns a client instance ready to issue API v2 requests

#### Scenario: Reject incomplete client configuration
- **WHEN** a consumer omits a required authentication or base configuration value
- **THEN** the library MUST fail fast with a typed validation error before any HTTP request is sent

### Requirement: Shared request execution
The client SHALL execute requests through a shared runtime that applies Clockodo-required headers, serializes request inputs, and decodes successful responses consistently across endpoints.

#### Scenario: Apply shared request behavior
- **WHEN** any endpoint method issues a request through the client runtime
- **THEN** the runtime MUST apply the configured authentication headers, base URL, and common request options before sending the request

### Requirement: Pagination support
The client SHALL provide a consistent way to request paginated Clockodo API v2 collections and expose pagination metadata when the API returns it.

#### Scenario: Read a paginated collection
- **WHEN** a consumer calls an endpoint that returns a paginated collection
- **THEN** the library MUST parse the collection items and any available pagination metadata into typed result objects
