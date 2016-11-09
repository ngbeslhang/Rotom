# Extensions
## Database wrapper
### Specs
- `required: list` - A list of required module(s)' name which will be used to import them dynamically using `importlib` to the bot.
- The wrapper will need to handle the database-specific exceptions inside itself.
- `DB: class` - The main class for a database wrapper
  - `__init__()`
    - Method 1
      - Requires `host: str`, `port: str`, `name: str`
      - Optional `username: str`, `password: str`
      - If not server based, self._server must be None
      - self._db for database itself
  - `insert()` (Method undecided)
    - Method 1 (Bias towards document store databases)
      - Accepts dict + Discord object (server, channel, user and their variants)
      - (Depends) flatten the dict
      - Insert the result(s) into database using Discord object as indicator of where to insert
    - Method 2 (Bias towards key-value store databases) (preferred)
      - Accepts 1-key dict/an iterable of 1-key dicts + Discord object
        - Use `:` inside key string to indicate subdicts 
          - e.g. music:tag:AAA or settings:disable:music)
      - (Depends) If they key was separated, create a dict out of it
      - Insert the result(s) into database using Discord object as indicator of where to insert
  - `remove()` (Method undecided)
    - Methods are same as `insert()` except it search and removes instead
  - `find()` (Method undecided)
    - Methods are same as `insert()` it search and returns a dict of matching kv instead
