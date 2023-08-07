from typing import overload
import typing

import FtxApi
import FtxApi.Rest.Models
import FtxApi.WebSocket
import FtxApi.WebSocket.Models
import System
import System.Collections.Generic
import System.Threading
import System.Threading.Tasks


class FtxSenderClientWebSocket(System.Object):
    """This class has no documentation."""

    @staticmethod
    def FtxAuthentication(webSocket: typing.Any, client: FtxApi.Client) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    def SendFtxPing(webSocket: typing.Any) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def SubscribeFtxChannel(webSocket: typing.Any, channel: str, market: str) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def SubscribeFtxChannel(webSocket: typing.Any, channel: str) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def UnsubscribeFtxChannel(webSocket: typing.Any, channel: str) -> System.Threading.Tasks.Task:
        ...

    @staticmethod
    @overload
    def UnsubscribeFtxChannel(webSocket: typing.Any, channel: str, market: str) -> System.Threading.Tasks.Task:
        ...


class FtxWsMarkets(System.Object, System.IDisposable):
    """This class has no documentation."""

    Url: str

    @property
    def ReceiveUpdates(self) -> typing.Callable[[System.Collections.Generic.List[FtxApi.WebSocket.Models.MarketState]], System.Threading.Tasks.Task]:
        ...

    @ReceiveUpdates.setter
    def ReceiveUpdates(self, value: typing.Callable[[System.Collections.Generic.List[FtxApi.WebSocket.Models.MarketState]], System.Threading.Tasks.Task]):
        ...

    def __init__(self, logger: typing.Any) -> None:
        ...

    def Dispose(self) -> None:
        ...

    def Start(self, ct: typing.Optional[System.Threading.CancellationToken] = None) -> None:
        ...

    def Stop(self) -> None:
        ...


class FtxWsOrderBooks(System.Object, System.IDisposable):
    """This class has no documentation."""

    Url: str

    ChannelName: str = "orderbook"

    @property
    def ReceiveUpdates(self) -> typing.Callable[[FtxApi.WebSocket.Models.FtxOrderBook], System.Threading.Tasks.Task]:
        ...

    @ReceiveUpdates.setter
    def ReceiveUpdates(self, value: typing.Callable[[FtxApi.WebSocket.Models.FtxOrderBook], System.Threading.Tasks.Task]):
        ...

    def __init__(self, logger: typing.Any) -> None:
        ...

    def Dispose(self) -> None:
        ...

    def Resubscribe(self, symbols: System.Collections.Generic.IList[str]) -> System.Threading.Tasks.Task:
        ...

    def Start(self, ct: typing.Optional[System.Threading.CancellationToken] = None) -> None:
        ...

    def Stop(self) -> None:
        ...

    def Subscribe(self, symbols: System.Collections.Generic.IList[str]) -> System.Threading.Tasks.Task:
        ...

    def Unsubscribe(self, symbols: System.Collections.Generic.IList[str]) -> System.Threading.Tasks.Task:
        ...


class FtxWsOrders(System.Object, System.IDisposable):
    """This class has no documentation."""

    Url: str

    @property
    def OrderUpdates(self) -> typing.Callable[[FtxApi.Rest.Models.Order], System.Threading.Tasks.Task]:
        ...

    @OrderUpdates.setter
    def OrderUpdates(self, value: typing.Callable[[FtxApi.Rest.Models.Order], System.Threading.Tasks.Task]):
        ...

    @property
    def FillUpdates(self) -> typing.Callable[[FtxApi.Rest.Models.Fill], System.Threading.Tasks.Task]:
        ...

    @FillUpdates.setter
    def FillUpdates(self, value: typing.Callable[[FtxApi.Rest.Models.Fill], System.Threading.Tasks.Task]):
        ...

    def __init__(self, client: FtxApi.Client, logger: typing.Any) -> None:
        ...

    def Dispose(self) -> None:
        ...

    def Start(self, ct: typing.Optional[System.Threading.CancellationToken] = None) -> None:
        ...

    def Stop(self) -> None:
        ...


class FtxWsPrices(System.Object, System.IDisposable):
    """This class has no documentation."""

    Url: str

    ChannelName: str = "ticker"

    @property
    def ReceiveUpdates(self) -> typing.Callable[[FtxApi.WebSocket.Models.FtxTicker], System.Threading.Tasks.Task]:
        ...

    @ReceiveUpdates.setter
    def ReceiveUpdates(self, value: typing.Callable[[FtxApi.WebSocket.Models.FtxTicker], System.Threading.Tasks.Task]):
        ...

    def __init__(self, logger: typing.Any) -> None:
        ...

    def Dispose(self) -> None:
        ...

    def Resubscribe(self, symbols: System.Collections.Generic.IList[str]) -> System.Threading.Tasks.Task:
        ...

    def Start(self, ct: typing.Optional[System.Threading.CancellationToken] = None) -> None:
        ...

    def Stop(self) -> None:
        ...

    def Subscribe(self, symbols: System.Collections.Generic.IList[str]) -> System.Threading.Tasks.Task:
        ...

    def Unsubscribe(self, symbols: System.Collections.Generic.IList[str]) -> System.Threading.Tasks.Task:
        ...


