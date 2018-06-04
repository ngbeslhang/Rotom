# Plugin Development: Library Plugin

A library plugin is a plugin that won't run on its own but provide features for other plugins to use, which is basically the same as a programming library.

Rotom is coded in a way that it will only *and only* import a library plugin if another non_library plugin specifies it as a requisite. Rotom **WILL NOT** import a library plugin by itself and will ignore it.

## Specifications

- **MUST NOT** include `setup()` at module-level.
- All library plugins' (file)names **MUST** start with `lib_`
