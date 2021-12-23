import pytest
from brownie.exceptions import VirtualMachineError


@pytest.fixture(scope="module", autouse=True)
def setup(alice, token):
    token._mint_for_testing(alice, 10 ** 24, {"from": alice})


def test_sender_balance_decreases(alice, bob, token):
    sender_balance = token.balanceOf(alice)
    amount = sender_balance // 4

    token.transfer(bob, amount, {"from": alice})

    assert token.balanceOf(alice) == sender_balance - amount


def test_receiver_balance_increases(alice, bob, token):
    receiver_balance = token.balanceOf(bob)
    amount = token.balanceOf(alice) // 4

    token.transfer(bob, amount, {"from": alice})

    assert token.balanceOf(bob) == receiver_balance + amount


def test_total_supply_not_affected(alice, bob, token):
    total_supply = token.totalSupply()
    amount = token.balanceOf(alice)

    token.transfer(bob, amount, {"from": alice})

    assert token.totalSupply() == total_supply


def test_return_value(alice, bob, token, success_retval):
    amount = token.balanceOf(alice)
    tx = token.transfer(bob, amount, {"from": alice})

    assert tx.return_value is success_retval


def test_transfer_full_balance(alice, bob, token):
    amount = token.balanceOf(alice)
    receiver_balance = token.balanceOf(bob)

    token.transfer(bob, amount, {"from": alice})

    assert token.balanceOf(alice) == 0
    assert token.balanceOf(bob) == receiver_balance + amount


def test_transfer_zero_tokens(alice, bob, token):
    sender_balance = token.balanceOf(alice)
    receiver_balance = token.balanceOf(bob)

    token.transfer(bob, 0, {"from": alice})

    assert token.balanceOf(alice) == sender_balance
    assert token.balanceOf(bob) == receiver_balance


def test_transfer_to_self(alice, bob, token):
    sender_balance = token.balanceOf(alice)
    amount = sender_balance // 4

    token.transfer(alice, amount, {"from": alice})

    assert token.balanceOf(alice) == sender_balance


def test_insufficient_balance(alice, bob, token, fail_retval):
    balance = token.balanceOf(alice)

    if fail_retval == "revert":
        with pytest.raises(VirtualMachineError):
            token.transfer(bob, balance + 1, {"from": alice})
    else:
        tx = token.transfer(bob, balance + 1, {"from": alice})
        assert tx.return_value is fail_retval


def test_transfer_event_fires(alice, bob, token):
    amount = token.balanceOf(alice)
    tx = token.transfer(bob, amount, {"from": alice})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [alice, bob, amount]
