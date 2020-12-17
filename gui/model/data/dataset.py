class Dataset:
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path

    def __eq__(self, other):
        return self.name == other.name and self.path == other.path

    def get_str(self):
        return ';'.join([self.name, self.path])
