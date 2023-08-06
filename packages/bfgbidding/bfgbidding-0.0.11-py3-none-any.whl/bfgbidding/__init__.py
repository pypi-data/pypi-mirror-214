"""Expose the classes in the API."""
from ._version import __version__

VERSION = __version__

from .source.hand import Hand
from .source.comments import comments, strategies, comment_xrefs, convert_text_to_html
from .source.strategy_xref import StrategyXref, strategy_descriptions
from .source.bidding import Bid, Pass, Double
from .source.player import Player
