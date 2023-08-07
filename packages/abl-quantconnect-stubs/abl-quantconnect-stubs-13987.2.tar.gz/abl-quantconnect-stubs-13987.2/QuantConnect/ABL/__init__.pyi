from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.ABL
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Securities
import System
import System.Collections.Generic

QuantConnect_ABL_QueryExchangeResult_T = typing.TypeVar("QuantConnect_ABL_QueryExchangeResult_T")
QuantConnect_ABL_ServerCallResult_T = typing.TypeVar("QuantConnect_ABL_ServerCallResult_T")
QuantConnect_ABL__EventContainer_Callable = typing.TypeVar("QuantConnect_ABL__EventContainer_Callable")
QuantConnect_ABL__EventContainer_ReturnType = typing.TypeVar("QuantConnect_ABL__EventContainer_ReturnType")


class StocksSplitInfo(System.Object):
    """"""

    @property
    def SplitFactor(self) -> float:
        ...

    @SplitFactor.setter
    def SplitFactor(self, value: float):
        ...

    @property
    def SplitDate(self) -> datetime.datetime:
        ...

    @SplitDate.setter
    def SplitDate(self, value: datetime.datetime):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...


class SplitManager(System.Object):
    """This class has no documentation."""

    def __init__(self, path: str) -> None:
        ...

    def GetSplit(self, symbol: str, date: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.ABL.StocksSplitInfo:
        ...


class StocksDividendInfo(System.Object):
    """This class has no documentation."""

    @property
    def PayDate(self) -> datetime.datetime:
        ...

    @PayDate.setter
    def PayDate(self, value: datetime.datetime):
        ...

    @property
    def ExDividendDate(self) -> datetime.datetime:
        ...

    @ExDividendDate.setter
    def ExDividendDate(self, value: datetime.datetime):
        ...

    @property
    def DividendCash(self) -> float:
        ...

    @DividendCash.setter
    def DividendCash(self, value: float):
        ...


class StocksDividend(System.Object):
    """This class has no documentation."""

    def __init__(self, content: str) -> None:
        ...

    def GetDividend(self, date: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.ABL.StocksDividendInfo:
        ...


class DividendManager(System.Object):
    """This class has no documentation."""

    def __init__(self, path: str) -> None:
        ...

    def GetDividend(self, symbol: str, date: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.ABL.StocksDividendInfo:
        ...


class EtfOptionChange(System.Object):
    """This class has no documentation."""

    @property
    def Underlying(self) -> str:
        ...

    @Underlying.setter
    def Underlying(self, value: str):
        ...

    @property
    def ExpiryDate(self) -> datetime.datetime:
        ...

    @ExpiryDate.setter
    def ExpiryDate(self, value: datetime.datetime):
        ...

    @property
    def NewExpiryDate(self) -> datetime.datetime:
        ...

    @NewExpiryDate.setter
    def NewExpiryDate(self, value: datetime.datetime):
        ...

    @property
    def ActionDate(self) -> datetime.datetime:
        ...

    @ActionDate.setter
    def ActionDate(self, value: datetime.datetime):
        ...

    def __init__(self, underlying: str, expiryDate: typing.Union[datetime.datetime, datetime.date], newExpiryDate: typing.Union[datetime.datetime, datetime.date], actionDate: typing.Union[datetime.datetime, datetime.date]) -> None:
        ...


class EtfOptionChangeManager(System.Object):
    """This class has no documentation."""

    def __init__(self, file: str) -> None:
        ...

    def AddEtfOptionChange(self, etfOptionChange: QuantConnect.ABL.EtfOptionChange) -> None:
        ...

    def GetEtfOptionChange(self, underlying: str, actionDate: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.List[QuantConnect.ABL.EtfOptionChange]:
        ...

    def GetEtfOptionChanges(self) -> System.Collections.Generic.Dictionary[str, System.Collections.Generic.List[QuantConnect.ABL.EtfOptionChange]]:
        ...


class AblSymbolDatabase(System.Object):
    """AblSymbolDatabase"""

    ExchangeUtcTimeTicks: int = 0
    """ExchangeUtcTimeTicks"""

    IsWarmingUp: bool = True
    """IsWarmingUp"""

    @staticmethod
    def FromDataFolder() -> None:
        """FromDataFolder"""
        ...

    @staticmethod
    def GetAdjustFactor(symbol: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> float:
        """GetAdjustFactor"""
        ...

    @staticmethod
    def GetDividend(symbol: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.ABL.StocksDividendInfo:
        """GetDividend"""
        ...

    @staticmethod
    def GetDividendTicker(symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """GetDividendTicker"""
        ...

    @staticmethod
    def GetExpiryChangeTicker(symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """GetExpiryChangeTicker"""
        ...

    @staticmethod
    def GetForwardAdjustFactor(symbol: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> float:
        """GetForwardAdjustFactor"""
        ...

    @staticmethod
    def GetOptionChange(symbol: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.List[QuantConnect.ABL.EtfOptionChange]:
        """GetOptionChange"""
        ...

    @staticmethod
    def GetOptionChangedTicker(symbol: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> str:
        """GetOptionChangedTicker"""
        ...

    @staticmethod
    def GetSplit(symbol: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.ABL.StocksSplitInfo:
        """GetSplit"""
        ...

    @staticmethod
    def IsChinaEtf(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """IsChinaEtf"""
        ...

    @staticmethod
    def IsChinaIndex(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """IsChinaIndex"""
        ...

    @staticmethod
    def IsChinaStocks(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """IsChinaStocks"""
        ...

    @staticmethod
    def IsDividendTicker(symbol: str) -> bool:
        """IsDividendTicker"""
        ...

    @staticmethod
    def IsExpiryChangeTicker(symbol: str) -> bool:
        """IsExpiryChangeTicker"""
        ...

    @staticmethod
    def LockDividendSymbol(underlying: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> None:
        """LockDividendSymbol"""
        ...

    @staticmethod
    def UnlockDividendSymbol(underlying: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> None:
        """UnlockDividendSymbol"""
        ...

    @staticmethod
    def WaitForDividendSymbolLock(underlying: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> int:
        """WaitForDividendSymbolLock"""
        ...


class ExchangeQueryInfo(System.Object):
    """"""

    @property
    def QueryType(self) -> int:
        """
        QueryType
        
        This property contains the int value of a member of the QuantConnect.ABL.ExchangeQueryType enum.
        """
        ...

    @QueryType.setter
    def QueryType(self, value: int):
        """
        QueryType
        
        This property contains the int value of a member of the QuantConnect.ABL.ExchangeQueryType enum.
        """
        ...

    @property
    def UserId(self) -> str:
        """UserId"""
        ...

    @UserId.setter
    def UserId(self, value: str):
        """UserId"""
        ...

    @property
    def RequestId(self) -> str:
        """RequestId"""
        ...

    @RequestId.setter
    def RequestId(self, value: str):
        """RequestId"""
        ...


class UserTransferType(System.Enum):
    """UserTransferType"""

    Spot2UmFuture = 0
    """Spot2UmFuture"""

    UmFuture2Spot = 1
    """UmFuture2Spot"""


class TransferInfo(System.Object):
    """"""

    @property
    def Amount(self) -> float:
        """Amount"""
        ...

    @property
    def TransferType(self) -> int:
        """
        TransferType
        
        This property contains the int value of a member of the QuantConnect.ABL.UserTransferType enum.
        """
        ...

    @property
    def Currency(self) -> str:
        """Currency"""
        ...

    def __init__(self, amount: float, type: QuantConnect.ABL.UserTransferType, currency: str) -> None:
        """"""
        ...


class QueryExchangeResult(typing.Generic[QuantConnect_ABL_QueryExchangeResult_T], System.Object):
    """"""

    @property
    def Data(self) -> QuantConnect_ABL_QueryExchangeResult_T:
        ...

    @Data.setter
    def Data(self, value: QuantConnect_ABL_QueryExchangeResult_T):
        ...

    @property
    def RequestId(self) -> str:
        ...

    @RequestId.setter
    def RequestId(self, value: str):
        ...

    @property
    def IsLast(self) -> bool:
        ...

    @IsLast.setter
    def IsLast(self, value: bool):
        ...


class RiskDegreeInfo(System.Object):
    """"""

    @property
    def RiskDegree(self) -> float:
        ...

    @RiskDegree.setter
    def RiskDegree(self, value: float):
        ...

    @property
    def UserRiskDegree(self) -> float:
        ...

    @UserRiskDegree.setter
    def UserRiskDegree(self, value: float):
        ...


class ServerCallResult(typing.Generic[QuantConnect_ABL_ServerCallResult_T], System.Object):
    """"""

    @property
    def Data(self) -> QuantConnect_ABL_ServerCallResult_T:
        ...

    @Data.setter
    def Data(self, value: QuantConnect_ABL_ServerCallResult_T):
        ...

    @property
    def ErrorMessage(self) -> str:
        ...

    @ErrorMessage.setter
    def ErrorMessage(self, value: str):
        ...

    @property
    def Success(self) -> bool:
        ...

    @Success.setter
    def Success(self, value: bool):
        ...

    def __init__(self, data: QuantConnect_ABL_ServerCallResult_T) -> None:
        """"""
        ...

    @staticmethod
    def Failure(data: QuantConnect_ABL_ServerCallResult_T, error: str) -> QuantConnect.ABL.ServerCallResult[QuantConnect_ABL_ServerCallResult_T]:
        """"""
        ...


class AlgorithmBoost(System.Object):
    """Algorithm Boost"""

    @property
    def AlgorithmEnd(self) -> _EventContainer[typing.Callable[[], None], None]:
        ...

    @AlgorithmEnd.setter
    def AlgorithmEnd(self, value: _EventContainer[typing.Callable[[], None], None]):
        ...

    @property
    def SymbolListed(self) -> _EventContainer[typing.Callable[[System.Collections.Generic.IList[QuantConnect.Symbol]], None], None]:
        ...

    @SymbolListed.setter
    def SymbolListed(self, value: _EventContainer[typing.Callable[[System.Collections.Generic.IList[QuantConnect.Symbol]], None], None]):
        ...

    @property
    def SymbolDelisted(self) -> _EventContainer[typing.Callable[[System.Collections.Generic.IList[QuantConnect.Symbol]], None], None]:
        ...

    @SymbolDelisted.setter
    def SymbolDelisted(self, value: _EventContainer[typing.Callable[[System.Collections.Generic.IList[QuantConnect.Symbol]], None], None]):
        ...

    @property
    def QueryExchangeBalanceCompleted(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Securities.CashAmount]], None], None]:
        ...

    @QueryExchangeBalanceCompleted.setter
    def QueryExchangeBalanceCompleted(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Securities.CashAmount]], None], None]):
        ...

    @property
    def QueryExchangeHoldingCompleted(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Holding]], None], None]:
        ...

    @QueryExchangeHoldingCompleted.setter
    def QueryExchangeHoldingCompleted(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Holding]], None], None]):
        ...

    @property
    def QueryExchangeOpenOrderCompleted(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Orders.Order]], None], None]:
        ...

    @QueryExchangeOpenOrderCompleted.setter
    def QueryExchangeOpenOrderCompleted(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Orders.Order]], None], None]):
        ...

    @property
    def QueryBalanceCompleted(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Securities.CashAmount]], None], None]:
        ...

    @QueryBalanceCompleted.setter
    def QueryBalanceCompleted(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Securities.CashAmount]], None], None]):
        ...

    @property
    def QueryHoldingCompleted(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Holding]], None], None]:
        ...

    @QueryHoldingCompleted.setter
    def QueryHoldingCompleted(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Holding]], None], None]):
        ...

    @property
    def QueryOpenOrderCompleted(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Orders.Order]], None], None]:
        ...

    @QueryOpenOrderCompleted.setter
    def QueryOpenOrderCompleted(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.QueryExchangeResult[QuantConnect.Orders.Order]], None], None]):
        ...

    @property
    def RiskDegreeChanged(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.RiskDegreeInfo], None], None]:
        ...

    @RiskDegreeChanged.setter
    def RiskDegreeChanged(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.RiskDegreeInfo], None], None]):
        ...

    @property
    def TransferFinished(self) -> _EventContainer[typing.Callable[[QuantConnect.ABL.ServerCallResult[QuantConnect.ABL.TransferInfo]], None], None]:
        ...

    @TransferFinished.setter
    def TransferFinished(self, value: _EventContainer[typing.Callable[[QuantConnect.ABL.ServerCallResult[QuantConnect.ABL.TransferInfo]], None], None]):
        ...

    @property
    def TransferAction(self) -> typing.Callable[[QuantConnect.ABL.TransferInfo], None]:
        ...

    @TransferAction.setter
    def TransferAction(self, value: typing.Callable[[QuantConnect.ABL.TransferInfo], None]):
        ...

    @property
    def QueryExchangeAction(self) -> typing.Callable[[QuantConnect.ABL.ExchangeQueryInfo], None]:
        ...

    @QueryExchangeAction.setter
    def QueryExchangeAction(self, value: typing.Callable[[QuantConnect.ABL.ExchangeQueryInfo], None]):
        ...

    @property
    def CryptoSymbolProvider(self) -> QuantConnect.Interfaces.ICryptoChainProvider:
        ...

    @CryptoSymbolProvider.setter
    def CryptoSymbolProvider(self, value: QuantConnect.Interfaces.ICryptoChainProvider):
        ...

    @property
    def TradingIsReady(self) -> bool:
        """TradingIsReady"""
        ...

    @TradingIsReady.setter
    def TradingIsReady(self, value: bool):
        """TradingIsReady"""
        ...

    def RaiseAlgorithmEnd(self) -> None:
        """"""
        ...

    def RaiseOnQueryExchangeHolding(self, holding: QuantConnect.Holding, requestId: str, isLast: bool) -> None:
        """RaiseOnQueryExchangeHolding"""
        ...

    def RaiseQueryBalanceCompleted(self, balance: QuantConnect.Securities.CashAmount, requestId: str) -> None:
        """RaiseQueryBalanceCompleted"""
        ...

    def RaiseQueryExchangeBalanceCompleted(self, balance: QuantConnect.Securities.CashAmount, requestId: str, isLast: bool) -> None:
        """RaiseQueryExchangeBalanceCompleted"""
        ...

    def RaiseQueryExchangeOpenOrderCompleted(self, order: QuantConnect.Orders.Order, requestId: str, isLast: bool) -> None:
        """RaiseQueryExchangeOpenOrderCompleted"""
        ...

    def RaiseQueryHoldingCompleted(self, holding: QuantConnect.Holding, requestId: str) -> None:
        """RaiseQueryHolding"""
        ...

    def RaiseQueryOpenOrderCompleted(self, order: QuantConnect.Orders.Order, requestId: str) -> None:
        """RaiseQueryOpenOrderCompleted"""
        ...

    def RaiseRiskDegreeChanged(self, riskDegree: float, userRiskDegree: float) -> None:
        """RaiseRiskDegreeChanged"""
        ...

    def RaiseSymbolDelisted(self, symbols: System.Collections.Generic.IList[QuantConnect.Symbol]) -> None:
        """RaiseSymbolDelisted"""
        ...

    def RaiseSymbolListed(self, symbols: System.Collections.Generic.IList[QuantConnect.Symbol]) -> None:
        """RaiseSymbolListed"""
        ...

    def RaiseTransferFinished(self, amount: float, type: QuantConnect.ABL.UserTransferType, currency: str, error: str = None) -> None:
        """"""
        ...


class ExchangeQueryType(System.Enum):
    """"""

    OpenOrder = 1
    """OpenOrder"""

    Holding = 1
    """Holding"""

    CashBalance = 2
    """CashBalance"""

    ExchangeOpenOrder = 3
    """"""

    ExchangeHolding = 4
    """"""

    ExchangeCashBalance = 5
    """"""


class PriceFactorManager(System.Object):
    """PriceFactorManager"""

    def __init__(self, path: str) -> None:
        """PriceFactorManager"""
        ...

    def GetAdjustFactor(self, symbol: str, date: typing.Union[datetime.datetime, datetime.date]) -> float:
        """GetAdjustFactor"""
        ...

    def GetForwardAdjustFactor(self, symbol: str, date: typing.Union[datetime.datetime, datetime.date]) -> float:
        """GetForwardAdjustFactor"""
        ...


class StocksPriceFactor(System.Object):
    """StocksPriceFactor"""

    @property
    def LastFactor(self) -> float:
        ...

    @property
    def LastDate(self) -> datetime.datetime:
        ...

    @property
    def FirstDate(self) -> datetime.datetime:
        ...

    def __init__(self, file: str) -> None:
        """StocksPriceFactor"""
        ...

    def GetAdjustFactor(self, date: typing.Union[datetime.datetime, datetime.date]) -> float:
        ...

    def GetForwardAdjustFactor(self, date: typing.Union[datetime.datetime, datetime.date]) -> float:
        ...


class _EventContainer(typing.Generic[QuantConnect_ABL__EventContainer_Callable, QuantConnect_ABL__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_ABL__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_ABL__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_ABL__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


