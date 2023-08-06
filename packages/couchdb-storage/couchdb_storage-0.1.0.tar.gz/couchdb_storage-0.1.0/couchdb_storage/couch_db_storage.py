import couchdb
import time


class CouchDbStorage(object):
    def __init__(self, server, username, password):
        server_url = f'http://{username}:{password}@{server}:5984/'
        self.server = couchdb.Server(server_url)

    def get_db(self, db_name):
        try:
            self.server.create(db_name)
        except:
            pass
        return self.server[db_name]
    
    def get_timestamp(self):
        return time.time()

    def simple_find(self, db, selector):
        offset = 0
        limit = 25
        while True:
            mongo = {
                'selector': selector,
                'skip': offset,
                'limit': limit
            }
            cnt = 0
            for i in db.find(mongo):
                cnt += 1
                yield i
            if cnt != limit:
                return
            offset += limit

