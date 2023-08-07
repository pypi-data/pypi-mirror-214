from typing import overload
import abc
import typing

import Calculators.DataType
import Calculators.Margins
import System
import System.Collections.Concurrent
import System.Collections.Generic


class IFTXMarginModel(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def CalculateMarginFraction(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding], isInitial: bool) -> float:
        ...

    def GetAvailableCollateral(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding]) -> float:
        ...

    def GetCollateral(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding], isInitial: bool) -> float:
        ...

    def IsAtRiskForLiquidation(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding], riskControlMultiplier: float) -> bool:
        ...

    def TryUpdateCollateralParameters(self, coin: str, totalWeight: float) -> None:
        ...


class FTXMarginModel(System.Object, Calculators.Margins.IFTXMarginModel):
    """This class has no documentation."""

    @property
    def _quoteCurrency(self) -> str:
        """This field is protected."""
        ...

    _collateralParametersMap: System.Collections.Concurrent.ConcurrentDictionary[str, Calculators.DataType.FTXCollateralParameters]
    """This field is protected."""

    @property
    def _logger(self) -> typing.Any:
        """This field is protected."""
        ...

    @_logger.setter
    def _logger(self, value: typing.Any):
        """This field is protected."""
        ...

    def __init__(self, location: str = ..., quoteCurrency: str = "USD") -> None:
        ...

    def CalculateInitialMargin(self, holding: Calculators.DataType.Holding) -> float:
        """This method is protected."""
        ...

    def CalculateMarginFraction(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding], isInitial: bool) -> float:
        ...

    def CalculateNotional(self, holding: Calculators.DataType.Holding) -> float:
        """This method is protected."""
        ...

    def GetAvailableCollateral(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding]) -> float:
        """
        collateral used is equal to:
            For PRESIDENT: initialMarginRequirement * openSize * (risk price)
            For MOVE: initialMarginRequirement * openSize * (index price)
            Otherwise: initialMarginRequirement * openSize * (mark price)
        """
        ...

    def GetCollateral(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding], isInitial: bool) -> float:
        ...

    @overload
    def IsAtRiskForLiquidation(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding], riskControlMultiplier: float = 1) -> bool:
        """
        FTX will trade your non-USD collateral into USD if your USD balance is negative and any of the following hold:
            You are close to liquidation: your account's margin fraction is less than (20bps + maintenance margin fraction requirement)
            Your negative USD balance is large: over $30,000 in magnitude
            Your negative USD balance is large when compared to overall collateral: its magnitude is over 4 times larger than your net account collateral
        From: https://help.ftx.com/hc/en-us/articles/360031149632-Non-USD-Collateral
        
        :param riskControlMultiplier: a multiplier to adjust USD remaining requirement, should be between 0-1 to strengthen the rules
        """
        ...

    @overload
    def IsAtRiskForLiquidation(self, marginFraction: float, weightedAverageMaintenanceMarginRequirement: float, usdPosition: float, netCollateral: float) -> bool:
        ...

    def TryUpdateCollateralParameters(self, coin: str, totalWeight: float) -> None:
        ...


class FTXMarginModelFactory(System.Object):
    """This class has no documentation."""

    @staticmethod
    def Init(location: str) -> None:
        ...

    @staticmethod
    def Resolve(enableSpotMargin: bool) -> Calculators.Margins.IFTXMarginModel:
        ...


class FTXMarginModelWithSpotMargin(Calculators.Margins.FTXMarginModel):
    """This class has no documentation."""

    def __init__(self, location: str = ..., quoteCurrency: str = "USD") -> None:
        ...

    def CalculateInitialMargin(self, holding: Calculators.DataType.Holding) -> float:
        """This method is protected."""
        ...

    def CalculateNotional(self, holding: Calculators.DataType.Holding) -> float:
        """This method is protected."""
        ...

    def GetInitialMarginRequirementForCrypto(self, holding: Calculators.DataType.Holding) -> float:
        ...

    def GetMaintenanceMarginRequirementForCrypto(self, holding: Calculators.DataType.Holding) -> float:
        ...

    def IsAtRiskForLiquidation(self, holdings: System.Collections.Generic.IList[Calculators.DataType.Holding], riskControlMultiplier: float = 1) -> bool:
        """
        The auto-close margin--the point at which you are not just liquidated but in fact closed down off-exchange--is 50% of the maintenance margin requirement
        From: https://help.ftx.com/hc/en-us/articles/360053007671
        for safety, we send liquidation warning once reach mantenance margin
        """
        ...


