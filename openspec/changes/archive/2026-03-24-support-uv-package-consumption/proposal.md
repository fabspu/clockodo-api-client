## Why

The library already builds with `uv`, but the consumer story is still ambiguous. The current README installation section describes contributor setup, not how another project should depend on this package, which makes reuse harder than it needs to be.

## What Changes

- Define an explicit `uv` consumption contract for this library aimed at downstream projects rather than contributors.
- Document the supported installation flows for consumers, including local path usage, editable local development, and installation from a built wheel.
- Separate consumer installation guidance from contributor setup guidance in the package documentation.
- Add release-readiness validation that proves the documented consumer installation flows continue to work in an isolated environment.

## Capabilities

### New Capabilities
- `uv-package-consumption`: Defines how downstream Python projects can install and use the library with `uv`, including supported package formats, documentation expectations, and validation of those workflows.

### Modified Capabilities
- None.

## Impact

- Affects package-facing documentation in `README.md`.
- Affects packaging and validation workflow in `pyproject.toml` and related verification commands or tests.
- Clarifies the supported downstream installation story without changing the public Python import path or API surface.
