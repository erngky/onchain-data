from web3 import Web3, HTTPProvider
import json

URL = "https://mainnet.infura.io/v3/7148d2a369be41ffbc2729082be6f49a"
UNISWAP_FACTORY_ADDRESS = "0x1F98431c8aD98523631AE4a59f267346ea31F984" 
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" 
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

with open("UniswapV3Factory.json", "r") as f:
    uniswap_factory_abi = json.loads(f.read())
with open("UniswapV3Pool.json", "r") as f:
    uniswap_pool_abi = json.loads(f.read())

w3 = Web3(HTTPProvider(URL))

def uniswap_price_feed():
    factory = w3.eth.contract(address=UNISWAP_FACTORY_ADDRESS, abi=uniswap_factory_abi)

    pool_address = factory.functions.getPool(USDC_ADDRESS, WETH_ADDRESS, 500).call()
    pool = w3.eth.contract(address=pool_address, abi=uniswap_pool_abi)

    slot0 = pool.functions.slot0().call()
    sqrtPriceX96 = slot0[0]

    price = sqrtPriceX96 ** 2 / 2 ** 192
    price = 1 / price * 10 ** 12
    
    print("Uniswap ETH price:", price - (price * 0.05 / 100))

uniswap_price_feed()
