import hashlib
from timeit import default_timer as timer
from datetime import timedelta

class ProofOfWork:
    
    Start = 1
    Zeros = 4
        
    def __init__(self, zeros=4):
        Zeros = zeros

    def run(self):
        self.Proof()

    def Proof(self):
            proof = 0
            while not self.ValidProof(self.Start, proof):
                proof += 1

            return proof

    def ValidProof(self, lastProof, proof):
        guess = f'{lastProof}{proof}'.encode()
        guessHash = hashlib.sha256(guess).hexdigest()
        print(proof, guessHash)
        return guessHash[:4] == "0" * self.Zeros


if __name__ == "__main__":
    start = timer()
    
    worker = ProofOfWork()
    worker.run()
    
    end = timer()
    print('Proof of work took: ', timedelta(seconds=end-start))
