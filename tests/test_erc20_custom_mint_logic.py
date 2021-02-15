import itertools
import pytest
from brownie import Contract

import brownie_tokens
from brownie_tokens import MintableForkToken

tokens = [f.split("_")[1] for f in dir(brownie_tokens.forked) if f[:4] == "mint" and f[5] == "0"]


def ERC20(address):
    return MintableForkToken(Contract.from_explorer(address))


@pytest.mark.parametrize("amount,address", list(itertools.product([1e24], tokens)))
def test_custom_minting(alice, amount, address):
    token = ERC20(address)
    token._mint_for_testing(alice, amount, {"from": alice})
    assert token.balanceOf(alice) == amount
