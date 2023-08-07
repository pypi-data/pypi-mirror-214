from typing import overload
import typing

import QuantConnect
import QuantConnect.Algorithm.CSharp.LiveStrategy.DataType
import QuantConnect.Data.Market
import QuantConnect.Statistics
import System

IEquatable = typing.Any


class AssetAllocationConfig(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def Asset(self) -> float:
        ...

    @Asset.setter
    def Asset(self, value: float):
        ...

    @property
    def StartDate(self) -> typing.Any:
        ...

    @StartDate.setter
    def StartDate(self, value: typing.Any):
        ...

    @property
    def EndDate(self) -> typing.Any:
        ...

    @EndDate.setter
    def EndDate(self, value: typing.Any):
        ...


class DeribitCalendarSpreadTradingConfig(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def MaxSizePerExpiry(self) -> float:
        ...

    @MaxSizePerExpiry.setter
    def MaxSizePerExpiry(self, value: float):
        ...

    @property
    def TargetPosition(self) -> float:
        ...

    @TargetPosition.setter
    def TargetPosition(self, value: float):
        ...

    @property
    def RequiredReturn(self) -> float:
        ...

    @RequiredReturn.setter
    def RequiredReturn(self, value: float):
        ...

    @property
    def MaxCloseCost(self) -> float:
        ...

    @MaxCloseCost.setter
    def MaxCloseCost(self, value: float):
        ...

    @property
    def MinT2M(self) -> float:
        ...

    @MinT2M.setter
    def MinT2M(self, value: float):
        ...

    @property
    def MaxPerpetualTradeVolume(self) -> float:
        ...

    @MaxPerpetualTradeVolume.setter
    def MaxPerpetualTradeVolume(self, value: float):
        ...


class DeribitCallOptionTradingConfig(System.Object):
    """This class has no documentation."""

    @property
    def Contract(self) -> QuantConnect.Data.Market.OptionContract:
        ...

    @Contract.setter
    def Contract(self, value: QuantConnect.Data.Market.OptionContract):
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...

    @property
    def Status(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Statistics.OptionStatus enum."""
        ...

    @Status.setter
    def Status(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Statistics.OptionStatus enum."""
        ...

    @property
    def TradedVolume(self) -> float:
        ...

    @TradedVolume.setter
    def TradedVolume(self, value: float):
        ...

    def __init__(self, contract: QuantConnect.Data.Market.OptionContract, quantity: float, status: QuantConnect.Statistics.OptionStatus, tradedVolume: float) -> None:
        ...


class DeribitParityTradingConfig(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def OptionLotSize(self) -> float:
        ...

    @OptionLotSize.setter
    def OptionLotSize(self, value: float):
        ...

    @property
    def OptionMaxTradeSize(self) -> float:
        ...

    @OptionMaxTradeSize.setter
    def OptionMaxTradeSize(self, value: float):
        ...

    @property
    def TargetOptionPosition(self) -> float:
        ...

    @TargetOptionPosition.setter
    def TargetOptionPosition(self, value: float):
        ...

    @property
    def RequiredAnnualReturn(self) -> float:
        ...

    @RequiredAnnualReturn.setter
    def RequiredAnnualReturn(self, value: float):
        ...

    @property
    def MaxFuturesVolume(self) -> float:
        ...

    @MaxFuturesVolume.setter
    def MaxFuturesVolume(self, value: float):
        ...

    @property
    def MaxT2M(self) -> int:
        ...

    @MaxT2M.setter
    def MaxT2M(self, value: int):
        ...

    @property
    def MinT2M(self) -> int:
        ...

    @MinT2M.setter
    def MinT2M(self, value: int):
        ...

    @property
    def OptionParityTradeMode(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.OptionParityTradeMode enum."""
        ...

    @OptionParityTradeMode.setter
    def OptionParityTradeMode(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.OptionParityTradeMode enum."""
        ...


class FTXOptionForHedge(System.Object):
    """This class has no documentation."""

    @property
    def Underlying(self) -> str:
        ...

    @property
    def Type(self) -> int:
        """This property contains the int value of a member of the QuantConnect.OptionRight enum."""
        ...

    @property
    def Strike(self) -> float:
        ...

    @property
    def Expiry(self) -> typing.Any:
        ...

    @property
    def Size(self) -> float:
        ...

    @property
    def QuoteId(self) -> int:
        ...

    @property
    def IsHedging(self) -> bool:
        ...

    @IsHedging.setter
    def IsHedging(self, value: bool):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    def __init__(self, strike: float, expiry: typing.Any, size: float, quoteId: int, isHedging: bool = False, underlying: str = "BTC", type: QuantConnect.OptionRight = ..., cashDelta: float = 0) -> None:
        ...

    def ToString(self) -> str:
        ...


class LiveAssetAllocation(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def Asset(self) -> float:
        ...

    @Asset.setter
    def Asset(self, value: float):
        ...

    @property
    def HasCrypto(self) -> bool:
        ...

    @HasCrypto.setter
    def HasCrypto(self, value: bool):
        ...

    @property
    def T2M(self) -> float:
        ...

    @T2M.setter
    def T2M(self, value: float):
        ...

    @property
    def T2MUpdateRatio(self) -> float:
        ...

    @T2MUpdateRatio.setter
    def T2MUpdateRatio(self, value: float):
        ...

    @property
    def UpdateStrikes(self) -> bool:
        ...

    @UpdateStrikes.setter
    def UpdateStrikes(self, value: bool):
        ...

    @property
    def StrikeSpread(self) -> float:
        ...

    @StrikeSpread.setter
    def StrikeSpread(self, value: float):
        ...


class OptionInPortfolio(System.Object):
    """This class has no documentation."""

    @property
    def OptionType(self) -> str:
        ...

    @OptionType.setter
    def OptionType(self, value: str):
        ...

    @property
    def Strike(self) -> float:
        ...

    @Strike.setter
    def Strike(self, value: float):
        ...

    @property
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...

    @property
    def IsCrossUpline(self) -> bool:
        ...

    @IsCrossUpline.setter
    def IsCrossUpline(self, value: bool):
        ...

    @property
    def IsAddOption(self) -> bool:
        ...

    @IsAddOption.setter
    def IsAddOption(self, value: bool):
        ...

    def __init__(self, optionType: str, strike: float, volume: float, isCrossUpline: bool, isAddOption: bool) -> None:
        ...


class Straddle(IEquatable):
    """This class has no documentation."""

    @property
    def CallOption(self) -> QuantConnect.Data.Market.OptionContract:
        ...

    @property
    def PutOption(self) -> QuantConnect.Data.Market.OptionContract:
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Expiry(self) -> typing.Any:
        ...

    @property
    def Traded(self) -> bool:
        ...

    @Traded.setter
    def Traded(self, value: bool):
        ...

    def __init__(self, callOption: QuantConnect.Data.Market.OptionContract, putOption: QuantConnect.Data.Market.OptionContract, size: float, traded: bool = False) -> None:
        ...

    @overload
    def Equals(self, that: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Straddle) -> bool:
        ...

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetDelta(self, underlyingPrice: float, q: float, r: float, sigma: float, timeNow: typing.Any) -> float:
        ...

    def TryAdd(self, straddle: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Straddle) -> bool:
        ...


class Underlying(IEquatable):
    """This class has no documentation."""

    @property
    def CoinPair(self) -> str:
        ...

    @property
    def HasCrypto(self) -> bool:
        ...

    @HasCrypto.setter
    def HasCrypto(self, value: bool):
        ...

    @property
    def HasFutures(self) -> bool:
        ...

    @HasFutures.setter
    def HasFutures(self, value: bool):
        ...

    def __init__(self, coinPair: str, hasCrypto: bool, hasFuturues: bool) -> None:
        ...

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def Equals(self, that: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> bool:
        ...


