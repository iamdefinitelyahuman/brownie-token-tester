import brownie

from brownie_tokens.forked import BrownieTokensError, MintableForkToken, skip_holders
from brownie_tokens.template import ERC20

brownie.config["autofetch_sources"] = True
