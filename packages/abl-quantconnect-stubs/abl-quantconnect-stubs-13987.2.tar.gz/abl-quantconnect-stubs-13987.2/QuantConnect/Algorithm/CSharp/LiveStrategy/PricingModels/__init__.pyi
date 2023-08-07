from typing import overload
import typing

import QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels
import System


class BSModel(System.Object):
    """
    This example demonstrates how to add options for a given underlying equity security.
    It also shows how you can prefilter contracts easily based on strikes and expirations, and how you
    can inspect the option chain to pick a specific option contract to trade.
    """

    class EPutCall(System.Enum):
        """This class has no documentation."""

        Call = 0

        Put = 1

    PutCall: int
    """This property contains the int value of a member of the QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall enum."""

    @staticmethod
    def GetDelta(S: float, X: float, q: float, r: float, sigma: float, t: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall) -> float:
        ...

    @staticmethod
    def GetGamma(S: float, X: float, q: float, r: float, sigma: float, t: float) -> float:
        ...

    @staticmethod
    def GetImpliedVol(S: float, X: float, q: float, r: float, optionPrice: float, t: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall, accuracy: float, maxIterations: int) -> float:
        ...

    @staticmethod
    def GetImpliedVolBisection(S: float, X: float, q: float, r: float, optionPrice: float, t: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall, accuracy: float, maxIterations: int) -> float:
        ...

    @staticmethod
    def GetOptionValue(S: float, X: float, q: float, r: float, sigma: float, t: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall) -> float:
        ...

    @staticmethod
    def GetRho(S: float, X: float, q: float, r: float, sigma: float, t: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall) -> float:
        ...

    @staticmethod
    def GetTheta(S: float, X: float, q: float, r: float, sigma: float, t: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall) -> float:
        ...

    @staticmethod
    def GetVega(S: float, X: float, q: float, r: float, sigma: float, t: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall) -> float:
        ...

    @staticmethod
    def n(d: float) -> float:
        ...

    @staticmethod
    def N(d: float) -> float:
        ...

    @staticmethod
    def ZakDelta(S: float, X: float, r: float, sigma: float, t: float, cost: float, risk: float, PutCall: QuantConnect.Algorithm.CSharp.LiveStrategy.PricingModels.BSModel.EPutCall) -> typing.Any:
        ...

    @staticmethod
    def ZakDeltaMulti(S: float, r: float, sigma: float, t: float, cost: float, risk: float, delta_multi: float, gamma_multi: float) -> typing.Any:
        ...


