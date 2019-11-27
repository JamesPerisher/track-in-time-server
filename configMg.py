import json

class configManager():
    def __init__(self, file="config.json"):
        self.file = file
        self.data = {}

        self.load()

    def _load(self):
        try:
            with open(self.file, "r") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            with open(self.file, "a") as f:
                f.write('{"_authors": ["PaulN07 - https://github.com/JamesPerisher", "JKook - https://github.com/JKookaburra"]}')

    def load(self):
        self.data = self._load()
        self.data = {} if self.data == None else self.data

    def save(self):
        with open(self.file, "w") as f:
            f.write(json.dumps(self.data))

    def get(self):
        return self.data

    def update(self):
        self.data.update(self._load())

        self.save()

    def set(self, data):
        self.data = data
        self.save()


if __name__ == '__main__':
    c = configManager()
    c.update()


    c.get()["a"] = "test"
