from typing import overload
import datetime
import typing

import Calculators
import Calculators.DataType
import System


class FTXCollateralParameters(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def TotalWeight(self) -> float:
        ...

    @TotalWeight.setter
    def TotalWeight(self, value: float):
        ...

    @property
    def InitialWeight(self) -> float:
        ...

    @InitialWeight.setter
    def InitialWeight(self, value: float):
        ...

    @property
    def IMFFactor(self) -> float:
        ...

    @IMFFactor.setter
    def IMFFactor(self, value: float):
        ...

    def __init__(self, coin: str, totalWeight: float, initialWeight: float, imfFactor: float) -> None:
        ...

    def Copy(self, totalWeight: float) -> Calculators.DataType.FTXCollateralParameters:
        ...


class Holding(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @property
    def Quantity(self) -> float:
        ...

    @property
    def MarkPrice(self) -> float:
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @property
    def SecurityType(self) -> int:
        """This property contains the int value of a member of the Calculators.SecurityType enum."""
        ...

    @property
    def MaintenanceMarginRequirement(self) -> float:
        ...

    @property
    def InitialMarginRequirement(self) -> float:
        ...

    def __init__(self, coin: str, quantity: float, markPrice: float, quoteCurrency: str, securityType: Calculators.SecurityType, maintenanceMarginRequirement: float, initialMarginRequirement: float) -> None:
        ...

    def CalculateCollateralValue(self, collateralConfig: Calculators.DataType.FTXCollateralParameters, isInitial: bool) -> float:
        ...

    def ToString(self) -> str:
        ...


class StopLossInfo(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def StartTime(self) -> datetime.datetime:
        ...

    @StartTime.setter
    def StartTime(self, value: datetime.datetime):
        ...

    @property
    def MaxLossBase(self) -> float:
        ...

    @MaxLossBase.setter
    def MaxLossBase(self, value: float):
        ...

    @property
    def MaxLossRatio(self) -> float:
        ...

    @MaxLossRatio.setter
    def MaxLossRatio(self, value: float):
        ...

    @property
    def MinProfit(self) -> float:
        ...

    @MinProfit.setter
    def MinProfit(self, value: float):
        ...

    @property
    def MaxVentureDays(self) -> int:
        ...

    @MaxVentureDays.setter
    def MaxVentureDays(self, value: int):
        ...

    @property
    def IsStopLoss(self) -> bool:
        ...

    @IsStopLoss.setter
    def IsStopLoss(self, value: bool):
        ...

    def StopLoss(self, currentTime: typing.Union[datetime.datetime, datetime.date], pnl: float, price: float) -> bool:
        ...


