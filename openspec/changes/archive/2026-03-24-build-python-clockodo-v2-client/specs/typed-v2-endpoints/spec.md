## ADDED Requirements

### Requirement: Full documented v2 endpoint coverage
The library SHALL expose all documented Clockodo API v2 endpoints through Python methods before the change is considered complete.

#### Scenario: Review endpoint coverage
- **WHEN** implementation is reviewed against the documented Clockodo API v2 endpoint inventory
- **THEN** every documented endpoint MUST have a corresponding supported client method or resource operation

### Requirement: Typed request and response models
Each supported endpoint SHALL use typed request and response models defined with `pydantic` wherever the API accepts structured inputs or returns structured data.

#### Scenario: Parse endpoint responses into models
- **WHEN** an endpoint returns a successful JSON response
- **THEN** the library MUST parse that payload into the documented `pydantic` model for that endpoint instead of returning an untyped raw dictionary by default

### Requirement: Discoverable endpoint organization
The public Python API SHALL organize endpoint methods in a way that remains navigable as the full v2 surface is added.

#### Scenario: Access related endpoint methods coherently
- **WHEN** a consumer uses multiple endpoints from the same Clockodo resource area
- **THEN** the client API MUST expose those operations through a consistent naming and module structure
