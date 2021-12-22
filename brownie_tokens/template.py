from brownie import Contract, compile_source
from brownie.network.account import Account
from jinja2 import Environment, PackageLoader
from typing import Union

env = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=PackageLoader("brownie_tokens"),
)


def ERC20(
    name: str = "Test Token",
    symbol: str = "TST",
    decimals: int = 18,
    success: Union[bool, None] = True,
    fail: Union[bool, str, None] = "revert",
    deployer: Union[Account, str, None] = None,
    use_eip2612: bool = False,
) -> Contract:
    """
    Deploy an ERC20 contract for testing purposes.

    Arguments
    ---------
    name : str, optional
        Full name of the token.
    symbol: str, optional
        Short symbol for the token.
    decimals : int, optional
        Number of token decimal places.
    success : bool, optional
        Value returned upon successful transfer or approval.
    fail : bool | str, optional
        Value or action upon failed transfer or approval. Use "revert"
        to make the transaction revert.
    deployer: Account | str, optional
        Address to deploy the contract from.
    use_eip2612: bool, optional
        Include EIP-2612 (permit) support in the resulting contract

    Returns
    -------
    Contract
        Deployed ERC20 contract
    """
    # input validation
    if not (isinstance(success, bool) or success is None):
        raise TypeError(f"Argument `success` has invalid type: '{type(success)}'")
    if not (isinstance(fail, (bool, str)) or fail is None):
        raise TypeError(f"Argument `fail` has invalid type: '{type(fail)}'")
    if isinstance(fail, str) and fail.lower() != "revert":
        raise ValueError(f"Argument `fail` has invalid value: '{fail}'")

    # fetch and render template
    template = env.get_template("ERC20.vy")
    src = template.render(retval=success, failval=fail, use_eip2612=use_eip2612)

    ERC20 = compile_source(src, vyper_version="0.3.1").Vyper

    tx_params = {
        "from": deployer or "0x0000000000000000000000000000000000001337",
        "silent": deployer is not None,
    }
    return ERC20.deploy(name, symbol, decimals, tx_params)
