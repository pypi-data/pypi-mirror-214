from typing import overload
import typing

import FtxApi
import System

StringEnumConverter = typing.Any


class Client(System.Object):
    """This class has no documentation."""

    @property
    def ApiKey(self) -> str:
        ...

    @property
    def ApiSecret(self) -> str:
        ...

    @property
    def SubAccount(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, apiKey: str, apiSecret: str, subAccount: str = None) -> None:
        ...


class FtxStringEnumConverter(StringEnumConverter):
    """This class has no documentation."""

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        ...


