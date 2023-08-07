from typing import overload
import datetime
import typing

import MomCrypto.Api
import MomCrypto.DataApi
import System


class MomHistoryData(System.Object):
    """This class has no documentation."""

    @property
    def OpenTime(self) -> datetime.datetime:
        ...

    @OpenTime.setter
    def OpenTime(self, value: datetime.datetime):
        ...

    @property
    def Open(self) -> float:
        ...

    @Open.setter
    def Open(self, value: float):
        ...

    @property
    def High(self) -> float:
        ...

    @High.setter
    def High(self, value: float):
        ...

    @property
    def Low(self) -> float:
        ...

    @Low.setter
    def Low(self, value: float):
        ...

    @property
    def Close(self) -> float:
        ...

    @Close.setter
    def Close(self, value: float):
        ...

    @property
    def BaseVolume(self) -> float:
        ...

    @BaseVolume.setter
    def BaseVolume(self, value: float):
        ...

    @property
    def CloseTime(self) -> datetime.datetime:
        ...

    @CloseTime.setter
    def CloseTime(self, value: datetime.datetime):
        ...

    @property
    def QuoteVolume(self) -> float:
        ...

    @QuoteVolume.setter
    def QuoteVolume(self, value: float):
        ...

    @property
    def TradeCount(self) -> int:
        ...

    @TradeCount.setter
    def TradeCount(self, value: int):
        ...

    @property
    def TakerBuyBaseVolume(self) -> float:
        ...

    @TakerBuyBaseVolume.setter
    def TakerBuyBaseVolume(self, value: float):
        ...

    @property
    def TakerBuyQuoteVolume(self) -> float:
        ...

    @TakerBuyQuoteVolume.setter
    def TakerBuyQuoteVolume(self, value: float):
        ...


class MomQryHistoryData(MomCrypto.Api.MomQryField):
    """This class has no documentation."""

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def TimeStart(self) -> str:
        ...

    @TimeStart.setter
    def TimeStart(self, value: str):
        ...

    @property
    def TimeEnd(self) -> str:
        ...

    @TimeEnd.setter
    def TimeEnd(self, value: str):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def DataType(self) -> int:
        ...

    @DataType.setter
    def DataType(self, value: int):
        ...


class MomHistoryDataApi(System.Object):
    """This class has no documentation."""

    def __init__(self, address: str, logger: typing.Any) -> None:
        ...

    def GetAccounts(self) -> typing.List[MomCrypto.Api.MomAccount]:
        ...

    def GetAccountTrades(self, account: str, localId: int = 0, count: int = 1000) -> typing.List[MomCrypto.Api.MomTrade]:
        ...

    def GetFundAccounts(self) -> typing.List[MomCrypto.Api.MomFundAccount]:
        ...

    def GetFundPositions(self, account: str) -> typing.List[MomCrypto.Api.MomFundPosition]:
        ...

    def GetFundTrades(self, account: str, localId: int = 0, count: int = 1000) -> typing.List[MomCrypto.Api.MomFundTrade]:
        ...

    def GetUserPositions(self, user: str) -> typing.List[MomCrypto.Api.MomPosition]:
        ...

    def GetUserTrades(self, user: str, localId: int = 0, count: int = 1000) -> typing.List[MomCrypto.Api.MomTrade]:
        ...

    def QryBinanceHistoryData(self, qryData: MomCrypto.DataApi.MomQryHistoryData) -> str:
        ...

    def QryDeribitHistoryData(self, qryData: MomCrypto.DataApi.MomQryHistoryData) -> str:
        ...

    def QryFtxHistoryData(self, qryData: MomCrypto.DataApi.MomQryHistoryData) -> str:
        ...

    def QryHistoryData(self, qryData: MomCrypto.DataApi.MomQryHistoryData, market: str) -> str:
        ...

    def SendDingMsg(self, text: str, token: str = None, key: str = None) -> None:
        ...


class MomHistoryDataType(System.Enum):
    """This class has no documentation."""

    OneMinute = 0

    ThreeMinutes = 1

    FiveMinutes = 2

    FifteenMinutes = 3

    ThirtyMinutes = 4

    OneHour = 5

    TwoHour = 6

    FourHour = 7

    SixHour = 8

    EightHour = 9

    TwelveHour = 10

    OneDay = 11

    ThreeDay = 12

    OneWeek = 13

    OneMonth = 14


