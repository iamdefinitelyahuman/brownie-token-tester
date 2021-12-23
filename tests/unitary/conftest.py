import pytest

from brownie_tokens import ERC20


@pytest.fixture(scope="module", params=(False, True, None))
def success_retval(request):
    return request.param


@pytest.fixture(scope="module", params=(False, True, None, "revert"))
def fail_retval(request):
    return request.param


@pytest.fixture(scope="module")
def token(alice, success_retval, fail_retval):
    contract = ERC20(success=success_retval, fail=fail_retval)
    contract._mint_for_testing(alice, 10 ** 21, {"from": alice})
    return contract
