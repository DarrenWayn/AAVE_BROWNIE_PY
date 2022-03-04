from brownie import network, config
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.get_weth import get_weth
from brownie import interface
from web3 import Web3

# 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):  # only use account 0 instead of us using private key every single time
        get_weth()  # if we want to work on mainnet-fork that have o weth lets use get_weth()
    # Evert time we want to be working with contract we always needs:
    # ABI
    # Address
    lending_pool = get_lending_pool()
    print(lending_pool)
    # Approve sending out ERC20 token
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")
    # ... How much should we borrow?
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("Let's Borrow!")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    # borrowable_eth -> borrowable_dai * 95%
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    # Now we will borrow!
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI!")
    get_borrowable_data(lending_pool, account)
    # How do we Repaid
    # repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)
    get_borrowable_data(lending_pool, account)
    print("You just Deposited, Borrowed, and Repaid with Aave, Brownie, and Chainlink!")


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repaid!")


def get_asset_price(price_feed_address):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)
    # 0.000383355870000000


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrow_eth} worth of ETH")
    return (float(available_borrow_eth), float(total_debt_eth))


def get_lending_pool():
    # ABI we can use abi = but we re just gonna use interfave because life is greate xD
    # Address
    # one of the great things with interface is if we know we are only gonna use 1 or 2 function we can make the interfaces ourselve
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    Lending_pool_addresses = lending_pool_addresses_provider.getLendingPool()
    # ABI
    # Address in here is = Lending_pool_addresses ,Checked!
    lending_pool = interface.ILendingPool(Lending_pool_addresses)
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):  # this is input parameter
    print("Approving ERC20 Token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx
    # ABI
    # Address
