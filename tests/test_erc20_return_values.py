import itertools
import pytest
from brownie.exceptions import VirtualMachineError

from brownie_tokens import ERC20
from brownie_tokens.template import FAIL_STATEMENT, RETURN_STATEMENT


@pytest.fixture(scope="module", params=itertools.product(RETURN_STATEMENT, FAIL_STATEMENT))
def token(request, alice):
    success, fail = request.param
    if None in (fail, success) and fail is not success:
        pytest.skip()
    contract = ERC20(success=success, fail=fail)
    contract._mint_for_testing(alice, 10 ** 18, {"from": alice})
    yield (contract, success, fail)


def test_transfer_success(alice, bob, token):
    token, success, fail = token
    tx = token.transfer(bob, 0, {"from": alice})
    if success is None:
        assert len(tx.return_value) == 0
    else:
        assert tx.return_value is success


def test_transfer_fail(alice, bob, token):
    token, success, fail = token
    if fail == "revert":
        with pytest.raises(VirtualMachineError):
            token.transfer(bob, 10 ** 19, {"from": alice})
    else:
        tx = token.transfer(bob, 10 ** 19, {"from": alice})
        if fail is None:
            assert len(tx.return_value) == 0
        else:
            assert tx.return_value is fail


def test_approve(alice, bob, token):
    token, success, fail = token
    tx = token.approve(alice, 10 ** 21, {"from": bob})
    if success is None:
        assert len(tx.return_value) == 0
    else:
        assert tx.return_value is success


def test_transferFrom_success(alice, bob, token):
    token, success, fail = token
    tx = token.transferFrom(alice, bob, 0, {"from": alice})
    if success is None:
        assert len(tx.return_value) == 0
    else:
        assert tx.return_value is success


def test_transferFrom_fail_allowance(alice, bob, token):
    token, success, fail = token
    if fail == "revert":
        with pytest.raises(VirtualMachineError):
            token.transferFrom(alice, bob, 10 ** 18, {"from": bob})
    else:
        tx = token.transferFrom(alice, bob, 10 ** 18, {"from": bob})
        if fail is None:
            assert len(tx.return_value) == 0
        else:
            assert tx.return_value is fail


def test_transferFrom_fail_balance(alice, bob, token):
    token, success, fail = token
    token.approve(bob, 10 ** 21, {"from": alice})
    if fail == "revert":
        with pytest.raises(VirtualMachineError):
            token.transferFrom(alice, bob, 10 ** 21, {"from": bob})
    else:
        tx = token.transferFrom(alice, bob, 10 ** 21, {"from": bob})
        if fail is None:
            assert len(tx.return_value) == 0
        else:
            assert tx.return_value is fail
