PANCAKESWAP_V2_FACTORY_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_feeToSetter",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "token0",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "token1",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "pair",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "", "type": "uint256"
            }
        ],
        "name": "PairCreated",
        "type": "event"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "INIT_CODE_PAIR_HASH",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "allPairs",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "allPairsLength",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "tokenA",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "tokenB",
                "type": "address"
            }
        ],
        "name": "createPair",
        "outputs": [
            {
                "internalType": "address",
                "name": "pair",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "feeTo",
        "outputs": [
            {"internalType": "address",
             "name": "",
             "type": "address"
             }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "feeToSetter",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
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
        "name": "getPair",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "_feeTo",
                "type": "address"
            }
        ],
        "name": "setFeeTo",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "_feeToSetter",
                "type": "address"
            }
        ],
        "name": "setFeeToSetter",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
