from typing import overload
import typing

import QuantConnect
import QuantConnect.Algorithm.CSharp.LiveStrategy.DataType
import QuantConnect.Algorithm.CSharp.qlnet.tools
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Securities
import QuantConnect.Statistics
import System
import System.Collections.Concurrent


class DeltaTrader(System.Object):
    """This class has no documentation."""

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @property
    def CryptoSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def FuturesSymbol(self) -> QuantConnect.Symbol:
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying, market: str, marketOrder: typing.Any, limitOrder: typing.Any, stopLimitOrder: typing.Any, getOpenOrders: typing.Any, getOrderTicket: typing.Any, getOrderById: typing.Any, futureSymbol: typing.Union[QuantConnect.Symbol, str], cryptoSymbol: typing.Union[QuantConnect.Symbol, str], enableMarginTrading: bool = False) -> None:
        ...

    def CreateClosingTwap(self, tradeVolume: float) -> None:
        ...

    def CreateTwaps(self, targetDelta: float, securities: QuantConnect.Securities.SecurityManager, cashBook: QuantConnect.Securities.CashBook, time: typing.Any, balanceNow: float, quoteCurrencyForSpotOnly: float, actionRequiredMessages: typing.Any, response: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def GetLeftTwapVolume(self, securities: QuantConnect.Securities.SecurityManager) -> float:
        ...

    def IsClosing(self) -> bool:
        ...

    def IsTrading(self) -> bool:
        ...

    def ManageOrders(self, utcNow: typing.Any) -> None:
        ...

    def ProcessOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def TradeClosingTwap(self, time: typing.Any, security: QuantConnect.Securities.Security, response: typing.Optional[str]) -> typing.Union[bool, str]:
        ...

    def TradeTwaps(self, time: typing.Any, securities: QuantConnect.Securities.SecurityManager) -> bool:
        ...


class DeribitOptionTrader(System.Object):
    """This class has no documentation."""

    class PriceType(System.Enum):
        """This class has no documentation."""

        MidPrice = 0

        QuarterPrice = 1

        CounterPartyPrice = 2

    @property
    def Contract(self) -> QuantConnect.Data.Market.OptionContract:
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...

    @property
    def Status(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Statistics.OptionStatus enum."""
        ...

    @Status.setter
    def Status(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Statistics.OptionStatus enum."""
        ...

    @property
    def OrderId(self) -> int:
        ...

    @OrderId.setter
    def OrderId(self, value: int):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def TradePrice(self) -> float:
        ...

    @TradePrice.setter
    def TradePrice(self, value: float):
        ...

    @property
    def HedgeRange(self) -> float:
        ...

    @HedgeRange.setter
    def HedgeRange(self, value: float):
        ...

    @property
    def LastCheckTime(self) -> typing.Any:
        ...

    @LastCheckTime.setter
    def LastCheckTime(self, value: typing.Any):
        ...

    @property
    def StartHedgeTime(self) -> typing.Any:
        ...

    @StartHedgeTime.setter
    def StartHedgeTime(self, value: typing.Any):
        ...

    @overload
    def __init__(self, contract: QuantConnect.Data.Market.OptionContract, quantity: float, midPrice: float, markPrice: float, bidPrice: float, askPrice: float, minPrice: float, lotSize: float, transactions: QuantConnect.Securities.SecurityTransactionManager, dingKey: str, dingToken: str, limitOrder: typing.Any, hedgeRange: float, sliceTime: typing.Any, minPriceVariation: float) -> None:
        ...

    @overload
    def __init__(self, contract: QuantConnect.Data.Market.OptionContract, quantity: float, transactions: QuantConnect.Securities.SecurityTransactionManager, status: QuantConnect.Statistics.OptionStatus, tradedVolume: float, lotSize: float, limitOrder: typing.Any, dingKey: str, dingToken: str, hedgeRange: float, sliceTime: typing.Any, minPriceVariation: float) -> None:
        ...

    def CalculateDelta(self, underlyingPrice: float, q: float, r: float, sigma: float, sliceTime: typing.Any, hedgeAll: bool) -> float:
        ...

    def CancelOrder(self, sliceTime: typing.Any) -> None:
        ...

    def GetTradedVolume(self) -> float:
        ...

    def NeedHedge(self) -> bool:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def SetPrices(self, midPrice: float, markPrice: float, bidPrice: float, askPrice: float, minPrice: float) -> None:
        ...

    def ToString(self) -> str:
        ...

    def TradeNext(self) -> None:
        ...

    def TryAdd(self, option: QuantConnect.Algorithm.CSharp.qlnet.tools.DeribitOptionTrader) -> bool:
        ...


class MyOrder(System.Object):
    """This class has no documentation."""

    @property
    def TradeSymbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def TargetVolume(self) -> float:
        ...

    @property
    def FilledVolume(self) -> float:
        ...

    @FilledVolume.setter
    def FilledVolume(self, value: float):
        ...

    @property
    def OrderType(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Orders.OrderType enum."""
        ...

    @property
    def OrderStatus(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Orders.OrderStatus enum."""
        ...

    @OrderStatus.setter
    def OrderStatus(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Orders.OrderStatus enum."""
        ...

    @property
    def Finished(self) -> bool:
        ...

    @Finished.setter
    def Finished(self, value: bool):
        ...

    @property
    def OrderID(self) -> int:
        ...

    @OrderID.setter
    def OrderID(self, value: int):
        ...

    @property
    def StopPrice(self) -> float:
        ...

    @property
    def LimitPrice(self) -> float:
        ...

    @property
    def OrderProperties(self) -> QuantConnect.Interfaces.IOrderProperties:
        ...

    def __init__(self, tradeSymbol: typing.Union[QuantConnect.Symbol, str], targetVolume: float, orderType: QuantConnect.Orders.OrderType, limitPrice: float = 0, stopPrice: float = 0) -> None:
        ...


class OrderManager(System.Object):
    """This class has no documentation."""

    @property
    def LocalOrders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Algorithm.CSharp.qlnet.tools.MyOrder]:
        ...

    @LocalOrders.setter
    def LocalOrders(self, value: System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Algorithm.CSharp.qlnet.tools.MyOrder]):
        ...

    @property
    def BrokerOrders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]:
        ...

    @BrokerOrders.setter
    def BrokerOrders(self, value: System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]):
        ...

    @property
    def TempOrders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]:
        ...

    @TempOrders.setter
    def TempOrders(self, value: System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]):
        ...

    def __init__(self, coinSymbol: typing.Union[QuantConnect.Symbol, str], marketOrder: typing.Any, limitOrder: typing.Any, stopLimitOrder: typing.Any, getOpenOrders: typing.Any, getOrderTicket: typing.Any, getOrderById: typing.Any) -> None:
        """创建订单管理实例"""
        ...

    def AddOrder(self, tradeSymbol: typing.Union[QuantConnect.Symbol, str], targetVolume: float, orderType: QuantConnect.Orders.OrderType, limitPrice: float = 0, stopPrice: float = 0) -> int:
        """添加期权order"""
        ...

    def CheckOrder(self) -> bool:
        """检查策略记录的订单和broker返回的订单是否一致"""
        ...

    def HasOpenOrder(self) -> bool:
        """检查是否有open order"""
        ...

    def ManageOrder(self, now: typing.Any) -> None:
        """处理所有的order"""
        ...

    def SubmitOrder(self, order: QuantConnect.Algorithm.CSharp.qlnet.tools.MyOrder) -> int:
        """提交期货order"""
        ...

    def UpdateOrder(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """用orderevent对order信息进行更新"""
        ...


class OrderMessage(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    def SendMessage(self, message: str, key: str, messageKey: str = ...) -> None:
        ...


class PositionManager(System.Object):
    """This class has no documentation."""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        ...

    @Symbol.setter
    def Symbol(self, value: QuantConnect.Symbol):
        ...

    def __init__(self, virtualPosition: float, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """创建仓位管理实例"""
        ...

    def AddPosition(self, vol: float) -> None:
        """在添加order时增加虚拟持仓"""
        ...

    def CheckPosition(self) -> bool:
        """检查策略记录的订单和broker返回的订单是否一致"""
        ...

    def ManagePosition(self, currentPosition: float) -> None:
        """处理现有的position"""
        ...

    def UpdatePosition(self, orderEvent: QuantConnect.Orders.OrderEvent, order: QuantConnect.Orders.Order) -> None:
        """用orderevent对position信息进行更新"""
        ...


class Utils(System.Object):
    """This class has no documentation."""

    class MoveStrikeType(System.Enum):
        """This class has no documentation."""

        MoveDownCashGamma = -1

        MoveBothCashGamma = 0

        MoveUpCashGamma = 1

    class OptionParityTradeMode(System.Enum):
        """This class has no documentation."""

        BuyBoth = 0

        OnlyBuyOTM = 1

        OnlyBuyITM = 2

    @staticmethod
    def CalculateMinOptionCost(mode: QuantConnect.Statistics.MinOptionCostMode, t2MDays: float, costMultiplier: float, underlyingPrice: float, strike: float, sigmaAddition: float, sigma: float) -> float:
        ...

    @staticmethod
    def RoundTradeVolume(tradeVolume: float, lotSize: float) -> float:
        ...

    @staticmethod
    def Sqrt(x: float, epsilon: float = ...) -> float:
        ...

    @staticmethod
    def Var(v: typing.Any) -> float:
        ...


