# test_system.py - Simple test script for the Digital Asset Trading Platform

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5001"

def test_system():
    print("🚀 Testing Digital Asset Trading Platform...")
    
    # Test 1: Create wallets
    print("\n1. Creating test wallets...")
    users = [
        {"user_address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b", "initial_balance": 5000},
        {"user_address": "0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c", "initial_balance": 3000}
    ]
    
    for user in users:
        response = requests.post(f"{BASE_URL}/create_wallet", json=user)
        print(f"   Wallet {user['user_address'][:10]}... created: {response.status_code == 201}")
    
    # Test 2: Create digital asset
    print("\n2. Creating digital asset...")
    asset_data = {
        "asset_id": "test_nft_001",
        "name": "Test Digital Art",
        "description": "A test NFT for demonstration",
        "creator_address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
        "asset_type": "NFT",
        "metadata": {"test": True, "rarity": "Common"}
    }
    response = requests.post(f"{BASE_URL}/create_asset", json=asset_data)
    print(f"   Asset created: {response.status_code == 201}")
    
    # Test 3: List asset for sale
    print("\n3. Listing asset for sale...")
    listing_data = {
        "asset_id": "test_nft_001",
        "seller_address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
        "price": 1000
    }
    response = requests.post(f"{BASE_URL}/list_for_sale", json=listing_data)
    print(f"   Asset listed: {response.status_code == 201}")
    
    # Test 4: Check marketplace
    print("\n4. Checking marketplace...")
    response = requests.get(f"{BASE_URL}/marketplace")
    marketplace = response.json()
    print(f"   Active listings: {marketplace.get('total_listings', 0)}")
    
    # Test 5: Buy asset
    print("\n5. Buying asset...")
    buy_data = {
        "asset_id": "test_nft_001",
        "buyer_address": "0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c"
    }
    response = requests.post(f"{BASE_URL}/buy_asset", json=buy_data)
    print(f"   Asset purchased: {response.status_code == 200}")
    
    # Test 6: Check portfolio
    print("\n6. Checking buyer's portfolio...")
    response = requests.get(f"{BASE_URL}/portfolio/0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c")
    portfolio = response.json()
    owned_assets = len(portfolio.get('portfolio', {}).get('owned_assets', []))
    print(f"   Assets owned: {owned_assets}")
    
    # Test 7: Mine a block
    print("\n7. Mining a block...")
    response = requests.get(f"{BASE_URL}/mine")
    print(f"   Block mined: {response.status_code == 200}")
    
    # Test 8: Get stats
    print("\n8. Getting platform stats...")
    response = requests.get(f"{BASE_URL}/stats")
    stats = response.json()
    print(f"   Total users: {stats.get('total_users', 0)}")
    print(f"   Total assets: {stats.get('total_assets', 0)}")
    print(f"   Total blocks: {stats.get('total_blocks', 0)}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    try:
        test_system()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("   Make sure to run 'python digital-asset-trading.py' first!")
    except Exception as e:
        print(f"❌ Error: {e}")
