import pytest


@pytest.mark.parametrize("idx", range(5))
def test_initial_approval_is_zero(alice, accounts, idx, token):
    assert token.allowance(alice, accounts[idx]) == 0


def test_approve(alice, bob, token):
    token.approve(bob, 10 ** 19, {"from": alice})

    assert token.allowance(alice, bob) == 10 ** 19


def test_modify_approve_nonzero(alice, bob, token):
    token.approve(bob, 10 ** 19, {"from": alice})
    token.approve(bob, 12345678, {"from": alice})

    assert token.allowance(alice, bob) == 12345678


def test_modify_approve_zero_nonzero(alice, bob, token):
    token.approve(bob, 10 ** 19, {"from": alice})
    token.approve(bob, 0, {"from": alice})
    token.approve(bob, 12345678, {"from": alice})

    assert token.allowance(alice, bob) == 12345678


def test_revoke_approve(alice, bob, token):
    token.approve(bob, 10 ** 19, {"from": alice})
    token.approve(bob, 0, {"from": alice})

    assert token.allowance(alice, bob) == 0


def test_approve_self(alice, bob, token):
    token.approve(alice, 10 ** 19, {"from": alice})

    assert token.allowance(alice, alice) == 10 ** 19


def test_only_affects_target(alice, bob, token):
    token.approve(bob, 10 ** 19, {"from": alice})

    assert token.allowance(bob, alice) == 0


def test_return_value(alice, bob, token, success_retval):
    tx = token.approve(bob, 10 ** 19, {"from": alice})

    assert tx.return_value is success_retval


def test_approval_event_fires(alice, bob, token):
    tx = token.approve(bob, 10 ** 19, {"from": alice})

    assert len(tx.events) == 1
    assert tx.events["Approval"].values() == [alice, bob, 10 ** 19]
