from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm.CSharp.qlnet.AlgoTrade
import QuantConnect.Algorithm.CSharp.qlnet.tools
import QuantConnect.Orders
import QuantConnect.Securities
import System


class OptionTwap(System.Object):
    """This class has no documentation."""

    class PriceType(System.Enum):
        """This class has no documentation."""

        MidPrice = 0

        QuoterPrice = 1

        CounterPartyPrice = 2

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        ...

    @property
    def OrderId(self) -> int:
        ...

    @OrderId.setter
    def OrderId(self, value: int):
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], targetVolume: float, transactions: QuantConnect.Securities.SecurityTransactionManager, totalSeconds: float, interval: float, bidPriceWeight: float, bidPrice: float, askPrice: float, minPrice: float, limitOrder: typing.Any, dingKey: str, dingToken: str, lotSize: float = 1) -> None:
        ...

    def IsFinished(self) -> bool:
        ...

    def OnOrderEvent(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        ...

    def ToString(self) -> str:
        ...

    def UpdatePrices(self, bidPriceWeight: float, bidPrice: float, askPrice: float, minPrice: float) -> None:
        ...


class Twap(System.Object):
    """This class has no documentation."""

    @property
    def IsFinished(self) -> bool:
        ...

    @IsFinished.setter
    def IsFinished(self, value: bool):
        ...

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        ...

    def __init__(self, om: QuantConnect.Algorithm.CSharp.qlnet.tools.OrderManager, symbol: typing.Union[QuantConnect.Symbol, str], target_vol: float, order_type: QuantConnect.Orders.OrderType, totalseconds: float, count: int) -> None:
        ...

    def CurrentLeftVolume(self) -> float:
        ...

    def TwapTrade(self, sliceTime: typing.Union[datetime.datetime, datetime.date], security: QuantConnect.Securities.Security, getOrderById: typing.Any) -> bool:
        ...

    def UpdateTwapStatus(self, security: QuantConnect.Securities.Security, getOrderById: typing.Any) -> None:
        ...


