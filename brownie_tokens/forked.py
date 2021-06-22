import os
import requests
import sys
from brownie import Contract, Wei
from brownie.convert import to_address
from typing import Dict, List, Optional

_ethplorer_api_key: str = os.getenv("ETHPLORER_API_KEY") or "freekey"

_token_holders: Dict = {}
_skip_list: List[str] = []

_token_names = ["Aave"]


class BrownieTokensError(Exception):
    pass


def update_skipped_addresses(token: Optional[str] = None) -> None:
    if token:
        _token_holders[token] = [a for a in _token_holders[token] if a not in _skip_list]
    else:
        for token in _token_holders:
            update_skipped_addresses(token)


def get_top_holders(address: str) -> List:
    address = to_address(address)
    if address not in _token_holders:
        holders = requests.get(
            f"https://api.ethplorer.io/getTopTokenHolders/{address}",
            params={"apiKey": _ethplorer_api_key, "limit": "50"},
        ).json()
        if "error" in holders:
            api_key_message = ""
            if _ethplorer_api_key == "freekey":
                api_key_message = (
                    " Adding $ETHPLORER_API_KEY (from https://ethplorer.io) as environment variable"
                    " may solve the problem."
                )
            raise BrownieTokensError(
                f"Ethplorer returned error: {holders['error']}." + api_key_message
            )

        _token_holders[address] = [to_address(i["address"]) for i in holders["holders"]]
        if address in _token_holders[address]:
            # don't steal from the treasury - that could cause wierdness
            _token_holders[address].remove(address)
        update_skipped_addresses(address)

    return _token_holders[address]


def skip_holders(*addresses: str) -> None:
    """
    Addresses that will remain untouched via '_mint_for_testing'.
    Does not include minting with custom logic.
    """
    global _skip_list
    _skip_list = list(set(_skip_list + list(addresses)))
    update_skipped_addresses()


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

        # check for token name if no custom minting logic exists for address
        if hasattr(self, "name") and not self.name.abi["inputs"]:
            name = self.name()
            fn_name = next((f"mint_{i}" for i in _token_names if name.startswith(i)), "")
            if fn_name and hasattr(sys.modules[__name__], fn_name):
                mint_result = getattr(sys.modules[__name__], fn_name)(self, target, amount)
                if mint_result:
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


def _snx_exchanger() -> str:
    abi = [
        {
            "inputs": [{"name": "name", "type": "bytes32"}],
            "name": "getAddress",
            "outputs": [{"internalType": "uint256", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        }
    ]
    resolver = Contract.from_abi(
        "AddressResolver", "0x4E3b31eB0E5CB73641EE1E65E7dCEFe520bA3ef2", abi
    )
    return resolver.getAddress("0x45786368616e6765720000000000000000000000000000000000000000000000")


def mint_0xE95A203B1a91a908F9B9CE46459d101078c2c3cb(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # aETH (ankrETH)
    owner = "0x2ffc59d32a524611bb891cab759112a51f9e33c0"
    token.updateGlobalPoolContract(owner, {"from": owner})
    token.mint(target, amount, {"from": owner})


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


def mint_0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # USDC
    minter = "0xe982615d461dd5cd06575bbea87624fda4e3de17"
    token.configureMinter(minter, amount, {"from": minter})
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


def mint_0x9559Aaa82d9649C7A7b220E7c461d2E74c9a3593(
    token: MintableForkToken, target: str, amount: int
) -> None:
    # rETH
    MINTER_ROLE = "0x9f2df0fed2c77648de5860a4cc508cd0818c85b8b8a1ab4ceeef8d981c8956a6"
    minter = token.getRoleMember(MINTER_ROLE, 0)
    token.mint(target, amount, {"from": minter})


# To add custom minting logic for a token that starts with [NAME], add [NAME] to `_token_names`
# and add a function `mint_[NAME]`. The function should include sanity-checks to prevent false
# positives, and return a bool indicating if the mint operation was successful.


def mint_Aave(token: MintableForkToken, target: str, amount: int) -> bool:
    # Aave aTokens
    if not hasattr(token, "UNDERLYING_ASSET_ADDRESS"):
        return False

    token = MintableForkToken(token.UNDERLYING_ASSET_ADDRESS())
    lending_pool = Contract("0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9")
    token._mint_for_testing(target, amount)
    token.approve(lending_pool, amount, {"from": target})
    lending_pool.deposit(token, amount, target, 0, {"from": target})
    return True


def mint_Synth(token: MintableForkToken, target: str, amount: int) -> bool:
    # Synthetix synths
    if not hasattr(token, "target"):
        return False

    abi = [
        {
            "inputs": [{"name": "name", "type": "bytes32"}],
            "name": "getAddress",
            "outputs": [{"internalType": "uint256", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        }
    ]
    resolver = Contract.from_abi(
        "AddressResolver", "0x4E3b31eB0E5CB73641EE1E65E7dCEFe520bA3ef2", abi
    )
    exchanger_key = "0x45786368616e6765720000000000000000000000000000000000000000000000"
    exchanger = resolver.getAddress(exchanger_key)

    target_contract = token.target()
    target_contract.issue(target, amount, {"from": exchanger})
    return True
