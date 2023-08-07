from typing import overload
import datetime
import typing

import FtxApi.Rest.Models.Markets
import System
import System.Collections.Generic


class Market(System.Object):
    """This class has no documentation."""

    @property
    def Type(self) -> str:
        """"future" or "spot\""""
        ...

    @Type.setter
    def Type(self, value: str):
        """"future" or "spot\""""
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def Underlying(self) -> str:
        ...

    @Underlying.setter
    def Underlying(self, value: str):
        ...

    @property
    def BaseCurrency(self) -> str:
        ...

    @BaseCurrency.setter
    def BaseCurrency(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def Enabled(self) -> bool:
        ...

    @Enabled.setter
    def Enabled(self, value: bool):
        ...

    @property
    def Ask(self) -> typing.Optional[float]:
        ...

    @Ask.setter
    def Ask(self, value: typing.Optional[float]):
        ...

    @property
    def Bid(self) -> typing.Optional[float]:
        ...

    @Bid.setter
    def Bid(self, value: typing.Optional[float]):
        ...

    @property
    def Last(self) -> typing.Optional[float]:
        ...

    @Last.setter
    def Last(self, value: typing.Optional[float]):
        ...

    @property
    def PriceIncrement(self) -> float:
        ...

    @PriceIncrement.setter
    def PriceIncrement(self, value: float):
        ...

    @property
    def SizeIncrement(self) -> float:
        ...

    @SizeIncrement.setter
    def SizeIncrement(self, value: float):
        ...

    @property
    def MinProvideSize(self) -> typing.Optional[float]:
        ...

    @MinProvideSize.setter
    def MinProvideSize(self, value: typing.Optional[float]):
        ...

    def ToString(self) -> str:
        ...


class Orderbook(System.Object):
    """This class has no documentation."""

    @property
    def Bids(self) -> System.Collections.Generic.List[System.Collections.Generic.List[float]]:
        ...

    @Bids.setter
    def Bids(self, value: System.Collections.Generic.List[System.Collections.Generic.List[float]]):
        ...

    @property
    def Asks(self) -> System.Collections.Generic.List[System.Collections.Generic.List[float]]:
        ...

    @Asks.setter
    def Asks(self, value: System.Collections.Generic.List[System.Collections.Generic.List[float]]):
        ...


class Trade(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Liquidation(self) -> bool:
        ...

    @Liquidation.setter
    def Liquidation(self, value: bool):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
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


