
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests

from Block import Block

class BlockChain:

    def __init__(self):
        self.currentTransactions = []
        self.Chain = []
        self.Nodes = set()
        
        # Create the genesis block
        self.NewBlock(prevHash='1', proof=100)


    def RegisterNode(self, address):

        parsedUrl = urlparse(address)
        
        if parsedUrl.netloc:
            self.Nodes.add(parsedUrl.netloc)

        elif parsedUrl.path:
            self.Nodes.add(parsedUrl.path)

        else:
            raise ValueError('malformated URL')
    

    def NewBlock(self, proof, prevHash):

        block = Block(len(self.Chain) + 1,
         time(),
         self.currentTransactions, 
         proof, 
         prevHash or self.hash(self.Chain[-1]))

        # Reset the current list of transactions
        self.currentTransactions = []

        self.Chain.append(block)

        return block

if __name__ == "__main__":
    chain = BlockChain()
