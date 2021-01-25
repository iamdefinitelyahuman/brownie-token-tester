# brownie-token-tester

Helper objects for generating ERC20s while testing a Brownie project.

## Dependencies

- [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater, python3-dev
- [brownie](https://github.com/eth-brownie/brownie) version [1.11.6](https://github.com/eth-brownie/brownie/releases/tag/v1.11.6) or greater
- [ganache-cli](https://github.com/trufflesuite/ganache-cli) version [6.11.0](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.11.0) or greater

## Installation

### via `pipx`

If you have installed Brownie using [`pipx`](https://github.com/pipxproject/pipx), you need to add `brownie-token-tester` into the same virtual environment:

```bash
pipx inject eth-brownie brownie-token-tester
```

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install brownie-token-tester
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/iamdefinitelyahuman/brownie-token-tester.git
cd brownie-token-tester
python3 setup.py install
```

## Quick Usage

Import the library from within a Brownie test, script or console:

```python
from brownie_tokens import ERC20, MintableForkToken
```

You can then make use of the following functionality:

### `ERC20`

Deploys a generic ERC20 contract for testing purposes.

```python
def ERC20(
    name: str = "Test Token",
    symbol: str = "TST",
    decimals: int = 18,
    success: Union[bool, None] = True,
    fail: Union[bool, str, None] = "revert",
) -> Contract:
```

- The `success` kwarg is used to set the token's return value upon a successful call to `approve`, `transfer` or `transferFrom`. Valid values are `True`, `False`, and `None`.
- The `fail` kwarg sets the token's behaviour upon failed calls to the above methods. Use `"revert"` if the transaction should revert, or `True`, `False`, and `None` to return a value without reverting.

The resulting deployment adheres to the [ERC20 Token Standard](https://eips.ethereum.org/EIPS/eip-20) and additionally implements one non-standard method:

```python
def _mint_for_testing(target: address, amount: uint256): nonpayable
```

This method increases the balance of `target` by `amount`. It may be called by any account.

### `MintableForkToken`

`MintableForkToken` is used to standardize the process of minting tokens when working in a [forked mainnet](https://eth-brownie.readthedocs.io/en/stable/network-management.html#using-a-forked-development-network) environment. The `MintableForkToken` class inherits from and may be used interchangeably with the [`Contract`](https://eth-brownie.readthedocs.io/en/stable/api-network.html#contract-and-projectcontract) class. It exposes one additional method, `_mint_for_testing`, with the same API as given above.

For tokens where [custom logic is implemented](https://github.com/iamdefinitelyahuman/brownie-token-tester/blob/master/brownie_tokens/forked.py#L52), this is an actual minting event. For most tokens, the "minting" process involves a query to the [Ethplorer API](https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API#get-top-token-holders) to get a list of top token holders, and then transferring their balances to `target`.

Tokens for which custom logic is currently implemented:

- [x] Aave tokens
- [x] LinkUSD
- [x] pBTC
- [x] renBTC
- [x] renZEC
- [x] RSV
- [x] USDN
- [x] sBTC
- [x] tBTC
- [x] wBTC
- [x] wZEC

## Development

This project is still in early development and should be considered an alpha. Comments, questions, criticisms and pull requests are welcomed.

## License

This project is licensed under the [MIT license](LICENSE).
