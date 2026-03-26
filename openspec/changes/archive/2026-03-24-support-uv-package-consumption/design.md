## Context

The package already has a working `uv` build configuration and can produce a wheel and source distribution. The gap is not basic packaging support, but the lack of a clear downstream-consumer contract: the current README installation section is aimed at contributors and does not show how another project should add this library with `uv`.

This change needs to align three things:

- package metadata and artifacts that downstream projects can consume
- documentation that distinguishes consumer usage from contributor setup
- validation that proves the documented install flows continue to work

## Goals / Non-Goals

**Goals:**
- Define the supported `uv` installation workflows for downstream consumers.
- Keep the public package name `clockodo-api-lib` and import path `clockodo_api_lib` unchanged.
- Document consumer installation separately from local development setup.
- Add repeatable validation for the supported install paths in an isolated consumer environment.

**Non-Goals:**
- Publishing the package to PyPI in this change.
- Introducing a new build backend or restructuring the library package layout.
- Changing the public Python API surface of the Clockodo client.
- Supporting every possible distribution channel, such as direct Git installation, before the repo is ready to validate them.

## Decisions

### Keep the existing `uv_build` backend and refine the consumer contract around it

The current project already builds successfully with `uv_build`, so this change should not replace the backend. Instead, implementation should build on the existing packaging setup and add any missing metadata or validation needed for downstream consumption.

Alternatives considered:
- Switch build backends: rejected because there is no current build failure or backend limitation driving that change.
- Treat the package as local-development-only: rejected because the user explicitly wants to consume it from another project.

### Support only installation modes that can be documented and validated locally

The supported flows for this change should be:

- local path dependency via `uv add /path/to/clockodo-api-lib`
- editable local path dependency via `uv add --editable /path/to/clockodo-api-lib`
- built wheel installation via `uv add /path/to/dist/*.whl`

These flows cover both day-to-day local development and artifact-based consumption without depending on external publishing infrastructure.

Alternatives considered:
- Include Git URL installation now: rejected because this workspace is not set up to validate a Git-origin workflow end to end.
- Include PyPI installation now: rejected because publishing and release automation are outside the scope of this change.

### Split consumer documentation from contributor setup

The README should have a consumer-facing installation section that explains how another project adds the package, and a separate contributor/development section for `uv sync --group dev`, tests, and local maintenance tasks. This avoids conflating "use the library" with "work on the library."

Alternatives considered:
- Keep a single installation section: rejected because it preserves the current ambiguity.

### Validate consumption with isolated smoke tests or scripted commands

The implementation should add a repeatable validation path that creates a clean temporary `uv` project, installs the package using supported flows, and verifies a basic import such as `from clockodo_api_lib import ClockodoClient`. A lightweight scripted or documented smoke test is enough; the goal is to protect the install contract rather than retest all client behavior.

Alternatives considered:
- Rely on `uv build` alone: rejected because a successful build does not prove that downstream installation guidance is correct.
- Add a large integration test suite: rejected because it adds maintenance cost beyond the packaging contract this change needs.

## Risks / Trade-offs

- [Validation that spawns temporary consumer projects can be brittle] -> Mitigation: keep smoke checks minimal and focused on install plus import.
- [Documentation can drift from actual commands] -> Mitigation: tie validation commands to the same supported workflows documented in the README.
- [Limiting scope to local path and wheel flows leaves some consumer channels undocumented] -> Mitigation: state the supported scope explicitly and defer Git or registry publication to a later change.

## Migration Plan

1. Update package-facing documentation to define supported consumer installation modes.
2. Add any packaging metadata or helper commands required by those documented workflows.
3. Add a repeatable consumer-install validation flow against a clean temporary `uv` project.
4. Run packaging and consumer smoke validation before considering the change complete.

Rollback is low risk: documentation and validation can be reverted without affecting the client runtime or API behavior.

## Open Questions

- Should a later change add Git-based installation guidance once this repository has a validated remote source of truth?
- Do we want the consumer smoke validation wired into CI immediately, or kept as a documented release-readiness command first?
