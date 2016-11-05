# Extensions
## Database wrapper
### Specs
- `insert()` (Method undecided)
  - Method 1 (Bias towards document store databases)
    - Accepts dict + Discord object (server, channel, user and their variants)
    - (Depends) flatten the dict
    - Insert the result(s) into database using Discord object as indicator of where to insert
  - Method 2 (Bias towards key-value store databases)
    - Accepts 1-key dict/an iterable of 1-key dicts + Discord object
      - Use `:` inside key string to indicate subdicts 
        - e.g. music:tag:AAA or settings:disable:music)
    - (Depends) If they key was separated, create a dict out of it
    - Insert the result(s) into database using Discord object as indicator of where to insert
- `find()` (Method undecided)
