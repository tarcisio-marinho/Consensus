import json

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.Sender = sender 
        self.Recipient = recipient 
        self.Amount = amount 

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True)

if __name__ == "__main__":
    t = Transaction('tarcisio', 'satoshi', 5000)

    print(t)