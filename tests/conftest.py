import brownie
import pytest
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption("--mainnet-fork", action="store_true", help="run forked mainnet tests")


def pytest_configure(config):
    if config.getoption("--mainnet-fork"):
        brownie.network.connect("mainnet-fork")
    else:
        brownie.network.connect("development")


def pytest_ignore_collect(path, config):
    path = Path(path)
    this_path = Path(__file__).parent
    path_parts = path.relative_to(this_path).parts

    if path.is_dir():
        return None

    if path_parts[:1] == ("forked",) and not config.getoption("--mainnet-fork"):
        return True

    if path_parts[:1] != ("forked",) and config.getoption("--mainnet-fork"):
        return True


@pytest.fixture(scope="module", autouse=True)
def mod_isolation():
    brownie.chain.snapshot()
    yield
    brownie.chain.revert()


@pytest.fixture(autouse=True)
def isolation():
    start = len(brownie.history)
    yield
    end = len(brownie.history)
    if end - start > 0:
        brownie.chain.undo(end - start)


@pytest.fixture(scope="session")
def alice():
    yield brownie.accounts[0]


@pytest.fixture(scope="session")
def bob():
    yield brownie.accounts[1]


@pytest.fixture(scope="session")
def accounts():
    return brownie.accounts
