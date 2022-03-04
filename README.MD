the first thing tht we need to do is swap our eth to weth which is into erc20 token
1. Deposit some ETH(WETH) into Aave
2. Borrow some asset with the ETH colleteral
 1. Sell that borrowed asset. (short selling)
3. Repay everything back

Testing:

Integration test: Kovan
Unit test: Mainnet-fork (Mock the entire mainnet rather that using mock)

<!-- 
Default Testing Network 
 Development with Mocking

If you have oracles:
 You can use mainnet-fork for testing -->