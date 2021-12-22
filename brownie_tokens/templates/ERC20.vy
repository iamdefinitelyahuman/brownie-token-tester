{% macro return_type(retval) %}{% if retval is boolean %} -> bool {%- endif %}{% endmacro -%}

{% macro return_statement(retval) %}
{% if retval is true %}
return True
{% elif retval is false %}
return False
{% else %}
return
{% endif %}
{% endmacro -%}

{# failval should be either boolean or string #}
{# from should be either `msg.sender` or `_from` #}
{% macro validate_transfer(failval, from) %}
{% if failval is boolean %}
user_balance: uint256 = self.balanceOf[{{ from }}]
if user_balance < _value:
    {% if failval is true %}
    return True
    {% else %}
    return False
    {% endif %}

self.balanceOf[{{ from }}] = user_balance - _value
{% else %}
self.balanceOf[{{ from }}] -= _value
{% endif %}
{% endmacro -%}

# @version 0.3.1
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
def approve(_spender: address, _value: uint256){{ return_type(retval) }}:
    """
    @notice Allow `_spender` to transfer/withdraw from your account multiple times, up to `_value`
        amount.
    @dev If this function is called again it overwrites the current allowance with `_value`.
    @param _spender The address given permission to transfer/withdraw tokens.
    @param _value The amount of tokens that may be transferred.
    """
    self.allowance[msg.sender][_spender] = _value

    log Approval(msg.sender, _spender, _value)
    {{ return_statement(retval)|trim }}


@external
def transfer(_to: address, _value: uint256){{ return_type(retval) }}:
    """
    @notice Transfer `_value` amount of tokens to address `_to`.
    @dev Reverts if caller's balance does not have enough tokens to spend.
    @param _to The address to increase the balance of.
    @param _value The amount of tokens to transfer.
    """
    {# input validation is handled prior to template rendering #}
    {{ validate_transfer(failval, "msg.sender")|indent|trim }}
    self.balanceOf[_to] += _value

    log Transfer(msg.sender, _to, _value)
    {{ return_statement(retval)|trim }}


@external
def transferFrom(_from: address, _to: address, _value: uint256){{ return_type(retval) }}:
    """
    @notice Transfers ~_value` amount of tokens from address `_from` to address `_to`.
    @dev Reverts if caller's allowance is not enough, or if `_from` address does not have a balance
        great enough.
    @param _from The account to transfer/withdraw tokens from.
    @param _to The account to transfer tokens to.
    @param _value The amount of tokens to transfer.
    """
    {# input validation is handled prior to template rendering #}
    {% if failval is boolean %}
    allowance: uint256 = self.allowance[msg.sender]
    if allowance < _value:
        {% if failval is true %}
        return True
        {% else %}
        return False
        {% endif %}

    {{ validate_transfer(failval, "_from")|indent|trim }}
    self.balanceOf[_to] += _value
    self.allowance[msg.sender] = allowance - _value
    {% else %}
    {{ validate_transfer(failval, "_from")|indent|trim }}
    self.balanceOf[_to] += _value
    self.allowance[msg.sender] -= _value
    {% endif %}

    log Transfer(_from, _to, _value)
    {{ return_statement(retval)|trim }}


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
