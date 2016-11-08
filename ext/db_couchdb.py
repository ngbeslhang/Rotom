"""
db_couchdb.py - CouchDB wrapper for Rotom
"""
import couchdb

required = ["couchdb"]

class DB:
    def __init__(self, host, port, name, ):
        self._db = "placeholder" # couchdb.Server