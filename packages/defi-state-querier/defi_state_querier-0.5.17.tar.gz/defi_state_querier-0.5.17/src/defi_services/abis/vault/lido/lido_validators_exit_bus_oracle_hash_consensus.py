import json

LIDO_VALIDATORS_EXIT_BUS_ORACLE_HASH_CONSENSUS_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "slotsPerEpoch",
        "type": "uint256"
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
      },
      {
        "internalType": "uint256",
        "name": "epochsPerFrame",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "fastLaneLengthSlots",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "admin",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "reportProcessor",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
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
    "name": "ConsensusReportAlreadyProcessing",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "DuplicateMember",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "DuplicateReport",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "EmptyReport",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "EpochsPerFrameCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "FastLanePeriodCannotBeLongerThanFrame",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InitialEpochAlreadyArrived",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InitialEpochIsYetToArrive",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InitialEpochRefSlotCannotBeEarlierThanProcessingSlot",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidChainConfig",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidSlot",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NewProcessorCannotBeTheSame",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NonFastLaneMemberCannotReportWithinFastLaneInterval",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NonMember",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NumericOverflow",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "minQuorum",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "receivedQuorum",
        "type": "uint256"
      }
    ],
    "name": "QuorumTooSmall",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ReportProcessorCannotBeZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "StaleReport",
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
    "name": "UnexpectedConsensusVersion",
    "type": "error"
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
    "name": "ConsensusLost",
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
        "name": "report",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "support",
        "type": "uint256"
      }
    ],
    "name": "ConsensusReached",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "fastLaneLengthSlots",
        "type": "uint256"
      }
    ],
    "name": "FastLaneConfigSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newInitialEpoch",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newEpochsPerFrame",
        "type": "uint256"
      }
    ],
    "name": "FrameConfigSet",
    "type": "event"
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
        "indexed": false,
        "internalType": "uint256",
        "name": "newTotalMembers",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newQuorum",
        "type": "uint256"
      }
    ],
    "name": "MemberAdded",
    "type": "event"
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
        "indexed": false,
        "internalType": "uint256",
        "name": "newTotalMembers",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newQuorum",
        "type": "uint256"
      }
    ],
    "name": "MemberRemoved",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newQuorum",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "totalMembers",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "prevQuorum",
        "type": "uint256"
      }
    ],
    "name": "QuorumSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "processor",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "prevProcessor",
        "type": "address"
      }
    ],
    "name": "ReportProcessorSet",
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
        "indexed": true,
        "internalType": "address",
        "name": "member",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "report",
        "type": "bytes32"
      }
    ],
    "name": "ReportReceived",
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
    "name": "DISABLE_CONSENSUS_ROLE",
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
    "name": "MANAGE_FAST_LANE_CONFIG_ROLE",
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
    "name": "MANAGE_FRAME_CONFIG_ROLE",
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
    "name": "MANAGE_MEMBERS_AND_QUORUM_ROLE",
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
    "name": "MANAGE_REPORT_PROCESSOR_ROLE",
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
        "internalType": "address",
        "name": "addr",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "quorum",
        "type": "uint256"
      }
    ],
    "name": "addMember",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "disableConsensus",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getChainConfig",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "slotsPerEpoch",
        "type": "uint256"
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
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getConsensusState",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "internalType": "bytes32",
        "name": "consensusReport",
        "type": "bytes32"
      },
      {
        "internalType": "bool",
        "name": "isReportProcessing",
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
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "getConsensusStateForMember",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "currentFrameRefSlot",
            "type": "uint256"
          },
          {
            "internalType": "bytes32",
            "name": "currentFrameConsensusReport",
            "type": "bytes32"
          },
          {
            "internalType": "bool",
            "name": "isMember",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isFastLane",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "canReport",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "lastMemberReportRefSlot",
            "type": "uint256"
          },
          {
            "internalType": "bytes32",
            "name": "currentFrameMemberReport",
            "type": "bytes32"
          }
        ],
        "internalType": "struct HashConsensus.MemberConsensusState",
        "name": "result",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getCurrentFrame",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "refSlot",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "reportProcessingDeadlineSlot",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getFastLaneMembers",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "addresses",
        "type": "address[]"
      },
      {
        "internalType": "uint256[]",
        "name": "lastReportedRefSlots",
        "type": "uint256[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getFrameConfig",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "initialEpoch",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "epochsPerFrame",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "fastLaneLengthSlots",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getInitialRefSlot",
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
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "getIsFastLaneMember",
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
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "getIsMember",
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
    "inputs": [],
    "name": "getMembers",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "addresses",
        "type": "address[]"
      },
      {
        "internalType": "uint256[]",
        "name": "lastReportedRefSlots",
        "type": "uint256[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getQuorum",
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
    "name": "getReportProcessor",
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
    "name": "getReportVariants",
    "outputs": [
      {
        "internalType": "bytes32[]",
        "name": "variants",
        "type": "bytes32[]"
      },
      {
        "internalType": "uint256[]",
        "name": "support",
        "type": "uint256[]"
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
        "name": "addr",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "quorum",
        "type": "uint256"
      }
    ],
    "name": "removeMember",
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
        "internalType": "uint256",
        "name": "fastLaneLengthSlots",
        "type": "uint256"
      }
    ],
    "name": "setFastLaneLengthSlots",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "epochsPerFrame",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "fastLaneLengthSlots",
        "type": "uint256"
      }
    ],
    "name": "setFrameConfig",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "quorum",
        "type": "uint256"
      }
    ],
    "name": "setQuorum",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "newProcessor",
        "type": "address"
      }
    ],
    "name": "setReportProcessor",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "slot",
        "type": "uint256"
      },
      {
        "internalType": "bytes32",
        "name": "report",
        "type": "bytes32"
      },
      {
        "internalType": "uint256",
        "name": "consensusVersion",
        "type": "uint256"
      }
    ],
    "name": "submitReport",
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
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "initialEpoch",
        "type": "uint256"
      }
    ],
    "name": "updateInitialEpoch",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
''')
