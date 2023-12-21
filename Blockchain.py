# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 20:15:36 2023

@author: Kinzang
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    
    def get_previous_block(self):
        return self.chain[-1]
    
   
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(previous_proof**2 - new_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1    
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
   
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            hash_operation = hashlib.sha256(str(previous_block['proof']**2 - block['proof']**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True
    
    
    
# create flask app    
app = Flask(__name__)

# create a block chain
blockchain = Blockchain()

# Getting full blockchain
@app.route('/', methods=['GET'])
def get_blockchain():
    response = {'length': len(blockchain.chain),
                'blockchain': blockchain.chain}
    return jsonify(response), 200


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you have mined a bew block',
                'block': block}
    return jsonify(response), 200    

# Getting full blockchain
@app.route('/is_valid_blockchain', methods=['GET'])
def is_valid_blockchain():
    valid_blockchain = blockchain.is_chain_valid(blockchain.chain)
    if valid_blockchain:
        message = 'All good. Blockchain is valid'
    else:
        message = 'We have a problem. Blockchain is not valid'
    response = {'message': message}
    return jsonify(response), 200

# Running the app
app.run(host='0.0.0.0', port=5000)