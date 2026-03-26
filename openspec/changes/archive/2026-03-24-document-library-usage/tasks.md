## 1. Restructure the consumer guide

- [x] 1.1 Rework `README.md` so consumer installation and usage guidance are clearly separated from contributor development commands
- [x] 1.2 Add a client setup section that documents the required authentication inputs and the optional `base_url`, `timeout`, and `language` settings

## 2. Document the public API surface

- [x] 2.1 Add a concise overview of the public client resource groups, including representative top-level attributes and nested groups such as `user_access`, `aggregates`, and `work_times.change_requests`
- [x] 2.2 Add guidance showing that request and parameter models come from `clockodo_api_lib.models` and are passed directly into client calls

## 3. Add representative usage workflows

- [x] 3.1 Add a copy-paste example that constructs `ClockodoClient` and performs a typed list request, including how to read returned items or pagination data
- [x] 3.2 Add at least one example covering a create workflow or nested-resource call using the current public API

## 4. Verify documentation accuracy

- [x] 4.1 Review all documented imports, client attributes, and example calls against the current public API in `src/clockodo_api_lib`
- [x] 4.2 Run the relevant project validation needed to confirm the documentation update did not introduce inconsistent commands or broken examples
