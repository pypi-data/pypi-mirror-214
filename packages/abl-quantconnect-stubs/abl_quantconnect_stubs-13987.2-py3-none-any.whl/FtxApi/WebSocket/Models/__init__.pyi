from typing import overload
import datetime
import typing

import FtxApi.WebSocket.Models
import System
import System.Collections.Generic

FtxApi_WebSocket_Models_FtxWebsocketReceive = typing.Any

FtxApi_WebSocket_Models_FtxWebsocketReceive_T = typing.TypeVar("FtxApi_WebSocket_Models_FtxWebsocketReceive_T")
FtxApi_WebSocket_Models_DataAction_T = typing.TypeVar("FtxApi_WebSocket_Models_DataAction_T")


class FtxOrderBook(System.Object):
    """This class has no documentation."""

    @property
    def time(self) -> float:
        ...

    @time.setter
    def time(self, value: float):
        ...

    @property
    def checksum(self) -> int:
        ...

    @checksum.setter
    def checksum(self, value: int):
        ...

    @property
    def action(self) -> str:
        ...

    @action.setter
    def action(self, value: str):
        ...

    @property
    def bids(self) -> System.Collections.Generic.List[typing.List[typing.Optional[float]]]:
        ...

    @bids.setter
    def bids(self, value: System.Collections.Generic.List[typing.List[typing.Optional[float]]]):
        ...

    @property
    def asks(self) -> System.Collections.Generic.List[typing.List[typing.Optional[float]]]:
        ...

    @asks.setter
    def asks(self, value: System.Collections.Generic.List[typing.List[typing.Optional[float]]]):
        ...

    @property
    def id(self) -> str:
        ...

    @id.setter
    def id(self, value: str):
        ...

    def Copy(self) -> FtxApi.WebSocket.Models.FtxOrderBook:
        ...

    def GetTime(self) -> System.DateTimeOffset:
        ...


class FtxOrderBookHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetFtxOrderBookPrice(array: typing.List[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    def GetFtxOrderBookVolume(array: typing.List[typing.Optional[float]]) -> typing.Optional[float]:
        ...


class FtxTicker(System.Object):
    """This class has no documentation."""

    @property
    def bid(self) -> typing.Optional[float]:
        ...

    @bid.setter
    def bid(self, value: typing.Optional[float]):
        ...

    @property
    def ask(self) -> typing.Optional[float]:
        ...

    @ask.setter
    def ask(self, value: typing.Optional[float]):
        ...

    @property
    def bidSize(self) -> typing.Optional[float]:
        ...

    @bidSize.setter
    def bidSize(self, value: typing.Optional[float]):
        ...

    @property
    def askSize(self) -> typing.Optional[float]:
        ...

    @askSize.setter
    def askSize(self, value: typing.Optional[float]):
        ...

    @property
    def last(self) -> typing.Optional[float]:
        ...

    @last.setter
    def last(self, value: typing.Optional[float]):
        ...

    @property
    def time(self) -> float:
        ...

    @time.setter
    def time(self, value: float):
        ...

    @property
    def id(self) -> str:
        ...

    @id.setter
    def id(self, value: str):
        ...

    def GetTime(self) -> System.DateTimeOffset:
        ...


class FtxWebsocketReceive(typing.Generic[FtxApi_WebSocket_Models_FtxWebsocketReceive_T], FtxApi_WebSocket_Models_FtxWebsocketReceive):
    """This class has no documentation."""

    Partial: str = "partial"

    Update: str = "update"

    @property
    def Channel(self) -> str:
        ...

    @Channel.setter
    def Channel(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def ErrorMessage(self) -> str:
        ...

    @ErrorMessage.setter
    def ErrorMessage(self, value: str):
        ...

    @property
    def Data(self) -> FtxApi_WebSocket_Models_FtxWebsocketReceive_T:
        ...

    @Data.setter
    def Data(self, value: FtxApi_WebSocket_Models_FtxWebsocketReceive_T):
        ...


class DataAction(typing.Generic[FtxApi_WebSocket_Models_DataAction_T], System.Object):
    """This class has no documentation."""

    @property
    def Data(self) -> FtxApi_WebSocket_Models_DataAction_T:
        ...

    @Data.setter
    def Data(self, value: FtxApi_WebSocket_Models_DataAction_T):
        ...

    @property
    def Action(self) -> str:
        ...

    @Action.setter
    def Action(self, value: str):
        ...


class MarketState(System.Object):
    """This class has no documentation."""

    class FutureState(System.Object):
        """This class has no documentation."""

        @property
        def name(self) -> str:
            ...

        @name.setter
        def name(self, value: str):
            ...

        @property
        def underlying(self) -> str:
            ...

        @underlying.setter
        def underlying(self, value: str):
            ...

        @property
        def description(self) -> str:
            ...

        @description.setter
        def description(self, value: str):
            ...

        @property
        def type(self) -> str:
            ...

        @type.setter
        def type(self, value: str):
            ...

        @property
        def expiry(self) -> typing.Optional[datetime.datetime]:
            ...

        @expiry.setter
        def expiry(self, value: typing.Optional[datetime.datetime]):
            ...

        @property
        def perpetual(self) -> bool:
            ...

        @perpetual.setter
        def perpetual(self, value: bool):
            ...

        @property
        def expired(self) -> bool:
            ...

        @expired.setter
        def expired(self, value: bool):
            ...

        @property
        def enabled(self) -> bool:
            ...

        @enabled.setter
        def enabled(self, value: bool):
            ...

        @property
        def postOnly(self) -> bool:
            ...

        @postOnly.setter
        def postOnly(self, value: bool):
            ...

        @property
        def imfFactor(self) -> float:
            ...

        @imfFactor.setter
        def imfFactor(self, value: float):
            ...

        @property
        def underlyingDescription(self) -> str:
            ...

        @underlyingDescription.setter
        def underlyingDescription(self, value: str):
            ...

        @property
        def expiryDescription(self) -> str:
            ...

        @expiryDescription.setter
        def expiryDescription(self, value: str):
            ...

        @property
        def moveStart(self) -> typing.Optional[datetime.datetime]:
            ...

        @moveStart.setter
        def moveStart(self, value: typing.Optional[datetime.datetime]):
            ...

        @property
        def positionLimitWeight(self) -> float:
            ...

        @positionLimitWeight.setter
        def positionLimitWeight(self, value: float):
            ...

        @property
        def group(self) -> str:
            ...

        @group.setter
        def group(self, value: str):
            ...

    SpotType: str = "spot"

    FutureType: str = "future"

    @property
    def name(self) -> str:
        ...

    @name.setter
    def name(self, value: str):
        ...

    @property
    def enabled(self) -> bool:
        ...

    @enabled.setter
    def enabled(self, value: bool):
        ...

    @property
    def postOnly(self) -> bool:
        ...

    @postOnly.setter
    def postOnly(self, value: bool):
        ...

    @property
    def priceIncrement(self) -> float:
        ...

    @priceIncrement.setter
    def priceIncrement(self, value: float):
        ...

    @property
    def sizeIncrement(self) -> float:
        ...

    @sizeIncrement.setter
    def sizeIncrement(self, value: float):
        ...

    @property
    def type(self) -> str:
        ...

    @type.setter
    def type(self, value: str):
        ...

    @property
    def baseCurrency(self) -> str:
        ...

    @baseCurrency.setter
    def baseCurrency(self, value: str):
        ...

    @property
    def quoteCurrency(self) -> str:
        ...

    @quoteCurrency.setter
    def quoteCurrency(self, value: str):
        ...

    @property
    def restricted(self) -> bool:
        ...

    @restricted.setter
    def restricted(self, value: bool):
        ...

    @property
    def underlying(self) -> str:
        ...

    @underlying.setter
    def underlying(self, value: str):
        ...

    @property
    def highLeverageFeeExempt(self) -> bool:
        ...

    @highLeverageFeeExempt.setter
    def highLeverageFeeExempt(self, value: bool):
        ...

    @property
    def future(self) -> FtxApi.WebSocket.Models.MarketState.FutureState:
        ...

    @future.setter
    def future(self, value: FtxApi.WebSocket.Models.MarketState.FutureState):
        ...

    @property
    def id(self) -> str:
        ...

    @id.setter
    def id(self, value: str):
        ...


