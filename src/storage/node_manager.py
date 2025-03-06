class NodeManager:
    def __init__(self):
        self.nodes = []

    def add_node(self, node_address):
        if node_address not in self.nodes:
            self.nodes.append(node_address)

    def remove_node(self, node_address):
        if node_address in self.nodes:
            self.nodes.remove(node_address)

    def get_nodes(self):
        return self.nodes

    def communicate_with_node(self, node_address, message):
        if node_address in self.nodes:
            # Placeholder for communication logic
            return f"Message sent to {node_address}: {message}"
        else:
            return f"Node {node_address} not found in the network."