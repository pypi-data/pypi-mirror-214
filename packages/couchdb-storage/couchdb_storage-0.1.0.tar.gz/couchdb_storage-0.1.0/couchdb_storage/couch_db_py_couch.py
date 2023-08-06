import pycouchdb


class CouchDbStorage(object):
    def __init__(self, server, username, password):
        server_url = f'http://{username}:{password}@{server}:5984/'
        self.server = pycouchdb.Server(server_url)

    def get_db(self, db_name):
        try:
            self.server.create(db_name)
        except:
            pass
        return self.server.database(db_name)
    
    def get_timestamp(self):
        return time.time()
