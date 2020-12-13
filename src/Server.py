from flask import Flask, jsonify, request
from uuid import uuid4

from BlockChain import BlockChain
from Block import Block

app = Flask("Consensus blockchain miner")

nodeId = str(uuid4()).replace('-', '')

blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    lastBlock = blockchain.LastBlock
    proof = blockchain.ProofOfWork(lastBlock)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.NewTransaction(
        sender="0",
        recipient=nodeId,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    prevHash = blockchain.Hash(lastBlock)
    block = blockchain.NewBlock(prevHash, proof)

    response = {
        'message': "New block created",
        'index': block.Index,
        'transactions': block.Transactions,
        'proof': block.Proof,
        'prevHash': block.PrevHash,
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def NewTransaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'invalid payload ! required fields: sender, recipient, amount.', 400

    index = blockchain.NewTransaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block at index: {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def FullChain():
    response = {
        'chain': blockchain.Chain,
        'length': len(blockchain.Chain),
    }

    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def RegisterNodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.RegisterNode(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def Consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }

    else:
        response = {
            'message': 'Our chain is at consensus',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
