# @version >=0.3.1
"""
@notice Mock ERC20
@dev See https://eips.ethereum.org/EIPS/eip-20
"""
from vyper.interfaces import ERC20

implements: ERC20


event Approval:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256


NAME: immutable(String[128])
SYMBOL: immutable(String[64])
DECIMALS: immutable(uint8)


allowance: public(HashMap[address, HashMap[address, uint256]])
balanceOf: public(HashMap[address, uint256])
totalSupply: public(uint256)


@external
def __init__(_name: String[128], _symbol: String[64], _decimals: uint8):
    NAME = _name
    SYMBOL = _symbol
    DECIMALS = _decimals


@external
def approve(_spender: address, _value: uint256) -> bool:
    """
    @notice Allow `_spender` to transfer/withdraw from your account multiple times, up to `_value`
        amount.
    @dev If this function is called again it overwrites the current allowance with `_value`.
    @param _spender The address given permission to transfer/withdraw tokens.
    @param _value The amount of tokens that may be transferred.
    """
    self.allowance[msg.sender][_spender] = _value

    log Approval(msg.sender, _spender, _value)
    return True


@external
def transfer(_to: address, _value: uint256) -> bool:
    """
    @notice Transfer `_value` amount of tokens to address `_to`.
    @dev Reverts if caller's balance does not have enough tokens to spend.
    @param _to The address to increase the balance of.
    @param _value The amount of tokens to transfer.
    """
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value

    log Transfer(msg.sender, _to, _value)
    return True


@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    """
    @notice Transfers ~_value` amount of tokens from address `_from` to address `_to`.
    @dev Reverts if caller's allowance is not enough, or if `_from` address does not have a balance
        great enough.
    @param _from The account to transfer/withdraw tokens from.
    @param _to The account to transfer tokens to.
    @param _value The amount of tokens to transfer.
    """
    self.allowance[_from][msg.sender] -= _value

    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value

    log Transfer(_from, _to, _value)
    return True


@view
@external
def name() -> String[128]:
    """
    @notice Query the name of the token.
    """
    return NAME


@view
@external
def symbol() -> String[64]:
    """
    @notice Query the symbol of the token.
    """
    return SYMBOL


@view
@external
def decimals() -> uint8:
    """
    @notice Query the decimals of the token.
    """
    return DECIMALS
