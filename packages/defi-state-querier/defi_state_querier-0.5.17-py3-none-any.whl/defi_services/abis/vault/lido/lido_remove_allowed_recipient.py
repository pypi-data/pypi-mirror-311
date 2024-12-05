import json

LIDO_REMOVE_ALLOWED_RECIPIENT_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_trustedCaller",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_allowedRecipientsRegistry",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "allowedRecipientsRegistry",
    "outputs": [
      {
        "internalType": "contract AllowedRecipientsRegistry",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_creator",
        "type": "address"
      },
      {
        "internalType": "bytes",
        "name": "_evmScriptCallData",
        "type": "bytes"
      }
    ],
    "name": "createEVMScript",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes",
        "name": "_evmScriptCallData",
        "type": "bytes"
      }
    ],
    "name": "decodeEVMScriptCallData",
    "outputs": [
      {
        "internalType": "address",
        "name": "recipientAddress",
        "type": "address"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "trustedCaller",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
''')