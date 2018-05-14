# Plugin Development: Database Plugin Specification

A database

## Domain-Specific Language

A SQL-like (both syntax and feature wise) DSL is designed right within `Bot.db()` to make it more developer-friendly. The full syntax is as follows:

```
<SET/GET/(DELETE/DEL)> type:key[.subkey] [value (only if GIVE is used)] [...] IN table_name 
[WHERE]
```

### Examples

```
SET id:1
    id:1.lang
    id:1.owner.id
    IN server
```

### Terminology

| DSL | SQL/Relation Database |
| --- | ---|
| Type | Column |
| `SET` | `CREATE`/`UPDATE` |

## Specification

In order to ensure 100% compactibility amongst other non-database plugins, all database plugins **MUST** follow the specifications *exactly* without adding any new features.

- All database plugins' (file)names **MUST** start with `db_`

### Initialization (`__init()`)

- The plugin will grab configuration from `Bot.get_conf()`

### CRUD