import brownie
import pytest


def pytest_configure():
    brownie.network.connect("development")


@pytest.fixture(scope="function", autouse=True)
def isolation():
    brownie.chain.snapshot()
    yield
    brownie.chain.revert()


@pytest.fixture(scope="session")
def alice():
    yield brownie.accounts[0]


@pytest.fixture(scope="session")
def bob():
    yield brownie.accounts[1]
