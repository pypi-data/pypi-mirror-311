import json

LIDO_ANCHOR_VAULT_ABI = json.loads('''
[
  {
    "name": "Deposited",
    "inputs": [
      {
        "name": "sender",
        "type": "address",
        "indexed": true
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": false
      },
      {
        "name": "terra_address",
        "type": "bytes32",
        "indexed": false
      },
      {
        "name": "beth_amount_received",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "Withdrawn",
    "inputs": [
      {
        "name": "recipient",
        "type": "address",
        "indexed": true
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": false
      },
      {
        "name": "steth_amount_received",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "Refunded",
    "inputs": [
      {
        "name": "recipient",
        "type": "address",
        "indexed": true
      },
      {
        "name": "beth_amount",
        "type": "uint256",
        "indexed": false
      },
      {
        "name": "steth_amount",
        "type": "uint256",
        "indexed": false
      },
      {
        "name": "comment",
        "type": "string",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "RefundedBethBurned",
    "inputs": [
      {
        "name": "beth_amount",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "RewardsCollected",
    "inputs": [
      {
        "name": "steth_amount",
        "type": "uint256",
        "indexed": false
      },
      {
        "name": "ust_amount",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "AdminChanged",
    "inputs": [
      {
        "name": "new_admin",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "EmergencyAdminChanged",
    "inputs": [
      {
        "name": "new_emergency_admin",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "BridgeConnectorUpdated",
    "inputs": [
      {
        "name": "bridge_connector",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "RewardsLiquidatorUpdated",
    "inputs": [
      {
        "name": "rewards_liquidator",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "InsuranceConnectorUpdated",
    "inputs": [
      {
        "name": "insurance_connector",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "LiquidationConfigUpdated",
    "inputs": [
      {
        "name": "liquidations_admin",
        "type": "address",
        "indexed": false
      },
      {
        "name": "no_liquidation_interval",
        "type": "uint256",
        "indexed": false
      },
      {
        "name": "restricted_liquidation_interval",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "AnchorRewardsDistributorUpdated",
    "inputs": [
      {
        "name": "anchor_rewards_distributor",
        "type": "bytes32",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "VersionIncremented",
    "inputs": [
      {
        "name": "new_version",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "OperationsStopped",
    "inputs": [],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "OperationsResumed",
    "inputs": [],
    "anonymous": false,
    "type": "event"
  },
  {
    "stateMutability": "nonpayable",
    "type": "constructor",
    "inputs": [],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "pause",
    "inputs": [],
    "outputs": [],
    "gas": 25752
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "resume",
    "inputs": [],
    "outputs": [],
    "gas": 40785
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "change_admin",
    "inputs": [
      {
        "name": "new_admin",
        "type": "address"
      }
    ],
    "outputs": [],
    "gas": 39315
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "get_rate",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 12581
  },
  {
    "stateMutability": "payable",
    "type": "function",
    "name": "submit",
    "inputs": [
      {
        "name": "_amount",
        "type": "uint256"
      },
      {
        "name": "_terra_address",
        "type": "bytes32"
      },
      {
        "name": "_extra_data",
        "type": "bytes"
      },
      {
        "name": "_expected_version",
        "type": "uint256"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      },
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 764
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "withdraw",
    "inputs": [
      {
        "name": "_beth_amount",
        "type": "uint256"
      },
      {
        "name": "_expected_version",
        "type": "uint256"
      }
    ],
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
    "name": "withdraw",
    "inputs": [
      {
        "name": "_beth_amount",
        "type": "uint256"
      },
      {
        "name": "_expected_version",
        "type": "uint256"
      },
      {
        "name": "_recipient",
        "type": "address"
      }
    ],
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
    "name": "finalize_upgrade_v4",
    "inputs": [],
    "outputs": [],
    "gas": 271242
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "collect_rewards",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 515
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "admin",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 2628
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "beth_token",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 2658
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "steth_token",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 2688
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "bridge_connector",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 2718
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "rewards_liquidator",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 2748
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "insurance_connector",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 2778
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "anchor_rewards_distributor",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "bytes32"
      }
    ],
    "gas": 2808
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "liquidations_admin",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 2838
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "no_liquidation_interval",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 2868
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "restricted_liquidation_interval",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 2898
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "last_liquidation_time",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 2928
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "last_liquidation_share_price",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 2958
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "last_liquidation_shares_burnt",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 2988
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "version",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 3018
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "emergency_admin",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "gas": 3048
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "operations_allowed",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "gas": 3078
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "total_beth_refunded",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "gas": 3108
  }
]
''')