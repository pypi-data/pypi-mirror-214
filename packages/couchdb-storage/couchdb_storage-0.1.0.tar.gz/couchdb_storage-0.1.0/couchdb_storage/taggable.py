

class Taggable(object):
    TAG_ATTR_NAME = 'tags'

    def __init__(self, data, db):
        self.data = data
        self.is_changed = False
        self.db = db

    def get_tags(self):
        if self.TAG_ATTR_NAME in self.data:
            return self.data[self.TAG_ATTR_NAME]
        return []

    def append_tags(self, tags):
        current_tags = []
        if self.TAG_ATTR_NAME in self.data:
            current_tags = self.data[self.TAG_ATTR_NAME]
        current_tag_len = len(current_tags)
        current_tags.extend(tags)
        new_tags = set(current_tags)
        if len(new_tags) != current_tag_len:
            self.data[self.TAG_ATTR_NAME] = list(new_tags)
            self.is_changed = True

    def save(self):
        if self.is_changed:
            self.db.save(self.data)