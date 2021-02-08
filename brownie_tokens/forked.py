import requests
import sys
from brownie import Contract, Wei
from brownie.convert import to_address
from typing import Dict, List

_token_holders: Dict = {}

_token_names = ["Aave"]

# dev: mapping of proxy contracts to implementation
_proxy_contracts = {
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "0xb7277a6e95992041568d9391d09d0122023778a2",  # USDC
}


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
    def __init__(self, address):
        if address in _proxy_contracts.keys():
            address = _proxy_contracts[address]
        super().__init__(address)

    def _mint_for_testing(self, target: str, amount: Wei, tx: Dict = None) -> None:
        # check for custom minting logic
        fn_name = f"mint_{self.address}"
        if hasattr(sys.modules[__name__], fn_name):
            getattr(sys.modules[__name__], fn_name)(self, target, amount)
            return

        # check for token name if no custom minting
        # logic exists for address
        for name in _token_names:
            if hasattr(self, "name") and self.name().startswith(name):
                fn_name = f"mint_{name}"
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


def mint_0x6B175474E89094C44Da98b954EedeAC495271d0F(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # DAI
    token.mint(target, amount, {"from": "0x9759A6Ac90977b93B58547b4A71c78317f391A28"})

def mint_0xdB25f211AB05b1c97D595516F45794528a807ad8(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # EURS
    owner = "0x2EbBbc541E8f8F24386FA319c79CedA0579f1Efb"
    token.createTokens(amount, {"from": owner})
    token.transfer(target, amount, {"from": owner})


def mint_0x0E2EC54fC0B509F445631Bf4b91AB8168230C752(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # LinkUSD
    token.mint(target, amount, {"from": "0x62F31E08e279f3091d9755a09914DF97554eAe0b"})


def mint_0x5228a22e72ccC52d415EcFd199F99D0665E7733b(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # pBTC
    token.mint(target, amount, {"from": "0x3423Fb35149875e965f06c926DA8BA82D63f7ddb"})


def mint_0xEB4C2781e4ebA804CE9a9803C67d0893436bB27D(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # renBTC
    token.mint(target, amount, {"from": "0xe4b679400F0f267212D5D812B95f58C83243EE71"})


def mint_0x1C5db575E2Ff833E46a2E9864C22F4B22E0B37C2(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # renZEC
    token.mint(target, amount, {"from": "0xc3BbD5aDb611dd74eCa6123F05B18acc886e122D"})


def mint_0x196f4727526eA7FB1e17b2071B3d8eAA38486988(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # RSV
    token.changeMaxSupply(2 ** 128, {"from": token.owner()})
    token.mint(target, amount, {"from": token.minter()})


def mint_0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # Synth sBTC
    target_contract = Contract("0xDB91E4B3b6E19bF22E810C43273eae48C9037e74")
    target_contract.issue(target, amount, {"from": "0x778D2d3E3515e42573EB1e6a8d8915D4a22D9d54"})


def mint_0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # Synth sETH
    target_contract = Contract("0x87641989057242Bff28D0D6108d007C79774D06f")
    target_contract.issue(target, amount, {"from": "0x778D2d3E3515e42573EB1e6a8d8915D4a22D9d54"})


def mint_0xD71eCFF9342A5Ced620049e616c5035F1dB98620(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # Synth sEURS
    target_contract = Contract("0xC61b352fCc311Ae6B0301459A970150005e74b3E")
    target_contract.issue(target, amount, {"from": "0x778D2d3E3515e42573EB1e6a8d8915D4a22D9d54"})


def mint_0x57Ab1ec28D129707052df4dF418D58a2D46d5f51(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # Synth sUSD
    target_contract = Contract("0x6C85C5198C3CC4dB1b87Cb43b2674241a30f4845")
    target_contract.issue(target, amount, {"from": "0x778D2d3E3515e42573EB1e6a8d8915D4a22D9d54"})


def mint_0x8dAEBADE922dF735c38C80C7eBD708Af50815fAa(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # tBTC
    token.mint(target, amount, {"from": "0x526c08E5532A9308b3fb33b7968eF78a5005d2AC"})


def mint_0xdAC17F958D2ee523a2206206994597C13D831ec7(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # USDT
    owner = "0xc6cde7c39eb2f0f0095f41570af89efc2c1ea828"
    token.issue(amount, {"from": owner})
    token.transfer(target, amount, {"from": owner})


def mint_0x674C6Ad92Fd080e4004b2312b45f796a192D27a0(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # USDN
    token.deposit(target, amount, {"from": "0x90f85042533F11b362769ea9beE20334584Dcd7D"})


def mint_0xB7277a6e95992041568D9391D09d0122023778A2(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # USDC
    # dev: mint from implementation (not from proxy)
    minter = "0x0000000000000000000000000000000000000001"
    token.configureMinter(minter, amount , {"from": minter})
    token.mint(target, amount, {"from": minter})


def mint_0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # wBTC
    token.mint(target, amount, {"from": "0xCA06411bd7a7296d7dbdd0050DFc846E95fEBEB7"})


def mint_0x4A64515E5E1d1073e83f30cB97BEd20400b66E10(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # wZEC
    token.mint(target, amount, {"from": "0x5Ca1262e25A5Fb6CA8d74850Da2753f0c896e16c"})


# to add custom minting logic for a token that starts with [NAME], add [NAME] to
# `_token_names` and add a function `mint_[NAME]`


def mint_Aave(token: MintableForkToken, target: str, amount: int) -> None:
    # aave token
    token = MintableForkToken(token.UNDERLYING_ASSET_ADDRESS())
    lending_pool = Contract("0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9")
    token._mint_for_testing(target, amount)
    token.approve(lending_pool, amount, {"from": target})
    lending_pool.deposit(token, amount, target, 0, {"from": target})
