import json

LIDO_ACCOUNTING_ORACLE_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "lidoLocator",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "lido",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "legacyOracle",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "secondsPerSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "genesisTime",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "AddressCannotBeSame",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "AddressCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "AdminCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "CannotSubmitExtraDataBeforeMainData",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ExtraDataAlreadyProcessed",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ExtraDataHashCannotBeZeroForNonEmptyData",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ExtraDataItemsCountCannotBeZeroForNonEmptyData",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ExtraDataListOnlySupportsSingleTx",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "HashCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "code",
        "type": "uint256"
      }
    ],
    "name": "IncorrectOracleMigration",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "initialRefSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "processingRefSlot",
        "type": "uint256"
      }
    ],
    "name": "InitialRefSlotCannotBeLessThanProcessingOne",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidContractVersionIncrement",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidExitedValidatorsData",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "itemIndex",
        "type": "uint256"
      }
    ],
    "name": "InvalidExtraDataItem",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "itemIndex",
        "type": "uint256"
      }
    ],
    "name": "InvalidExtraDataSortOrder",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "LegacyOracleCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "LidoCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "LidoLocatorCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NoConsensusReportToProcess",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NonZeroContractVersionOnInit",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "deadline",
        "type": "uint256"
      }
    ],
    "name": "ProcessingDeadlineMissed",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "RefSlotAlreadyProcessing",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "prevRefSlot",
        "type": "uint256"
      }
    ],
    "name": "RefSlotCannotDecrease",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "processingRefSlot",
        "type": "uint256"
      }
    ],
    "name": "RefSlotMustBeGreaterThanProcessingOne",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SecondsPerSlotCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SenderIsNotTheConsensusContract",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SenderNotAllowed",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "UnexpectedChainConfig",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "expectedVersion",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "receivedVersion",
        "type": "uint256"
      }
    ],
    "name": "UnexpectedConsensusVersion",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "expected",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "received",
        "type": "uint256"
      }
    ],
    "name": "UnexpectedContractVersion",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "consensusHash",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "receivedHash",
        "type": "bytes32"
      }
    ],
    "name": "UnexpectedDataHash",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "expectedFormat",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "receivedFormat",
        "type": "uint256"
      }
    ],
    "name": "UnexpectedExtraDataFormat",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "consensusHash",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "receivedHash",
        "type": "bytes32"
      }
    ],
    "name": "UnexpectedExtraDataHash",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "expectedIndex",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "receivedIndex",
        "type": "uint256"
      }
    ],
    "name": "UnexpectedExtraDataIndex",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "expectedCount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "receivedCount",
        "type": "uint256"
      }
    ],
    "name": "UnexpectedExtraDataItemsCount",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "consensusRefSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "dataRefSlot",
        "type": "uint256"
      }
    ],
    "name": "UnexpectedRefSlot",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "format",
        "type": "uint256"
      }
    ],
    "name": "UnsupportedExtraDataFormat",
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
        "name": "dataType",
        "type": "uint256"
      }
    ],
    "name": "UnsupportedExtraDataType",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "VersionCannotBeSame",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "addr",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "prevAddr",
        "type": "address"
      }
    ],
    "name": "ConsensusHashContractSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "version",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "prevVersion",
        "type": "uint256"
      }
    ],
    "name": "ConsensusVersionSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "version",
        "type": "uint256"
      }
    ],
    "name": "ContractVersionSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "itemsProcessed",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "itemsCount",
        "type": "uint256"
      }
    ],
    "name": "ExtraDataSubmitted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "hash",
        "type": "bytes32"
      }
    ],
    "name": "ProcessingStarted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "hash",
        "type": "bytes32"
      }
    ],
    "name": "ReportDiscarded",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "hash",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "processingDeadlineTime",
        "type": "uint256"
      }
    ],
    "name": "ReportSubmitted",
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
        "indexed": true,
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "processedItemsCount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "itemsCount",
        "type": "uint256"
      }
    ],
    "name": "WarnExtraDataIncompleteProcessing",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      }
    ],
    "name": "WarnProcessingMissed",
    "type": "event"
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
    "name": "EXTRA_DATA_FORMAT_EMPTY",
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
    "name": "EXTRA_DATA_FORMAT_LIST",
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
    "name": "EXTRA_DATA_TYPE_EXITED_VALIDATORS",
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
    "name": "EXTRA_DATA_TYPE_STUCK_VALIDATORS",
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
    "name": "GENESIS_TIME",
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
    "name": "LEGACY_ORACLE",
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
    "name": "LIDO",
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
    "name": "LOCATOR",
    "outputs": [
      {
        "internalType": "contract ILidoLocator",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "MANAGE_CONSENSUS_CONTRACT_ROLE",
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
    "name": "MANAGE_CONSENSUS_VERSION_ROLE",
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
    "name": "SECONDS_PER_SLOT",
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
    "name": "SUBMIT_DATA_ROLE",
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
        "name": "refSlot",
        "type": "uint256"
      }
    ],
    "name": "discardConsensusReport",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getConsensusContract",
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
    "name": "getConsensusReport",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "hash",
        "type": "bytes32"
      },
      {
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "processingDeadlineTime",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "processingStarted",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getConsensusVersion",
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
    "name": "getContractVersion",
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
    "name": "getLastProcessingRefSlot",
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
    "name": "getProcessingState",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "currentFrameRefSlot",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "processingDeadlineTime",
            "type": "uint256"
          },
          {
            "internalType": "bytes32",
            "name": "mainDataHash",
            "type": "bytes32"
          },
          {
            "internalType": "bool",
            "name": "mainDataSubmitted",
            "type": "bool"
          },
          {
            "internalType": "bytes32",
            "name": "extraDataHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "extraDataFormat",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "extraDataSubmitted",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "extraDataItemsCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "extraDataItemsSubmitted",
            "type": "uint256"
          }
        ],
        "internalType": "struct AccountingOracle.ProcessingState",
        "name": "result",
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
        "internalType": "address",
        "name": "admin",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "consensusContract",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "consensusVersion",
        "type": "uint256"
      }
    ],
    "name": "initialize",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "admin",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "consensusContract",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "consensusVersion",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "lastProcessingRefSlot",
        "type": "uint256"
      }
    ],
    "name": "initializeWithoutMigration",
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
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "setConsensusContract",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "version",
        "type": "uint256"
      }
    ],
    "name": "setConsensusVersion",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "reportHash",
        "type": "bytes32"
      },
      {
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "deadline",
        "type": "uint256"
      }
    ],
    "name": "submitConsensusReport",
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
            "name": "consensusVersion",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "refSlot",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "numValidators",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "clBalanceGwei",
            "type": "uint256"
          },
          {
            "internalType": "uint256[]",
            "name": "stakingModuleIdsWithNewlyExitedValidators",
            "type": "uint256[]"
          },
          {
            "internalType": "uint256[]",
            "name": "numExitedValidatorsByStakingModule",
            "type": "uint256[]"
          },
          {
            "internalType": "uint256",
            "name": "withdrawalVaultBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "elRewardsVaultBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "sharesRequestedToBurn",
            "type": "uint256"
          },
          {
            "internalType": "uint256[]",
            "name": "withdrawalFinalizationBatches",
            "type": "uint256[]"
          },
          {
            "internalType": "uint256",
            "name": "simulatedShareRate",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isBunkerMode",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "extraDataFormat",
            "type": "uint256"
          },
          {
            "internalType": "bytes32",
            "name": "extraDataHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "extraDataItemsCount",
            "type": "uint256"
          }
        ],
        "internalType": "struct AccountingOracle.ReportData",
        "name": "data",
        "type": "tuple"
      },
      {
        "internalType": "uint256",
        "name": "contractVersion",
        "type": "uint256"
      }
    ],
    "name": "submitReportData",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "submitReportExtraDataEmpty",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes",
        "name": "items",
        "type": "bytes"
      }
    ],
    "name": "submitReportExtraDataList",
    "outputs": [],
    "stateMutability": "nonpayable",
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