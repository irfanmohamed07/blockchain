# digital-asset-trading.py

import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_cors import CORS

class DigitalAssetTradingBlockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.users = {}  # Store user wallets and balances
        self.assets = {}  # Store digital assets (NFTs, tokens, etc.)
        self.marketplace = {}  # Store active marketplace listings
        
        # Initialize with some base currency for the system
        self.base_currency = "DAT"  # Digital Asset Token
        
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def create_user_wallet(self, user_address, initial_balance=1000):
        """Create a new user wallet with initial balance"""
        if user_address not in self.users:
            self.users[user_address] = {
                'address': user_address,
                'balance': initial_balance,
                'assets_owned': [],
                'created_at': time()
            }
            return True
        return False

    def create_digital_asset(self, asset_id, name, description, creator_address, asset_type="NFT", metadata=None):
        """Create a new digital asset (NFT, Token, etc.)"""
        if asset_id not in self.assets and creator_address in self.users:
            self.assets[asset_id] = {
                'id': asset_id,
                'name': name,
                'description': description,
                'creator': creator_address,
                'current_owner': creator_address,
                'asset_type': asset_type,
                'metadata': metadata or {},
                'created_at': time(),
                'transaction_history': []
            }
            
            # Add to creator's owned assets
            self.users[creator_address]['assets_owned'].append(asset_id)
            
            # Record creation transaction
            self.current_transactions.append({
                'type': 'asset_creation',
                'asset_id': asset_id,
                'creator': creator_address,
                'timestamp': time()
            })
            
            return True
        return False

    def list_asset_for_sale(self, asset_id, seller_address, price):
        """List an asset for sale in the marketplace"""
        if (asset_id in self.assets and 
            self.assets[asset_id]['current_owner'] == seller_address and
            asset_id not in self.marketplace):
            
            self.marketplace[asset_id] = {
                'asset_id': asset_id,
                'seller': seller_address,
                'price': price,
                'listed_at': time(),
                'status': 'active'
            }
            return True
        return False

    def buy_asset(self, asset_id, buyer_address):
        """Buy an asset from the marketplace"""
        if (asset_id not in self.marketplace or 
            self.marketplace[asset_id]['status'] != 'active' or
            buyer_address not in self.users):
            return False, "Asset not available or buyer not found"
        
        listing = self.marketplace[asset_id]
        seller = listing['seller']
        price = listing['price']
        
        # Check if buyer has enough balance
        if self.users[buyer_address]['balance'] < price:
            return False, "Insufficient balance"
        
        # Execute the transaction
        # Transfer payment
        self.users[buyer_address]['balance'] -= price
        self.users[seller]['balance'] += price
        
        # Transfer asset ownership
        self.users[seller]['assets_owned'].remove(asset_id)
        self.users[buyer_address]['assets_owned'].append(asset_id)
        self.assets[asset_id]['current_owner'] = buyer_address
        
        # Record transaction history
        transaction_record = {
            'type': 'asset_purchase',
            'asset_id': asset_id,
            'from': seller,
            'to': buyer_address,
            'price': price,
            'timestamp': time()
        }
        
        self.assets[asset_id]['transaction_history'].append(transaction_record)
        self.current_transactions.append(transaction_record)
        
        # Remove from marketplace
        self.marketplace[asset_id]['status'] = 'sold'
        del self.marketplace[asset_id]
        
        return True, "Asset purchased successfully"

    def transfer_currency(self, from_address, to_address, amount):
        """Transfer currency between users"""
        if (from_address not in self.users or to_address not in self.users):
            return False, "User not found"
        
        if self.users[from_address]['balance'] < amount:
            return False, "Insufficient balance"
        
        # Execute transfer
        self.users[from_address]['balance'] -= amount
        self.users[to_address]['balance'] += amount
        
        # Record transaction
        self.current_transactions.append({
            'type': 'currency_transfer',
            'from': from_address,
            'to': to_address,
            'amount': amount,
            'timestamp': time()
        })
        
        return True, "Transfer completed successfully"

    def get_user_portfolio(self, user_address):
        """Get user's complete portfolio"""
        if user_address not in self.users:
            return None
        
        user = self.users[user_address]
        portfolio = {
            'user_info': user,
            'owned_assets': []
        }
        
        for asset_id in user['assets_owned']:
            if asset_id in self.assets:
                portfolio['owned_assets'].append(self.assets[asset_id])
        
        return portfolio

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# === Flask Setup ===
app = Flask(__name__)
CORS(app)
node_id = str(uuid4()).replace('-', '')
blockchain = DigitalAssetTradingBlockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Add mining reward transaction
    blockchain.current_transactions.append({
        'type': 'mining_reward',
        'miner': node_id,
        'reward': 10,  # 10 DAT tokens
        'timestamp': time()
    })

    block = blockchain.new_block(proof)

    return jsonify({
        'message': "New Block Mined",
        'block': block,
        'reward': '10 DAT tokens'
    }), 200

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    values = request.get_json()
    if 'user_address' not in values:
        return jsonify({'error': 'Missing user_address'}), 400
    
    initial_balance = values.get('initial_balance', 1000)
    success = blockchain.create_user_wallet(values['user_address'], initial_balance)
    
    if success:
        return jsonify({
            'message': 'Wallet created successfully',
            'address': values['user_address'],
            'initial_balance': initial_balance
        }), 201
    else:
        return jsonify({'error': 'Wallet already exists'}), 400

@app.route('/create_asset', methods=['POST'])
def create_asset():
    values = request.get_json()
    required = ['asset_id', 'name', 'description', 'creator_address']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    success = blockchain.create_digital_asset(
        values['asset_id'], values['name'], values['description'],
        values['creator_address'], values.get('asset_type', 'NFT'),
        values.get('metadata', {})
    )
    
    if success:
        return jsonify({'message': 'Digital asset created successfully'}), 201
    else:
        return jsonify({'error': 'Asset creation failed or creator not found'}), 400

@app.route('/list_for_sale', methods=['POST'])
def list_for_sale():
    values = request.get_json()
    required = ['asset_id', 'seller_address', 'price']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    success = blockchain.list_asset_for_sale(
        values['asset_id'], values['seller_address'], values['price']
    )
    
    if success:
        return jsonify({'message': 'Asset listed for sale successfully'}), 201
    else:
        return jsonify({'error': 'Failed to list asset (not owned or already listed)'}), 400

@app.route('/buy_asset', methods=['POST'])
def buy_asset():
    values = request.get_json()
    required = ['asset_id', 'buyer_address']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    success, message = blockchain.buy_asset(values['asset_id'], values['buyer_address'])
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@app.route('/transfer_currency', methods=['POST'])
def transfer_currency():
    values = request.get_json()
    required = ['from_address', 'to_address', 'amount']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    success, message = blockchain.transfer_currency(
        values['from_address'], values['to_address'], values['amount']
    )
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@app.route('/marketplace', methods=['GET'])
def get_marketplace():
    return jsonify({
        'marketplace': blockchain.marketplace,
        'total_listings': len(blockchain.marketplace)
    }), 200

@app.route('/assets', methods=['GET'])
def get_assets():
    return jsonify({
        'assets': blockchain.assets,
        'total_assets': len(blockchain.assets)
    }), 200

@app.route('/user/<user_address>', methods=['GET'])
def get_user_info(user_address):
    if user_address not in blockchain.users:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': blockchain.users[user_address]
    }), 200

@app.route('/portfolio/<user_address>', methods=['GET'])
def get_portfolio(user_address):
    portfolio = blockchain.get_user_portfolio(user_address)
    if portfolio is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'portfolio': portfolio}), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'total_users': len(blockchain.users),
        'total_assets': len(blockchain.assets),
        'active_listings': len(blockchain.marketplace),
        'total_blocks': len(blockchain.chain),
        'base_currency': blockchain.base_currency
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
