
import json

DEFAULT_RESERVE_INTEREST_RATE_STRATEGY = json.loads("""
[
    {
      "inputs": [
        {
          "internalType": "contract ILendingPoolAddressesProvider",
          "name": "provider",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "optimalUtilizationRate",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "baseVariableBorrowRate",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "variableRateSlope1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "variableRateSlope2",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "stableRateSlope1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "stableRateSlope2",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "EXCESS_UTILIZATION_RATE",
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
      "name": "OPTIMAL_UTILIZATION_RATE",
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
      "name": "addressesProvider",
      "outputs": [
        {
          "internalType": "contract ILendingPoolAddressesProvider",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "baseVariableBorrowRate",
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
          "name": "reserve",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "availableLiquidity",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "totalStableDebt",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "totalVariableDebt",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "averageStableBorrowRate",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reserveFactor",
          "type": "uint256"
        }
      ],
      "name": "calculateInterestRates",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
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
      "name": "getMaxVariableBorrowRate",
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
      "name": "stableRateSlope1",
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
      "name": "stableRateSlope2",
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
      "name": "variableRateSlope1",
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
      "name": "variableRateSlope2",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
]
""")
        