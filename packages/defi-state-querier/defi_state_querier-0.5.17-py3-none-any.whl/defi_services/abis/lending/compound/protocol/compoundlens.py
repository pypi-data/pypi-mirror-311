
import json

COMPOUNDLENS = json.loads("""
[
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken",
        "name": "cToken",
        "type": "address"
      },
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "cTokenBalances",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "balanceOf",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowBalanceCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "balanceOfUnderlying",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenAllowance",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenBalances",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken[]",
        "name": "cTokens",
        "type": "address[]"
      },
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "cTokenBalancesAll",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "balanceOf",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowBalanceCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "balanceOfUnderlying",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenAllowance",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenBalances[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken",
        "name": "cToken",
        "type": "address"
      }
    ],
    "name": "cTokenMetadata",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRateCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "supplyRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "reserveFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalBorrows",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalReserves",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalSupply",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalCash",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "collateralFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAssetAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "cTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "compSupplySpeed",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "compBorrowSpeed",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenMetadata",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken[]",
        "name": "cTokens",
        "type": "address[]"
      }
    ],
    "name": "cTokenMetadataAll",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRateCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "supplyRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "reserveFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalBorrows",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalReserves",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalSupply",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalCash",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "collateralFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAssetAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "cTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "compSupplySpeed",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "compBorrowSpeed",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenMetadata[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken",
        "name": "cToken",
        "type": "address"
      }
    ],
    "name": "cTokenUnderlyingPrice",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "underlyingPrice",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenUnderlyingPrice",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken[]",
        "name": "cTokens",
        "type": "address[]"
      }
    ],
    "name": "cTokenUnderlyingPriceAll",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "underlyingPrice",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenUnderlyingPrice[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract ComptrollerLensInterface",
        "name": "comptroller",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getAccountLimits",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract CToken[]",
            "name": "markets",
            "type": "address[]"
          },
          {
            "internalType": "uint256",
            "name": "liquidity",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "shortfall",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.AccountLimits",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "contract Comp",
        "name": "comp",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getCompBalanceMetadata",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "balance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "votes",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "delegate",
            "type": "address"
          }
        ],
        "internalType": "struct CompoundLens.CompBalanceMetadata",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract Comp",
        "name": "comp",
        "type": "address"
      },
      {
        "internalType": "contract ComptrollerLensInterface",
        "name": "comptroller",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getCompBalanceMetadataExt",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "balance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "votes",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "delegate",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "allocated",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CompBalanceMetadataExt",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "contract Comp",
        "name": "comp",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "internalType": "uint32[]",
        "name": "blockNumbers",
        "type": "uint32[]"
      }
    ],
    "name": "getCompVotes",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "blockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "votes",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CompVotes[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "contract GovernorBravoInterface",
        "name": "governor",
        "type": "address"
      },
      {
        "internalType": "uint256[]",
        "name": "proposalIds",
        "type": "uint256[]"
      }
    ],
    "name": "getGovBravoProposals",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "proposalId",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "proposer",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "eta",
            "type": "uint256"
          },
          {
            "internalType": "address[]",
            "name": "targets",
            "type": "address[]"
          },
          {
            "internalType": "uint256[]",
            "name": "values",
            "type": "uint256[]"
          },
          {
            "internalType": "string[]",
            "name": "signatures",
            "type": "string[]"
          },
          {
            "internalType": "bytes[]",
            "name": "calldatas",
            "type": "bytes[]"
          },
          {
            "internalType": "uint256",
            "name": "startBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "endBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "forVotes",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "againstVotes",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "abstainVotes",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "canceled",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "executed",
            "type": "bool"
          }
        ],
        "internalType": "struct CompoundLens.GovBravoProposal[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "contract GovernorBravoInterface",
        "name": "governor",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "voter",
        "type": "address"
      },
      {
        "internalType": "uint256[]",
        "name": "proposalIds",
        "type": "uint256[]"
      }
    ],
    "name": "getGovBravoReceipts",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "proposalId",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "hasVoted",
            "type": "bool"
          },
          {
            "internalType": "uint8",
            "name": "support",
            "type": "uint8"
          },
          {
            "internalType": "uint96",
            "name": "votes",
            "type": "uint96"
          }
        ],
        "internalType": "struct CompoundLens.GovBravoReceipt[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "contract GovernorAlpha",
        "name": "governor",
        "type": "address"
      },
      {
        "internalType": "uint256[]",
        "name": "proposalIds",
        "type": "uint256[]"
      }
    ],
    "name": "getGovProposals",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "proposalId",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "proposer",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "eta",
            "type": "uint256"
          },
          {
            "internalType": "address[]",
            "name": "targets",
            "type": "address[]"
          },
          {
            "internalType": "uint256[]",
            "name": "values",
            "type": "uint256[]"
          },
          {
            "internalType": "string[]",
            "name": "signatures",
            "type": "string[]"
          },
          {
            "internalType": "bytes[]",
            "name": "calldatas",
            "type": "bytes[]"
          },
          {
            "internalType": "uint256",
            "name": "startBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "endBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "forVotes",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "againstVotes",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "canceled",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "executed",
            "type": "bool"
          }
        ],
        "internalType": "struct CompoundLens.GovProposal[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "internalType": "contract GovernorAlpha",
        "name": "governor",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "voter",
        "type": "address"
      },
      {
        "internalType": "uint256[]",
        "name": "proposalIds",
        "type": "uint256[]"
      }
    ],
    "name": "getGovReceipts",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "proposalId",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "hasVoted",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "support",
            "type": "bool"
          },
          {
            "internalType": "uint96",
            "name": "votes",
            "type": "uint96"
          }
        ],
        "internalType": "struct CompoundLens.GovReceipt[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
""")
        