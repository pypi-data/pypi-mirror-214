from typing import overload
import typing

import FtxApi.WsEngine
import System
import System.Threading.Tasks

ClientWebSocket = typing.Any


class WebsocketEngine(System.Object, System.IDisposable):
    """This class has no documentation."""

    InitBufferSize: int

    @property
    def OnConnect(self) -> typing.Callable[[ClientWebSocket], System.Threading.Tasks.Task]:
        ...

    @OnConnect.setter
    def OnConnect(self, value: typing.Callable[[ClientWebSocket], System.Threading.Tasks.Task]):
        ...

    @property
    def OnDisconnect(self) -> typing.Callable[[], System.Threading.Tasks.Task]:
        ...

    @OnDisconnect.setter
    def OnDisconnect(self, value: typing.Callable[[], System.Threading.Tasks.Task]):
        ...

    @property
    def OnReceive(self) -> typing.Callable[[ClientWebSocket, str], System.Threading.Tasks.Task]:
        ...

    @OnReceive.setter
    def OnReceive(self, value: typing.Callable[[ClientWebSocket, str], System.Threading.Tasks.Task]):
        ...

    @property
    def SendPing(self) -> typing.Callable[[ClientWebSocket], System.Threading.Tasks.Task]:
        ...

    @SendPing.setter
    def SendPing(self, value: typing.Callable[[ClientWebSocket], System.Threading.Tasks.Task]):
        ...

    def __init__(self, name: str, url: str, pingIntervalMSec: int, silenceDisconnectIntervalMSec: int, logger: typing.Any) -> None:
        ...

    def Dispose(self) -> None:
        ...

    def GetClientWebSocket(self) -> typing.Optional[ClientWebSocket]:
        ...

    def OnConnectAsync(self, clientWebSocket: typing.Any) -> System.Threading.Tasks.Task:
        ...

    def OnDisconnectAsync(self) -> System.Threading.Tasks.Task:
        ...

    def OnReceiveAsync(self, webSocket: typing.Any, message: str) -> System.Threading.Tasks.Task:
        ...

    def Run(self) -> System.Threading.Tasks.Task:
        ...

    def SendPingMessage(self, clientWebSocket: typing.Any) -> System.Threading.Tasks.Task:
        ...

    def Start(self) -> None:
        ...

    def Stop(self) -> None:
        ...


