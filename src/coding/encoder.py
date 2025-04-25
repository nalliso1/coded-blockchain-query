import zfec
import math

class Encoder:
    def __init__(self, redundancy=2):
        self.data_shares = 3  #Number of data fragments
        self.redundancy = redundancy
        self.total_shares = self.data_shares + self.redundancy
        
    def encode(self, block_serialized):
        if isinstance(block_serialized, str):
            data_bytes = block_serialized.encode('utf-8')
        else:
            data_bytes = block_serialized
            
        chunk_size = math.ceil(len(data_bytes) / self.data_shares)
        
        padded_size = chunk_size * self.data_shares
        padding_size = padded_size - len(data_bytes)
        data_bytes += b'\x00' * padding_size
        
        chunks = []
        for i in range(self.data_shares):
            start = i * chunk_size
            end = start + chunk_size
            chunks.append(data_bytes[start:end])
        
        encoder = zfec.Encoder(self.data_shares, self.total_shares)
        
        shares = encoder.encode(chunks)
        
        fragments = []
        for i, share in enumerate(shares):
            metadata = f"{i},{self.data_shares},{self.total_shares},{padding_size},{chunk_size}"
            fragments.append(f"SHARE{i}:{metadata}:{share.hex()}")
            
        return fragments