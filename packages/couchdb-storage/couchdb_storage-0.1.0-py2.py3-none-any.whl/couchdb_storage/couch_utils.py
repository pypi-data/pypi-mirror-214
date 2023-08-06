from .couch_db_storage import CouchDbStorage
import pprint


class CouchUtils(object):
    def __init__(self, server, username, password, db_name, data_type):
        self.server = CouchDbStorage(server, username, password)
        self.db = self.server.get_db(db_name)
        self.data_type = data_type
        self.data = []
        self.not_saved = []

    def load_all(self):
        skip = 0
        limit = 1000

        while True:
            mongo = {
                'selector': {
                    'type': self.data_type
                },
                'skip': skip,
                'limit': limit
            }
            result = self.db.find(mongo)
            cnt = 0
            print(dir(result))
            for row in result:
                pprint.pprint(row)
                cnt = cnt + 1
                self.data.append(row)
                # break
            skip = skip + limit
            # print(skip, skip+cnt)

            if cnt < limit:
                break

    def append(self, document):
        self.not_saved.append(document)
        if len(self.not_saved) >= 100:
            self.db.update(self.not_saved)
            self.not_saved = []
