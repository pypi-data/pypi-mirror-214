from typing import overload
import datetime
import typing

import MomCrypto.Frontend
import System
import System.Collections.Generic
import System.Threading

LongRunningTask = typing.Any

MomCrypto_Frontend__EventContainer_Callable = typing.TypeVar("MomCrypto_Frontend__EventContainer_Callable")
MomCrypto_Frontend__EventContainer_ReturnType = typing.TypeVar("MomCrypto_Frontend__EventContainer_ReturnType")


class ByteArrayEqualsComparer(System.Object, System.Collections.Generic.IEqualityComparer[typing.List[int]]):
    """This class has no documentation."""

    Instance: MomCrypto.Frontend.ByteArrayEqualsComparer = ...

    def Equals(self, x: typing.List[int], y: typing.List[int]) -> bool:
        ...

    def GetHashCode(self, obj: typing.List[int]) -> int:
        ...


class FrontendConnector(LongRunningTask):
    """This class has no documentation."""

    @property
    def pollTimerInterval(self) -> datetime.timedelta:
        """This field is protected."""
        ...

    @pollTimerInterval.setter
    def pollTimerInterval(self, value: datetime.timedelta):
        """This field is protected."""
        ...

    @property
    def PerMaxSendBlock(self) -> int:
        ...

    @PerMaxSendBlock.setter
    def PerMaxSendBlock(self, value: int):
        ...

    @property
    def PerMaxRecvBlock(self) -> int:
        ...

    @PerMaxRecvBlock.setter
    def PerMaxRecvBlock(self, value: int):
        ...

    @property
    def Address(self) -> str:
        ...

    @property
    def DebugMode(self) -> bool:
        ...

    @property
    def OnDisconnected(self) -> _EventContainer[typing.Callable[[MomCrypto.Frontend.FrontendConnector, int], None], None]:
        ...

    @OnDisconnected.setter
    def OnDisconnected(self, value: _EventContainer[typing.Callable[[MomCrypto.Frontend.FrontendConnector, int], None], None]):
        ...

    @property
    def OnSocketConnected(self) -> _EventContainer[typing.Callable[[MomCrypto.Frontend.FrontendConnector], None], None]:
        ...

    @OnSocketConnected.setter
    def OnSocketConnected(self, value: _EventContainer[typing.Callable[[MomCrypto.Frontend.FrontendConnector], None], None]):
        ...

    @property
    def ReceiveQueue(self) -> typing.Any:
        ...

    @property
    def SendQueue(self) -> typing.Any:
        ...

    def __init__(self, address: str, logger: typing.Any, debugMode: bool = False) -> None:
        ...

    def OnDealerConnected(self, sender: typing.Any, e: typing.Any) -> None:
        """This method is protected."""
        ...

    def OnDealerDisconnected(self, sender: typing.Any, e: typing.Any) -> None:
        """This method is protected."""
        ...

    def Run(self, ct: System.Threading.CancellationToken) -> None:
        """This method is protected."""
        ...


class FrontendEvent(System.Object):
    """This class has no documentation."""

    MaxMsgSize: int = ...

    @property
    def Identity(self) -> typing.List[int]:
        ...

    @Identity.setter
    def Identity(self, value: typing.List[int]):
        ...

    @property
    def MsgData(self) -> System.Collections.Generic.List[typing.List[int]]:
        ...

    @property
    def MsgSize(self) -> System.Collections.Generic.List[int]:
        ...

    @overload
    def __init__(self, identity: typing.List[int] = None) -> None:
        ...

    @overload
    def __init__(self, identity: typing.List[int], e: MomCrypto.Frontend.FrontendEvent) -> None:
        ...


class FrontendListener(LongRunningTask):
    """This class has no documentation."""

    @property
    def PerMaxSendBlock(self) -> int:
        ...

    @PerMaxSendBlock.setter
    def PerMaxSendBlock(self, value: int):
        ...

    @property
    def PerMaxRecvBlock(self) -> int:
        ...

    @PerMaxRecvBlock.setter
    def PerMaxRecvBlock(self, value: int):
        ...

    @property
    def pollTimerInterval(self) -> datetime.timedelta:
        """This field is protected."""
        ...

    @pollTimerInterval.setter
    def pollTimerInterval(self, value: datetime.timedelta):
        """This field is protected."""
        ...

    @property
    def Address(self) -> str:
        ...

    @property
    def DebugMode(self) -> bool:
        ...

    @property
    def ReceiveQueue(self) -> typing.Any:
        ...

    @property
    def SendQueue(self) -> typing.Any:
        ...

    def __init__(self, address: str, logger: typing.Any, debugMode: bool = False) -> None:
        ...

    def Run(self, ct: System.Threading.CancellationToken) -> None:
        """This method is protected."""
        ...


class IdentityEqualsComparer(System.Object, System.Collections.Generic.IEqualityComparer[typing.List[int]]):
    """This class has no documentation."""

    Instance: MomCrypto.Frontend.IdentityEqualsComparer = ...

    def Equals(self, x: typing.List[int], y: typing.List[int]) -> bool:
        ...

    def GetHashCode(self, buffer: typing.List[int]) -> int:
        ...


class NetMQHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetSocketHandle(socket: typing.Any) -> int:
        ...


class _EventContainer(typing.Generic[MomCrypto_Frontend__EventContainer_Callable, MomCrypto_Frontend__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> MomCrypto_Frontend__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: MomCrypto_Frontend__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: MomCrypto_Frontend__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


