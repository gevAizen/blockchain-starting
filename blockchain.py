#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   Create a blockchain

"""
Created on Sat Mar 19 13:27:27 2022

@author: gev
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify

#   PART 1 - Building a Blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
        
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    #   Proof of work function: the "Nonce" code
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #   Defining our puzzle problem
            #   First step - defining the function to run
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #   Second step - defining the condition the output of the function must validate (leading zeros)
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #   hash function: it is all [the data in] the block that is encoded in order to create a hash code
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self, chain):
        #   start getting the first block of the chain
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            #   get the current block
            current_block = chain[block_index]
            #   check if the current block's "previous_hash" field is equal to his previous block's hash code
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            #   get the prooves
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            #   check if the current block's proof validate our condition
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            block_index += 1
        return True

#   PART 2 - Mining our Blockchain

# Creating a Web App - 500 Internal Server Error
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#   Creating a Blockchain
blockchain = Blockchain()

#   Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    #   creating a new block
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    new_proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    new_block = blockchain.create_block(new_proof, previous_hash)
    new_hash = blockchain.hash(new_block)
    
    #   creation an http response
    response = {
        'message': 'Congratulations, ou just mined a block!',
        'index': new_block['index'],
        'timestamp': new_block['timestamp'],
        'proof': new_block['proof'],
        'hash': new_hash,
        'previous_hash': new_block['previous_hash']
    }
    return jsonify(response), 200

#   Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

#   Checking if the blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    response = {'isValid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200

#   Running the app
app.run(host = '0.0.0.0', port = 5000)





