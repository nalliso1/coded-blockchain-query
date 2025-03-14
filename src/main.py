from blockchain.chain import Blockchain
from coding.encoder import Encoder
from coding.decoder import Decoder
from indexing.amvsl import AMVSL
from indexing.range_query import RangeQuery
from storage.distributed_store import DistributedStore
from storage.node_manager import NodeManager
import random
import time
import pandas as pd
import json


def generate_sample_data(count=10, counter=0):
    """Generate sample key-value pairs for demonstration with zero-padded keys"""
    data = {}
    for i in range(count):
        x = counter+i
        key = f"{x:04d}"
        value = f"value_{random.randint(1000, 9999)}"
        data[key] = value
    return data

def load_data_from_csv(file_path, key_column=None, records_per_block=10):
    """Load data from CSV and organize it into blocks"""
    try:
        df = pd.read_csv(file_path)
        blocks_data = []
        
        # Process in batches for blocks
        for i in range(0, len(df), records_per_block):
            block_data = {}
            batch = df.iloc[i:i+records_per_block]
            
            for idx, row in batch.iterrows():
                if key_column:
                    key = f"{row[key_column]}"
                else:
                    key = f"{idx:04d}"  # Use row number as key if none specified
                
                # Store all columns as a dictionary
                block_data[key] = row.to_dict()
            
            blocks_data.append(block_data)
            
        return blocks_data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def main():
    # Initialize components
    blockchain = Blockchain()
    encoder = Encoder(block_size=1024, redundancy=2)
    decoder = Decoder(num_fragments=3, threshold=2)
    amvsl = AMVSL()
    range_query = RangeQuery(amvsl_index=amvsl) 
    node_manager = NodeManager(base_port=5000)
    distributed_store = DistributedStore(node_manager)

    print("Coded Blockchain Range Query Application Initialized.")
    
    # Load from CSV instead of generating data
    print("\n=== Loading data from CSV ===")
    csv_path = "src/data/students.csv"  # Updated path
    blocks_data = load_data_from_csv(csv_path, key_column="id")
    
    # Create blocks from CSV data batches
    print("\n=== Adding blocks to blockchain ===")
    for i, data in enumerate(blocks_data):
        print(f"Creating block {i} with {len(data)} records")
        block = blockchain.create_block(data)
    
    # Encode blocks and distribute fragments
    print("\n=== Encoding and distributing blocks ===")
    node_ids = node_manager.get_available_nodes()
    if not node_ids:
        print("No available nodes for distribution!")
        return
    
    for block in blockchain.get_blocks():
        print(f"Encoding block: {block.index}")
        # Use JSON instead of str() for data serialization
        data_str = json.dumps(block.data)
        fragments = encoder.encode(data_str)
        
        print(f"Distributing {len(fragments)} fragments across {len(node_ids)} nodes")
        for i, fragment in enumerate(fragments):
            node_id = node_ids[i % len(node_ids)]
            distributed_store.store(node_id, block.index, i, fragment)
    
    # Create secondary indices for columns to query
    amvsl.create_secondary_index("math.grade")
    amvsl.create_secondary_index("english.grade")
    
    # Build index from blockchain data
    print("\n=== Building indices ===")
    for block in blockchain.get_blocks():
        for key, value in block.data.items():
            amvsl.insert(key, value, block.index)
    
    # Example: Range query by math grade (3.0 to 5.0 range)
    print("\n=== Executing grade range query ===")
    grade_results = range_query.execute_by_column("math.grade", 9.0, 11.0)
    print(f"Students with math grades B+ to A+: {len(grade_results)}")
    
    # Extract unique block IDs from results
    unique_block_ids = set()
    for result in grade_results:
        if 'block_id' in result:
            unique_block_ids.add(result['block_id'])
    
    print(f"\n=== Found matching students in {len(unique_block_ids)} blocks ===")
    
    # Retrieve each block and display matching students
    for block_id in unique_block_ids:
        print(f"\nRetrieving data for block: {block_id}")
        
        # Get keys in this block
        keys_in_block = [result['key'] for result in grade_results 
                        if result.get('block_id') == block_id]
        print(f"Student IDs to retrieve: {keys_in_block}")
        
        # Retrieve fragments from nodes
        fragments = []
        for i in range(len(node_ids)):
            if len(fragments) < decoder.threshold:
                node_id = node_ids[i % len(node_ids)]
                print(f"Attempting to retrieve fragment {i} from node {node_id}...")
                fragment = distributed_store.retrieve(node_id, block_id, i)
                if fragment:
                    fragments.append(fragment)
                    print(f"Successfully retrieved fragment {i} from {node_id}")
        
        # Decode if we have enough fragments
        if len(fragments) >= decoder.threshold:
            recovered_data_str = decoder.decode(fragments)
            
            # Use JSON instead of ast.literal_eval for decoding
            recovered_data = json.loads(recovered_data_str)
            
            # Display information about students that match our query
            print("\nMatching student records:")
            for key in keys_in_block:
                if key in recovered_data:
                    student = recovered_data[key]
                    print(f"ID: {key}, Name: {student.get('name')}, Math Grade: {student.get('math.grade')}")
        else:
            print(f"Not enough fragments retrieved: {len(fragments)}/{decoder.threshold} required")

if __name__ == "__main__":
    main()