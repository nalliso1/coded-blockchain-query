class DistributedStore:
    def __init__(self):
        self.storage = {}

    def store_fragment(self, node_id, fragment):
        if node_id not in self.storage:
            self.storage[node_id] = []
        self.storage[node_id].append(fragment)

    def retrieve_fragments(self, node_id):
        return self.storage.get(node_id, [])

    def get_all_fragments(self):
        all_fragments = []
        for fragments in self.storage.values():
            all_fragments.extend(fragments)
        return all_fragments

    def remove_fragment(self, node_id, fragment):
        if node_id in self.storage:
            self.storage[node_id].remove(fragment)