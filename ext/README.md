You should be ignoring this README.
***NOTE: THE IDEA OF MODULAR DATABASE WRAPPERS HAVE BEEN ABANDONED.***

# Extensions
## Database wrapper
### Specs
- `required: list` - A list of required module(s)' name which will be used to import them dynamically using `importlib` to the bot.
- The wrapper will need to handle the database-specific exceptions inside itself.
- `DB: class` - The main class for a database wrapper
  - `__init__()`
    - Requires `host: str`, `port: str`, `name: str`
    - Optional `username: str`, `password: str`
    - If not server based, self._server must be None
    - self._db for database itself
  - `insert()` (Method undecided)
    - Accepts non-nested dict + Discord object
    - Use `:` inside key string to indicate subdicts 
      - e.g. music:tag:AAA or settings:disable:music)
    - (Depends) If they key was separated, create a dict out of it
    - Insert the result(s) into database using Discord object as indicator of where to insert
  - `remove()` (Method undecided)
    - Methods are same as `insert()` except it search and removes instead
  - `find()` (Method undecided)
    - Methods are same as `insert()` it search and returns a dict of matching kv instead

'''
        # Setting up database
        try:
            self.log.info("[DB] Importing database wrapper...")
            db_temp = importlib.import_module("ext.db_{}".format(self.config[
                'db']['wrapper']))
            self.log.info("[DB] Success!")
            self.log.info("[DB] Attempting to connect to database...")

            self.log.info(
                "[DB] Importing required module(s) stated by database wrapper..."
            )

            for mod in db_temp.required:
                try:
                    importlib.import_module(mod)
                except ImportError:
                    self.log.error(
                        "[DB] Unable to import module {}! ".format(mod) +
                        "Please download the module either by pip or official sources."
                    )
                    sys.exit()

            self.db = db_temp.DB(
                self.config['db']['name'], self.config['db']['host'],
                self.config['db']['port'], self.config['db']['user'],
                self.config['db']['passwd'])

            del db_temp
        except ImportError:
            self.log.error(
                "[DB] Unable to find database wrapper with the given "
                "name in config file! Please double-check to make "
                "sure there's no typo or the database wrapper does exist.")
            sys.exit()
        except AttributeError:
            self.log.error("[DB] Unable to find connect()!")
            sys.exit()
'''