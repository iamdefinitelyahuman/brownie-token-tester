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
    case_a = success_retval is None and isinstance(fail_retval, bool)
    case_b = fail_retval is None and isinstance(success_retval, bool)
    if case_a or case_b:
        pytest.xfail()

    return ERC20(success=success_retval, fail=fail_retval)
