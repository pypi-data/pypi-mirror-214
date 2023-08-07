from typing import overload
import abc
import datetime
import typing

import Calculators.Estimators
import QuantConnect
import QuantConnect.ABL
import QuantConnect.Algorithm
import QuantConnect.Algorithm.CSharp
import QuantConnect.Algorithm.CSharp.LiveStrategy.Strategies
import QuantConnect.Algorithm.CSharp.qlnet.tools
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Statistics
import System


class Call_Delta_50ETF_backtest(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    class OrderClass(System.Object):
        """This class has no documentation."""

        @property
        def symbol(self) -> QuantConnect.Symbol:
            ...

        @symbol.setter
        def symbol(self, value: QuantConnect.Symbol):
            ...

        @property
        def quantity(self) -> float:
            ...

        @quantity.setter
        def quantity(self, value: float):
            ...

        @property
        def message(self) -> str:
            ...

        @message.setter
        def message(self, value: str):
            ...

        def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, message: str) -> None:
            ...

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def spread(self) -> float:
        ...

    @spread.setter
    def spread(self, value: float):
        ...

    opennew: bool = True

    hasopt: bool = False

    @property
    def firstrun(self) -> bool:
        ...

    @firstrun.setter
    def firstrun(self, value: bool):
        ...

    @property
    def underlying_price_now(self) -> float:
        ...

    @underlying_price_now.setter
    def underlying_price_now(self, value: float):
        ...

    @property
    def expirydatenow(self) -> typing.Any:
        ...

    @expirydatenow.setter
    def expirydatenow(self, value: typing.Any):
        ...

    PendingOrders: typing.Any = ...

    price_list: typing.Any = ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...


class Delta_IH_backtest(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add futures for a given underlying asset.
    It also shows how you can prefilter contracts easily based on expirations, and how you
    can inspect the futures chain to pick a specific contract to trade.
    """

    @property
    def SZ50(self) -> QuantConnect.Symbol:
        ...

    @SZ50.setter
    def SZ50(self, value: QuantConnect.Symbol):
        ...

    hasopt: bool = False

    @property
    def firstrun(self) -> bool:
        ...

    @firstrun.setter
    def firstrun(self, value: bool):
        ...

    @property
    def underlying_price_now(self) -> float:
        ...

    @underlying_price_now.setter
    def underlying_price_now(self, value: float):
        ...

    @property
    def upline_now(self) -> float:
        ...

    @upline_now.setter
    def upline_now(self, value: float):
        ...

    @property
    def expirydatenow(self) -> typing.Any:
        ...

    @expirydatenow.setter
    def expirydatenow(self, value: typing.Any):
        ...

    price_list: typing.Any = ...

    price_list_long: typing.Any = ...

    endOfDay: typing.Any = ...

    @property
    def iscrossupline(self) -> bool:
        ...

    @iscrossupline.setter
    def iscrossupline(self, value: bool):
        ...

    @property
    def future_trade(self) -> QuantConnect.Data.Market.FuturesContract:
        ...

    @future_trade.setter
    def future_trade(self, value: QuantConnect.Data.Market.FuturesContract):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        """Initialize your algorithm and add desired assets."""
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    @staticmethod
    def Var(v: typing.Any) -> float:
        ...


class Delta_IH_backtest_v2(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add futures for a given underlying asset.
    It also shows how you can prefilter contracts easily based on expirations, and how you
    can inspect the futures chain to pick a specific contract to trade.
    """

    @property
    def SZ50(self) -> QuantConnect.Symbol:
        ...

    @SZ50.setter
    def SZ50(self, value: QuantConnect.Symbol):
        ...

    hasopt: bool = False

    @property
    def firstrun(self) -> bool:
        ...

    @firstrun.setter
    def firstrun(self, value: bool):
        ...

    @property
    def underlying_price_now(self) -> float:
        ...

    @underlying_price_now.setter
    def underlying_price_now(self, value: float):
        ...

    @property
    def upline_now(self) -> float:
        ...

    @upline_now.setter
    def upline_now(self, value: float):
        ...

    @property
    def expirydatenow(self) -> typing.Any:
        ...

    @expirydatenow.setter
    def expirydatenow(self, value: typing.Any):
        ...

    price_list: typing.Any = ...

    price_list_long: typing.Any = ...

    endOfDay: typing.Any = ...

    @property
    def iscrossupline(self) -> bool:
        ...

    @iscrossupline.setter
    def iscrossupline(self, value: bool):
        ...

    @property
    def future_trade(self) -> QuantConnect.Data.Market.FuturesContract:
        ...

    @future_trade.setter
    def future_trade(self, value: QuantConnect.Data.Market.FuturesContract):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        """Initialize your algorithm and add desired assets."""
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    @staticmethod
    def Var(v: typing.Any) -> float:
        ...


class DeribitPutCallParity_backtest(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def Perpetual(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def liquidationTime(self) -> typing.Any:
        ...

    @liquidationTime.setter
    def liquidationTime(self, value: typing.Any):
        ...

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...


class LongGammaShortVega(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def checkTime(self) -> typing.Any:
        ...

    @checkTime.setter
    def checkTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...

    @staticmethod
    def SelectATMContracts(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, k_add: float) -> typing.Any:
        ...


class LongVega(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def checkExtendTime(self) -> typing.Any:
        ...

    @checkExtendTime.setter
    def checkExtendTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    @staticmethod
    def GetFandK(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, rf: float) -> typing.Any:
        ...

    def GetVarContribution(self, chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, rf: float, K: float) -> typing.Any:
        ...

    def GetVix(self, chain: QuantConnect.Data.Market.OptionChain) -> float:
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...

    @staticmethod
    def SelectATMContracts(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, k_add: float) -> typing.Any:
        ...


class LongVegaShortGamma(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def checkTime(self) -> typing.Any:
        ...

    @checkTime.setter
    def checkTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...

    @staticmethod
    def SelectATMContracts(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, k_add: float) -> typing.Any:
        ...


class MarketMaking(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def jsonpath1(self) -> str:
        ...

    @jsonpath1.setter
    def jsonpath1(self, value: str):
        ...

    @property
    def jsonpath2(self) -> str:
        ...

    @jsonpath2.setter
    def jsonpath2(self, value: str):
        ...

    @property
    def jsonpath3(self) -> str:
        ...

    @jsonpath3.setter
    def jsonpath3(self, value: str):
        ...

    @property
    def jsonpath4(self) -> str:
        ...

    @jsonpath4.setter
    def jsonpath4(self, value: str):
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...


class MarketMakingRealTrade(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def jsonpath1(self) -> str:
        ...

    @jsonpath1.setter
    def jsonpath1(self, value: str):
        ...

    @property
    def jsonpath2(self) -> str:
        ...

    @jsonpath2.setter
    def jsonpath2(self, value: str):
        ...

    @property
    def jsonpath3(self) -> str:
        ...

    @jsonpath3.setter
    def jsonpath3(self, value: str):
        ...

    @property
    def jsonpath4(self) -> str:
        ...

    @jsonpath4.setter
    def jsonpath4(self, value: str):
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...

    @staticmethod
    def SelectATMContracts(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, k_add: float) -> typing.Any:
        ...


class MarketMakingV2(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def jsonpath1(self) -> str:
        ...

    @jsonpath1.setter
    def jsonpath1(self, value: str):
        ...

    @property
    def jsonpath2(self) -> str:
        ...

    @jsonpath2.setter
    def jsonpath2(self, value: str):
        ...

    @property
    def jsonpath3(self) -> str:
        ...

    @jsonpath3.setter
    def jsonpath3(self, value: str):
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...

    @staticmethod
    def SelectATMContracts(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any) -> typing.Any:
        ...


class MarketMakingV3(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def jsonpath1(self) -> str:
        ...

    @jsonpath1.setter
    def jsonpath1(self, value: str):
        ...

    @property
    def jsonpath2(self) -> str:
        ...

    @jsonpath2.setter
    def jsonpath2(self, value: str):
        ...

    @property
    def jsonpath3(self) -> str:
        ...

    @jsonpath3.setter
    def jsonpath3(self, value: str):
        ...

    @property
    def jsonpath4(self) -> str:
        ...

    @jsonpath4.setter
    def jsonpath4(self, value: str):
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...

    @staticmethod
    def SelectATMContracts(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, k_add: float) -> typing.Any:
        ...


class MarketMakingV4(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def openTime(self) -> typing.Any:
        ...

    @openTime.setter
    def openTime(self, value: typing.Any):
        ...

    @property
    def checkTime(self) -> typing.Any:
        ...

    @checkTime.setter
    def checkTime(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    @staticmethod
    def GetFandK(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, rf: float) -> typing.Any:
        ...

    def GetHistoryVol(self, prc_list: typing.Any) -> float:
        ...

    def GetRollingStd(self, diff_list: typing.Any) -> float:
        ...

    def GetVarContribution(self, chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, rf: float, K: float) -> typing.Any:
        ...

    def GetVix(self, chain: QuantConnect.Data.Market.OptionChain) -> float:
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...

    @staticmethod
    def SelectATMContracts(chain: QuantConnect.Data.Market.OptionChain, expiry: typing.Any, k_add: float) -> typing.Any:
        ...


class MCPricing_backtest(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This example demonstrates how to use Monte Carlo method to do option pricing."""

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...


class PutCallParity(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def Perpetual(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def liquidationTime(self) -> typing.Any:
        ...

    @liquidationTime.setter
    def liquidationTime(self, value: typing.Any):
        ...

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def jsonpath(self) -> str:
        ...

    @jsonpath.setter
    def jsonpath(self, value: str):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...


class PutCallParityPaperTrade(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def Perpetual(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def liquidationTime(self) -> typing.Any:
        ...

    @liquidationTime.setter
    def liquidationTime(self, value: typing.Any):
        ...

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def jsonpath(self) -> str:
        ...

    @jsonpath.setter
    def jsonpath(self, value: str):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...


class SVIDeribit(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    class OrderClass(System.Object):
        """This class has no documentation."""

        @property
        def symbol(self) -> QuantConnect.Symbol:
            ...

        @symbol.setter
        def symbol(self, value: QuantConnect.Symbol):
            ...

        @property
        def quantity(self) -> float:
            ...

        @quantity.setter
        def quantity(self, value: float):
            ...

        def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float) -> None:
            ...

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def spread(self) -> float:
        ...

    @spread.setter
    def spread(self, value: float):
        ...

    endOfDay: typing.Any = ...

    last_underlying_close: float = 0

    PendingOrders: typing.Any = ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...


class SVIMarketMaking(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...


class SVIMarketMakingPaperTrade(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...


class SVI_GET(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    @staticmethod
    def Maxi(array: typing.Any) -> int:
        ...

    @staticmethod
    def Mini(array: typing.Any) -> int:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...


class VolatilitySmileDrawDemo(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnWarmupFinished(self) -> None:
        ...


class FTXJsonCreator(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    filePath: str = ...

    @property
    def symbol_balance(self) -> typing.Any:
        ...

    @symbol_balance.setter
    def symbol_balance(self, value: typing.Any):
        ...

    @property
    def symbol_dict(self) -> typing.Any:
        ...

    @symbol_dict.setter
    def symbol_dict(self, value: typing.Any):
        ...

    @property
    def account(self) -> str:
        ...

    @account.setter
    def account(self, value: str):
        ...

    @property
    def firstfun(self) -> bool:
        ...

    @firstfun.setter
    def firstfun(self, value: bool):
        ...

    @property
    def cryptoSymbol_dict(self) -> typing.Any:
        ...

    @cryptoSymbol_dict.setter
    def cryptoSymbol_dict(self, value: typing.Any):
        ...

    @property
    def jsonpath(self) -> str:
        ...

    @jsonpath.setter
    def jsonpath(self, value: str):
        ...

    @property
    def AddOneStrategies(self) -> typing.Any:
        ...

    @AddOneStrategies.setter
    def AddOneStrategies(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def AddAos(self, symbol: str, expiry: typing.Any, balance: float, account: str) -> QuantConnect.Algorithm.CSharp.LiveStrategy.Strategies.DeltaCollarStrategyPutOnlyMoveStrike:
        ...

    def ChangeAosJson(self, aoss: typing.Any, symbol: str, balance: float, account: str) -> typing.Any:
        ...

    def ChangeJsonFinal(self, slice: QuantConnect.Data.Slice) -> bool:
        ...

    def ChangeLeverageJson(self, aoss: typing.Any, leverage_change_ratio: float) -> typing.Any:
        ...

    def checkDelta(self, aoss: typing.Any) -> None:
        ...

    def ClearAccount(self, aoss: typing.Any) -> typing.Any:
        ...

    def ClearJson(self, aoss: typing.Any) -> typing.Any:
        ...

    def DeletAos(self, aoss: typing.Any, symbol: str) -> typing.Any:
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...


class JsonCreator(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    filePath: str = ...

    @property
    def symbol_balance(self) -> typing.Any:
        ...

    @symbol_balance.setter
    def symbol_balance(self, value: typing.Any):
        ...

    @property
    def symbol_dict(self) -> typing.Any:
        ...

    @symbol_dict.setter
    def symbol_dict(self, value: typing.Any):
        ...

    @property
    def account(self) -> str:
        ...

    @account.setter
    def account(self, value: str):
        ...

    @property
    def firstfun(self) -> bool:
        ...

    @firstfun.setter
    def firstfun(self, value: bool):
        ...

    @property
    def cryptoSymbol_dict(self) -> typing.Any:
        ...

    @cryptoSymbol_dict.setter
    def cryptoSymbol_dict(self, value: typing.Any):
        ...

    @property
    def jsonpath(self) -> str:
        ...

    @jsonpath.setter
    def jsonpath(self, value: str):
        ...

    @property
    def AddOneStrategies(self) -> typing.Any:
        ...

    @AddOneStrategies.setter
    def AddOneStrategies(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def AddAos(self, symbol: str, expiry: typing.Any, balance: float, account: str) -> QuantConnect.Algorithm.CSharp.LiveStrategy.Strategies.DeltaCollarStrategy:
        ...

    def ChangeAosJson(self, aoss: typing.Any, symbol: str, balance: float, account: str) -> typing.Any:
        ...

    def ChangeJsonFinal(self, slice: QuantConnect.Data.Slice) -> bool:
        ...

    def ChangeLeverageJson(self, aoss: typing.Any, leverage_change_ratio: float) -> typing.Any:
        ...

    def checkDelta(self, aoss: typing.Any) -> None:
        ...

    def ClearAccount(self, aoss: typing.Any) -> typing.Any:
        ...

    def ClearJson(self, aoss: typing.Any) -> typing.Any:
        ...

    def DeletAos(self, aoss: typing.Any, symbol: str) -> typing.Any:
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        """
        Event - v3.0 DATA EVENT HANDLER: (Pattern) Basic template for user to override for receiving all subscription data in a single event
        
        :param slice: The current slice of data keyed by symbol string
        """
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Order fill event handler. On an order fill update the resulting information is passed to this method.
        
        :param orderEvent: Order event details containing details of the evemts
        """
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...


class BinanceFuturesBollingGetJson(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def WarmUpDays(self) -> int:
        ...

    @WarmUpDays.setter
    def WarmUpDays(self, value: int):
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def StatisticsSummaryFIlePath(self) -> str:
        ...

    @StatisticsSummaryFIlePath.setter
    def StatisticsSummaryFIlePath(self, value: str):
        ...

    _endOfDay: typing.Any = ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...


class BinanceFuturesEWMASigma(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def WarmUpDays(self) -> int:
        ...

    @WarmUpDays.setter
    def WarmUpDays(self, value: int):
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def StatisticsSummaryFilePath(self) -> str:
        ...

    @StatisticsSummaryFilePath.setter
    def StatisticsSummaryFilePath(self, value: str):
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def StrategyType(self) -> QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType:
        ...

    @StrategyType.setter
    def StrategyType(self, value: QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType):
        ...

    @property
    def BalanceRatio(self) -> float:
        ...

    @BalanceRatio.setter
    def BalanceRatio(self, value: float):
        ...

    @property
    def GetBase(self) -> bool:
        ...

    @GetBase.setter
    def GetBase(self, value: bool):
        ...

    @property
    def PutStrikeRatio(self) -> float:
        ...

    @PutStrikeRatio.setter
    def PutStrikeRatio(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def WarmUpByMinute(self) -> bool:
        ...

    @WarmUpByMinute.setter
    def WarmUpByMinute(self, value: bool):
        ...

    _endOfDay: typing.Any = ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...


class BinanceFuturesMoveStrike(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def WarmUpDays(self) -> int:
        ...

    @WarmUpDays.setter
    def WarmUpDays(self, value: int):
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def StatisticsSummaryFilePath(self) -> str:
        ...

    @StatisticsSummaryFilePath.setter
    def StatisticsSummaryFilePath(self, value: str):
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def StrategyType(self) -> QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType:
        ...

    @StrategyType.setter
    def StrategyType(self, value: QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType):
        ...

    @property
    def BalanceRatio(self) -> float:
        ...

    @BalanceRatio.setter
    def BalanceRatio(self, value: float):
        ...

    @property
    def GetBase(self) -> bool:
        ...

    @GetBase.setter
    def GetBase(self, value: bool):
        ...

    @property
    def PutStrikeRatio(self) -> float:
        ...

    @PutStrikeRatio.setter
    def PutStrikeRatio(self, value: float):
        ...

    @property
    def JsonFilePath(self) -> str:
        ...

    @JsonFilePath.setter
    def JsonFilePath(self, value: str):
        ...

    _endOfDay: typing.Any = ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...


class BinanceFuturesStopWin(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def WarmUpDays(self) -> int:
        ...

    @WarmUpDays.setter
    def WarmUpDays(self, value: int):
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def StatisticsSummaryFilePath(self) -> str:
        ...

    @StatisticsSummaryFilePath.setter
    def StatisticsSummaryFilePath(self, value: str):
        ...

    @property
    def BalanceRatio(self) -> float:
        ...

    @BalanceRatio.setter
    def BalanceRatio(self, value: float):
        ...

    @property
    def GetBase(self) -> bool:
        ...

    @GetBase.setter
    def GetBase(self, value: bool):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def WarmUpByMinute(self) -> bool:
        ...

    @WarmUpByMinute.setter
    def WarmUpByMinute(self, value: bool):
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def StrategyType(self) -> QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType:
        ...

    @StrategyType.setter
    def StrategyType(self, value: QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType):
        ...

    @property
    def HedgeRange(self) -> float:
        ...

    @HedgeRange.setter
    def HedgeRange(self, value: float):
        ...

    _endOfDay: typing.Any = ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...


class CryptoCreateJson(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    datelist: typing.Any = ...

    tradesymbol: str = "AXS"

    _endOfDay: typing.Any = ...

    @property
    def _accountName(self) -> str:
        ...

    @_accountName.setter
    def _accountName(self, value: str):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...


class DeribitBaseAlgorithm(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def ImportantMessageKey(self) -> str:
        """This field is protected."""
        ...

    @ImportantMessageKey.setter
    def ImportantMessageKey(self, value: str):
        """This field is protected."""
        ...

    @property
    def ImportantMessageToken(self) -> str:
        """This field is protected."""
        ...

    @ImportantMessageToken.setter
    def ImportantMessageToken(self, value: str):
        """This field is protected."""
        ...

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def OrderMessage(self) -> QuantConnect.Algorithm.CSharp.qlnet.tools.OrderMessage:
        """This field is protected."""
        ...

    @property
    def SubscribeAllOptions(self) -> bool:
        """This field is protected."""
        ...

    @SubscribeAllOptions.setter
    def SubscribeAllOptions(self, value: bool):
        """This field is protected."""
        ...

    @property
    def SubscribeAllFutures(self) -> bool:
        """This field is protected."""
        ...

    @SubscribeAllFutures.setter
    def SubscribeAllFutures(self, value: bool):
        """This field is protected."""
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def LimitOrder(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, price: float, limitOrderType: QuantConnect.Orders.DeribitTimeInForce, tag: str = ...) -> QuantConnect.Orders.OrderTicket:
        """This method is protected."""
        ...

    def OnExpiry(self) -> None:
        ...

    def OnSymbolListed(self, symbols: typing.Any) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def TradingIsReady(self) -> bool:
        ...


class DeribitCombined(QuantConnect.Algorithm.CSharp.DeribitBaseAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def BidPriceWeight(self) -> float:
        ...

    @BidPriceWeight.setter
    def BidPriceWeight(self, value: float):
        ...

    @property
    def PutStrategyJsonPath(self) -> str:
        ...

    @PutStrategyJsonPath.setter
    def PutStrategyJsonPath(self, value: str):
        ...

    @property
    def SellCallStrategyJsonPath(self) -> str:
        ...

    @SellCallStrategyJsonPath.setter
    def SellCallStrategyJsonPath(self, value: str):
        ...

    @property
    def ShortVegaCallStrategyJsonPath(self) -> str:
        ...

    @ShortVegaCallStrategyJsonPath.setter
    def ShortVegaCallStrategyJsonPath(self, value: str):
        ...

    @property
    def ShortVegaPutStrategyJsonPath(self) -> str:
        ...

    @ShortVegaPutStrategyJsonPath.setter
    def ShortVegaPutStrategyJsonPath(self, value: str):
        ...

    @property
    def SpotRatio(self) -> float:
        ...

    @SpotRatio.setter
    def SpotRatio(self, value: float):
        ...

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def MinDeltaUpdateRatio(self) -> float:
        ...

    @MinDeltaUpdateRatio.setter
    def MinDeltaUpdateRatio(self, value: float):
        ...

    @property
    def OptionLotSize(self) -> float:
        ...

    @OptionLotSize.setter
    def OptionLotSize(self, value: float):
        ...

    @property
    def OptionCreateInterval(self) -> float:
        ...

    @OptionCreateInterval.setter
    def OptionCreateInterval(self, value: float):
        ...

    @property
    def OptionPositionReportInterval(self) -> float:
        ...

    @OptionPositionReportInterval.setter
    def OptionPositionReportInterval(self, value: float):
        ...

    @property
    def TotalTradeHours(self) -> float:
        ...

    @TotalTradeHours.setter
    def TotalTradeHours(self, value: float):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def HedgeLambda(self) -> float:
        ...

    @HedgeLambda.setter
    def HedgeLambda(self, value: float):
        ...

    @property
    def FilterLambda(self) -> float:
        ...

    @FilterLambda.setter
    def FilterLambda(self, value: float):
        ...

    @property
    def OutputDirectory(self) -> str:
        ...

    @OutputDirectory.setter
    def OutputDirectory(self, value: str):
        ...

    @property
    def SpotHedgeRange(self) -> float:
        ...

    @SpotHedgeRange.setter
    def SpotHedgeRange(self, value: float):
        ...

    @property
    def OptionHedgeRange(self) -> float:
        ...

    @OptionHedgeRange.setter
    def OptionHedgeRange(self, value: float):
        ...

    @property
    def TwapSeconds(self) -> float:
        ...

    @TwapSeconds.setter
    def TwapSeconds(self, value: float):
        ...

    @property
    def TwapCounts(self) -> int:
        ...

    @TwapCounts.setter
    def TwapCounts(self, value: int):
        ...

    @property
    def MaxTwapMinutes(self) -> float:
        ...

    @MaxTwapMinutes.setter
    def MaxTwapMinutes(self, value: float):
        ...

    @property
    def MinT2M(self) -> int:
        ...

    @MinT2M.setter
    def MinT2M(self, value: int):
        ...

    @property
    def MaxT2M(self) -> int:
        ...

    @MaxT2M.setter
    def MaxT2M(self, value: int):
        ...

    @property
    def SVMinT2M(self) -> int:
        ...

    @SVMinT2M.setter
    def SVMinT2M(self, value: int):
        ...

    @property
    def SVMaxT2M(self) -> int:
        ...

    @SVMaxT2M.setter
    def SVMaxT2M(self, value: int):
        ...

    @property
    def OptionTradeInterval(self) -> float:
        ...

    @OptionTradeInterval.setter
    def OptionTradeInterval(self, value: float):
        ...

    @property
    def PositionAllocationMode(self) -> QuantConnect.Statistics.PositionAllocationMode:
        ...

    @PositionAllocationMode.setter
    def PositionAllocationMode(self, value: QuantConnect.Statistics.PositionAllocationMode):
        ...

    @property
    def WriteAllOptionConditions(self) -> bool:
        ...

    @WriteAllOptionConditions.setter
    def WriteAllOptionConditions(self, value: bool):
        ...

    @property
    def MinStrikeRatio(self) -> float:
        ...

    @MinStrikeRatio.setter
    def MinStrikeRatio(self, value: float):
        ...

    @property
    def MaxStrikeRatio(self) -> float:
        ...

    @MaxStrikeRatio.setter
    def MaxStrikeRatio(self, value: float):
        ...

    @property
    def UseImpliedVolLimit(self) -> bool:
        ...

    @UseImpliedVolLimit.setter
    def UseImpliedVolLimit(self, value: bool):
        ...

    @property
    def MinOptionCostMode(self) -> QuantConnect.Statistics.MinOptionCostMode:
        ...

    @MinOptionCostMode.setter
    def MinOptionCostMode(self, value: QuantConnect.Statistics.MinOptionCostMode):
        ...

    @property
    def CostMultiplier(self) -> float:
        ...

    @CostMultiplier.setter
    def CostMultiplier(self, value: float):
        ...

    @property
    def MinCallStrike(self) -> float:
        ...

    @MinCallStrike.setter
    def MinCallStrike(self, value: float):
        ...

    @property
    def MaxCallStrike(self) -> float:
        ...

    @MaxCallStrike.setter
    def MaxCallStrike(self, value: float):
        ...

    @property
    def MinPutStrike(self) -> float:
        ...

    @MinPutStrike.setter
    def MinPutStrike(self, value: float):
        ...

    @property
    def MaxPutStrike(self) -> float:
        ...

    @MaxPutStrike.setter
    def MaxPutStrike(self, value: float):
        ...

    @property
    def MinThetaGammaRatio(self) -> float:
        ...

    @MinThetaGammaRatio.setter
    def MinThetaGammaRatio(self, value: float):
        ...

    @property
    def ShortVegaCallRatio(self) -> float:
        ...

    @ShortVegaCallRatio.setter
    def ShortVegaCallRatio(self, value: float):
        ...

    @property
    def ShortVegaPutRatio(self) -> float:
        ...

    @ShortVegaPutRatio.setter
    def ShortVegaPutRatio(self, value: float):
        ...

    @property
    def SellCallRatio(self) -> float:
        ...

    @SellCallRatio.setter
    def SellCallRatio(self, value: float):
        ...

    @property
    def MaxHedgeVolatility(self) -> float:
        ...

    @MaxHedgeVolatility.setter
    def MaxHedgeVolatility(self, value: float):
        ...

    @property
    def MinTwapVolume(self) -> float:
        ...

    @MinTwapVolume.setter
    def MinTwapVolume(self, value: float):
        ...

    @property
    def FuturesSymbol(self) -> QuantConnect.Symbol:
        """This field is protected."""
        ...

    @FuturesSymbol.setter
    def FuturesSymbol(self, value: QuantConnect.Symbol):
        """This field is protected."""
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        """This field is protected."""
        ...

    @OptionSymbol.setter
    def OptionSymbol(self, value: QuantConnect.Symbol):
        """This field is protected."""
        ...

    @property
    def PriceList(self) -> typing.Any:
        """This field is protected."""
        ...

    @PriceList.setter
    def PriceList(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def FuturesOrderManager(self) -> QuantConnect.Algorithm.CSharp.qlnet.tools.OrderManager:
        """This field is protected."""
        ...

    @FuturesOrderManager.setter
    def FuturesOrderManager(self, value: QuantConnect.Algorithm.CSharp.qlnet.tools.OrderManager):
        """This field is protected."""
        ...

    @property
    def TargetSellCallPosition(self) -> float:
        """This field is protected."""
        ...

    @TargetSellCallPosition.setter
    def TargetSellCallPosition(self, value: float):
        """This field is protected."""
        ...

    @property
    def TargetShortVegaCallPosition(self) -> float:
        """This field is protected."""
        ...

    @TargetShortVegaCallPosition.setter
    def TargetShortVegaCallPosition(self, value: float):
        """This field is protected."""
        ...

    @property
    def TargetShortVegaPutPosition(self) -> float:
        """This field is protected."""
        ...

    @TargetShortVegaPutPosition.setter
    def TargetShortVegaPutPosition(self, value: float):
        """This field is protected."""
        ...

    @property
    def SellCallOptions(self) -> typing.Any:
        """This field is protected."""
        ...

    @SellCallOptions.setter
    def SellCallOptions(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def ShortVegaCallOptions(self) -> typing.Any:
        """This field is protected."""
        ...

    @ShortVegaCallOptions.setter
    def ShortVegaCallOptions(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def ShortVegaPutOptions(self) -> typing.Any:
        """This field is protected."""
        ...

    @ShortVegaPutOptions.setter
    def ShortVegaPutOptions(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def FilterVolatilityEstimator(self) -> Calculators.Estimators.EWMAVolatilityEstimator:
        """This field is protected."""
        ...

    @FilterVolatilityEstimator.setter
    def FilterVolatilityEstimator(self, value: Calculators.Estimators.EWMAVolatilityEstimator):
        """This field is protected."""
        ...

    @property
    def CryptoSymbol(self) -> QuantConnect.Symbol:
        """This field is protected."""
        ...

    @CryptoSymbol.setter
    def CryptoSymbol(self, value: QuantConnect.Symbol):
        """This field is protected."""
        ...

    @property
    def IsBacktest(self) -> bool:
        """This field is protected."""
        ...

    @IsBacktest.setter
    def IsBacktest(self, value: bool):
        """This field is protected."""
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def __init__(self) -> None:
        ...

    def AddOptions(self, validContracts: typing.Any, sliceTime: typing.Any, options: typing.Any) -> None:
        """This method is protected."""
        ...

    def CalculateGreeks(self) -> None:
        """This method is protected."""
        ...

    def CalculateOptionValue(self, option: QuantConnect.Data.Market.OptionContract, sliceTime: typing.Any, sigma: float, t2M: float) -> float:
        """This method is protected."""
        ...

    def CalculateTargetPositions(self, contracts: typing.Any, targetPosition: float, totalPosition: float, options: typing.Any, minT2M: int, maxT2M: int) -> typing.Any:
        """This method is protected."""
        ...

    def CalculateThetaGammaRatio(self, option: QuantConnect.Data.Market.OptionContract, sliceTime: typing.Any, sigma: float) -> float:
        """This method is protected."""
        ...

    def Initialize(self) -> None:
        ...

    def NeedHedge(self, hedgeBase: float, tradeVolume: float) -> bool:
        """This method is protected."""
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOptionExpire(self) -> None:
        """This method is protected."""
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def PostInitialize(self) -> None:
        ...

    def ReportTargetPosition(self) -> None:
        """This method is protected."""
        ...

    def ResetOptionMaxTradeSize(self) -> None:
        """This method is protected."""
        ...

    def SetupCharts(self) -> None:
        """This method is protected."""
        ...

    def TimedPlotting(self) -> None:
        """This method is protected."""
        ...

    def TryAddNewSellCallOptions(self, optionChain: QuantConnect.Data.Market.OptionChain, sliceTime: typing.Any, sigma: float, validContracts: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """This method is protected."""
        ...

    def TryAddNewShortVegaCallOptions(self, optionChain: QuantConnect.Data.Market.OptionChain, sliceTime: typing.Any, sigma: float, validContracts: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """This method is protected."""
        ...

    def TryAddNewShortVegaPutOptions(self, optionChain: QuantConnect.Data.Market.OptionChain, sliceTime: typing.Any, sigma: float, validContracts: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """This method is protected."""
        ...

    def TryGetFuturesPrice(self, slice: QuantConnect.Data.Slice, price: typing.Optional[float]) -> typing.Union[bool, float]:
        """This method is protected."""
        ...

    def UpdatePrice(self) -> None:
        """This method is protected."""
        ...

    def UpdateSpotPosition(self) -> None:
        """This method is protected."""
        ...

    def WriteOutput(self) -> None:
        """This method is protected."""
        ...


class DeribitCombinedBacktest(QuantConnect.Algorithm.CSharp.DeribitCombined):
    """This class has no documentation."""

    @property
    def StartDate_(self) -> typing.Any:
        ...

    @StartDate_.setter
    def StartDate_(self, value: typing.Any):
        ...

    @property
    def EndDate_(self) -> typing.Any:
        ...

    @EndDate_.setter
    def EndDate_(self, value: typing.Any):
        ...

    @property
    def StartQuantity(self) -> float:
        ...

    @StartQuantity.setter
    def StartQuantity(self, value: float):
        ...

    @property
    def StartPrice(self) -> float:
        ...

    @StartPrice.setter
    def StartPrice(self, value: float):
        ...

    @property
    def FilterStartVolatility(self) -> float:
        ...

    @FilterStartVolatility.setter
    def FilterStartVolatility(self, value: float):
        ...

    @property
    def StatisticsSummaryPath(self) -> str:
        ...

    @StatisticsSummaryPath.setter
    def StatisticsSummaryPath(self, value: str):
        ...

    def Initialize(self) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnExpiry(self) -> None:
        ...

    def OnOptionExpire(self) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def TryGetFuturesPrice(self, slice: QuantConnect.Data.Slice, price: typing.Optional[float]) -> typing.Union[bool, float]:
        """This method is protected."""
        ...

    def UpdatePrice(self) -> None:
        """This method is protected."""
        ...

    def WriteOutput(self) -> None:
        """This method is protected."""
        ...


class DeribitAlgorithm(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def BidPriceWeight(self) -> float:
        ...

    @BidPriceWeight.setter
    def BidPriceWeight(self, value: float):
        ...

    @property
    def PutStrategyJsonPath(self) -> str:
        ...

    @PutStrategyJsonPath.setter
    def PutStrategyJsonPath(self, value: str):
        ...

    @property
    def CallStrategyJsonPath(self) -> str:
        ...

    @CallStrategyJsonPath.setter
    def CallStrategyJsonPath(self, value: str):
        ...

    @property
    def OptionRatio(self) -> float:
        ...

    @OptionRatio.setter
    def OptionRatio(self, value: float):
        ...

    @property
    def SpotRatio(self) -> float:
        ...

    @SpotRatio.setter
    def SpotRatio(self, value: float):
        ...

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def MinDeltaUpdateRatio(self) -> float:
        ...

    @MinDeltaUpdateRatio.setter
    def MinDeltaUpdateRatio(self, value: float):
        ...

    @property
    def OptionLotSize(self) -> float:
        ...

    @OptionLotSize.setter
    def OptionLotSize(self, value: float):
        ...

    @property
    def OptionCreateInterval(self) -> float:
        ...

    @OptionCreateInterval.setter
    def OptionCreateInterval(self, value: float):
        ...

    @property
    def OptionPositionReportInterval(self) -> float:
        ...

    @OptionPositionReportInterval.setter
    def OptionPositionReportInterval(self, value: float):
        ...

    @property
    def TotalTradeHours(self) -> float:
        ...

    @TotalTradeHours.setter
    def TotalTradeHours(self, value: float):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def HedgeLambda(self) -> float:
        ...

    @HedgeLambda.setter
    def HedgeLambda(self, value: float):
        ...

    @property
    def FilterLambda(self) -> float:
        ...

    @FilterLambda.setter
    def FilterLambda(self, value: float):
        ...

    @property
    def OutputDirectory(self) -> str:
        ...

    @OutputDirectory.setter
    def OutputDirectory(self, value: str):
        ...

    @property
    def SpotHedgeRange(self) -> float:
        ...

    @SpotHedgeRange.setter
    def SpotHedgeRange(self, value: float):
        ...

    @property
    def OptionHedgeRange(self) -> float:
        ...

    @OptionHedgeRange.setter
    def OptionHedgeRange(self, value: float):
        ...

    @property
    def TwapSeconds(self) -> float:
        ...

    @TwapSeconds.setter
    def TwapSeconds(self, value: float):
        ...

    @property
    def TwapCounts(self) -> int:
        ...

    @TwapCounts.setter
    def TwapCounts(self, value: int):
        ...

    @property
    def MaxTwapMinutes(self) -> float:
        ...

    @MaxTwapMinutes.setter
    def MaxTwapMinutes(self, value: float):
        ...

    @property
    def MinT2M(self) -> int:
        ...

    @MinT2M.setter
    def MinT2M(self, value: int):
        ...

    @property
    def MaxT2M(self) -> int:
        ...

    @MaxT2M.setter
    def MaxT2M(self, value: int):
        ...

    @property
    def OptionTradeInterval(self) -> float:
        ...

    @OptionTradeInterval.setter
    def OptionTradeInterval(self, value: float):
        ...

    @property
    def PositionAllocationMode(self) -> QuantConnect.Statistics.PositionAllocationMode:
        ...

    @PositionAllocationMode.setter
    def PositionAllocationMode(self, value: QuantConnect.Statistics.PositionAllocationMode):
        ...

    @property
    def WriteAllOptionConditions(self) -> bool:
        ...

    @WriteAllOptionConditions.setter
    def WriteAllOptionConditions(self, value: bool):
        ...

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def FuturesSymbol(self) -> QuantConnect.Symbol:
        """This field is protected."""
        ...

    @FuturesSymbol.setter
    def FuturesSymbol(self, value: QuantConnect.Symbol):
        """This field is protected."""
        ...

    @property
    def OptionSymbol(self) -> QuantConnect.Symbol:
        """This field is protected."""
        ...

    @OptionSymbol.setter
    def OptionSymbol(self, value: QuantConnect.Symbol):
        """This field is protected."""
        ...

    @property
    def PriceList(self) -> typing.Any:
        """This field is protected."""
        ...

    @PriceList.setter
    def PriceList(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def ImportantMessageKey(self) -> str:
        """This field is protected."""
        ...

    @ImportantMessageKey.setter
    def ImportantMessageKey(self, value: str):
        """This field is protected."""
        ...

    @property
    def ImportantMessageToken(self) -> str:
        """This field is protected."""
        ...

    @ImportantMessageToken.setter
    def ImportantMessageToken(self, value: str):
        """This field is protected."""
        ...

    @property
    def OrderMessage(self) -> QuantConnect.Algorithm.CSharp.qlnet.tools.OrderMessage:
        """This field is protected."""
        ...

    @OrderMessage.setter
    def OrderMessage(self, value: QuantConnect.Algorithm.CSharp.qlnet.tools.OrderMessage):
        """This field is protected."""
        ...

    @property
    def _futuresOrderManager(self) -> QuantConnect.Algorithm.CSharp.qlnet.tools.OrderManager:
        """This field is protected."""
        ...

    @_futuresOrderManager.setter
    def _futuresOrderManager(self, value: QuantConnect.Algorithm.CSharp.qlnet.tools.OrderManager):
        """This field is protected."""
        ...

    @property
    def TargetPosition(self) -> float:
        """This field is protected."""
        ...

    @TargetPosition.setter
    def TargetPosition(self, value: float):
        """This field is protected."""
        ...

    @property
    def CallOptions(self) -> typing.Any:
        """This field is protected."""
        ...

    @CallOptions.setter
    def CallOptions(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def LastOptionTradeTime(self) -> typing.Any:
        """This field is protected."""
        ...

    @LastOptionTradeTime.setter
    def LastOptionTradeTime(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def FilterVolatilityEstimator(self) -> Calculators.Estimators.EWMAVolatilityEstimator:
        """This field is protected."""
        ...

    @FilterVolatilityEstimator.setter
    def FilterVolatilityEstimator(self, value: Calculators.Estimators.EWMAVolatilityEstimator):
        """This field is protected."""
        ...

    @property
    def _putStrategies(self) -> typing.Any:
        """This field is protected."""
        ...

    @_putStrategies.setter
    def _putStrategies(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def _cryptoSymbol(self) -> QuantConnect.Symbol:
        """This field is protected."""
        ...

    @_cryptoSymbol.setter
    def _cryptoSymbol(self, value: QuantConnect.Symbol):
        """This field is protected."""
        ...

    @property
    def IsBacktest(self) -> bool:
        """This field is protected."""
        ...

    @IsBacktest.setter
    def IsBacktest(self, value: bool):
        """This field is protected."""
        ...

    @property
    def OptionMaxTradeSize(self) -> float:
        """This field is protected."""
        ...

    @OptionMaxTradeSize.setter
    def OptionMaxTradeSize(self, value: float):
        """This field is protected."""
        ...

    @property
    def BalanceNow(self) -> float:
        """This field is protected."""
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        """This field is protected."""
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def AddOptions(self, validContracts: typing.Any, sliceTime: typing.Any) -> None:
        """This method is protected."""
        ...

    def CalculateOptionValue(self, option: QuantConnect.Data.Market.OptionContract, sliceTime: typing.Any, sigma: float, t2M: float) -> float:
        """This method is protected."""
        ...

    def CalculateTargetPositions(self, contracts: typing.Any, targetPosition: float) -> typing.Any:
        """This method is protected."""
        ...

    def CalculateThetaGammaRatio(self, option: QuantConnect.Data.Market.OptionContract, sliceTime: typing.Any, sigma: float) -> float:
        """This method is protected."""
        ...

    def HedgeAllOptions(self) -> bool:
        """This method is protected."""
        ...

    def Initialize(self) -> None:
        ...

    def NeedHedge(self, hedgeBase: float, tradeVolume: float) -> bool:
        """This method is protected."""
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOptionExpire(self) -> None:
        """This method is protected."""
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnSymbolListed(self, symbols: typing.Any) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def PostInitialize(self) -> None:
        ...

    def ReportTargetPosition(self) -> None:
        """This method is protected."""
        ...

    def ResetOptionMaxTradeSize(self) -> None:
        """This method is protected."""
        ...

    def SetupCharts(self) -> None:
        """This method is protected."""
        ...

    def TimedPlotting(self) -> None:
        """This method is protected."""
        ...

    def TryAddNewOptions(self, optionChain: QuantConnect.Data.Market.OptionChain, sliceTime: typing.Any, sigma: float, validContracts: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """This method is protected."""
        ...

    def TryGetFuturesPrice(self, slice: QuantConnect.Data.Slice, price: typing.Optional[float]) -> typing.Union[bool, float]:
        """This method is protected."""
        ...

    def UpdatePrice(self) -> None:
        """This method is protected."""
        ...

    def UpdateSpotPosition(self) -> None:
        """This method is protected."""
        ...

    def WriteOutput(self) -> None:
        """This method is protected."""
        ...


class DeribitSellCall(QuantConnect.Algorithm.CSharp.DeribitAlgorithm):
    """This class has no documentation."""

    @property
    def MinStrikeRatio(self) -> float:
        ...

    @MinStrikeRatio.setter
    def MinStrikeRatio(self, value: float):
        ...

    @property
    def MaxStrikeRatio(self) -> float:
        ...

    @MaxStrikeRatio.setter
    def MaxStrikeRatio(self, value: float):
        ...

    @property
    def UseImpliedVolLimit(self) -> bool:
        ...

    @UseImpliedVolLimit.setter
    def UseImpliedVolLimit(self, value: bool):
        ...

    @property
    def MinOptionCostMode(self) -> QuantConnect.Statistics.MinOptionCostMode:
        ...

    @MinOptionCostMode.setter
    def MinOptionCostMode(self, value: QuantConnect.Statistics.MinOptionCostMode):
        ...

    @property
    def CostMultiplier(self) -> float:
        ...

    @CostMultiplier.setter
    def CostMultiplier(self, value: float):
        ...

    def HedgeAllOptions(self) -> bool:
        """This method is protected."""
        ...

    def TryAddNewOptions(self, optionChain: QuantConnect.Data.Market.OptionChain, sliceTime: typing.Any, sigma: float, validContracts: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """This method is protected."""
        ...


class DeribitSellCallBacktest(QuantConnect.Algorithm.CSharp.DeribitSellCall):
    """This class has no documentation."""

    @property
    def StartDate_(self) -> datetime.datetime:
        ...

    @StartDate_.setter
    def StartDate_(self, value: datetime.datetime):
        ...

    @property
    def EndDate_(self) -> datetime.datetime:
        ...

    @EndDate_.setter
    def EndDate_(self, value: datetime.datetime):
        ...

    @property
    def StartQuantity(self) -> float:
        ...

    @StartQuantity.setter
    def StartQuantity(self, value: float):
        ...

    @property
    def StartPrice(self) -> float:
        ...

    @StartPrice.setter
    def StartPrice(self, value: float):
        ...

    @property
    def FilterStartVolatility(self) -> float:
        ...

    @FilterStartVolatility.setter
    def FilterStartVolatility(self, value: float):
        ...

    def Initialize(self) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOptionExpire(self) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def PostInitialize(self) -> None:
        ...

    def TryGetFuturesPrice(self, slice: QuantConnect.Data.Slice, price: typing.Optional[float]) -> typing.Union[bool, float]:
        """This method is protected."""
        ...

    def UpdatePrice(self) -> None:
        """This method is protected."""
        ...

    def WriteOutput(self) -> None:
        """This method is protected."""
        ...


class DeribitShortVegaCall(QuantConnect.Algorithm.CSharp.DeribitAlgorithm):
    """This class has no documentation."""

    @property
    def MinCallStrike(self) -> float:
        ...

    @MinCallStrike.setter
    def MinCallStrike(self, value: float):
        ...

    @property
    def MaxCallStrike(self) -> float:
        ...

    @MaxCallStrike.setter
    def MaxCallStrike(self, value: float):
        ...

    @property
    def UseImpliedVolLimit(self) -> bool:
        ...

    @UseImpliedVolLimit.setter
    def UseImpliedVolLimit(self, value: bool):
        ...

    @property
    def MinThetaGammaRatio(self) -> float:
        ...

    @MinThetaGammaRatio.setter
    def MinThetaGammaRatio(self, value: float):
        ...

    def HedgeAllOptions(self) -> bool:
        """This method is protected."""
        ...

    def TryAddNewOptions(self, optionChain: QuantConnect.Data.Market.OptionChain, sliceTime: typing.Any, sigma: float, validContracts: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """This method is protected."""
        ...


class DeribitShortVegaCallBacktest(QuantConnect.Algorithm.CSharp.DeribitShortVegaCall):
    """This class has no documentation."""

    @property
    def StartDate_(self) -> typing.Any:
        ...

    @StartDate_.setter
    def StartDate_(self, value: typing.Any):
        ...

    @property
    def EndDate_(self) -> typing.Any:
        ...

    @EndDate_.setter
    def EndDate_(self, value: typing.Any):
        ...

    @property
    def StartQuantity(self) -> float:
        ...

    @StartQuantity.setter
    def StartQuantity(self, value: float):
        ...

    @property
    def StartPrice(self) -> float:
        ...

    @StartPrice.setter
    def StartPrice(self, value: float):
        ...

    @property
    def FilterStartVolatility(self) -> float:
        ...

    @FilterStartVolatility.setter
    def FilterStartVolatility(self, value: float):
        ...

    def Initialize(self) -> None:
        ...

    def OnEndOfAlgorithm(self) -> None:
        ...

    def OnOptionExpire(self) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def PostInitialize(self) -> None:
        ...

    def TryGetFuturesPrice(self, slice: QuantConnect.Data.Slice, price: typing.Optional[float]) -> typing.Union[bool, float]:
        """This method is protected."""
        ...

    def UpdatePrice(self) -> None:
        """This method is protected."""
        ...

    def WriteOutput(self) -> None:
        """This method is protected."""
        ...


class ZYDeltaCollarLiveBinanceBacktesting(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    datelist: typing.Any = ...

    tradesymbol: str = "ETH"

    _endOfDay: typing.Any = ...

    @property
    def _accountName(self) -> str:
        ...

    @_accountName.setter
    def _accountName(self, value: str):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...


class ClearPositionsBase(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def Coins(self) -> typing.Any:
        """This field is protected."""
        ...

    @Coins.setter
    def Coins(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def Underlyings(self) -> typing.Any:
        """This field is protected."""
        ...

    @Underlyings.setter
    def Underlyings(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def DeltaTraders(self) -> typing.Any:
        """This field is protected."""
        ...

    @DeltaTraders.setter
    def DeltaTraders(self, value: typing.Any):
        """This field is protected."""
        ...

    @property
    def TwapTradesInInterval(self) -> int:
        """This field is protected."""
        ...

    @TwapTradesInInterval.setter
    def TwapTradesInInterval(self, value: int):
        """This field is protected."""
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...


class BinanceClearPositions(QuantConnect.Algorithm.CSharp.ClearPositionsBase):
    """This class has no documentation."""

    def Initialize(self) -> None:
        ...


class BinanceCloseSpot(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def _accountName(self) -> str:
        ...

    @_accountName.setter
    def _accountName(self, value: str):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...


class DeltaCollarLiveBinance(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def UseBolling(self) -> bool:
        ...

    @UseBolling.setter
    def UseBolling(self, value: bool):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnTransferCompleted(self, amount: float, type: QuantConnect.ABL.UserTransferType, currency: str) -> None:
        """This method is protected."""
        ...

    def OnTransferFailed(self, amount: float, type: QuantConnect.ABL.UserTransferType, currency: str, error: str) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def TryTradeClosing(self, time: typing.Union[datetime.datetime, datetime.date]) -> bool:
        ...


class DeltaCollarLiveBinanceBear(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveBinanceLeverage(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveBinanceSigma(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def _accountName(self) -> str:
        ...

    @_accountName.setter
    def _accountName(self, value: str):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnTransferCompleted(self, amount: float, type: QuantConnect.ABL.UserTransferType, currency: str) -> None:
        """This method is protected."""
        ...

    def OnTransferFailed(self, amount: float, type: QuantConnect.ABL.UserTransferType, currency: str, error: str) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...

    def TryTradeClosing(self, time: typing.Union[datetime.datetime, datetime.date]) -> bool:
        ...


class DeltaCollarLiveFTX(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXBear(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXDeltaDecay(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def UsdBolling(self) -> bool:
        ...

    @UsdBolling.setter
    def UsdBolling(self, value: bool):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXLeverage(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXNew(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXOption(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def CallJsonPath(self) -> str:
        ...

    @CallJsonPath.setter
    def CallJsonPath(self, value: str):
        ...

    @property
    def PutJsonPathsString(self) -> str:
        ...

    @PutJsonPathsString.setter
    def PutJsonPathsString(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def OptionRatio(self) -> float:
        ...

    @OptionRatio.setter
    def OptionRatio(self, value: float):
        ...

    @property
    def QuotePriceHistoryFile(self) -> str:
        ...

    @QuotePriceHistoryFile.setter
    def QuotePriceHistoryFile(self, value: str):
        ...

    @property
    def MinStrike(self) -> float:
        ...

    @MinStrike.setter
    def MinStrike(self, value: float):
        ...

    @property
    def CostMultiplier(self) -> float:
        ...

    @CostMultiplier.setter
    def CostMultiplier(self, value: float):
        ...

    @property
    def MinOptionCostMode(self) -> QuantConnect.Statistics.MinOptionCostMode:
        ...

    @MinOptionCostMode.setter
    def MinOptionCostMode(self, value: QuantConnect.Statistics.MinOptionCostMode):
        ...

    @property
    def UseImpliedVolLimit(self) -> bool:
        ...

    @UseImpliedVolLimit.setter
    def UseImpliedVolLimit(self, value: bool):
        ...

    @property
    def OptionPositionUpdateInvertal(self) -> float:
        ...

    @OptionPositionUpdateInvertal.setter
    def OptionPositionUpdateInvertal(self, value: float):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXOptionNew(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def CallJsonPath(self) -> str:
        ...

    @CallJsonPath.setter
    def CallJsonPath(self, value: str):
        ...

    @property
    def PutJsonPathsString(self) -> str:
        ...

    @PutJsonPathsString.setter
    def PutJsonPathsString(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def OptionRatio(self) -> float:
        ...

    @OptionRatio.setter
    def OptionRatio(self, value: float):
        ...

    @property
    def QuotePriceHistoryFile(self) -> str:
        ...

    @QuotePriceHistoryFile.setter
    def QuotePriceHistoryFile(self, value: str):
        ...

    @property
    def MinStrike(self) -> float:
        ...

    @MinStrike.setter
    def MinStrike(self, value: float):
        ...

    @property
    def CostMultiplier(self) -> float:
        ...

    @CostMultiplier.setter
    def CostMultiplier(self, value: float):
        ...

    @property
    def MinOptionCostMode(self) -> QuantConnect.Statistics.MinOptionCostMode:
        ...

    @MinOptionCostMode.setter
    def MinOptionCostMode(self, value: QuantConnect.Statistics.MinOptionCostMode):
        ...

    @property
    def UseImpliedVolLimit(self) -> bool:
        ...

    @UseImpliedVolLimit.setter
    def UseImpliedVolLimit(self, value: bool):
        ...

    @property
    def OptionPositionUpdateInvertal(self) -> float:
        ...

    @OptionPositionUpdateInvertal.setter
    def OptionPositionUpdateInvertal(self, value: float):
        ...

    @property
    def MaxStrike(self) -> float:
        ...

    @MaxStrike.setter
    def MaxStrike(self, value: float):
        ...

    @property
    def TotalStrikes(self) -> int:
        ...

    @TotalStrikes.setter
    def TotalStrikes(self, value: int):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def HedgeLambda(self) -> float:
        ...

    @HedgeLambda.setter
    def HedgeLambda(self, value: float):
        ...

    @property
    def FilterLambda(self) -> float:
        ...

    @FilterLambda.setter
    def FilterLambda(self, value: float):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXPutOnly(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def UsdBolling(self) -> bool:
        ...

    @UsdBolling.setter
    def UsdBolling(self, value: bool):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXSigma(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def UsdBolling(self) -> bool:
        ...

    @UsdBolling.setter
    def UsdBolling(self, value: bool):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXStopLoss(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def StopLossConfigPath(self) -> str:
        ...

    @StopLossConfigPath.setter
    def StopLossConfigPath(self, value: str):
        ...

    @property
    def MaxLossRatio(self) -> float:
        ...

    @MaxLossRatio.setter
    def MaxLossRatio(self, value: float):
        ...

    @property
    def MaxVentureDays(self) -> int:
        ...

    @MaxVentureDays.setter
    def MaxVentureDays(self, value: int):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeltaCollarLiveFTXStopWin(QuantConnect.Algorithm.FTXQCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def FutureUSDRatio(self) -> float:
        ...

    @FutureUSDRatio.setter
    def FutureUSDRatio(self, value: float):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def JsonPath(self) -> str:
        ...

    @JsonPath.setter
    def JsonPath(self, value: str):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    @property
    def MinInitialMarginFraction(self) -> float:
        ...

    @MinInitialMarginFraction.setter
    def MinInitialMarginFraction(self, value: float):
        ...

    @property
    def RiskControlMultiplier(self) -> float:
        ...

    @RiskControlMultiplier.setter
    def RiskControlMultiplier(self, value: float):
        ...

    @property
    def WarmUpResulotion(self) -> QuantConnect.Resolution:
        ...

    @WarmUpResulotion.setter
    def WarmUpResulotion(self, value: QuantConnect.Resolution):
        ...

    @property
    def WarmUpPeriods(self) -> float:
        ...

    @WarmUpPeriods.setter
    def WarmUpPeriods(self, value: float):
        ...

    @property
    def Lambda(self) -> float:
        ...

    @Lambda.setter
    def Lambda(self, value: float):
        ...

    @property
    def FtxSubAccount(self) -> str:
        ...

    @FtxSubAccount.setter
    def FtxSubAccount(self, value: str):
        ...

    @property
    def FtxApiKey(self) -> str:
        ...

    @FtxApiKey.setter
    def FtxApiKey(self, value: str):
        ...

    @property
    def FtxApiToken(self) -> str:
        ...

    @FtxApiToken.setter
    def FtxApiToken(self, value: str):
        ...

    @property
    def MarginCheckFrequency(self) -> float:
        ...

    @MarginCheckFrequency.setter
    def MarginCheckFrequency(self, value: float):
        ...

    @property
    def MarginBearRatio(self) -> float:
        ...

    @MarginBearRatio.setter
    def MarginBearRatio(self, value: float):
        ...

    @property
    def AutoCloseRatio(self) -> float:
        ...

    @AutoCloseRatio.setter
    def AutoCloseRatio(self, value: float):
        ...

    @property
    def AssetAllocationConfigFile(self) -> str:
        ...

    @AssetAllocationConfigFile.setter
    def AssetAllocationConfigFile(self, value: str):
        ...

    @property
    def _isFirstRuns(self) -> typing.Any:
        ...

    @_isFirstRuns.setter
    def _isFirstRuns(self, value: typing.Any):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...

    def OnRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeribitCalendarSpread(QuantConnect.Algorithm.CSharp.DeribitBaseAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def DeribitTradeConfigPath(self) -> str:
        ...

    @DeribitTradeConfigPath.setter
    def DeribitTradeConfigPath(self, value: str):
        ...

    @property
    def EstimatedTradingCosts(self) -> float:
        ...

    @EstimatedTradingCosts.setter
    def EstimatedTradingCosts(self, value: float):
        ...

    @property
    def PerpetualTradeInterval(self) -> float:
        ...

    @PerpetualTradeInterval.setter
    def PerpetualTradeInterval(self, value: float):
        ...

    @property
    def ConfigReadInterval(self) -> float:
        ...

    @ConfigReadInterval.setter
    def ConfigReadInterval(self, value: float):
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnSymbolListed(self, symbols: typing.Any) -> None:
        """This method is protected."""
        ...

    def OnWarmupFinished(self) -> None:
        ...


class DeribitPutCallParity(QuantConnect.Algorithm.CSharp.DeribitBaseAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def PutCallParityJsonPath(self) -> str:
        ...

    @PutCallParityJsonPath.setter
    def PutCallParityJsonPath(self, value: str):
        ...

    @property
    def DeribitTradeConfigPath(self) -> str:
        ...

    @DeribitTradeConfigPath.setter
    def DeribitTradeConfigPath(self, value: str):
        ...

    @property
    def EstimatedTradingCosts(self) -> float:
        ...

    @EstimatedTradingCosts.setter
    def EstimatedTradingCosts(self, value: float):
        ...

    @property
    def FuturesTradeInterval(self) -> float:
        ...

    @FuturesTradeInterval.setter
    def FuturesTradeInterval(self, value: float):
        ...

    @property
    def OptionTradeInterval(self) -> float:
        ...

    @OptionTradeInterval.setter
    def OptionTradeInterval(self, value: float):
        ...

    @property
    def MaxTradableProfit(self) -> float:
        ...

    @MaxTradableProfit.setter
    def MaxTradableProfit(self, value: float):
        ...

    @property
    def MaxCloseCost(self) -> float:
        ...

    @MaxCloseCost.setter
    def MaxCloseCost(self, value: float):
        ...

    @property
    def SingleSideOptionsPath(self) -> str:
        ...

    @SingleSideOptionsPath.setter
    def SingleSideOptionsPath(self, value: str):
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def OnProgramExit(self) -> None:
        """This method is protected."""
        ...


class DeribitStraddle(QuantConnect.Algorithm.QCAlgorithm, QuantConnect.Interfaces.IRegressionAlgorithmDefinition):
    """This class has no documentation."""

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def StraddleJsonPath(self) -> str:
        ...

    @StraddleJsonPath.setter
    def StraddleJsonPath(self, value: str):
        ...

    @property
    def StraddleSpotRatio(self) -> float:
        ...

    @StraddleSpotRatio.setter
    def StraddleSpotRatio(self, value: float):
        ...

    @property
    def RegularMessageKey(self) -> str:
        ...

    @RegularMessageKey.setter
    def RegularMessageKey(self, value: str):
        ...

    @property
    def RegularMessageToken(self) -> str:
        ...

    @RegularMessageToken.setter
    def RegularMessageToken(self, value: str):
        ...

    @property
    def BidPriceWeight(self) -> float:
        ...

    @BidPriceWeight.setter
    def BidPriceWeight(self, value: float):
        ...

    @property
    def MinCallStrike(self) -> float:
        ...

    @MinCallStrike.setter
    def MinCallStrike(self, value: float):
        ...

    @property
    def MaxCallStrike(self) -> float:
        ...

    @MaxCallStrike.setter
    def MaxCallStrike(self, value: float):
        ...

    @property
    def MinPutStrike(self) -> float:
        ...

    @MinPutStrike.setter
    def MinPutStrike(self, value: float):
        ...

    @property
    def MaxPutStrike(self) -> float:
        ...

    @MaxPutStrike.setter
    def MaxPutStrike(self, value: float):
        ...

    @property
    def PortfolioManagerName(self) -> str:
        ...

    @property
    def CanRunLocally(self) -> bool:
        """This is used by the regression test system to indicate if the open source Lean repository has the required data to run this algorithm."""
        ...

    @property
    def Languages(self) -> typing.List[QuantConnect.Language]:
        """This is used by the regression test system to indicate which languages this algorithm is written in."""
        ...

    @property
    def ExpectedStatistics(self) -> typing.Any:
        """This is used by the regression test system to indicate what the expected statistics are from running the algorithm"""
        ...

    def Initialize(self) -> None:
        ...

    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...


class FTXClearPositions(QuantConnect.Algorithm.CSharp.ClearPositionsBase):
    """This class has no documentation."""

    @property
    def EnableMarginTrading(self) -> bool:
        ...

    @EnableMarginTrading.setter
    def EnableMarginTrading(self, value: bool):
        ...

    @property
    def FTXCollateralConfig(self) -> str:
        ...

    @FTXCollateralConfig.setter
    def FTXCollateralConfig(self, value: str):
        ...

    def Initialize(self) -> None:
        ...


