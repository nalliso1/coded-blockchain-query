class NodeManager:
    def __init__(self):
        self.nodes = []
        # Add some default nodes for testing
        self.add_node("node_1")
        self.add_node("node_2")
        self.add_node("node_3")

    def add_node(self, node_address):
        if node_address not in self.nodes:
            self.nodes.append(node_address)

    def remove_node(self, node_address):
        if node_address in self.nodes:
            self.nodes.remove(node_address)

    def get_nodes(self):
        return self.nodes
    
    def get_available_nodes(self):
        """Get the currently available nodes"""
        # In a real system, this would check node availability
        return self.nodes

    def communicate_with_node(self, node_address, message):
        if node_address in self.nodes:
            # Placeholder for communication logic
            return f"Message sent to {node_address}: {message}"
        else:
            return f"Node {node_address} not found in the network."