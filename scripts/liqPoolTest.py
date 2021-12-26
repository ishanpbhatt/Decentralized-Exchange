import json
from web3 import Web3, HTTPProvider


# Load and setup contract information
blockchain_address = 'http://127.0.0.1:9545'
web3 = Web3(HTTPProvider(blockchain_address))

compiled_LP_path = "/Users/ishan/Desktop/eth_dev/build/contracts/LiquidityPool.json"
compiled_IT_path = "/Users/ishan/Desktop/eth_dev/build/contracts/IshToken.json"
compiled_BT_path = "/Users/ishan/Desktop/eth_dev/build/contracts/BhtToken.json"

with open(compiled_LP_path) as file:
    contract_json = json.load(file)
    lp_abi = contract_json['abi']

with open(compiled_IT_path) as file:
    contract_json = json.load(file)
    it_abi = contract_json['abi']

with open(compiled_BT_path) as file:
    contract_json = json.load(file)
    bt_abi = contract_json['abi']

web3.eth.defaultAccount = web3.eth.accounts[0]

ishToken = web3.eth.contract(
    address="0x520529D7548FdC6C691a9ED5971d7F0658073Dc5", abi=it_abi)
bhtToken = web3.eth.contract(
    address="0xb434481cCDd7B5aBE7aa8eFB9f2822321B6127b8", abi=bt_abi)
liqPool = web3.eth.contract(
    address="0x9254055f9A3E0f0953C6AC0e3C9529B80B4986E1", abi=lp_abi)

# Distribute Coins to three wallets
ishToken.functions.giveCoin(10**8).transact({"from": web3.eth.accounts[0]})
bhtToken.functions.giveCoin(10**7).transact({"from": web3.eth.accounts[0]})
acc_zero_ish = ishToken.functions.balanceOf(web3.eth.accounts[0]).call()
acc_zero_bht = bhtToken.functions.balanceOf(web3.eth.accounts[0]).call()
print("Balance of Account[0]: ")
print("IshToken: " + str(acc_zero_ish))
print("BhtToken: " + str(acc_zero_bht))

ishToken.functions.giveCoin(10**6).transact({"from": web3.eth.accounts[1]})
bhtToken.functions.giveCoin(2 * 10**6).transact({"from": web3.eth.accounts[1]})
acc_one_ish = ishToken.functions.balanceOf(web3.eth.accounts[1]).call()
acc_one_bht = bhtToken.functions.balanceOf(web3.eth.accounts[1]).call()
print("\nBalance of Account[1]: ")
print("IshToken: " + str(acc_one_ish))
print("BhtToken: " + str(acc_one_bht))

ishToken.functions.giveCoin(10**5).transact({"from": web3.eth.accounts[2]})
acc_two_ish = ishToken.functions.balanceOf(web3.eth.accounts[2]).call()
acc_two_bht = bhtToken.functions.balanceOf(web3.eth.accounts[2]).call()
print("\nBalance of Account[2]: ")
print("IshToken: " + str(acc_two_ish))
print("BhtToken: " + str(acc_two_bht))

lp_ish = ishToken.functions.balanceOf(liqPool.address).call()
lp_bht = bhtToken.functions.balanceOf(liqPool.address).call()
print("\nBalance of LP: ")
print("IshToken: " + str(lp_ish))
print("BhtToken: " + str(lp_bht))

# Initialize a pool with accounts[0]
ishToken.functions.approve(
    liqPool.address, 10**18 + 1).transact({"from": web3.eth.accounts[0]})
bhtToken.functions.approve(
    liqPool.address, 10**18 + 1).transact({"from": web3.eth.accounts[0]})
liqPool.functions.initPool(
    10**5, 10**4).transact({"from": web3.eth.accounts[0]})


print("============================")
acc_zero_ish = ishToken.functions.balanceOf(web3.eth.accounts[0]).call()
acc_zero_bht = bhtToken.functions.balanceOf(web3.eth.accounts[0]).call()
print("\nBalance of Account[0] after starting Pool: (ISH: 10^5, BHT: 10^4)")
print("IshToken: " + str(acc_zero_ish))
print("BhtToken: " + str(acc_zero_bht))

lp_ish = ishToken.functions.balanceOf(liqPool.address).call()
lp_bht = bhtToken.functions.balanceOf(liqPool.address).call()
print("\nBalance of LP: ")
print("IshToken: " + str(lp_ish))
print("BhtToken: " + str(lp_bht))
print("============================")
# Add liquidity with accounts[1]
ishToken.functions.approve(
    liqPool.address, 10**18 + 1).transact({"from": web3.eth.accounts[1]})
bhtToken.functions.approve(
    liqPool.address, 10**18 + 1).transact({"from": web3.eth.accounts[1]})
liqPool.functions.addLiquidity(
    10**4, 10**3).transact({"from": web3.eth.accounts[1]})
acc_one_ish = ishToken.functions.balanceOf(web3.eth.accounts[1]).call()
acc_one_bht = bhtToken.functions.balanceOf(web3.eth.accounts[1]).call()
print("\nBalance of Account[1] after adding liquidity: ")
print("IshToken: " + str(acc_one_ish))
print("BhtToken: " + str(acc_one_bht))

lp_ish = ishToken.functions.balanceOf(liqPool.address).call()
lp_bht = bhtToken.functions.balanceOf(liqPool.address).call()
print("\nBalance of LP: ")
print("IshToken: " + str(lp_ish))
print("BhtToken: " + str(lp_bht))

print("============================")
# Swap tokens with accounts[2]
ishToken.functions.approve(liqPool.address, 10**18 +
                           1).transact({"from": web3.eth.accounts[2]})
liqPool.functions.swapOutOne(1000).transact({"from": web3.eth.accounts[2]})
acc_two_ish = ishToken.functions.balanceOf(web3.eth.accounts[2]).call()
acc_two_bht = bhtToken.functions.balanceOf(web3.eth.accounts[2]).call()
print("\nBalance of Account[2] after swapping ishToken: (ISH: -1000)")
print("IshToken: " + str(acc_two_ish))
print("BhtToken: " + str(acc_two_bht))

lp_ish = ishToken.functions.balanceOf(liqPool.address).call()
lp_bht = bhtToken.functions.balanceOf(liqPool.address).call()
print("\nBalance of LP: ")
print("IshToken: " + str(lp_ish))
print("BhtToken: " + str(lp_bht))

print("============================")
# Swap tokens with accounts[1]
ishToken.functions.approve(
    liqPool.address, 10**19).transact({"from": web3.eth.accounts[1]})
liqPool.functions.swapOutTwo(500).transact({"from": web3.eth.accounts[1]})
acc_one_ish = ishToken.functions.balanceOf(web3.eth.accounts[1]).call()
acc_one_bht = bhtToken.functions.balanceOf(web3.eth.accounts[1]).call()
print("\nBalance of Account[1] after swapping bhtToken: (BHT: -500)")
print("IshToken: " + str(acc_one_ish))
print("BhtToken: " + str(acc_one_bht))

lp_ish = ishToken.functions.balanceOf(liqPool.address).call()
lp_bht = bhtToken.functions.balanceOf(liqPool.address).call()
print("\nBalance of LP: ")
print("IshToken: " + str(lp_ish))
print("BhtToken: " + str(lp_bht))
print("============================")
# Withdrawing fees/rewards to accounts[0]
liqPool.functions.payoutRewards().transact({"from": web3.eth.accounts[0]})
acc_zero_ish = ishToken.functions.balanceOf(web3.eth.accounts[0]).call()
acc_zero_bht = bhtToken.functions.balanceOf(web3.eth.accounts[0]).call()
print("\nWithdrawing fees to accounts[0]: ")
print("IshToken: " + str(acc_zero_ish))
print("BhtToken: " + str(acc_zero_bht))

lp_ish = ishToken.functions.balanceOf(liqPool.address).call()
lp_bht = bhtToken.functions.balanceOf(liqPool.address).call()
print("\nBalance of LP: ")
print("IshToken: " + str(lp_ish))
print("BhtToken: " + str(lp_bht))
print("============================")

# Remove liquidity, 50% to accounts[0]
liqPool.functions.removeLiquidity(50).transact({"from": web3.eth.accounts[0]})
acc_zero_ish = ishToken.functions.balanceOf(web3.eth.accounts[0]).call()
acc_zero_bht = bhtToken.functions.balanceOf(web3.eth.accounts[0]).call()
print("\nExiting 50% of LP position for account[0]:")
print("IshToken: " + str(acc_zero_ish))
print("BhtToken: " + str(acc_zero_bht))

lp_ish = ishToken.functions.balanceOf(liqPool.address).call()
lp_bht = bhtToken.functions.balanceOf(liqPool.address).call()
print("\nBalance of LP: ")
print("IshToken: " + str(lp_ish))
print("BhtToken: " + str(lp_bht))
print("============================")
