import json

SILO_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "contract ISiloRepository",
        "name": "_repository",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_siloAsset",
        "type": "address"
      },
      {
        "internalType": "uint128",
        "name": "_version",
        "type": "uint128"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "AssetDoesNotExist",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "BorrowNotPossible",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "DepositNotPossible",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "DepositsExceedLimit",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "DifferentArrayLength",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidRepository",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidSiloVersion",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "LiquidationReentrancyCall",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "MaximumLTVReached",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NotEnoughDeposits",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NotEnoughLiquidity",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NotSolvent",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "OnlyRouter",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "Paused",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "TokenIsNotAContract",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "UnexpectedEmptyReturn",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "UnsupportedLTVType",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "UserIsZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ZeroAssets",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ZeroShares",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "enum IBaseSilo.AssetStatus",
        "name": "status",
        "type": "uint8"
      }
    ],
    "name": "AssetStatusUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "Borrow",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "depositor",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "bool",
        "name": "collateralOnly",
        "type": "bool"
      }
    ],
    "name": "Deposit",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "shareAmountRepaid",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "seizedCollateral",
        "type": "uint256"
      }
    ],
    "name": "Liquidate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "Repay",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "depositor",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "receiver",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "bool",
        "name": "collateralOnly",
        "type": "bool"
      }
    ],
    "name": "Withdraw",
    "type": "event"
  },
  {
    "inputs": [],
    "name": "VERSION",
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
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "accrueInterest",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "interest",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "assetStorage",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract IShareToken",
            "name": "collateralToken",
            "type": "address"
          },
          {
            "internalType": "contract IShareToken",
            "name": "collateralOnlyToken",
            "type": "address"
          },
          {
            "internalType": "contract IShareToken",
            "name": "debtToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "totalDeposits",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "collateralOnlyDeposits",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalBorrowAmount",
            "type": "uint256"
          }
        ],
        "internalType": "struct IBaseSilo.AssetStorage",
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
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "borrow",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "debtAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "debtShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_borrower",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_receiver",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "borrowFor",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "debtAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "debtShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_borrower",
        "type": "address"
      }
    ],
    "name": "borrowPossible",
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
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "_collateralOnly",
        "type": "bool"
      }
    ],
    "name": "deposit",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "collateralAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "collateralShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_depositor",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "_collateralOnly",
        "type": "bool"
      }
    ],
    "name": "depositFor",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "collateralAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "collateralShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_depositor",
        "type": "address"
      }
    ],
    "name": "depositPossible",
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
        "internalType": "address[]",
        "name": "_users",
        "type": "address[]"
      },
      {
        "internalType": "bytes",
        "name": "_flashReceiverData",
        "type": "bytes"
      }
    ],
    "name": "flashLiquidate",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "assets",
        "type": "address[]"
      },
      {
        "internalType": "uint256[][]",
        "name": "receivedCollaterals",
        "type": "uint256[][]"
      },
      {
        "internalType": "uint256[][]",
        "name": "shareAmountsToRepay",
        "type": "uint256[][]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAssets",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "assets",
        "type": "address[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAssetsWithState",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "assets",
        "type": "address[]"
      },
      {
        "components": [
          {
            "internalType": "contract IShareToken",
            "name": "collateralToken",
            "type": "address"
          },
          {
            "internalType": "contract IShareToken",
            "name": "collateralOnlyToken",
            "type": "address"
          },
          {
            "internalType": "contract IShareToken",
            "name": "debtToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "totalDeposits",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "collateralOnlyDeposits",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalBorrowAmount",
            "type": "uint256"
          }
        ],
        "internalType": "struct IBaseSilo.AssetStorage[]",
        "name": "assetsStorage",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "harvestProtocolFees",
    "outputs": [
      {
        "internalType": "uint256[]",
        "name": "harvestedAmounts",
        "type": "uint256[]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "initAssetsTokens",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "interestData",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "harvestedProtocolFees",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "protocolFees",
            "type": "uint256"
          },
          {
            "internalType": "uint64",
            "name": "interestRateTimestamp",
            "type": "uint64"
          },
          {
            "internalType": "enum IBaseSilo.AssetStatus",
            "name": "status",
            "type": "uint8"
          }
        ],
        "internalType": "struct IBaseSilo.AssetInterestData",
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
        "name": "_user",
        "type": "address"
      }
    ],
    "name": "isSolvent",
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
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "liquidity",
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
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "repay",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "repaidAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "repaidShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_borrower",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "repayFor",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "repaidAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "repaidShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "siloAsset",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "siloRepository",
    "outputs": [
      {
        "internalType": "contract ISiloRepository",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "syncBridgeAssets",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "utilizationData",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "totalDeposits",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalBorrowAmount",
            "type": "uint256"
          },
          {
            "internalType": "uint64",
            "name": "interestRateTimestamp",
            "type": "uint64"
          }
        ],
        "internalType": "struct IBaseSilo.UtilizationData",
        "name": "data",
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
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "_collateralOnly",
        "type": "bool"
      }
    ],
    "name": "withdraw",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "withdrawnAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "withdrawnShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_depositor",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_receiver",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "_collateralOnly",
        "type": "bool"
      }
    ],
    "name": "withdrawFor",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "withdrawnAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "withdrawnShare",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
''')