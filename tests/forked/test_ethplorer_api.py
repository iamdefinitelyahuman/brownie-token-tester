import pytest
from test_default_mint_logic import token_address_default

import brownie_tokens.forked
from brownie_tokens import BrownieTokensError, MintableForkToken


@pytest.fixture(scope="function")
def invalid_ethplorer_key():
    prev_key = brownie_tokens.forked._ethplorer_api_key
    brownie_tokens.forked._ethplorer_api_key = "invalid_key"
    yield
    brownie_tokens.forked._ethplorer_api_key = prev_key


def test_ethplorer_error(alice, invalid_ethplorer_key):
    brownie_tokens.forked._token_holders.clear()
    ethplorer_error = {"code": 1, "message": "Invalid API key"}

    token = MintableForkToken(token_address_default)
    with pytest.raises(BrownieTokensError, match=f"Ethplorer returned error: {ethplorer_error}.*"):
        token._mint_for_testing(alice, 10 ** 6)
        assert False, "Should fail with Ethplorer request error."
