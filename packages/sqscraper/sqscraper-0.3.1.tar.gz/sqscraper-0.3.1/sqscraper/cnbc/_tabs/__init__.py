"""
"""

from decimal import Decimal
import re
import typing


def expand_value(value: str) -> int:
    """
    :param value:
    :return:
    """
    powers = {"K": 3, "M": 6, "B": 9, "T": 12}
    regex = re.compile(r"^(.*)([KMBT])$")

    quantity, magnitude = regex.search(value).groups()
    return int(Decimal(quantity) * 10 ** powers[magnitude])


class QuotePageTab:
    """
    """
    def __init__(self, symbol: str, data: typing.Dict[str, typing.Any]):
        self.symbol = symbol
        self._data = data

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbol={self.symbol})"

    def __getitem__(self, key: str) -> str:
        return self._data[key]
