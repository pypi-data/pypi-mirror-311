import json

LIDO_ORACLE_REPORT_SANITY_CHECKER_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_lidoLocator",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_admin",
        "type": "address"
      },
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "churnValidatorsPerDayLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "oneOffCLBalanceDecreaseBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "annualBalanceIncreaseBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "simulatedShareRateDeviationBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxValidatorExitRequestsPerReport",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxAccountingExtraDataListItemsCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxNodeOperatorsPerExtraDataItemCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "requestTimestampMargin",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxPositiveTokenRebase",
            "type": "uint256"
          }
        ],
        "internalType": "struct LimitsList",
        "name": "_limitsList",
        "type": "tuple"
      },
      {
        "components": [
          {
            "internalType": "address[]",
            "name": "allLimitsManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "churnValidatorsPerDayLimitManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "oneOffCLBalanceDecreaseLimitManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "annualBalanceIncreaseLimitManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "shareRateDeviationLimitManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "maxValidatorExitRequestsPerReportManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "maxAccountingExtraDataListItemsCountManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "maxNodeOperatorsPerExtraDataItemCountManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "requestTimestampMarginManagers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "maxPositiveTokenRebaseManagers",
            "type": "address[]"
          }
        ],
        "internalType": "struct OracleReportSanityChecker.ManagersRoster",
        "name": "_managersRoster",
        "type": "tuple"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "ActualShareRateIsZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "AdminCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "limitPerDay",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "exitedPerDay",
        "type": "uint256"
      }
    ],
    "name": "ExitedValidatorsLimitExceeded",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "churnLimit",
        "type": "uint256"
      }
    ],
    "name": "IncorrectAppearedValidators",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "oneOffCLBalanceDecreaseBP",
        "type": "uint256"
      }
    ],
    "name": "IncorrectCLBalanceDecrease",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "annualBalanceDiff",
        "type": "uint256"
      }
    ],
    "name": "IncorrectCLBalanceIncrease",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "actualELRewardsVaultBalance",
        "type": "uint256"
      }
    ],
    "name": "IncorrectELRewardsVaultBalance",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "churnLimit",
        "type": "uint256"
      }
    ],
    "name": "IncorrectExitedValidators",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "minAllowedValue",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "maxAllowedValue",
        "type": "uint256"
      }
    ],
    "name": "IncorrectLimitValue",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "maxRequestsCount",
        "type": "uint256"
      }
    ],
    "name": "IncorrectNumberOfExitRequestsPerReport",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "requestCreationBlock",
        "type": "uint256"
      }
    ],
    "name": "IncorrectRequestFinalization",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "actualSharesToBurn",
        "type": "uint256"
      }
    ],
    "name": "IncorrectSharesRequestedToBurn",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "simulatedShareRate",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "actualShareRate",
        "type": "uint256"
      }
    ],
    "name": "IncorrectSimulatedShareRate",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "actualWithdrawalVaultBalance",
        "type": "uint256"
      }
    ],
    "name": "IncorrectWithdrawalsVaultBalance",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "maxItemsCount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "receivedItemsCount",
        "type": "uint256"
      }
    ],
    "name": "MaxAccountingExtraDataItemsCountExceeded",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NegativeTotalPooledEther",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "TooHighTokenRebaseLimit",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "TooLowTokenRebaseLimit",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "itemIndex",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "nodeOpsCount",
        "type": "uint256"
      }
    ],
    "name": "TooManyNodeOpsPerExtraDataItem",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "annualBalanceIncreaseBPLimit",
        "type": "uint256"
      }
    ],
    "name": "AnnualBalanceIncreaseBPLimitSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "churnValidatorsPerDayLimit",
        "type": "uint256"
      }
    ],
    "name": "ChurnValidatorsPerDayLimitSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "maxAccountingExtraDataListItemsCount",
        "type": "uint256"
      }
    ],
    "name": "MaxAccountingExtraDataListItemsCountSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "maxNodeOperatorsPerExtraDataItemCount",
        "type": "uint256"
      }
    ],
    "name": "MaxNodeOperatorsPerExtraDataItemCountSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "maxPositiveTokenRebase",
        "type": "uint256"
      }
    ],
    "name": "MaxPositiveTokenRebaseSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "maxValidatorExitRequestsPerReport",
        "type": "uint256"
      }
    ],
    "name": "MaxValidatorExitRequestsPerReportSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "oneOffCLBalanceDecreaseBPLimit",
        "type": "uint256"
      }
    ],
    "name": "OneOffCLBalanceDecreaseBPLimitSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "requestTimestampMargin",
        "type": "uint256"
      }
    ],
    "name": "RequestTimestampMarginSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "previousAdminRole",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "newAdminRole",
        "type": "bytes32"
      }
    ],
    "name": "RoleAdminChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "sender",
        "type": "address"
      }
    ],
    "name": "RoleGranted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "sender",
        "type": "address"
      }
    ],
    "name": "RoleRevoked",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "simulatedShareRateDeviationBPLimit",
        "type": "uint256"
      }
    ],
    "name": "SimulatedShareRateDeviationBPLimitSet",
    "type": "event"
  },
  {
    "inputs": [],
    "name": "ALL_LIMITS_MANAGER_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "ANNUAL_BALANCE_INCREASE_LIMIT_MANAGER_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "CHURN_VALIDATORS_PER_DAY_LIMIT_MANAGER_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "DEFAULT_ADMIN_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "MAX_ACCOUNTING_EXTRA_DATA_LIST_ITEMS_COUNT_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "MAX_NODE_OPERATORS_PER_EXTRA_DATA_ITEM_COUNT_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "MAX_POSITIVE_TOKEN_REBASE_MANAGER_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "MAX_VALIDATOR_EXIT_REQUESTS_PER_REPORT_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "ONE_OFF_CL_BALANCE_DECREASE_LIMIT_MANAGER_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "REQUEST_TIMESTAMP_MARGIN_MANAGER_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "SHARE_RATE_DEVIATION_LIMIT_MANAGER_ROLE",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_extraDataListItemsCount",
        "type": "uint256"
      }
    ],
    "name": "checkAccountingExtraDataListItemsCount",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_timeElapsed",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_preCLBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_postCLBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_withdrawalVaultBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_elRewardsVaultBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_sharesRequestedToBurn",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_preCLValidators",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_postCLValidators",
        "type": "uint256"
      }
    ],
    "name": "checkAccountingOracleReport",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_exitRequestsCount",
        "type": "uint256"
      }
    ],
    "name": "checkExitBusOracleReport",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_exitedValidatorsCount",
        "type": "uint256"
      }
    ],
    "name": "checkExitedValidatorsRatePerDay",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_itemIndex",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_nodeOperatorsCount",
        "type": "uint256"
      }
    ],
    "name": "checkNodeOperatorsPerExtraDataItemCount",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_postTotalPooledEther",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_postTotalShares",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_etherLockedOnWithdrawalQueue",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_sharesBurntDueToWithdrawals",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_simulatedShareRate",
        "type": "uint256"
      }
    ],
    "name": "checkSimulatedShareRate",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_lastFinalizableRequestId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_reportTimestamp",
        "type": "uint256"
      }
    ],
    "name": "checkWithdrawalQueueOracleReport",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getLidoLocator",
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
    "name": "getMaxPositiveTokenRebase",
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
    "name": "getOracleReportLimits",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "churnValidatorsPerDayLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "oneOffCLBalanceDecreaseBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "annualBalanceIncreaseBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "simulatedShareRateDeviationBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxValidatorExitRequestsPerReport",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxAccountingExtraDataListItemsCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxNodeOperatorsPerExtraDataItemCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "requestTimestampMargin",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxPositiveTokenRebase",
            "type": "uint256"
          }
        ],
        "internalType": "struct LimitsList",
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
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      }
    ],
    "name": "getRoleAdmin",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "internalType": "uint256",
        "name": "index",
        "type": "uint256"
      }
    ],
    "name": "getRoleMember",
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
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      }
    ],
    "name": "getRoleMemberCount",
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
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "grantRole",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "hasRole",
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
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "renounceRole",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "role",
        "type": "bytes32"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "revokeRole",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_annualBalanceIncreaseBPLimit",
        "type": "uint256"
      }
    ],
    "name": "setAnnualBalanceIncreaseBPLimit",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_churnValidatorsPerDayLimit",
        "type": "uint256"
      }
    ],
    "name": "setChurnValidatorsPerDayLimit",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_maxAccountingExtraDataListItemsCount",
        "type": "uint256"
      }
    ],
    "name": "setMaxAccountingExtraDataListItemsCount",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_maxValidatorExitRequestsPerReport",
        "type": "uint256"
      }
    ],
    "name": "setMaxExitRequestsPerOracleReport",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_maxNodeOperatorsPerExtraDataItemCount",
        "type": "uint256"
      }
    ],
    "name": "setMaxNodeOperatorsPerExtraDataItemCount",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_maxPositiveTokenRebase",
        "type": "uint256"
      }
    ],
    "name": "setMaxPositiveTokenRebase",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_oneOffCLBalanceDecreaseBPLimit",
        "type": "uint256"
      }
    ],
    "name": "setOneOffCLBalanceDecreaseBPLimit",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "churnValidatorsPerDayLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "oneOffCLBalanceDecreaseBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "annualBalanceIncreaseBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "simulatedShareRateDeviationBPLimit",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxValidatorExitRequestsPerReport",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxAccountingExtraDataListItemsCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxNodeOperatorsPerExtraDataItemCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "requestTimestampMargin",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxPositiveTokenRebase",
            "type": "uint256"
          }
        ],
        "internalType": "struct LimitsList",
        "name": "_limitsList",
        "type": "tuple"
      }
    ],
    "name": "setOracleReportLimits",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_requestTimestampMargin",
        "type": "uint256"
      }
    ],
    "name": "setRequestTimestampMargin",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_simulatedShareRateDeviationBPLimit",
        "type": "uint256"
      }
    ],
    "name": "setSimulatedShareRateDeviationBPLimit",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_preTotalPooledEther",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_preTotalShares",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_preCLBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_postCLBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_withdrawalVaultBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_elRewardsVaultBalance",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_sharesRequestedToBurn",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_etherToLockForWithdrawals",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_newSharesToBurnForWithdrawals",
        "type": "uint256"
      }
    ],
    "name": "smoothenTokenRebase",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "withdrawals",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "elRewards",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "simulatedSharesToBurn",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "sharesToBurn",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes4",
        "name": "interfaceId",
        "type": "bytes4"
      }
    ],
    "name": "supportsInterface",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
''')