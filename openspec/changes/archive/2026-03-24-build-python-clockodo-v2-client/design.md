## Context

This repository is currently an OpenSpec scaffold without an implemented Python package. The requested change is to create a Python library that covers the full Clockodo API v2 surface, uses `pydantic` for models, and is managed with `uv`. The user also suggested `FastAPI` for calling the API; this design treats that as a requirement to choose an appropriate Python networking stack, and selects `httpx` instead because `FastAPI` is for serving APIs rather than consuming them.

The change has three main pressures:

- Endpoint breadth: "all v2 endpoints" implies a large surface that must remain organized and maintainable.
- Type safety: request and response payloads must be validated and represented as Python models rather than loose dictionaries.
- Local bootstrap: the implementation should be able to initialize Python and `uv` tooling in the developer environment if they are absent, with Homebrew preferred and `apt` as fallback where appropriate.

## Goals / Non-Goals

**Goals:**
- Create a package structure that can represent the entire Clockodo API v2 without collapsing into a single monolithic client file.
- Use `pydantic` models for request/response typing and validation.
- Use a client-side HTTP transport suited to library development, with shared configuration for auth, timeouts, retries if added later, and response parsing.
- Define a maintainable pattern for adding all v2 endpoints and testing their behavior.
- Make packaging and developer workflows `uv`-native.

**Non-Goals:**
- Building a server application, webhook receiver, or any `FastAPI`-based API service.
- Generating code from undocumented assumptions about the Clockodo API.
- Supporting asynchronous and synchronous client APIs in the first implementation unless that falls out cleanly from the chosen structure.
- Promising backward compatibility before the initial package contract is established.

## Decisions

### Use `httpx` for API transport and `pydantic` for models

`httpx` is a better fit than `FastAPI` because this project needs an HTTP client library, not an HTTP server framework. `pydantic` remains the right fit for declarative models, parsed responses, and input validation.

Alternatives considered:
- `FastAPI`: rejected because it does not solve outbound client transport.
- `requests`: simpler, but weaker as a foundation for typed transport abstractions and future async expansion.
- Plain dictionaries/dataclasses instead of `pydantic`: rejected because the user explicitly wants typed models and validation.

### Organize endpoints by resource modules behind a shared client runtime

The library should separate transport/runtime concerns from endpoint definitions. A shared runtime layer will own base URL selection, authentication headers, request execution, response decoding, and common pagination helpers. Resource modules will own endpoint-specific request/response models and public methods.

This produces a structure closer to:

```text
clockodo/
├── client.py
├── config.py
├── exceptions.py
├── transport.py
├── pagination.py
├── models/
└── resources/
    ├── customers.py
    ├── projects.py
    ├── entries.py
    └── ...
```

Alternatives considered:
- One giant client class with all endpoint methods: rejected because "all v2 endpoints" will become unwieldy quickly.
- One file per endpoint only: rejected because it can scatter shared concerns and make discovery harder.

### Prefer a sync-first public API with future async compatibility kept internal

The initial implementation should bias toward a synchronous public client unless the discovered endpoint work makes async support effectively free. This keeps the first version smaller while still allowing transport and model layering that would support a later async client.

Alternatives considered:
- Build both sync and async clients immediately: rejected because the endpoint breadth already creates substantial scope.
- Async-only client: rejected because it would narrow adoption for common scripts and server-side integrations.

### Make endpoint coverage explicit and testable against documented v2 resources

"All v2 endpoints" must be treated as a coverage contract, not a vague aspiration. Implementation should create an explicit inventory of documented Clockodo v2 resources and map each one to client methods, models, and tests. That inventory can live in docs or tests, but it must exist so endpoint coverage is reviewable.

Alternatives considered:
- Ad hoc endpoint additions as needed: rejected because it will drift away from the stated requirement.

### Include environment bootstrap in the implementation plan, not in the runtime package

The user asked for Python and `uv` to be installed if absent, preferring Homebrew first and `apt` second. That requirement belongs to implementation setup and contributor workflow, not the runtime behavior of the package. The design therefore treats bootstrap as a task-level concern that may require local environment checks and installation commands during `/opsx:apply`.

## Risks / Trade-offs

- [Clockodo v2 surface may be broader or more inconsistent than expected] -> Mitigation: create an endpoint inventory early and implement by resource group rather than improvising.
- [Typed models can become verbose for a large API] -> Mitigation: centralize shared field types and base models to avoid duplication.
- [The API may return inconsistent payload shapes across endpoints] -> Mitigation: isolate parsing at the resource boundary and raise explicit validation exceptions when payloads diverge from expected schemas.
- [A sync-first API may require later expansion for async users] -> Mitigation: keep transport boundaries clean so async support can be added without rewriting models.
- [Tool bootstrap may differ across machines] -> Mitigation: verify local availability of Python and `uv` during implementation and use package-manager-specific setup steps only when needed.

## Migration Plan

This is a net-new package, so there is no production data migration. The practical rollout is:

1. Bootstrap local Python and `uv` tooling if missing.
2. Initialize the package and dependency metadata.
3. Implement runtime, endpoint modules, and tests incrementally by resource group.
4. Validate packaging, tests, and example usage before publishing or handing off.

Rollback is straightforward because the repository does not yet contain an existing implementation to preserve.

## Open Questions

- Should the first implementation include only a synchronous public client, or is dual sync/async support worth the added surface area? A: only synchronous
- Do we want a flat public API (`client.get_customers()`) or grouped resources (`client.customers.list()`) for long-term ergonomics? A: grouped resources
- Is there any Clockodo API behavior such as rate-limit headers, custom auth header formatting, or bulk endpoints that should become first-class abstractions instead of raw method wrappers? A: use the internet herefor look it up in the clockodo documentation
