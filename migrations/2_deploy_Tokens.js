const IshToken = artifacts.require("IshToken")
const BhtToken = artifacts.require("BhtToken")
const LiquidityPool = artifacts.require("LiquidityPool")

module.exports = async function (deployer, network, accounts) {
  // Deploy IshToken
  await deployer.deploy(IshToken, 0)
  const ishToken = await IshToken.deployed()

  // Deploy BhtToken
  await deployer.deploy(BhtToken, 0)
  const bhtToken = await BhtToken.deployed()

  await deployer.deploy(LiquidityPool, IshToken.address, BhtToken.address, 100)
  const liqPool = await LiquidityPool.deployed()
}
