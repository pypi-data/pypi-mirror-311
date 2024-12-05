import json

COMET_EXT_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "name32",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "symbol32",
            "type": "bytes32"
          }
        ],
        "internalType": "struct CometConfiguration.ExtConfiguration",
        "name": "config",
        "type": "tuple"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "BadAmount",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "BadNonce",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "BadSignatory",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidInt104",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidInt256",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidUInt104",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidUInt128",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidUInt64",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidValueS",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidValueV",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NegativeNumber",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SignatureExpired",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "owner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "Approval",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "manager",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "isAllowed_",
        "type": "bool"
      }
    ],
    "name": "allow",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "manager",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "isAllowed_",
        "type": "bool"
      },
      {
        "internalType": "uint256",
        "name": "nonce",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "expiry",
        "type": "uint256"
      },
      {
        "internalType": "uint8",
        "name": "v",
        "type": "uint8"
      },
      {
        "internalType": "bytes32",
        "name": "r",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "s",
        "type": "bytes32"
      }
    ],
    "name": "allowBySig",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      }
    ],
    "name": "allowance",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "baseAccrualScale",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "",
        "type": "uint64"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "baseIndexScale",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "",
        "type": "uint64"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "baseTrackingAccrued",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "",
        "type": "uint64"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "asset",
        "type": "address"
      }
    ],
    "name": "collateralBalanceOf",
    "outputs": [
      {
        "internalType": "uint128",
        "name": "",
        "type": "uint128"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "factorScale",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "",
        "type": "uint64"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "manager",
        "type": "address"
      }
    ],
    "name": "hasPermission",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "isAllowed",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "liquidatorPoints",
    "outputs": [
      {
        "internalType": "uint32",
        "name": "numAbsorbs",
        "type": "uint32"
      },
      {
        "internalType": "uint64",
        "name": "numAbsorbed",
        "type": "uint64"
      },
      {
        "internalType": "uint128",
        "name": "approxSpend",
        "type": "uint128"
      },
      {
        "internalType": "uint32",
        "name": "_reserved",
        "type": "uint32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "maxAssets",
    "outputs": [
      {
        "internalType": "uint8",
        "name": "",
        "type": "uint8"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "name",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "priceScale",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "",
        "type": "uint64"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "symbol",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "totalsBasic",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint64",
            "name": "baseSupplyIndex",
            "type": "uint64"
          },
          {
            "internalType": "uint64",
            "name": "baseBorrowIndex",
            "type": "uint64"
          },
          {
            "internalType": "uint64",
            "name": "trackingSupplyIndex",
            "type": "uint64"
          },
          {
            "internalType": "uint64",
            "name": "trackingBorrowIndex",
            "type": "uint64"
          },
          {
            "internalType": "uint104",
            "name": "totalSupplyBase",
            "type": "uint104"
          },
          {
            "internalType": "uint104",
            "name": "totalBorrowBase",
            "type": "uint104"
          },
          {
            "internalType": "uint40",
            "name": "lastAccrualTime",
            "type": "uint40"
          },
          {
            "internalType": "uint8",
            "name": "pauseFlags",
            "type": "uint8"
          }
        ],
        "internalType": "struct CometStorage.TotalsBasic",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "totalsCollateral",
    "outputs": [
      {
        "internalType": "uint128",
        "name": "totalSupplyAsset",
        "type": "uint128"
      },
      {
        "internalType": "uint128",
        "name": "_reserved",
        "type": "uint128"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "userBasic",
    "outputs": [
      {
        "internalType": "int104",
        "name": "principal",
        "type": "int104"
      },
      {
        "internalType": "uint64",
        "name": "baseTrackingIndex",
        "type": "uint64"
      },
      {
        "internalType": "uint64",
        "name": "baseTrackingAccrued",
        "type": "uint64"
      },
      {
        "internalType": "uint16",
        "name": "assetsIn",
        "type": "uint16"
      },
      {
        "internalType": "uint8",
        "name": "_reserved",
        "type": "uint8"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "userCollateral",
    "outputs": [
      {
        "internalType": "uint128",
        "name": "balance",
        "type": "uint128"
      },
      {
        "internalType": "uint128",
        "name": "_reserved",
        "type": "uint128"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "userNonce",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "version",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
''')