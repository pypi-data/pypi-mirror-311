UNISWAP_V3_FACTORY_ABI= [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":True,"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"FeeAmountEnabled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"token0","type":"address"},{"indexed":True,"internalType":"address","name":"token1","type":"address"},{"indexed":True,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":False,"internalType":"int24","name":"tickSpacing","type":"int24"},{"indexed":False,"internalType":"address","name":"pool","type":"address"}],"name":"PoolCreated","type":"event"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"}],"name":"createPool","outputs":[{"internalType":"address","name":"pool","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"enableFeeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"","type":"uint24"}],"name":"feeAmountTickSpacing","outputs":[{"internalType":"int24","name":"","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parameters","outputs":[{"internalType":"address","name":"factory","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"}]