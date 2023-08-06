"""
"""

import datetime
import math
import typing

import numpy as np


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
