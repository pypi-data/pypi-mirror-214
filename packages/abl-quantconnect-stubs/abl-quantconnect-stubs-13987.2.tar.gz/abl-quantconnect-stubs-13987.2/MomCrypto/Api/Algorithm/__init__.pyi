from typing import overload
import typing

import MomCrypto.Api.Algorithm
import System


class Utils(System.Object):
    """This class has no documentation."""

    @staticmethod
    def CalculateCoinTradePnL(tradeAmount: float, tradePrice: float, updatedAmount: typing.Optional[float], initialAmount: float = 0, initialPrice: float = 0) -> typing.Union[float, float]:
        ...

    @staticmethod
    def CalculateTradePnL(tradeVolume: float, tradePrice: float, updatedVolume: typing.Optional[float], updatedPrice: typing.Optional[float], initialVolume: float = 0, initialPrice: float = 0) -> typing.Union[float, float, float]:
        ...

    @staticmethod
    def GetCoinCloseProfit(volume: float, openPrice: float, closePrice: float, volumeMultiple: float) -> float:
        ...


