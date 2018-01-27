class Group(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __repr__(self):
        return "<" + self.name + " #" + self.id + ">"