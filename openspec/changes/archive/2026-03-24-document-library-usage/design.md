## Context

The repository already documents installation and includes a short usage snippet in `README.md`, but it does not yet function as a practical consumer guide. To answer basic questions such as which constructor arguments are required, how nested resource groups are exposed, or where request model classes come from, a user currently has to inspect `src/clockodo_api_lib/*` or the tests.

This change is documentation-only in terms of runtime behavior, but it still spans multiple public-facing concerns:

- consumer setup and client configuration
- discovery of resource entry points such as `client.customers` and `client.work_times.change_requests`
- use of typed request params and response models
- separation of consumer guidance from contributor commands

## Goals / Non-Goals

**Goals:**
- Make `README.md` sufficient for a first-time consumer to install the package and complete common API workflows without reading source code.
- Document the required authentication values and optional client settings that shape requests.
- Explain how the public client surface maps to endpoint groups and nested resource groups.
- Show where typed request and response models come from and how they are used in normal calls.

**Non-Goals:**
- Changing the public Python API, resource names, or model definitions.
- Adding a full standalone documentation site or generated API reference system.
- Explaining every Clockodo endpoint field in prose when the typed models already define them.
- Documenting publishing or distribution flows beyond what is already covered elsewhere.

## Decisions

### Keep the consumer guide in `README.md`

The project is small enough that splitting usage documentation into a separate docs site would add indirection without much value. Implementation should instead expand the README into a clearer consumer guide with sections for installation, configuration, core workflows, and development commands.

Alternatives considered:
- Add a `docs/` directory: rejected because it creates another place for documentation drift before the project has enough content to justify it.
- Leave the README minimal and rely on source browsing: rejected because that fails the stated goal of making the library easier to use.

### Organize usage guidance around common consumer questions

The document should answer, in order:

- how to install the package
- how to construct `ClockodoClient`
- which configuration values are required or optional
- how to call top-level and nested resource groups
- how to pass typed request models and inspect typed results

This structure matches how a consumer approaches a new client library and keeps the document task-oriented instead of mirroring the source tree.

Alternatives considered:
- Document files module-by-module: rejected because the internal package layout is not the mental model consumers need.
- Document every endpoint one by one: rejected because it would duplicate the endpoint inventory and become harder to maintain.

### Derive examples from the existing public API and tested workflows

Examples should be limited to behavior that is already represented by the current public API and unit tests: client construction, CRUD usage, list queries, and nested groups. This keeps the documentation aligned with stable entry points such as `ClockodoClient`, `client.customers`, `client.aggregates.users_me`, and `client.work_times.change_requests`.

Alternatives considered:
- Add speculative examples for workflows not exercised in the current package surface: rejected because it increases the chance of stale or misleading guidance.

### Treat resource discovery and model imports as first-class documentation topics

The current README implies that resources exist, but it does not explain the naming conventions or where request model classes live. Implementation should add a concise section that maps the public client attributes to resource groups and shows that request and parameter models are imported from `clockodo_api_lib.models`.

Alternatives considered:
- Assume users will infer naming from autocomplete: rejected because the current audience explicitly needs documentation to use the library.

## Risks / Trade-offs

- [A larger README can become harder to scan] -> Mitigation: keep sections short, task-oriented, and example-heavy rather than exhaustive.
- [Examples can drift from the public API over time] -> Mitigation: ground examples in existing tested entry points and verify them during implementation review.
- [A README-only approach may not scale forever] -> Mitigation: structure sections so they can be promoted into dedicated docs later if the library grows.

## Migration Plan

1. Restructure `README.md` so consumer usage appears as a coherent flow after installation.
2. Add sections for client construction, configuration options, resource discovery, typed models, and representative examples.
3. Keep contributor commands in a distinct development section so consumer guidance remains easy to scan.
4. Review the resulting commands and examples against the current public API before considering the change complete.

Rollback is straightforward: revert the documentation edits if the guidance proves confusing or inaccurate.

## Open Questions

- Should a later change add generated API reference tables from `ENDPOINT_INVENTORY`, or is a curated overview sufficient for now?
