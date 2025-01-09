# Blockchain Smart Contract System

## 1. Starting the Blockchain Node

First, start your Flask server:

```bash
python main.py
```

The server will start on `http://localhost:5000`

## 2. Initial Blockchain Setup and Mining

### 2.1 Check the Initial Chain State

```bash
curl http://localhost:5000/chain
```

Response:

```json
{
  "chain": [
    {
      "index": 1,
      "previous_hash": 1,
      "proof": 100,
      "timestamp": 1704812400,
      "transactions": []
    }
  ],
  "length": 1
}
```

### 2.2 Mine Some Initial Blocks

Mine a few blocks to get the blockchain started:

```bash
curl http://localhost:5000/mine
```

Response:

```json
{
  "message": "The new block has been forged",
  "index": 2,
  "transactions": [
    {
      "sender": "0",
      "recipient": "node_identifier",
      "amount": 1
    }
  ],
  "proof": 35293,
  "previous_hash": "2a2b4b5c5b4c..."
}
```

## 3. Smart Contract Deployment and Usage

### 3.1 Deploy a Token Contract

```bash
curl -X POST http://localhost:5000/contracts/deploy \
-H "Content-Type: application/json" \
-d '{
    "owner": "user123",
    "type": "token",
    "params": {
        "initial_supply": 1000000
    }
}'
```

Response:

```json
{
  "message": "Contract deployed successfully",
  "address": "8f2e3c7b1a4d..." // Save this contract address
}
```

### 3.2 Check Contract State

```bash
curl http://localhost:5000/contracts/8f2e3c7b1a4d/state
```

Response:

```json
{
  "address": "8f2e3c7b1a4d",
  "owner": "user123",
  "state": {
    "balances": {},
    "total_supply": 1000000
  }
}
```

### 3.3 Execute Token Transfer

```bash
curl -X POST http://localhost:5000/contracts/8f2e3c7b1a4d/execute \
-H "Content-Type: application/json" \
-d '{
    "method": "transfer",
    "params": {
        "from": "user123",
        "to": "user456",
        "amount": 100
    }
}'
```

Response:

```json
{
  "message": "Contract executed successfully",
  "result": true
}
```

### 3.4 Check Balance

```bash
curl -X POST http://localhost:5000/contracts/8f2e3c7b1a4d/execute \
-H "Content-Type: application/json" \
-d '{
    "method": "balance_of",
    "params": {
        "address": "user456"
    }
}'
```

Response:

```json
{
  "message": "Contract executed successfully",
  "result": 100
}
```
