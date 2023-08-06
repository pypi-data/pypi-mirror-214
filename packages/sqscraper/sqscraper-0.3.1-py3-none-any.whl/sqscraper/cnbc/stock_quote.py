"""
"""

import datetime
import math
import typing

import numpy as np
import requests

from ._tabs.summary import StockSummary


class QuoteStrip:
    """
    :param data:
    """
    def __init__(self, symbol: str, data: typing.Dict[str, typing.Any]):
        self.symbol = symbol
        self._data = data
        
    def __repr__(self) -> str:
        argnames = (
            "symbol", "market_status", "last", "last_time", "change", "change_pct", "volume"
        )
        arguments = ", ".join(f"{x}={self.__getattribute__(x)}" for x in argnames)

        return f"{type(self).__name__}({arguments})"

    def __str__(self) -> str:
        return "{}: {} {} ({})".format(
            self.symbol,
            self.last,
            "UNCH" if math.isnan(self.change) else f"{self.change_type}{self.change}",
            "UNCH" if math.isnan(self.change_pct) else f"{self.change_type}{self.change_pct}",
        )

    def __getitem__(self, key: str) -> str:
        return self._data[key]

    @property
    def market_status(self) -> str:
        """
        """
        return self["curmktstatus"]

    @property
    def last(self) -> float:
        """
        """
        return float(self["last"])

    @property
    def last_time(self) -> datetime.datetime:
        """
        """
        try:
            return datetime.datetime.strptime(self["last_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            return datetime.datetime.strptime(self["last_time"], "%Y-%m-%d")

    @property
    def change_type(self) -> str:
        """
        """
        return {"UP": "+", "DOWN": "-", "UNCH": "="}[self["changetype"]]

    @property
    def change(self) -> float:
        """
        """
        if self["change"] == "UNCH":
            return np.nan
        return float(self["change"])

    @property
    def change_pct(self) -> float:
        """
        """
        if self["change_pct"] == "UNCH":
            return np.nan
        return float(self["change_pct"].strip("%"))

    @property
    def volume(self) -> int:
        """
        """
        return int("".join(self["volume"].split(",")))


class ExtQuoteStrip(QuoteStrip):
    """
    :param data:
    """
    @property
    def market_status(self) -> str:
        """
        """
        return self["type"]


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

        self.summary = StockSummary(self.symbol, self.data)

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
