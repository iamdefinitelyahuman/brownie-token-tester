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


{% if use_eip2612 is true %}
EIP712_TYPEHASH: constant(bytes32) = keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)")
PERMIT_TYPEHASH: constant(bytes32) = keccak256("Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)")
VERSION: constant(String[8]) = "v0.1.0"
{% endif %}


{% if use_eip2612 is true %}
DOMAIN_SEPARATOR: immutable(bytes32)
{% endif %}

NAME: immutable(String[128])
SYMBOL: immutable(String[64])
DECIMALS: immutable(uint8)


allowance: public(HashMap[address, HashMap[address, uint256]])
balanceOf: public(HashMap[address, uint256])
totalSupply: public(uint256)

{% if use_eip2612 is true %}
nonces: public(HashMap[address, uint256])
{% endif %}


@external
def __init__(_name: String[128], _symbol: String[64], _decimals: uint8):
    NAME = _name
    SYMBOL = _symbol
    DECIMALS = _decimals

    {% if use_eip2612 is true %}
    DOMAIN_SEPARATOR = keccak256(
        _abi_encode(EIP712_TYPEHASH, keccak256(_name), keccak256(VERSION), chain.id, self)
    )
    {% endif %}


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

{% if use_eip2612 is true %}

@external
def permit(
    _owner: address,
    _spender: address,
    _value: uint256,
    _deadline: uint256,
    _v: uint8,
    _r: bytes32,
    _s: bytes32
):
    """
    @notice Approves spender by owner's signature to expend owner's tokens.
        See https://eips.ethereum.org/EIPS/eip-2612.
    @param _owner The address which is a source of funds and has signed the Permit.
    @param _spender The address which is allowed to spend the funds.
    @param _value The amount of tokens to be spent.
    @param _deadline The timestamp after which the Permit is no longer valid.
    @param _v The bytes[64] of the valid secp256k1 signature of permit by owner
    @param _r The bytes[0:32] of the valid secp256k1 signature of permit by owner
    @param _s The bytes[32:64] of the valid secp256k1 signature of permit by owner
    """
    assert _owner != ZERO_ADDRESS
    assert block.timestamp <= _deadline

    nonce: uint256 = self.nonces[_owner]
    digest: bytes32 = keccak256(
        concat(
            b"\x19\x01",
            DOMAIN_SEPARATOR,
            keccak256(_abi_encode(PERMIT_TYPEHASH, _owner, _spender, _value, nonce, _deadline))
        )
    )

    assert ecrecover(digest, convert(_v, uint256), convert(_r, uint256), convert(_s, uint256)) == _owner

    self.allowance[_owner][_spender] = _value
    self.nonces[_owner] = nonce + 1

    log Approval(_owner, _spender, _value)

{% endif %}

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
    allowance: uint256 = self.allowance[_from][msg.sender]
    if allowance < _value:
        {% if failval is true %}
        return True
        {% else %}
        return False
        {% endif %}

    {{ validate_transfer(failval, "_from")|indent|trim }}
    self.balanceOf[_to] += _value
    self.allowance[_from][msg.sender] = allowance - _value
    {% else %}
    {{ validate_transfer(failval, "_from")|indent|trim }}
    self.balanceOf[_to] += _value
    self.allowance[_from][msg.sender] -= _value
    {% endif %}

    log Transfer(_from, _to, _value)
    {{ return_statement(retval)|trim }}


@external
def _mint_for_testing(_to: address, _value: uint256):
    """
    @notice Mint new tokens
    """
    self.balanceOf[_to] += _value
    self.totalSupply += _value

    log Transfer(ZERO_ADDRESS, _to, _value)


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


{% if use_eip2612 is true %}
@view
@external
def DOMAIN_SEPARATOR() -> bytes32:
    """
    @notice Query the DOMAIN_SEPARATOR immutable value
    """
    return DOMAIN_SEPARATOR


@view
@external
def version() -> String[8]:
    """
    @notice Query the contract version, used for EIP-2612
    """
    return VERSION
{% endif %}
