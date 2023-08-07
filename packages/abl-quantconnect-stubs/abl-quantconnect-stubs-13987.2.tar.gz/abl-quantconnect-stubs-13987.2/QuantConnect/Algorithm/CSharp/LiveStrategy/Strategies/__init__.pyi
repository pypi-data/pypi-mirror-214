from typing import overload
import typing

import QuantConnect
import QuantConnect.Algorithm
import QuantConnect.Algorithm.CSharp.LiveStrategy.DataType
import QuantConnect.Algorithm.CSharp.LiveStrategy.Strategies
import QuantConnect.Algorithm.CSharp.qlnet.tools
import QuantConnect.Data.Market
import QuantConnect.Statistics
import System


class DeltaCollarStrategy(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, priceList: typing.Any) -> typing.Any:
        ...


class DeltaCollarStrategyBear(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def Sigma(self) -> float:
        ...

    @Sigma.setter
    def Sigma(self, value: float):
        ...

    @property
    def HedgeRange(self) -> float:
        ...

    @HedgeRange.setter
    def HedgeRange(self, value: float):
        ...

    @property
    def IsDecay(self) -> bool:
        ...

    @IsDecay.setter
    def IsDecay(self, value: bool):
        ...

    @property
    def OldStrike(self) -> float:
        ...

    @OldStrike.setter
    def OldStrike(self, value: float):
        ...

    @property
    def StrategeType(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @StrategeType.setter
    def StrategeType(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def Gamma(self) -> float:
        ...

    @Gamma.setter
    def Gamma(self, value: float):
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
    def Index(self) -> int:
        ...

    @Index.setter
    def Index(self, value: int):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, sigma: float, balanceNow: float = -1, stopProfit: bool = False) -> typing.Any:
        ...

    def NeedHedge(self) -> bool:
        ...


class DeltaCollarStrategyDeltaDecay(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def StrategeType(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @StrategeType.setter
    def StrategeType(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def PutStrikeRatio(self) -> float:
        ...

    @PutStrikeRatio.setter
    def PutStrikeRatio(self, value: float):
        ...

    @property
    def Gamma(self) -> float:
        ...

    @Gamma.setter
    def Gamma(self, value: float):
        ...

    @property
    def Sigma(self) -> float:
        ...

    @Sigma.setter
    def Sigma(self, value: float):
        ...

    @property
    def HedgeRange(self) -> float:
        ...

    @HedgeRange.setter
    def HedgeRange(self, value: float):
        ...

    @property
    def IsDecay(self) -> bool:
        ...

    @IsDecay.setter
    def IsDecay(self, value: bool):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, sigma: float, balanceNow: float = -1) -> typing.Any:
        ...

    def NeedHedge(self) -> bool:
        ...


class DeltaCollarStrategyFTXHedge(System.Object):
    """This class has no documentation."""

    @property
    def TargetPositions(self) -> typing.Any:
        ...

    @TargetPositions.setter
    def TargetPositions(self, value: typing.Any):
        ...

    @property
    def FTXOptions(self) -> typing.Any:
        ...

    @FTXOptions.setter
    def FTXOptions(self, value: typing.Any):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def OptionRatio(self) -> float:
        ...

    @OptionRatio.setter
    def OptionRatio(self, value: float):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def OutputFile(self) -> str:
        ...

    @OutputFile.setter
    def OutputFile(self, value: str):
        ...

    @property
    def PutStrategyJsonFiles(self) -> typing.List[str]:
        ...

    @PutStrategyJsonFiles.setter
    def PutStrategyJsonFiles(self, value: typing.List[str]):
        ...

    @property
    def MinStrike(self) -> float:
        ...

    @MinStrike.setter
    def MinStrike(self, value: float):
        ...

    @property
    def CostMultiplier(self) -> float:
        ...

    @CostMultiplier.setter
    def CostMultiplier(self, value: float):
        ...

    @property
    def MinOptionCostMode(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Statistics.MinOptionCostMode enum."""
        ...

    @MinOptionCostMode.setter
    def MinOptionCostMode(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Statistics.MinOptionCostMode enum."""
        ...

    @property
    def UseImpliedVolLimit(self) -> bool:
        ...

    @UseImpliedVolLimit.setter
    def UseImpliedVolLimit(self, value: bool):
        ...

    def __init__(self, putStrategyJsonFiles: typing.List[str], outputFile: str, optionRatio: float, transaction: QuantConnect.Algorithm.QCAlgorithm, minStrike: float, costMultiplier: float, minOptionCostMode: QuantConnect.Statistics.MinOptionCostMode, useImpliedVolLimit: bool) -> None:
        ...

    def CheckFTXOptionPositions(self) -> bool:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, priceList: typing.Any) -> typing.Any:
        ...

    def SetTargetPosition(self, underlyingPrice: float) -> None:
        ...

    def SetTransaction(self, transaction: QuantConnect.Algorithm.QCAlgorithm) -> None:
        ...


class DeltaCollarStrategyFTXHedgeNew(System.Object):
    """This class has no documentation."""

    @property
    def TargetPositions(self) -> typing.Any:
        ...

    @TargetPositions.setter
    def TargetPositions(self, value: typing.Any):
        ...

    @property
    def FTXOptions(self) -> typing.Any:
        ...

    @FTXOptions.setter
    def FTXOptions(self, value: typing.Any):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def OptionRatio(self) -> float:
        ...

    @OptionRatio.setter
    def OptionRatio(self, value: float):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def OutputFile(self) -> str:
        ...

    @OutputFile.setter
    def OutputFile(self, value: str):
        ...

    @property
    def PutStrategyJsonFiles(self) -> typing.List[str]:
        ...

    @PutStrategyJsonFiles.setter
    def PutStrategyJsonFiles(self, value: typing.List[str]):
        ...

    @property
    def MinStrike(self) -> float:
        ...

    @MinStrike.setter
    def MinStrike(self, value: float):
        ...

    @property
    def MaxStrike(self) -> float:
        ...

    @MaxStrike.setter
    def MaxStrike(self, value: float):
        ...

    @property
    def CostMultiplier(self) -> float:
        ...

    @CostMultiplier.setter
    def CostMultiplier(self, value: float):
        ...

    @property
    def MinOptionCostMode(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Statistics.MinOptionCostMode enum."""
        ...

    @MinOptionCostMode.setter
    def MinOptionCostMode(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Statistics.MinOptionCostMode enum."""
        ...

    @property
    def UseImpliedVolLimit(self) -> bool:
        ...

    @UseImpliedVolLimit.setter
    def UseImpliedVolLimit(self, value: bool):
        ...

    @property
    def TotalStrikes(self) -> int:
        ...

    @TotalStrikes.setter
    def TotalStrikes(self, value: int):
        ...

    def __init__(self, putStrategyJsonFiles: typing.List[str], outputFile: str, optionRatio: float, transaction: QuantConnect.Algorithm.QCAlgorithm, minStrike: float, costMultiplier: float, minOptionCostMode: QuantConnect.Statistics.MinOptionCostMode, useImpliedVolLimit: bool, totalStrikes: int, maxStrike: float) -> None:
        ...

    def CheckFTXOptionPositions(self) -> bool:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, hedgeSigma: float, filterSigma: float) -> typing.Any:
        ...

    def SetTargetPosition(self, underlyingPrice: float) -> None:
        ...

    def SetTransaction(self, transaction: QuantConnect.Algorithm.QCAlgorithm) -> None:
        ...


class DeltaCollarStrategyLeverage(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def Sigma(self) -> float:
        ...

    @Sigma.setter
    def Sigma(self, value: float):
        ...

    @property
    def HedgeRange(self) -> float:
        ...

    @HedgeRange.setter
    def HedgeRange(self, value: float):
        ...

    @property
    def IsDecay(self) -> bool:
        ...

    @IsDecay.setter
    def IsDecay(self, value: bool):
        ...

    @property
    def OldStrike(self) -> float:
        ...

    @OldStrike.setter
    def OldStrike(self, value: float):
        ...

    @property
    def StrategeType(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @StrategeType.setter
    def StrategeType(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def Gamma(self) -> float:
        ...

    @Gamma.setter
    def Gamma(self, value: float):
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
    def Index(self) -> int:
        ...

    @Index.setter
    def Index(self, value: int):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, sigma: float, balanceNow: float = -1, stopProfit: bool = False) -> typing.Any:
        ...

    def NeedHedge(self) -> bool:
        ...


class DeltaCollarStrategyNew(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, priceList: typing.Any) -> typing.Any:
        ...


class DeltaCollarStrategyPutOnly(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, priceList: typing.Any, usdBooling: bool = True) -> typing.Any:
        ...


class DeltaCollarStrategyPutOnlyMoveStrike(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def StrategeType(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @StrategeType.setter
    def StrategeType(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def PutStrikeRatio(self) -> float:
        ...

    @PutStrikeRatio.setter
    def PutStrikeRatio(self, value: float):
        ...

    @property
    def Gamma(self) -> float:
        ...

    @Gamma.setter
    def Gamma(self, value: float):
        ...

    @property
    def Sigma(self) -> float:
        ...

    @Sigma.setter
    def Sigma(self, value: float):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying, gammaLimit: float, strategyType: QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType, outputBaseDirectory: str) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, priceList: typing.Any, usdBooling: bool = True) -> typing.Any:
        ...


class DeltaCollarStrategySigma(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def StrategeType(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @StrategeType.setter
    def StrategeType(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def PutStrikeRatio(self) -> float:
        ...

    @PutStrikeRatio.setter
    def PutStrikeRatio(self, value: float):
        ...

    @property
    def Gamma(self) -> float:
        ...

    @Gamma.setter
    def Gamma(self, value: float):
        ...

    @property
    def Sigma(self) -> float:
        ...

    @Sigma.setter
    def Sigma(self, value: float):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, sigma: float) -> typing.Any:
        ...


class DeltaCollarStrategyStopProfit(System.Object):
    """This class has no documentation."""

    @property
    def HasOption(self) -> bool:
        ...

    @HasOption.setter
    def HasOption(self, value: bool):
        ...

    @property
    def BalanceNow(self) -> float:
        ...

    @BalanceNow.setter
    def BalanceNow(self, value: float):
        ...

    @property
    def Underlying(self) -> QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying:
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying):
        ...

    @property
    def UnderlyingPriceNow(self) -> float:
        ...

    @UnderlyingPriceNow.setter
    def UnderlyingPriceNow(self, value: float):
        ...

    @property
    def UplineNow(self) -> float:
        ...

    @UplineNow.setter
    def UplineNow(self, value: float):
        ...

    @property
    def ExpiryDateNow(self) -> typing.Any:
        ...

    @ExpiryDateNow.setter
    def ExpiryDateNow(self, value: typing.Any):
        ...

    @property
    def TargetDelta(self) -> float:
        ...

    @TargetDelta.setter
    def TargetDelta(self, value: float):
        ...

    @property
    def CashDelta(self) -> float:
        ...

    @CashDelta.setter
    def CashDelta(self, value: float):
        ...

    @property
    def OutputBaseDirectory(self) -> str:
        ...

    @OutputBaseDirectory.setter
    def OutputBaseDirectory(self, value: str):
        ...

    @property
    def TargetUnderlyingVolume(self) -> float:
        ...

    @TargetUnderlyingVolume.setter
    def TargetUnderlyingVolume(self, value: float):
        ...

    @property
    def Sigma(self) -> float:
        ...

    @Sigma.setter
    def Sigma(self, value: float):
        ...

    @property
    def HedgeRange(self) -> float:
        ...

    @HedgeRange.setter
    def HedgeRange(self, value: float):
        ...

    @property
    def IsDecay(self) -> bool:
        ...

    @IsDecay.setter
    def IsDecay(self, value: bool):
        ...

    @property
    def OldStrike(self) -> float:
        ...

    @OldStrike.setter
    def OldStrike(self, value: float):
        ...

    @property
    def StrategeType(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @StrategeType.setter
    def StrategeType(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.qlnet.tools.Utils.MoveStrikeType enum."""
        ...

    @property
    def GammaLimit(self) -> float:
        ...

    @GammaLimit.setter
    def GammaLimit(self, value: float):
        ...

    @property
    def Gamma(self) -> float:
        ...

    @Gamma.setter
    def Gamma(self, value: float):
        ...

    @property
    def Options(self) -> typing.Any:
        ...

    @Options.setter
    def Options(self, value: typing.Any):
        ...

    def __init__(self, underlying: QuantConnect.Algorithm.CSharp.LiveStrategy.DataType.Underlying) -> None:
        ...

    def DetectionStrategy(self, sliceTime: typing.Any, underlyingPrice: float, sigma: float, balanceNow: float = -1, stopProfit: bool = False) -> typing.Any:
        ...

    def NeedHedge(self) -> bool:
        ...


class PutCallParityPortfolio(System.Object):
    """This class has no documentation."""

    @property
    def CallOption(self) -> QuantConnect.Data.Market.OptionContract:
        ...

    @CallOption.setter
    def CallOption(self, value: QuantConnect.Data.Market.OptionContract):
        ...

    @property
    def PutOption(self) -> QuantConnect.Data.Market.OptionContract:
        ...

    @PutOption.setter
    def PutOption(self, value: QuantConnect.Data.Market.OptionContract):
        ...

    @property
    def FuturesSymbol(self) -> QuantConnect.Symbol:
        ...

    @FuturesSymbol.setter
    def FuturesSymbol(self, value: QuantConnect.Symbol):
        ...

    @property
    def CallQuantity(self) -> float:
        ...

    @CallQuantity.setter
    def CallQuantity(self, value: float):
        ...

    @property
    def AnnualReturn(self) -> float:
        ...

    @AnnualReturn.setter
    def AnnualReturn(self, value: float):
        ...

    def __init__(self, callOption: QuantConnect.Data.Market.OptionContract, putOption: QuantConnect.Data.Market.OptionContract, futuresSymbol: typing.Union[QuantConnect.Symbol, str], callQuantity: float, annualReturn: float) -> None:
        ...

    def ToString(self) -> str:
        ...


