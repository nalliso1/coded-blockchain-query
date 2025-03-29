import zfec

class Decoder:
    def __init__(self, num_fragments=5, threshold=3):
        self.num_fragments = num_fragments
        self.threshold = threshold
        
    def decode(self, fragments):
        if len(fragments) < self.threshold:
            raise ValueError(f"Not enough fragments: {len(fragments)}/{self.threshold} required")
            
        shares = []
        share_nums = []
        k = None
        m = None
        padding_size = None
        chunk_size = None
        
        for fragment in fragments:
            if not fragment.startswith("SHARE"):
                continue
                
            parts = fragment.split(":", 2)
            if len(parts) != 3:
                continue
                
            meta_parts = parts[1].split(",")
            if len(meta_parts) != 5:
                continue
                
            share_num = int(meta_parts[0])
            k_val = int(meta_parts[1])
            m_val = int(meta_parts[2])
            padding = int(meta_parts[3])
            chunk_sz = int(meta_parts[4])
            
            if k is None:
                k = k_val
                m = m_val
                padding_size = padding
                chunk_size = chunk_sz
            elif k != k_val or m != m_val or padding_size != padding or chunk_size != chunk_sz:
                continue 
                
            try:
                share_data = bytes.fromhex(parts[2])
                shares.append(share_data)
                share_nums.append(share_num)
            except ValueError:
                continue
                
        if len(shares) < k:
            raise ValueError(f"Not enough valid shares: {len(shares)}/{k} required")
            
        decoder = zfec.Decoder(k, m)
        chunks = decoder.decode(shares, share_nums)
        
        decoded_data = b''.join(chunks)
        
        if padding_size > 0:
            decoded_data = decoded_data[:-padding_size]
            
        return decoded_data.decode('utf-8')
        
    def verify_data(self, original_data, decoded_data):
        return original_data == decoded_data