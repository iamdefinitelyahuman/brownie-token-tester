import requests
import sys
from brownie import Contract, Wei
from brownie.convert import to_address
from typing import Dict, List

_token_holders: Dict = {}


def get_top_holders(address: str) -> List:
    address = to_address(address)
    if address not in _token_holders:
        holders = requests.get(
            f"https://api.ethplorer.io/getTopTokenHolders/{address}",
            params={"apiKey": "freekey", "limit": "50"},
        ).json()
        _token_holders[address] = [to_address(i["address"]) for i in holders["holders"]]
        if address in _token_holders[address]:
            # don't steal from the treasury - that could cause wierdness
            _token_holders[address].remove(address)

    return _token_holders[address]


class MintableForkToken(Contract):
    """
    ERC20 wrapper for forked mainnet tests that allows standardized token minting.
    """

    def _mint_for_testing(self, target: str, amount: Wei, tx: Dict = None) -> None:
        # check for custom minting logic
        fn_name = f"mint_{self.address}"
        if hasattr(sys.modules[__name__], fn_name):
            getattr(sys.modules[__name__], fn_name)(self, target, amount)
            return

        # if no custom logic, fetch a list of the top
        # token holders and start stealing from them
        for address in get_top_holders(self.address):
            balance = self.balanceOf(address)
            if not balance:
                continue
            if amount > balance:
                self.transfer(target, balance, {"from": address})
                amount -= balance
            else:
                self.transfer(target, amount, {"from": address})
                return

        raise ValueError(f"Insufficient tokens available to mint {self.name()}")


# to add custom minting logic, add a function named `mint_[CHECKSUMMED_ADDRESS]`
# be sure to include a comment with the symbol of the token


def mint_0x0E2EC54fC0B509F445631Bf4b91AB8168230C752(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # LinkUSD
    token.mint(target, amount, {"from": "0x62F31E08e279f3091d9755a09914DF97554eAe0b"})


def mint_0x196f4727526eA7FB1e17b2071B3d8eAA38486988(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # RSV
    token.changeMaxSupply(2 ** 128, {"from": token.owner()})
    token.mint(target, amount, {"from": token.minter()})


def mint_0x674C6Ad92Fd080e4004b2312b45f796a192D27a0(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # USDN
    token.deposit(target, amount, {"from": "0x90f85042533F11b362769ea9beE20334584Dcd7D"})
