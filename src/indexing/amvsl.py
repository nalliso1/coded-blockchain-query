class AMVSL:
    def __init__(self):
        self.index = {}

    def insert(self, key, value):
        if key not in self.index:
            self.index[key] = []
        self.index[key].append(value)

    def update(self, key, old_value, new_value):
        if key in self.index and old_value in self.index[key]:
            index = self.index[key].index(old_value)
            self.index[key][index] = new_value

    def retrieve(self, key):
        return self.index.get(key, [])

    def range_query(self, start_key, end_key):
        result = []
        for key in sorted(self.index.keys()):
            if start_key <= key <= end_key:
                result.extend(self.index[key])
        return result