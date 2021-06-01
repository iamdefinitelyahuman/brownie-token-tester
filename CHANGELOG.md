# CHANGELOG

All notable changes to this project are documented in this file.

This changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/iamdefinitelyahuman/brownie-token-tester)

## [0.2.2](https://github.com/iamdefinitelyahuman/brownie-token-tester/tree/v0.2.2) - 2021-06-01

### Changed
- Generalize minting logic for Synthetix synths

## [0.2.1](https://github.com/iamdefinitelyahuman/brownie-token-tester/tree/v0.2.1) - 2021-05-26

### Changed
- Use Vyper `v0.2.12`

### Fixed
- Query SNX exchanger address from address resolver

## [0.2.0](https://github.com/iamdefinitelyahuman/brownie-token-tester/tree/v0.2.0) - 2021-03-28

### Added

- Custom minting logic for: USDC, DAI, USDT, EURS, sEURS, sETH, sUSD, ankrETH, rETH
- Add fork tests for custom minting logic
- `deployer` kwarg for `ERC20`
- Use Vyper `v0.2.11`

## [0.1.0](https://github.com/iamdefinitelyahuman/brownie-token-tester/tree/v0.1.0) - 2021-01-25

### Added

- Custom minting logic for tokens: pBTC, wZEC, renZEC, renBTC, wBTC, sBTC, tBTC, aave tokens
- `forked.py`: Add handling of custom minting logic if token name starts with a specified prefix (e.g. 'AAVE') and custom minting logic for address does not exist
- Better error when using incompatible return types for `ERC20`

## [0.0.3](https://github.com/iamdefinitelyahuman/brownie-token-tester/tree/v0.0.3) - 2021-01-13

### Fixed

- `ERC20.transfer` bug

## [0.0.2](https://github.com/iamdefinitelyahuman/brownie-token-tester/tree/v0.0.2) - 2021-01-12

### Fixed

- Improved handling of string types for `success` and `revert` kwargs in `ERC20` init
- Explicitly target Vyper version `0.2.8` to avoid issues when Solidity is not installed

## [0.0.1](https://github.com/iamdefinitelyahuman/brownie-token-tester/tree/v0.0.1) - 2020-12-12

- Initial alpha release
