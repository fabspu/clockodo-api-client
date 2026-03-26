## Context

`ClockodoClient` is the main public entry point for the library, but it currently builds its resource surface from `build_default_resources()` and installs each resource group with `setattr()`. That keeps the runtime implementation compact, yet it hides the public attributes from static analysis because names such as `customers`, `projects`, `user_access`, and `work_times` do not exist in the class definition.

The underlying resource classes are already explicitly typed. Nested groups such as `UserAccessGroup`, `AggregatesGroup`, and `WorkTimesResource` also declare their own nested attributes. The typing gap is therefore concentrated at the top-level client object and in keeping that declared surface aligned with the resource factory over time.

## Goals / Non-Goals

**Goals:**
- Make the supported `ClockodoClient` resource attributes visible to IDE completion, LSPs, and static type checkers.
- Preserve the existing runtime API shape and endpoint behavior.
- Keep the declared client surface aligned with the resources produced by `build_default_resources()`.
- Cover both top-level attributes and existing nested groups in tests so future endpoint additions do not silently regress typing support.

**Non-Goals:**
- Redesigning the resource factory or changing endpoint naming conventions.
- Replacing the existing resource classes with protocols, stubs, or generated code.
- Introducing optional resource attributes that require `None` checks from consumers after successful client construction.
- Changing HTTP behavior, models, or endpoint inventory semantics.

## Decisions

### Add a dedicated typed superclass for the client surface

Implementation should introduce a dedicated base class, such as `_ClockodoClientSurface`, that declares every public `ClockodoClient` attribute with concrete types. `ClockodoClient` will inherit from that surface class and continue to populate the actual resource instances during initialization.

This keeps the typing contract separate from constructor logic, satisfies the requested "interface or superclass" direction, and makes the public surface easy to scan in one place.

Alternatives considered:
- Add annotations directly on `ClockodoClient`: rejected because it mixes the long resource surface declaration into the runtime constructor class and makes future maintenance noisier.
- Ship a `.pyi` stub instead: rejected because it creates a second source of truth for a small library that already ships typed Python modules.
- Type everything as `Any` or `Optional[...]`: rejected because it weakens the exact completion and type-checking benefit this change is meant to provide.

### Keep runtime initialization behavior but assign declared attributes explicitly

The constructor should continue to build resources from `build_default_resources()`, but it should assign the known public attributes onto `self` in a way that matches the declared surface. Explicit assignment makes the relationship between the factory output and the public surface obvious and avoids relying entirely on dynamic `setattr()` for the consumer-facing API.

Alternatives considered:
- Keep the loop with `setattr()` unchanged and rely only on annotations: acceptable in principle, but rejected because explicit assignment makes drift easier to notice in code review and provides a clearer bridge between types and runtime state.
- Remove `build_default_resources()` and construct each resource inline: rejected because it duplicates existing factory logic and makes the change broader than necessary.

### Treat nested group typing as part of the contract, not a separate feature

The top-level client surface should expose concrete group types for `user_access`, `aggregates`, and `work_times`. Because those classes already declare nested attributes such as `customer_projects`, `services`, `users_me`, and `change_requests`, consumers will gain nested discovery automatically once the top-level attributes are typed.

Alternatives considered:
- Add separate client attributes for nested resources: rejected because it would flatten an intentionally grouped API and diverge from the current public shape.

### Add parity tests between the declared surface and runtime resources

Tests should verify that the declared public attributes correspond to the runtime resources created by the default factory and that nested groups continue to expose the expected members. This reduces the risk that a future endpoint addition updates `ENDPOINT_INVENTORY` or `build_default_resources()` without updating the typed client surface.

Alternatives considered:
- Rely only on manual review when adding endpoints: rejected because typing drift is easy to miss and directly affects consumer ergonomics.

## Risks / Trade-offs

- [The declared client surface can drift from the resource factory] -> Mitigation: add tests that compare supported public paths and verify representative nested members.
- [Explicit attribute assignment adds some boilerplate] -> Mitigation: keep the surface centralized in a dedicated base class and keep assignments limited to known public attributes.
- [Future endpoint additions will require updating both factory and surface declarations] -> Mitigation: make that duplication intentional and test-enforced because it protects the public typing contract.

## Migration Plan

1. Add the typed client surface base class with annotations for config, transport, top-level resources, and nested groups.
2. Update `ClockodoClient` to inherit that surface and assign resource instances to the declared attributes during initialization.
3. Extend tests to verify the declared surface matches runtime resources and that representative nested paths remain accessible.
4. Update any consumer-facing documentation only if the current README needs an explicit note that client resource discovery is IDE-friendly.

Rollback is low risk: revert the typed surface and constructor wiring if the maintenance cost outweighs the tooling benefit.

## Open Questions

- Should the implementation expose the typed surface class as a public import, or keep it private and only surface the improved typing through `ClockodoClient`?
