# Digital Asset Trading Platform - Blockchain Implementation
> A comprehensive blockchain-based platform for trading digital assets, NFTs, and tokens

This is a sophisticated blockchain system that enables users to create, trade, and manage digital assets including NFTs, utility tokens, certificates, and more. Built with Python and Flask, it demonstrates key cryptocurrency concepts like wallets, transactions, marketplaces, and proof-of-work mining.

## Features

### Core Blockchain Features
- **Proof-of-Work Mining** - Secure block creation with mining rewards
- **Digital Wallets** - User accounts with balance tracking
- **Transaction History** - Complete audit trail of all activities
- **Decentralized Architecture** - No central authority required

### Digital Asset Management
- **Create Digital Assets** - NFTs, tokens, certificates, and more
- **Asset Ownership Tracking** - Immutable ownership records
- **Asset Metadata** - Rich information storage for each asset
- **Portfolio Management** - Complete user portfolio views

### Marketplace & Trading
- **Asset Marketplace** - List assets for sale
- **Secure Transactions** - Atomic buy/sell operations
- **Currency Transfers** - Send DAT tokens between users
- **Price Discovery** - Market-driven asset pricing

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/irfanmohamed07/DigitalAssetTrading-Blockchain.git
cd DigitalAssetTrading-Blockchain
```

### 2. Install dependencies
```bash 
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the application
```bash
python digital-asset-trading.py
```

The API server will start on `http://127.0.0.1:5001`

## API Usage Examples

### Create a User Wallet
```bash
curl -X POST http://127.0.0.1:5001/create_wallet \
-H "Content-Type: application/json" \
-d '{
  "user_address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
  "initial_balance": 5000
}'
```

### Create a Digital Asset (NFT)
```bash
curl -X POST http://127.0.0.1:5001/create_asset \
-H "Content-Type: application/json" \
-d '{
  "asset_id": "nft_001",
  "name": "Digital Art Masterpiece",
  "description": "A unique digital artwork",
  "creator_address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
  "asset_type": "NFT",
  "metadata": {
    "image_url": "https://example.com/art1.png",
    "artist": "CryptoArtist123",
    "rarity": "Legendary"
  }
}'
```

### List Asset for Sale
```bash
curl -X POST http://127.0.0.1:5001/list_for_sale \
-H "Content-Type: application/json" \
-d '{
  "asset_id": "nft_001",
  "seller_address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
  "price": 500
}'
```

### Buy an Asset
```bash
curl -X POST http://127.0.0.1:5001/buy_asset \
-H "Content-Type: application/json" \
-d '{
  "asset_id": "nft_001",
  "buyer_address": "0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c"
}'
```

### Transfer Currency
```bash
curl -X POST http://127.0.0.1:5001/transfer_currency \
-H "Content-Type: application/json" \
-d '{
  "from_address": "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
  "to_address": "0x2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c",
  "amount": 100
}'
```

## Monitoring & Analytics

### View Marketplace
```bash
curl http://127.0.0.1:5001/marketplace
```

### Check User Portfolio
```bash
curl http://127.0.0.1:5001/portfolio/0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b
```

### View All Assets
```bash
curl http://127.0.0.1:5001/assets
```

### Get Platform Statistics
```bash
curl http://127.0.0.1:5001/stats
```

### Mine a Block
```bash
curl http://127.0.0.1:5001/mine
```

### View Blockchain
```bash
curl http://127.0.0.1:5001/chain
```

## Asset Types Supported

- **NFTs** - Unique digital collectibles, art, trading cards
- **Tokens** - Utility tokens, game currencies, loyalty points  
- **Certificates** - Digital credentials, achievements, licenses
- **Custom Types** - Extensible system for new asset categories

## Technical Architecture

- **Backend**: Python Flask REST API
- **Blockchain**: Custom proof-of-work implementation
- **Storage**: In-memory (easily extensible to persistent storage)
- **Cryptography**: SHA-256 hashing for security
- **Currency**: DAT (Digital Asset Token) as base currency

## Sample Data

The `data/` directory contains sample users and digital assets to help you get started quickly:
- `sample_users.json` - Pre-configured user wallets
- `sample_digital_assets.json` - Example NFTs, tokens, and certificates

