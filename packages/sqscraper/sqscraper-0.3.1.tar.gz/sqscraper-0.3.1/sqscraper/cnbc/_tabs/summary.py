"""
"""

import datetime
import typing

import numpy as np
import pandas as pd

from . import QuotePageTab
from . import expand_value


class StockSummary(QuotePageTab):
    """
    """
    def __init__(self, symbol: str, data: typing.Dict[str, typing.Any]):
        super().__init__(symbol, data)

        self.key_stats = KeyStats(self.symbol, self._data)
        self.ratios = Ratios(self.symbol, self._data)
        self.events = Events(self.symbol, self._data["EventData"])


class _SummarySubsection(QuotePageTab):
    """
    """
    @property
    def series(self) -> pd.Series:
        """
        """
        raise NotImplementedError

    @staticmethod
    def quote_data(
        method: typing.Callable[["_SummarySubsection"], typing.Any]
    ) -> typing.Callable[["_SummarySubsection"], typing.Any]:
        """
        :param method:
        :return:
        """
        def wrapper(self: "_SummarySubsection") -> typing.Any:
            """
            :param self:
            :return:
            """
            try:
                return method(self)
            except KeyError:
                return None
        return wrapper


class KeyStats(_SummarySubsection):
    """
    """
    @property
    def series(self) -> pd.Series:
        """
        """
        data = {
            "Open": self.open, "Day High": self.day_high, "Day Low": self.day_low,
            "Previous Close": self.prev_close,
            "10 Day Average Volume": self.ten_day_average_volume,
            "52 Week High": self.fiftytwo_week_high,
            "52 Week High Date": self.fiftytwo_week_high_date,
            "52 Week Low": self.fiftytwo_week_low,
            "52 Week Low Date": self.fiftytwo_week_low_date,
            "Beta": self.beta, "Shares Out": self.shares_out, "Dividend": self.dividend,
            "Dividend Yield (%)": self.dividend_yield, "YTD % Change": self.ytd_pct_change
        }
        return pd.Series(data, name="Key Stats")

    @property
    @_SummarySubsection.quote_data
    def open(self) -> float:
        """
        """
        return float(self["open"])

    @property
    @_SummarySubsection.quote_data
    def day_high(self) -> float:
        """
        """
        return float(self["high"])

    @property
    @_SummarySubsection.quote_data
    def day_low(self) -> float:
        """
        """
        return float(self["low"])

    @property
    @_SummarySubsection.quote_data
    def prev_close(self) -> float:
        """
        """
        return float(self["previous_day_closing"])

    @property
    @_SummarySubsection.quote_data
    def ten_day_average_volume(self) -> int:
        """
        """
        return expand_value(self["tendayavgvol"])

    @property
    @_SummarySubsection.quote_data
    def fiftytwo_week_high(self) -> float:
        """
        """
        return float(self["yrhiprice"])

    @property
    @_SummarySubsection.quote_data
    def fiftytwo_week_high_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["yrhidate"], "%m/%d/%y")

    @property
    @_SummarySubsection.quote_data
    def fiftytwo_week_low(self) -> float:
        """
        """
        return float(self["yrloprice"])

    @property
    @_SummarySubsection.quote_data
    def fiftytwo_week_low_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["yrlodate"], "%m/%d/%y")

    @property
    @_SummarySubsection.quote_data
    def beta(self) -> float:
        """
        """
        return float(self["beta"])

    @property
    @_SummarySubsection.quote_data
    def market_cap(self) -> int:
        """
        """
        return expand_value(self["mktcapView"])

    @property
    @_SummarySubsection.quote_data
    def shares_out(self) -> int:
        """
        """
        return expand_value(self["sharesout"])

    @property
    @_SummarySubsection.quote_data
    def dividend(self) -> float:
        """
        """
        return float(self["dividend"])

    @property
    @_SummarySubsection.quote_data
    def dividend_yield(self) -> float:
        """
        """
        return float("".join(self["dividendyield"].strip("%").split(",")))

    @property
    @_SummarySubsection.quote_data
    def ytd_pct_change(self) -> float:
        """
        """
        return np.nan


class Ratios(_SummarySubsection):
    """
    """
    @property
    def series(self) -> pd.Series:
        """
        """
        data = {
            "EPS (TTM)": self.eps, "P/E (TTM)": self.pe, "Fwd P/E (NTM)": self.fwd_pe,
            "Revenue (TTM)": self.revenue, "ROE (TTM, %)": self.roe, "EBITDA (TTM)": self.ebitda,
            "Gross Margin (TTM, %)": self.gross_margin, "Net Margin (TTM, %)": self.net_margin,
            "Debt To Equity (TTM, %)": self.debt_to_equity
        }
        return pd.Series(data, name="Ratios/Profitability")

    @property
    @_SummarySubsection.quote_data
    def eps(self) -> float:
        """
        """
        return float(self["eps"])

    @property
    @_SummarySubsection.quote_data
    def pe(self) -> float:
        """
        """
        return float(self["pe"])

    @property
    @_SummarySubsection.quote_data
    def fwd_pe(self) -> float:
        """
        """
        return float(self["fpe"])

    @property
    @_SummarySubsection.quote_data
    def revenue(self) -> int:
        """
        """
        return expand_value(self["revenuettm"])

    @property
    @_SummarySubsection.quote_data
    def roe(self) -> float:
        """
        """
        return float("".join(self["ROETTEM"].strip("%").split(",")))

    @property
    @_SummarySubsection.quote_data
    def ebitda(self) -> int:
        """
        """
        return expand_value(self["TTMEBITD"])

    @property
    @_SummarySubsection.quote_data
    def gross_margin(self) -> float:
        """
        """
        return float("".join(self["GROSMGNTTM"].strip("%").split(",")))

    @property
    @_SummarySubsection.quote_data
    def net_margin(self) -> float:
        """
        """
        return float("".join(self["NETPROFTTM"].strip("%").split(",")))

    @property
    @_SummarySubsection.quote_data
    def debt_to_equity(self) -> float:
        """
        """
        return float("".join(self["DEBTEQTYQ"].strip("%").split(",")))


class Events(_SummarySubsection):
    """
    """
    @property
    def series(self) -> pd.Series:
        """
        """
        data = {
            "Earnings Date": self.earnings_date, "Split Date": self.split_date,
            "Ex Div Date": self.ex_div_date, "Split Factor": self.split_factor,
            "Div Amount": self.div_amount
        }
        return pd.Series(data, name="Events")

    @property
    @_SummarySubsection.quote_data
    def earnings_date(self) -> datetime.datetime:
        """
        """
        try:
            return datetime.datetime.strptime(self["next_earnings_date"], "%m/%d/%Y(est)")
        except ValueError:
            return datetime.datetime.strptime(self["next_earnings_date"], "%m/%d/%Y")

    @property
    @_SummarySubsection.quote_data
    def split_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["split_ex_date"], "%m/%d/%Y")

    @property
    @_SummarySubsection.quote_data
    def ex_div_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["div_ex_date"], "%m/%d/%Y")

    @property
    @_SummarySubsection.quote_data
    def split_factor(self) -> float:
        """
        """
        return float(self["split_factor"])

    @property
    @_SummarySubsection.quote_data
    def div_amount(self) -> float:
        """
        """
        return float(self["div_amount"])
