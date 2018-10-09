from json import load, dump, JSONDecodeError


class Persistence:
    def load(self):
        raise NotImplementedError()

    def store(self):
        raise NotImplementedError()


class DiskPersistence(Persistence):
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename) as storage:
                return load(storage)
        except (OSError, JSONDecodeError):
            return None

    def store(self, data):
        with open(self.filename, "w") as storage:
            dump(data, storage, indent=2)
