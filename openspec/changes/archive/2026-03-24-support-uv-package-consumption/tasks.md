## 1. Package consumption contract

- [x] 1.1 Review the current packaging metadata and keep or add only the fields needed to support the documented downstream `uv` installation contract
- [x] 1.2 Confirm the supported consumer workflows for this change are local path, editable local path, and built-wheel installation

## 2. Consumer-facing documentation

- [x] 2.1 Update `README.md` to separate downstream package installation from contributor setup
- [x] 2.2 Add copy-paste examples for `uv add /path/to/clockodo-api-lib`, `uv add --editable /path/to/clockodo-api-lib`, and installation from a built wheel
- [x] 2.3 Add a minimal consumer usage example that imports `ClockodoClient` from `clockodo_api_lib`

## 3. Validation

- [x] 3.1 Add a repeatable validation flow that builds the package and installs the wheel into an isolated temporary `uv` consumer project
- [x] 3.2 Add a repeatable validation flow that installs the repository as a local path dependency into an isolated temporary `uv` consumer project
- [x] 3.3 Run the packaging and consumer-install validation steps and fix any gaps uncovered by those checks
