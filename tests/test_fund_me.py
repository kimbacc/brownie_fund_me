from os import access
from brownie import (
    FundMe,
    MockV3Aggregator,
    accounts,
    network,
    config,
    web3,
    exceptions,
)
from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_DEVELOPMENTS,
)
from web3 import Web3
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    print(f"Entrance Fee = {entrance_fee}")
    print(f"Funding...")
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENTS:
        pytest.skip("only for local testing!")
    # account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
