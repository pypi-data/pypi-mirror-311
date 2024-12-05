import json

LIDO_VALIDATORS_EXIT_BUS_ORACLE_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "secondsPerSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "genesisTime",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "lidoLocator",
        "type": "address"
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
    "name": "ArgumentOutOfBounds",
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
    "name": "InvalidRequestsData",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidRequestsDataLength",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidRequestsDataSortOrder",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NoConsensusReportToProcess",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "moduleId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "nodeOpId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "prevRequestedValidatorIndex",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "requestedValidatorIndex",
        "type": "uint256"
      }
    ],
    "name": "NodeOpValidatorIndexMustIncrease",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NonZeroContractVersionOnInit",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "PauseUntilMustBeInFuture",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "PausedExpected",
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
    "name": "ResumedExpected",
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
    "inputs": [],
    "name": "UnexpectedRequestsDataLength",
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
    "name": "UnsupportedRequestsDataFormat",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "VersionCannotBeSame",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ZeroPauseDuration",
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
        "indexed": false,
        "internalType": "uint256",
        "name": "duration",
        "type": "uint256"
      }
    ],
    "name": "Paused",
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
    "inputs": [],
    "name": "Resumed",
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
        "name": "stakingModuleId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "nodeOperatorId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "validatorIndex",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "bytes",
        "name": "validatorPubkey",
        "type": "bytes"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      }
    ],
    "name": "ValidatorExitRequest",
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
        "name": "requestsProcessed",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "requestsCount",
        "type": "uint256"
      }
    ],
    "name": "WarnDataIncompleteProcessing",
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
    "name": "DATA_FORMAT_LIST",
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
    "name": "PAUSE_INFINITELY",
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
    "name": "PAUSE_ROLE",
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
    "name": "RESUME_ROLE",
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
    "inputs": [
      {
        "internalType": "uint256",
        "name": "moduleId",
        "type": "uint256"
      },
      {
        "internalType": "uint256[]",
        "name": "nodeOpIds",
        "type": "uint256[]"
      }
    ],
    "name": "getLastRequestedValidatorIndices",
    "outputs": [
      {
        "internalType": "int256[]",
        "name": "",
        "type": "int256[]"
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
            "name": "dataHash",
            "type": "bytes32"
          },
          {
            "internalType": "bool",
            "name": "dataSubmitted",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "dataFormat",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "requestsCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "requestsSubmitted",
            "type": "uint256"
          }
        ],
        "internalType": "struct ValidatorsExitBusOracle.ProcessingState",
        "name": "result",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getResumeSinceTimestamp",
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
    "inputs": [],
    "name": "getTotalRequestsProcessed",
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
      },
      {
        "internalType": "uint256",
        "name": "lastProcessingRefSlot",
        "type": "uint256"
      }
    ],
    "name": "initialize",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "isPaused",
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
        "internalType": "uint256",
        "name": "_duration",
        "type": "uint256"
      }
    ],
    "name": "pauseFor",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_pauseUntilInclusive",
        "type": "uint256"
      }
    ],
    "name": "pauseUntil",
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
    "inputs": [],
    "name": "resume",
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
            "name": "requestsCount",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "dataFormat",
            "type": "uint256"
          },
          {
            "internalType": "bytes",
            "name": "data",
            "type": "bytes"
          }
        ],
        "internalType": "struct ValidatorsExitBusOracle.ReportData",
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