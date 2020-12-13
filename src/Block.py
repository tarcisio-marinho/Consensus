import json

class Block:
    def __init__(self, index, timestamp, transactions, proof, prevHash):
        self.Index = index
        self.Timestamp = timestamp
        self.Transactions = transactions
        self.Proof = proof
        self.PrevHash = prevHash 

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True)

if __name__ == "__main__":
    from time import time
    b = Block(5, time(), ['test', 'test2'], 42, 4)
    print(b)