## Why

The library now has enough API surface to be useful, but the current README only shows installation and a short happy-path snippet. A new consumer still has to read source files and tests to understand how to configure the client, which resources are exposed, and how typed request and response models fit into normal usage.

## What Changes

- Add consumer-facing documentation that explains the package's public API and how to use it after installation.
- Document the required Clockodo authentication inputs and the optional client configuration values that affect requests.
- Add copy-paste examples for common usage patterns such as creating the client, listing resources, creating records, and traversing nested resource groups.
- Document how consumers discover typed request and response models and how endpoint groups map to client attributes.
- Clarify the difference between consumer documentation and contributor-focused development instructions.

## Capabilities

### New Capabilities
- `library-usage-documentation`: Defines the consumer documentation required for installing, configuring, and using the Clockodo client library without reading the implementation.

### Modified Capabilities
- None.

## Impact

- Affects package-facing documentation in `README.md`.
- May add supporting examples or documentation-oriented verification to keep usage guidance aligned with the public API.
- Does not change the package name, import path, or runtime client behavior.
