import json

class Block:
    def __init__(self, index, timestamp, transactions, proof, prevHash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.prevHash = prevHash 

    def __str__(self):
        return json.dumps(self)