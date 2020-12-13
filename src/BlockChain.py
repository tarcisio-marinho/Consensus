
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests

from Block import Block
from Transaction import Transaction

class BlockChain:

    def __init__(self, zeros=4):
        self.currentTransactions = []
        self.Chain = []
        self.Nodes = set()
        self.Zeros = zeros
        self.ChainEndpoint = 'chain'

        # Create the genesis block
        self.NewBlock(prevHash='1', proof=100)


    def ProofOfWork(self, lastBlock):

        lastProof = LastBlock.Proof
        lastHash = self.Hash(lastBlock)

        proof = 0
        while not self.ValidProof(lastProof, proof, lastHash):
            proof += 1

        return proof


    def ValidProof(lastProof, proof, lastHash):
        guess = f'{lastProof}{proof}{lastHash}'.encode()
        guessHash = hashlib.sha256(guess).hexdigest()
        return guessHash[:self.Zeros] == "0" * self.Zeros


    def RegisterNode(self, address):

        parsedUrl = urlparse(address)
        
        if parsedUrl.netloc:
            self.Nodes.add(parsedUrl.netloc)

        elif parsedUrl.path:
            self.Nodes.add(parsedUrl.path)

        else:
            raise ValueError('malformated URL')
    

    def NewBlock(self, prevHash, proof):

        block = Block(len(self.Chain) + 1,
         time(),
         self.currentTransactions, 
         proof, 
         prevHash or self.hash(self.LastBlock))

        # Reset the current list of transactions
        self.currentTransactions = []

        self.Chain.append(block)

        return block


    def NewTransaction(self, sender, recipient, amount):
        self.currentTransactions.append(
            Transaction(sender=sender,
             recipient=recipient,
              amount=amount)
        )

        return self.LastBlock.Index + 1


    @property
    def LastBlock(self):
        return self.Chain[-1]


    @staticmethod
    def Hash(block):
        return hashlib.sha256(str(block).encode()).hexdigest()



    def ResolveConflicts(self):
        # Return true if consensus achieved by update, otherwise, false
        newChain = None

        maxLen = len(self.Chain)

        for node in self.Nodes:
            response = requests.get(f'https://{node}/{self.ChainEndpoint}')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > maxLen and self.ValidProof(chain):
                    maxLen = length
                    newChain = chain

        if newChain:
            self.Chain = newChain
            return True

        return False


    def ValidChain(self, chain):

        lastBlock = Chain[0]
        currIndex = 1

        while currIndex < len(chain):
            block = chain[currIndex]
            print(f'{lastBlock}')
            print(f'{block}')
            print("\n-----------\n")
            # Check if the hash is correct
            lastBlockHash = self.hash(lastBlock)
            if block['previous_hash'] != lastBlockHash:
                return False

            # Check if Proof of Work is correct
            if not self.ValidProof(lastBlock.Proof, block.Proof, lastBlockHash):
                return False

            lastBlock = block
            currIndex += 1

        return True



if __name__ == "__main__":
    from time import time

    chain = BlockChain(4)
    
    block = Block(index=3, timestamp=time(), 
    transactions=[1243], proof=42, prevHash=2)

    hash = chain.Hash(block)

    print(hash)