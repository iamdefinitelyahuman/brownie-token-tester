from brownie import Wei

from brownie_tokens import MintableForkToken, skip_holders
from brownie_tokens.forked import _token_holders

# Token with default '_mint_for_testing' logic
token_address_default = "0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39"  # HEX


def test_skip_list(alice):
    token = MintableForkToken(token_address_default)
    # Fetch top holders
    token._mint_for_testing(alice, Wei(0))

    holders = [_token_holders[token.address][i] for i in [0, 1, 10]]
    initial_balances = [token.balanceOf(holder) for holder in holders]

    # Should remove addresses from current lists
    skip_holders(*holders)
    token._mint_for_testing(alice, 10 ** 6)
    for holder, initial_balance in zip(holders, initial_balances):
        assert token.balanceOf(holder) == initial_balance

    # Should not include addresses that were set to skip before
    _token_holders.clear()
    token._mint_for_testing(alice, 10 ** 6)
    for holder, initial_balance in zip(holders, initial_balances):
        assert token.balanceOf(holder) == initial_balance
