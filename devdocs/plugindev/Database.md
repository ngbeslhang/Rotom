# Plugin Development: Database Plugin Specification

A database plugin is a 

## Specification

In order to ensure 100% compactibility amongst other non-database plugins, all database plugins **MUST** follow the specifications *exactly* without adding any new features.

- All database plugins' (file)names **MUST** start with `db_`

### Initialization (`__init()`)

- The plugin will grab configuration from `Bot.get_conf()`

### CRUD

#### `db.set()` (CREATE and UPDATE combined)

#### `db.get()` (READ)

#### `db.del()` (DELETE)
