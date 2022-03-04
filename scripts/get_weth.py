from scripts.helpful_scripts import get_account
from brownie import interface, config, network, accounts


def main():
    get_weth()


def get_weth():
    """
    Mints Weth by depositing ETH.
    """
    # ABI
    # Address
    account = get_account()
    # interface.Iweth we have an ABI which came from the interface
    # (config["networks"][network.show_active()]["weth_token"]) we have an address
    weth = interface.Iweth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    print(f"Received 0.1 WETH")
    tx.wait(1)
