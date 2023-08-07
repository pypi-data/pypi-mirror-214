from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.OptionQuote
import QuantConnect.Orders
import System
import System.Collections.Generic


class OptionInfo(System.Object):
    """This class has no documentation."""

    @property
    def Underlying(self) -> str:
        ...

    @Underlying.setter
    def Underlying(self, value: str):
        ...

    @property
    def Type(self) -> QuantConnect.OptionRight:
        ...

    @Type.setter
    def Type(self, value: QuantConnect.OptionRight):
        ...

    @property
    def Strike(self) -> float:
        ...

    @Strike.setter
    def Strike(self, value: float):
        ...

    @property
    def Expiry(self) -> datetime.datetime:
        ...

    @Expiry.setter
    def Expiry(self, value: datetime.datetime):
        ...

    def Parse(self, symbol: str) -> None:
        ...

    @staticmethod
    def ParseExpiry(expiry: str) -> datetime.datetime:
        ...

    def ToString(self) -> str:
        ...


class OptionFill(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Option(self) -> QuantConnect.OptionQuote.OptionInfo:
        ...

    @Option.setter
    def Option(self, value: QuantConnect.OptionQuote.OptionInfo):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def Liquidity(self) -> str:
        """taker or maker"""
        ...

    @Liquidity.setter
    def Liquidity(self, value: str):
        """taker or maker"""
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def FeeRate(self) -> float:
        ...

    @FeeRate.setter
    def FeeRate(self, value: float):
        ...

    @property
    def Side(self) -> QuantConnect.Orders.OrderDirection:
        ...

    @Side.setter
    def Side(self, value: QuantConnect.Orders.OrderDirection):
        ...


class OptionPosition(System.Object):
    """This class has no documentation."""

    @property
    def NetSize(self) -> float:
        ...

    @NetSize.setter
    def NetSize(self, value: float):
        ...

    @property
    def EntryPrice(self) -> float:
        ...

    @EntryPrice.setter
    def EntryPrice(self, value: float):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Option(self) -> QuantConnect.OptionQuote.OptionInfo:
        ...

    @Option.setter
    def Option(self, value: QuantConnect.OptionQuote.OptionInfo):
        ...

    @property
    def Side(self) -> QuantConnect.Orders.OrderDirection:
        ...

    @Side.setter
    def Side(self, value: QuantConnect.Orders.OrderDirection):
        ...

    @property
    def PessimisticValuation(self) -> typing.Optional[float]:
        ...

    @PessimisticValuation.setter
    def PessimisticValuation(self, value: typing.Optional[float]):
        ...

    @property
    def PessimisticIndexPrice(self) -> typing.Optional[float]:
        ...

    @PessimisticIndexPrice.setter
    def PessimisticIndexPrice(self, value: typing.Optional[float]):
        ...

    @property
    def PessimisticVol(self) -> typing.Optional[float]:
        ...

    @PessimisticVol.setter
    def PessimisticVol(self, value: typing.Optional[float]):
        ...

    def ToString(self) -> str:
        ...


class Quote(System.Object):
    """This class has no documentation."""

    @property
    def Collateral(self) -> float:
        ...

    @Collateral.setter
    def Collateral(self, value: float):
        ...

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Option(self) -> QuantConnect.OptionQuote.OptionInfo:
        ...

    @Option.setter
    def Option(self, value: QuantConnect.OptionQuote.OptionInfo):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def QuoteExpiry(self) -> typing.Optional[datetime.datetime]:
        ...

    @QuoteExpiry.setter
    def QuoteExpiry(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def QuoterSide(self) -> typing.Optional[QuantConnect.Orders.OrderDirection]:
        ...

    @QuoterSide.setter
    def QuoterSide(self, value: typing.Optional[QuantConnect.Orders.OrderDirection]):
        ...

    @property
    def RequestId(self) -> typing.Optional[int]:
        ...

    @RequestId.setter
    def RequestId(self, value: typing.Optional[int]):
        ...

    @property
    def RequestSide(self) -> typing.Optional[QuantConnect.Orders.OrderDirection]:
        ...

    @RequestSide.setter
    def RequestSide(self, value: typing.Optional[QuantConnect.Orders.OrderDirection]):
        ...

    @property
    def Size(self) -> typing.Optional[float]:
        ...

    @Size.setter
    def Size(self, value: typing.Optional[float]):
        ...

    @property
    def Status(self) -> QuantConnect.Orders.OrderStatus:
        ...

    @Status.setter
    def Status(self, value: QuantConnect.Orders.OrderStatus):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    def ToString(self) -> str:
        ...


class QuoteRequest(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Option(self) -> QuantConnect.OptionQuote.OptionInfo:
        ...

    @Option.setter
    def Option(self, value: QuantConnect.OptionQuote.OptionInfo):
        ...

    @property
    def Side(self) -> QuantConnect.Orders.OrderDirection:
        ...

    @Side.setter
    def Side(self, value: QuantConnect.Orders.OrderDirection):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def RequestExpiry(self) -> datetime.datetime:
        ...

    @RequestExpiry.setter
    def RequestExpiry(self, value: datetime.datetime):
        ...

    @property
    def Status(self) -> QuantConnect.Orders.OrderStatus:
        ...

    @Status.setter
    def Status(self, value: QuantConnect.Orders.OrderStatus):
        ...

    @property
    def HideLimitPrice(self) -> typing.Optional[bool]:
        ...

    @HideLimitPrice.setter
    def HideLimitPrice(self, value: typing.Optional[bool]):
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        ...

    @LimitPrice.setter
    def LimitPrice(self, value: typing.Optional[float]):
        ...

    @property
    def Quotes(self) -> System.Collections.Generic.List[QuantConnect.OptionQuote.Quote]:
        ...

    @Quotes.setter
    def Quotes(self, value: System.Collections.Generic.List[QuantConnect.OptionQuote.Quote]):
        ...

    def ToString(self) -> str:
        ...


