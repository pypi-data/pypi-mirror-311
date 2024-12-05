import json

LIDO_MEV_BOOST_RELAY_ALLOWED_LIST = json.loads('''
[
  {
    "name": "RelayAdded",
    "inputs": [
      {
        "name": "uri_hash",
        "type": "string",
        "indexed": true
      },
      {
        "name": "relay",
        "type": "tuple",
        "components": [
          {
            "name": "uri",
            "type": "string"
          },
          {
            "name": "operator",
            "type": "string"
          },
          {
            "name": "is_mandatory",
            "type": "bool"
          },
          {
            "name": "description",
            "type": "string"
          }
        ],
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "RelayRemoved",
    "inputs": [
      {
        "name": "uri_hash",
        "type": "string",
        "indexed": true
      },
      {
        "name": "uri",
        "type": "string",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "AllowedListUpdated",
    "inputs": [
      {
        "name": "allowed_list_version",
        "type": "uint256",
        "indexed": true
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "OwnerChanged",
    "inputs": [
      {
        "name": "new_owner",
        "type": "address",
        "indexed": true
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "ManagerChanged",
    "inputs": [
      {
        "name": "new_manager",
        "type": "address",
        "indexed": true
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "ERC20Recovered",
    "inputs": [
      {
        "name": "token",
        "type": "address",
        "indexed": true
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": false
      },
      {
        "name": "recipient",
        "type": "address",
        "indexed": true
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "stateMutability": "nonpayable",
    "type": "constructor",
    "inputs": [
      {
        "name": "owner",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "get_relays_amount",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "get_owner",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "get_manager",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "get_relays",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "tuple[]",
        "components": [
          {
            "name": "uri",
            "type": "string"
          },
          {
            "name": "operator",
            "type": "string"
          },
          {
            "name": "is_mandatory",
            "type": "bool"
          },
          {
            "name": "description",
            "type": "string"
          }
        ]
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "get_relay_by_uri",
    "inputs": [
      {
        "name": "relay_uri",
        "type": "string"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "tuple",
        "components": [
          {
            "name": "uri",
            "type": "string"
          },
          {
            "name": "operator",
            "type": "string"
          },
          {
            "name": "is_mandatory",
            "type": "bool"
          },
          {
            "name": "description",
            "type": "string"
          }
        ]
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "get_allowed_list_version",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ]
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "add_relay",
    "inputs": [
      {
        "name": "uri",
        "type": "string"
      },
      {
        "name": "operator",
        "type": "string"
      },
      {
        "name": "is_mandatory",
        "type": "bool"
      },
      {
        "name": "description",
        "type": "string"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "remove_relay",
    "inputs": [
      {
        "name": "uri",
        "type": "string"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "change_owner",
    "inputs": [
      {
        "name": "owner",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "set_manager",
    "inputs": [
      {
        "name": "manager",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "dismiss_manager",
    "inputs": [],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "recover_erc20",
    "inputs": [
      {
        "name": "token",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "recipient",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "fallback"
  }
]
''')