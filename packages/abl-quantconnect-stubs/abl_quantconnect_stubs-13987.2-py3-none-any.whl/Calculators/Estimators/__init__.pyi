from typing import overload
import typing

import Calculators.Estimators
import System
import System.Collections.Generic


class EWMAVolatilityEstimator(System.Object):
    """use r0square as start point, allow empty price list"""

    @property
    def CurrentVolatility(self) -> float:
        ...

    @CurrentVolatility.setter
    def CurrentVolatility(self, value: float):
        ...

    @property
    def Volatilities(self) -> System.Collections.Generic.IList[float]:
        ...

    @Volatilities.setter
    def Volatilities(self, value: System.Collections.Generic.IList[float]):
        ...

    @overload
    def __init__(self, prices: System.Collections.Generic.IList[float], _lambda: float) -> None:
        ...

    @overload
    def __init__(self, price: float, currentVolatility: float, _lambda: float) -> None:
        ...

    def AddPrice(self, price: float) -> None:
        ...

    def AddPrices(self, prices: System.Collections.Generic.IList[float]) -> None:
        ...

    def UpdateEWMAVolatility(self, new_price: float, last_price: float) -> float:
        ...


