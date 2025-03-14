class Encoder:
    def __init__(self, block_size=1024, redundancy=2):
        self.block_size = block_size
        self.redundancy = redundancy
        self.num_fragments = redundancy + 1
    
    def encode(self, data):
        """
        Encode data into multiple fragments with redundancy.
        Simple implementation using replication with added markers.
        """
        fragments = []
        
        # Create the main fragment (original data)
        fragments.append(f"FRAG0:{data}")
        
        # Create redundant fragments
        for i in range(1, self.num_fragments):
            fragments.append(f"FRAG{i}:{data}")
        
        return fragments

    def _apply_error_correction(self, fragment):
        return fragment  # This should return the encoded fragment

    def get_coded_size(self):
        return self.block_size + self.redundancy

    def decode(self, coded_fragments):
        original_data = b''.join(coded_fragments)
        return original_data