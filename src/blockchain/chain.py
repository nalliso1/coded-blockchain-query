class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': self.get_current_timestamp(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def get_current_timestamp(self):
        from time import time
        return time()

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        import hashlib
        block_string = str(block).encode()
        return hashlib.sha256(block_string).hexdigest()

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            previous = self.chain[i - 1]
            current = self.chain[i]
            if current['previous_hash'] != self.hash(previous):
                return False
            if not self.valid_proof(previous['proof'], current['proof']):
                return False
        return True

    @staticmethod
    def valid_proof(previous_proof, current_proof):
        guess = f'{previous_proof}{current_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Example difficulty level