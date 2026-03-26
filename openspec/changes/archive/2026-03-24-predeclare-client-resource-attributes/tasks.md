## 1. Define the typed client surface

- [x] 1.1 Add a dedicated typed surface for `ClockodoClient` that declares every supported top-level public attribute and its concrete resource-group type
- [x] 1.2 Ensure the typed surface covers grouped resources such as `user_access`, `aggregates`, and `work_times` so existing nested members stay discoverable through the client

## 2. Wire the runtime client to the declared surface

- [x] 2.1 Update `ClockodoClient` to inherit the typed surface and assign the default resource instances onto the declared attributes during initialization
- [x] 2.2 Keep the declared client surface aligned with the default resource factory without changing endpoint names, constructor inputs, or request execution behavior

## 3. Verify typing and runtime parity

- [x] 3.1 Extend `tests/test_client.py` to verify the declared client attributes match the runtime resource installation and representative nested paths remain accessible
- [x] 3.2 Run the relevant test coverage for client construction and resource exposure to confirm the typed client surface does not regress existing behavior
