## Why

`ClockodoClient` currently attaches its resource groups with `setattr()` during initialization. That runtime behavior works, but static analysis tools and LSPs cannot see those attributes ahead of time, which makes valid access patterns such as `client.customers` or `client.work_times.change_requests` appear as unknown members to consumers.

## What Changes

- Define an explicitly typed public client surface for all top-level and nested resource groups that are currently attached dynamically.
- Update `ClockodoClient` construction so those public attributes exist in the type definition before runtime assignment while preserving the current runtime behavior.
- Cover the typed client surface with tests that verify the declared attributes stay aligned with the endpoint inventory and nested resource groups.
- Document the typing-oriented client surface where needed so consumers understand that IDE completion and static analysis are supported for resource discovery.

## Capabilities

### New Capabilities
- `typed-client-attributes`: Defines the statically declared `ClockodoClient` resource attributes that consumers can access, including nested groups such as `user_access`, `aggregates`, and `work_times.change_requests`.

### Modified Capabilities
- None.

## Impact

- Affects the public client type surface in `src/clockodo_api_lib/client.py` and potentially related resource type definitions.
- Likely adds or refines tests around client attribute exposure in `tests/test_client.py`.
- Improves editor and type-checker behavior for downstream consumers without changing endpoint names or request execution semantics.
