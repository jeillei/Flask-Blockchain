# main.py

from uuid import uuid4
from flask import Flask, request, jsonify
from blockchain import Blockchain
from smart_contract import TokenContract
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
node_identifier = str(uuid4()).replace('-', '')

# Initializing blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # Here we make the proof of work algorithm work
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # rewarding the miner for his contribution. 0 specifies new coin has been mined
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # now create the new block and add it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    return jsonify({
        'message': 'The new block has been forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    # Checking if the required data is there or not
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # creating a new transaction
    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])
    return jsonify({
        'message': f'Transaction is scheduled to be added to Block No. {str(index)}'
    }), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200


@app.route('/contracts/deploy', methods=['POST'])
def deploy_contract():
    values = request.get_json()

    required = ['owner', 'type', 'params']
    if not all(k in values for k in required):
        return 'Missing values', 400

    contract_type = values['type']
    owner = values['owner']
    params = values['params']

    if contract_type == 'token':
        if 'initial_supply' not in params:
            return 'Missing initial_supply for token contract', 400
        contract = TokenContract(params['initial_supply'])
    else:
        return f'Unknown contract type: {contract_type}', 400

    address = blockchain.deploy_contract(contract, owner)

    return jsonify({
        'message': 'Contract deployed successfully',
        'address': address
    }), 201


@app.route('/contracts/<address>/execute', methods=['POST'])
def execute_contract(address):
    values = request.get_json()

    required = ['method', 'params']
    if not all(k in values for k in required):
        return 'Missing values', 400

    method = values['method']
    params = values['params']

    try:
        contract = blockchain.get_contract(address)
        if contract is None:
            return 'Contract not found', 404

        result = contract.execute(method, params)

        return jsonify({
            'message': 'Contract executed successfully',
            'result': result
        }), 200
    except Exception as e:
        return str(e), 400


@app.route('/contracts/<address>/state', methods=['GET'])
def get_contract_state(address):
    contract = blockchain.get_contract(address)
    if contract is None:
        return 'Contract not found', 404

    return jsonify({
        'address': address,
        'owner': contract.owner,
        'state': contract.get_state()
    }), 200


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the Blockchain API!",
        "endpoints": {
            "/mine": "Mine a new block",
            "/transactions/new": "Add a new transaction",
            "/chain": "View the full blockchain",
            "/contracts/deploy": "Deploy a new smart contract. Specify 'owner', 'type', and 'params' in the request body.",
            "/contracts/<address>/execute": "Execute a method on a smart contract. Provide 'method' and 'params' in the request body.",
            "/contracts/<address>/state": "Get the current state of a smart contract by its address."
        }
    }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
