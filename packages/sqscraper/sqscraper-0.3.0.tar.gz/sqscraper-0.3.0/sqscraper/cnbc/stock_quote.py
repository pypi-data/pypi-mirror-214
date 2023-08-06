"""
"""

import typing

import requests

from .quote_strip import ExtQuoteStrip
from .quote_strip import QuoteStrip


class Quote:
    """
    :param data:
    """
    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.data = data

        self.quote_strip = QuoteStrip(self.symbol, self.data)
        try:
            self.ext_quote_strip = ExtQuoteStrip(self.symbol, self.data["ExtendedMktQuote"])
        except KeyError:
            self.ext_quote_strip = None

    def __repr__(self) -> str:
        argnames = ("symbol", "name", "exchange")
        arguments = ", ".join(f"{x}={self.__getattribute__(x)}" for x in argnames)

        return f"{type(self).__name__}({arguments})"

    def __getitem__(self, key: str) -> str:
        return self.data[key]

    @property
    def symbol(self) -> str:
        """
        """
        return self["symbol"]

    @property
    def name(self) -> str:
        """
        """
        return self["name"]

    @property
    def exchange(self) -> str:
        """
        """
        return self["exchange"]


class StockQuotes:
    """
    :param symbols: Ticker symbols to look up
    """
    _address = "https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol"

    def __init__(self, *symbols: str):
        self.symbols = tuple(set(symbols))

        self._params = {
            "symbols": "|".join(self.symbols), "fund": 1, "exthrs": 1, "events": 1
        }
        self._response = requests.get(self._address, params=self._params, timeout=100)

        self._url = self._response.url
        self._json = self._response.json()
        self._result = self._json["FormattedQuoteResult"]["FormattedQuote"]

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbols={self.symbols})"

    def __len__(self) -> int:
        return len(self.symbols)

    def __getitem__(self, key: str) -> str:
        return self.quotes[key]

    def __contains__(self, item: str) -> bool:
        return item in self.symbols

    @classmethod
    def get_quote(cls, symbol: str, **kwargs) -> Quote:
        """
        :param symbol:
        :param kwargs:
        :return:
        """
        return cls(symbol, **kwargs)[symbol]

    @property
    def data(self) -> typing.Dict[str, typing.Any]:
        """
        """
        return dict(zip(self.symbols, self._result))

    @property
    def quotes(self) -> typing.Dict[str, Quote]:
        """
        """
        return dict(zip(self.symbols, map(Quote, self._result)))
