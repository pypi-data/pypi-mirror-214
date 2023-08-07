from typing import overload
import abc
import datetime
import typing

import MomCrypto.Api
import System
import System.Collections
import System.Collections.Generic
import System.Security

MomCrypto_Api_MomInstrument = typing.Any

MomCrypto_Api_ISpscSourceBlock_TOutput = typing.TypeVar("MomCrypto_Api_ISpscSourceBlock_TOutput")
MomCrypto_Api_ISpscTargetBlock_TInput = typing.TypeVar("MomCrypto_Api_ISpscTargetBlock_TInput")
MomCrypto_Api_SpscBufferBlock_TOutput = typing.TypeVar("MomCrypto_Api_SpscBufferBlock_TOutput")
MomCrypto_Api_SpscBroadcastBlock_TOutput = typing.TypeVar("MomCrypto_Api_SpscBroadcastBlock_TOutput")
MomCrypto_Api_SpscActionBlock_TInput = typing.TypeVar("MomCrypto_Api_SpscActionBlock_TInput")
MomCrypto_Api_SpscBufferAction_TInput = typing.TypeVar("MomCrypto_Api_SpscBufferAction_TInput")
MomCrypto_Api_SpscQueue_T = typing.TypeVar("MomCrypto_Api_SpscQueue_T")
MomCrypto_Api__EventContainer_Callable = typing.TypeVar("MomCrypto_Api__EventContainer_Callable")
MomCrypto_Api__EventContainer_ReturnType = typing.TypeVar("MomCrypto_Api__EventContainer_ReturnType")


class AccountField(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def accountId(self) -> str:
        ...

    @accountId.setter
    def accountId(self, value: str):
        ...

    @property
    def accountType(self) -> str:
        ...

    @accountType.setter
    def accountType(self, value: str):
        ...

    @property
    def accountName(self) -> str:
        ...

    @accountName.setter
    def accountName(self, value: str):
        ...

    @property
    def currencyType(self) -> str:
        ...

    @currencyType.setter
    def currencyType(self, value: str):
        ...

    @property
    def fundAccountId(self) -> str:
        ...

    @fundAccountId.setter
    def fundAccountId(self, value: str):
        ...

    @property
    def channelType(self) -> str:
        ...

    @channelType.setter
    def channelType(self, value: str):
        ...

    @property
    def fundChannelType(self) -> str:
        ...

    @fundChannelType.setter
    def fundChannelType(self, value: str):
        ...

    @property
    def exchange(self) -> str:
        ...

    @exchange.setter
    def exchange(self, value: str):
        ...

    @property
    def market(self) -> str:
        ...

    @market.setter
    def market(self, value: str):
        ...

    @property
    def preBalance(self) -> float:
        ...

    @preBalance.setter
    def preBalance(self, value: float):
        ...

    @property
    def preMargin(self) -> float:
        ...

    @preMargin.setter
    def preMargin(self, value: float):
        ...

    @property
    def preEquity(self) -> float:
        ...

    @preEquity.setter
    def preEquity(self, value: float):
        ...

    @property
    def deposit(self) -> float:
        ...

    @deposit.setter
    def deposit(self, value: float):
        ...

    @property
    def withdraw(self) -> float:
        ...

    @withdraw.setter
    def withdraw(self, value: float):
        ...

    @property
    def currMargin(self) -> float:
        ...

    @currMargin.setter
    def currMargin(self, value: float):
        ...

    @property
    def frozenMargin(self) -> float:
        ...

    @frozenMargin.setter
    def frozenMargin(self, value: float):
        ...

    @property
    def unfrozenMargin(self) -> float:
        ...

    @unfrozenMargin.setter
    def unfrozenMargin(self, value: float):
        ...

    @property
    def commission(self) -> float:
        ...

    @commission.setter
    def commission(self, value: float):
        ...

    @property
    def frozenCommission(self) -> float:
        ...

    @frozenCommission.setter
    def frozenCommission(self, value: float):
        ...

    @property
    def unfrozenCommission(self) -> float:
        ...

    @unfrozenCommission.setter
    def unfrozenCommission(self, value: float):
        ...

    @property
    def premiumIn(self) -> float:
        ...

    @premiumIn.setter
    def premiumIn(self, value: float):
        ...

    @property
    def premiumOut(self) -> float:
        ...

    @premiumOut.setter
    def premiumOut(self, value: float):
        ...

    @property
    def frozenPremium(self) -> float:
        ...

    @frozenPremium.setter
    def frozenPremium(self, value: float):
        ...

    @property
    def unfrozenPremium(self) -> float:
        ...

    @unfrozenPremium.setter
    def unfrozenPremium(self, value: float):
        ...

    @property
    def closeProfit(self) -> float:
        ...

    @closeProfit.setter
    def closeProfit(self, value: float):
        ...

    @property
    def positionProfit(self) -> float:
        ...

    @positionProfit.setter
    def positionProfit(self, value: float):
        ...

    @property
    def balance(self) -> float:
        ...

    @balance.setter
    def balance(self, value: float):
        ...

    @property
    def available(self) -> float:
        ...

    @available.setter
    def available(self, value: float):
        ...

    @property
    def riskDegree(self) -> float:
        ...

    @riskDegree.setter
    def riskDegree(self, value: float):
        ...

    @property
    def version(self) -> int:
        ...

    @version.setter
    def version(self, value: int):
        ...

    @property
    def FundId(self) -> int:
        ...

    @FundId.setter
    def FundId(self, value: int):
        ...

    @property
    def fundId(self) -> int:
        ...

    @fundId.setter
    def fundId(self, value: int):
        ...

    @property
    def ChannelType(self) -> str:
        ...

    @ChannelType.setter
    def ChannelType(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def FundAccountId(self) -> str:
        ...

    @FundAccountId.setter
    def FundAccountId(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def FundChannelType(self) -> str:
        ...

    @FundChannelType.setter
    def FundChannelType(self, value: str):
        ...

    @property
    def AccountId(self) -> str:
        ...

    @AccountId.setter
    def AccountId(self, value: str):
        ...

    @property
    def AccountType(self) -> str:
        ...

    @AccountType.setter
    def AccountType(self, value: str):
        ...

    @property
    def AccountName(self) -> str:
        ...

    @AccountName.setter
    def AccountName(self, value: str):
        ...

    @property
    def PreBalance(self) -> float:
        ...

    @PreBalance.setter
    def PreBalance(self, value: float):
        ...

    @property
    def PreMargin(self) -> float:
        ...

    @PreMargin.setter
    def PreMargin(self, value: float):
        ...

    @property
    def PreEquity(self) -> float:
        ...

    @PreEquity.setter
    def PreEquity(self, value: float):
        ...

    @property
    def Deposit(self) -> float:
        ...

    @Deposit.setter
    def Deposit(self, value: float):
        ...

    @property
    def Withdraw(self) -> float:
        ...

    @Withdraw.setter
    def Withdraw(self, value: float):
        ...

    @property
    def CurrMargin(self) -> float:
        ...

    @CurrMargin.setter
    def CurrMargin(self, value: float):
        ...

    @property
    def FrozenMargin(self) -> float:
        ...

    @FrozenMargin.setter
    def FrozenMargin(self, value: float):
        ...

    @property
    def UnfrozenMargin(self) -> float:
        ...

    @UnfrozenMargin.setter
    def UnfrozenMargin(self, value: float):
        ...

    @property
    def Commission(self) -> float:
        ...

    @Commission.setter
    def Commission(self, value: float):
        ...

    @property
    def FrozenCommission(self) -> float:
        ...

    @FrozenCommission.setter
    def FrozenCommission(self, value: float):
        ...

    @property
    def UnfrozenCommission(self) -> float:
        ...

    @UnfrozenCommission.setter
    def UnfrozenCommission(self, value: float):
        ...

    @property
    def PremiumIn(self) -> float:
        ...

    @PremiumIn.setter
    def PremiumIn(self, value: float):
        ...

    @property
    def PremiumOut(self) -> float:
        ...

    @PremiumOut.setter
    def PremiumOut(self, value: float):
        ...

    @property
    def FrozenPremium(self) -> float:
        ...

    @FrozenPremium.setter
    def FrozenPremium(self, value: float):
        ...

    @property
    def UnfrozenPremium(self) -> float:
        ...

    @UnfrozenPremium.setter
    def UnfrozenPremium(self, value: float):
        ...

    @property
    def CloseProfit(self) -> float:
        ...

    @CloseProfit.setter
    def CloseProfit(self, value: float):
        ...

    @property
    def PositionProfit(self) -> float:
        ...

    @PositionProfit.setter
    def PositionProfit(self, value: float):
        ...

    @property
    def Balance(self) -> float:
        ...

    @Balance.setter
    def Balance(self, value: float):
        ...

    @property
    def Available(self) -> float:
        ...

    @Available.setter
    def Available(self, value: float):
        ...

    @property
    def CurrencyType(self) -> str:
        ...

    @CurrencyType.setter
    def CurrencyType(self, value: str):
        ...

    @property
    def RiskDegree(self) -> float:
        ...

    @RiskDegree.setter
    def RiskDegree(self, value: float):
        ...

    @property
    def Version(self) -> int:
        ...

    @Version.setter
    def Version(self, value: int):
        ...

    def CalcRiskDegree(self) -> None:
        ...

    def Reset(self) -> None:
        ...

    def UpdateVersion(self) -> None:
        ...


class ConstantHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetConstantValues() -> System.Collections.Generic.List[str]:
        ...

    @staticmethod
    def GetName(value: int) -> str:
        ...

    @staticmethod
    @overload
    def GetNames() -> System.Collections.Generic.IDictionary[int, str]:
        ...

    @staticmethod
    @overload
    def GetNames(values: System.Collections.Generic.IEnumerable[int]) -> str:
        ...

    @staticmethod
    @overload
    def GetNames(*values: int) -> str:
        ...

    @staticmethod
    def GetValue(name: str) -> int:
        ...

    @staticmethod
    @overload
    def GetValues() -> System.Collections.Generic.List[int]:
        ...

    @staticmethod
    @overload
    def GetValues(names: str) -> System.Collections.Generic.List[int]:
        ...

    @staticmethod
    def RegisterType(type: typing.Type) -> None:
        ...


class MomRspInfo(System.Object):
    """This class has no documentation."""

    @property
    def ErrorID(self) -> int:
        ...

    @ErrorID.setter
    def ErrorID(self, value: int):
        ...

    @property
    def ErrorMsg(self) -> str:
        ...

    @ErrorMsg.setter
    def ErrorMsg(self, value: str):
        ...

    def ToString(self) -> str:
        ...


class MomDepthMarketData:
    """This class has no documentation."""

    @property
    def InstrumentIndex(self) -> int:
        ...

    @InstrumentIndex.setter
    def InstrumentIndex(self, value: int):
        ...

    @property
    def TradingDay(self) -> str:
        ...

    @TradingDay.setter
    def TradingDay(self, value: str):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def ExchangeSymbol(self) -> str:
        ...

    @ExchangeSymbol.setter
    def ExchangeSymbol(self, value: str):
        ...

    @property
    def LastPrice(self) -> float:
        ...

    @LastPrice.setter
    def LastPrice(self, value: float):
        ...

    @property
    def PreSettlementPrice(self) -> float:
        ...

    @PreSettlementPrice.setter
    def PreSettlementPrice(self, value: float):
        ...

    @property
    def PreClosePrice(self) -> float:
        ...

    @PreClosePrice.setter
    def PreClosePrice(self, value: float):
        ...

    @property
    def PreOpenInterest(self) -> float:
        ...

    @PreOpenInterest.setter
    def PreOpenInterest(self, value: float):
        ...

    @property
    def OpenPrice(self) -> float:
        ...

    @OpenPrice.setter
    def OpenPrice(self, value: float):
        ...

    @property
    def HighestPrice(self) -> float:
        ...

    @HighestPrice.setter
    def HighestPrice(self, value: float):
        ...

    @property
    def LowestPrice(self) -> float:
        ...

    @LowestPrice.setter
    def LowestPrice(self, value: float):
        ...

    @property
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...

    @property
    def Turnover(self) -> float:
        ...

    @Turnover.setter
    def Turnover(self, value: float):
        ...

    @property
    def OpenInterest(self) -> float:
        ...

    @OpenInterest.setter
    def OpenInterest(self, value: float):
        ...

    @property
    def ClosePrice(self) -> float:
        ...

    @ClosePrice.setter
    def ClosePrice(self, value: float):
        ...

    @property
    def SettlementPrice(self) -> float:
        ...

    @SettlementPrice.setter
    def SettlementPrice(self, value: float):
        ...

    @property
    def UpperLimitPrice(self) -> float:
        ...

    @UpperLimitPrice.setter
    def UpperLimitPrice(self, value: float):
        ...

    @property
    def LowerLimitPrice(self) -> float:
        ...

    @LowerLimitPrice.setter
    def LowerLimitPrice(self, value: float):
        ...

    @property
    def TimeOffset(self) -> float:
        ...

    @TimeOffset.setter
    def TimeOffset(self, value: float):
        ...

    @property
    def CurrDelta(self) -> float:
        ...

    @CurrDelta.setter
    def CurrDelta(self, value: float):
        ...

    @property
    def UpdateTime(self) -> str:
        ...

    @UpdateTime.setter
    def UpdateTime(self, value: str):
        ...

    @property
    def UpdateMillisec(self) -> int:
        ...

    @UpdateMillisec.setter
    def UpdateMillisec(self, value: int):
        ...

    @property
    def BidPrice1(self) -> float:
        ...

    @BidPrice1.setter
    def BidPrice1(self, value: float):
        ...

    @property
    def BidVolume1(self) -> float:
        ...

    @BidVolume1.setter
    def BidVolume1(self, value: float):
        ...

    @property
    def AskPrice1(self) -> float:
        ...

    @AskPrice1.setter
    def AskPrice1(self, value: float):
        ...

    @property
    def AskVolume1(self) -> float:
        ...

    @AskVolume1.setter
    def AskVolume1(self, value: float):
        ...

    @property
    def BidPrice2(self) -> float:
        ...

    @BidPrice2.setter
    def BidPrice2(self, value: float):
        ...

    @property
    def BidVolume2(self) -> float:
        ...

    @BidVolume2.setter
    def BidVolume2(self, value: float):
        ...

    @property
    def AskPrice2(self) -> float:
        ...

    @AskPrice2.setter
    def AskPrice2(self, value: float):
        ...

    @property
    def AskVolume2(self) -> float:
        ...

    @AskVolume2.setter
    def AskVolume2(self, value: float):
        ...

    @property
    def BidPrice3(self) -> float:
        ...

    @BidPrice3.setter
    def BidPrice3(self, value: float):
        ...

    @property
    def BidVolume3(self) -> float:
        ...

    @BidVolume3.setter
    def BidVolume3(self, value: float):
        ...

    @property
    def AskPrice3(self) -> float:
        ...

    @AskPrice3.setter
    def AskPrice3(self, value: float):
        ...

    @property
    def AskVolume3(self) -> float:
        ...

    @AskVolume3.setter
    def AskVolume3(self, value: float):
        ...

    @property
    def BidPrice4(self) -> float:
        ...

    @BidPrice4.setter
    def BidPrice4(self, value: float):
        ...

    @property
    def BidVolume4(self) -> float:
        ...

    @BidVolume4.setter
    def BidVolume4(self, value: float):
        ...

    @property
    def AskPrice4(self) -> float:
        ...

    @AskPrice4.setter
    def AskPrice4(self, value: float):
        ...

    @property
    def AskVolume4(self) -> float:
        ...

    @AskVolume4.setter
    def AskVolume4(self, value: float):
        ...

    @property
    def BidPrice5(self) -> float:
        ...

    @BidPrice5.setter
    def BidPrice5(self, value: float):
        ...

    @property
    def BidVolume5(self) -> float:
        ...

    @BidVolume5.setter
    def BidVolume5(self, value: float):
        ...

    @property
    def AskPrice5(self) -> float:
        ...

    @AskPrice5.setter
    def AskPrice5(self, value: float):
        ...

    @property
    def AskVolume5(self) -> float:
        ...

    @AskVolume5.setter
    def AskVolume5(self, value: float):
        ...

    @property
    def AveragePrice(self) -> float:
        ...

    @AveragePrice.setter
    def AveragePrice(self, value: float):
        ...

    @property
    def ActionDay(self) -> str:
        ...

    @ActionDay.setter
    def ActionDay(self, value: str):
        ...

    @property
    def MarkPrice(self) -> float:
        ...

    @MarkPrice.setter
    def MarkPrice(self, value: float):
        ...

    @property
    def IndexPrice(self) -> float:
        ...

    @IndexPrice.setter
    def IndexPrice(self, value: float):
        ...

    @property
    def AskIV(self) -> float:
        ...

    @AskIV.setter
    def AskIV(self, value: float):
        ...

    @property
    def BidIV(self) -> float:
        ...

    @BidIV.setter
    def BidIV(self, value: float):
        ...

    @property
    def MarkIV(self) -> float:
        ...

    @MarkIV.setter
    def MarkIV(self, value: float):
        ...

    @property
    def Theta(self) -> float:
        ...

    @Theta.setter
    def Theta(self, value: float):
        ...

    @property
    def Vega(self) -> float:
        ...

    @Vega.setter
    def Vega(self, value: float):
        ...

    @property
    def Gamma(self) -> float:
        ...

    @Gamma.setter
    def Gamma(self, value: float):
        ...

    @property
    def Rho(self) -> float:
        ...

    @Rho.setter
    def Rho(self, value: float):
        ...


class MomSpecificInstrument(System.Object):
    """This class has no documentation."""

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...


class InputOrderField(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def channelIndex(self) -> int:
        ...

    @channelIndex.setter
    def channelIndex(self, value: int):
        ...

    @property
    def FundId(self) -> int:
        ...

    @FundId.setter
    def FundId(self, value: int):
        ...

    @property
    def fundId(self) -> int:
        ...

    @fundId.setter
    def fundId(self, value: int):
        ...

    @property
    def FundAccountId(self) -> str:
        ...

    @FundAccountId.setter
    def FundAccountId(self, value: str):
        ...

    @property
    def fundAccountId(self) -> str:
        ...

    @fundAccountId.setter
    def fundAccountId(self, value: str):
        ...

    @property
    def FundChannelType(self) -> str:
        ...

    @FundChannelType.setter
    def FundChannelType(self, value: str):
        ...

    @property
    def fundChannelType(self) -> str:
        ...

    @fundChannelType.setter
    def fundChannelType(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def AccountId(self) -> str:
        ...

    @AccountId.setter
    def AccountId(self, value: str):
        ...

    @property
    def accountId(self) -> str:
        ...

    @accountId.setter
    def accountId(self, value: str):
        ...

    @property
    def OrderRef(self) -> int:
        ...

    @OrderRef.setter
    def OrderRef(self, value: int):
        ...

    @property
    def orderRef(self) -> int:
        ...

    @orderRef.setter
    def orderRef(self, value: int):
        ...

    @property
    def InputLocalId(self) -> int:
        ...

    @InputLocalId.setter
    def InputLocalId(self, value: int):
        ...

    @property
    def inputLocalId(self) -> int:
        ...

    @inputLocalId.setter
    def inputLocalId(self, value: int):
        ...

    @property
    def StrategyInputId(self) -> int:
        ...

    @StrategyInputId.setter
    def StrategyInputId(self, value: int):
        ...

    @property
    def strategyInputId(self) -> int:
        ...

    @strategyInputId.setter
    def strategyInputId(self, value: int):
        ...

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def instrumentId(self) -> str:
        ...

    @instrumentId.setter
    def instrumentId(self, value: str):
        ...

    @property
    def ProductClass(self) -> int:
        ...

    @ProductClass.setter
    def ProductClass(self, value: int):
        ...

    @property
    def productClass(self) -> int:
        ...

    @productClass.setter
    def productClass(self, value: int):
        ...

    @property
    def ExchangeSymbol(self) -> str:
        ...

    @ExchangeSymbol.setter
    def ExchangeSymbol(self, value: str):
        ...

    @property
    def exchangeSymbol(self) -> str:
        ...

    @exchangeSymbol.setter
    def exchangeSymbol(self, value: str):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def exchangeId(self) -> str:
        ...

    @exchangeId.setter
    def exchangeId(self, value: str):
        ...

    @property
    def OrderStatus(self) -> int:
        ...

    @OrderStatus.setter
    def OrderStatus(self, value: int):
        ...

    @property
    def orderStatus(self) -> int:
        ...

    @orderStatus.setter
    def orderStatus(self, value: int):
        ...

    @property
    def OrderSubmitStatus(self) -> int:
        ...

    @OrderSubmitStatus.setter
    def OrderSubmitStatus(self, value: int):
        ...

    @property
    def orderSubmitStatus(self) -> int:
        ...

    @orderSubmitStatus.setter
    def orderSubmitStatus(self, value: int):
        ...

    @property
    def OrderSysId(self) -> str:
        ...

    @OrderSysId.setter
    def OrderSysId(self, value: str):
        ...

    @property
    def orderSysId(self) -> str:
        ...

    @orderSysId.setter
    def orderSysId(self, value: str):
        ...

    @property
    def OrderPriceType(self) -> int:
        ...

    @OrderPriceType.setter
    def OrderPriceType(self, value: int):
        ...

    @property
    def orderPriceType(self) -> int:
        ...

    @orderPriceType.setter
    def orderPriceType(self, value: int):
        ...

    @property
    def Direction(self) -> int:
        ...

    @Direction.setter
    def Direction(self, value: int):
        ...

    @property
    def direction(self) -> int:
        ...

    @direction.setter
    def direction(self, value: int):
        ...

    @property
    def LimitPrice(self) -> float:
        ...

    @LimitPrice.setter
    def LimitPrice(self, value: float):
        ...

    @property
    def limitPrice(self) -> float:
        ...

    @limitPrice.setter
    def limitPrice(self, value: float):
        ...

    @property
    def VolumeTotalOriginal(self) -> float:
        ...

    @VolumeTotalOriginal.setter
    def VolumeTotalOriginal(self, value: float):
        ...

    @property
    def volumeTotalOriginal(self) -> float:
        ...

    @volumeTotalOriginal.setter
    def volumeTotalOriginal(self, value: float):
        ...

    @property
    def OpenVolume(self) -> float:
        ...

    @OpenVolume.setter
    def OpenVolume(self, value: float):
        ...

    @property
    def openVolume(self) -> float:
        ...

    @openVolume.setter
    def openVolume(self, value: float):
        ...

    @property
    def CloseVolume(self) -> float:
        ...

    @CloseVolume.setter
    def CloseVolume(self, value: float):
        ...

    @property
    def closeVolume(self) -> float:
        ...

    @closeVolume.setter
    def closeVolume(self, value: float):
        ...

    @property
    def VolumeTraded(self) -> float:
        ...

    @VolumeTraded.setter
    def VolumeTraded(self, value: float):
        ...

    @property
    def volumeTraded(self) -> float:
        ...

    @volumeTraded.setter
    def volumeTraded(self, value: float):
        ...

    @property
    def TimeCondition(self) -> int:
        ...

    @TimeCondition.setter
    def TimeCondition(self, value: int):
        ...

    @property
    def timeCondition(self) -> int:
        ...

    @timeCondition.setter
    def timeCondition(self, value: int):
        ...

    @property
    def VolumeCondition(self) -> int:
        ...

    @VolumeCondition.setter
    def VolumeCondition(self, value: int):
        ...

    @property
    def volumeCondition(self) -> int:
        ...

    @volumeCondition.setter
    def volumeCondition(self, value: int):
        ...

    @property
    def ContingentCondition(self) -> int:
        ...

    @ContingentCondition.setter
    def ContingentCondition(self, value: int):
        ...

    @property
    def contingentCondition(self) -> int:
        ...

    @contingentCondition.setter
    def contingentCondition(self, value: int):
        ...

    @property
    def StopPrice(self) -> float:
        ...

    @StopPrice.setter
    def StopPrice(self, value: float):
        ...

    @property
    def stopPrice(self) -> float:
        ...

    @stopPrice.setter
    def stopPrice(self, value: float):
        ...

    @property
    def FrozenCommission(self) -> float:
        ...

    @FrozenCommission.setter
    def FrozenCommission(self, value: float):
        ...

    @property
    def frozenCommission(self) -> float:
        ...

    @frozenCommission.setter
    def frozenCommission(self, value: float):
        ...

    @property
    def FrozenMargin(self) -> float:
        ...

    @FrozenMargin.setter
    def FrozenMargin(self, value: float):
        ...

    @property
    def frozenMargin(self) -> float:
        ...

    @frozenMargin.setter
    def frozenMargin(self, value: float):
        ...

    @property
    def FrozenPremium(self) -> float:
        ...

    @FrozenPremium.setter
    def FrozenPremium(self, value: float):
        ...

    @property
    def frozenPremium(self) -> float:
        ...

    @frozenPremium.setter
    def frozenPremium(self, value: float):
        ...

    @property
    def Advanced(self) -> str:
        ...

    @Advanced.setter
    def Advanced(self, value: str):
        ...

    @property
    def advanced(self) -> str:
        ...

    @advanced.setter
    def advanced(self, value: str):
        ...

    @property
    def TriggerType(self) -> int:
        ...

    @TriggerType.setter
    def TriggerType(self, value: int):
        ...

    @property
    def triggerType(self) -> int:
        ...

    @triggerType.setter
    def triggerType(self, value: int):
        ...

    @property
    def StopOrderId(self) -> str:
        ...

    @StopOrderId.setter
    def StopOrderId(self, value: str):
        ...

    @property
    def stopOrderId(self) -> str:
        ...

    @stopOrderId.setter
    def stopOrderId(self, value: str):
        ...

    @property
    def StopWorkingType(self) -> int:
        ...

    @StopWorkingType.setter
    def StopWorkingType(self, value: int):
        ...

    @property
    def stopWorkingType(self) -> int:
        ...

    @stopWorkingType.setter
    def stopWorkingType(self, value: int):
        ...

    @property
    def StatusMsg(self) -> str:
        ...

    @StatusMsg.setter
    def StatusMsg(self, value: str):
        ...

    @property
    def statusMsg(self) -> str:
        ...

    @statusMsg.setter
    def statusMsg(self, value: str):
        ...

    @property
    def Timestamp1(self) -> int:
        ...

    @Timestamp1.setter
    def Timestamp1(self, value: int):
        ...

    @property
    def timestamp1(self) -> int:
        ...

    @timestamp1.setter
    def timestamp1(self, value: int):
        ...

    @property
    def Timestamp2(self) -> int:
        ...

    @Timestamp2.setter
    def Timestamp2(self, value: int):
        ...

    @property
    def timestamp2(self) -> int:
        ...

    @timestamp2.setter
    def timestamp2(self, value: int):
        ...

    @property
    def Version(self) -> int:
        ...

    @Version.setter
    def Version(self, value: int):
        ...

    @property
    def version(self) -> int:
        ...

    @version.setter
    def version(self, value: int):
        ...

    def UpdateVersion(self) -> None:
        ...


class MomInputOrder(MomCrypto.Api.InputOrderField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomInputOrder:
        ...

    def ToFundInput(self) -> MomCrypto.Api.MomFundInputOrder:
        ...

    def ToString(self) -> str:
        ...


class MomInputOrderAction(System.Object):
    """This class has no documentation."""

    @property
    def channelIndex(self) -> int:
        ...

    @channelIndex.setter
    def channelIndex(self, value: int):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def OrderRef(self) -> int:
        ...

    @OrderRef.setter
    def OrderRef(self, value: int):
        ...

    @property
    def orderRef(self) -> int:
        ...

    @orderRef.setter
    def orderRef(self, value: int):
        ...

    @property
    def InputLocalId(self) -> int:
        ...

    @InputLocalId.setter
    def InputLocalId(self, value: int):
        ...

    @property
    def inputLocalId(self) -> int:
        ...

    @inputLocalId.setter
    def inputLocalId(self, value: int):
        ...

    @property
    def StrategyInputId(self) -> int:
        ...

    @StrategyInputId.setter
    def StrategyInputId(self, value: int):
        ...

    @property
    def strategyInputId(self) -> int:
        ...

    @strategyInputId.setter
    def strategyInputId(self, value: int):
        ...

    @property
    def FundAccountId(self) -> str:
        ...

    @FundAccountId.setter
    def FundAccountId(self, value: str):
        ...

    @property
    def fundAccountId(self) -> str:
        ...

    @fundAccountId.setter
    def fundAccountId(self, value: str):
        ...

    @property
    def FundChannelType(self) -> str:
        ...

    @FundChannelType.setter
    def FundChannelType(self, value: str):
        ...

    @property
    def fundChannelType(self) -> str:
        ...

    @fundChannelType.setter
    def fundChannelType(self, value: str):
        ...

    @property
    def OrderSysId(self) -> str:
        ...

    @OrderSysId.setter
    def OrderSysId(self, value: str):
        ...

    @property
    def orderSysId(self) -> str:
        ...

    @orderSysId.setter
    def orderSysId(self, value: str):
        ...

    @property
    def StopOrderId(self) -> str:
        ...

    @StopOrderId.setter
    def StopOrderId(self, value: str):
        ...

    @property
    def stopOrderId(self) -> str:
        ...

    @stopOrderId.setter
    def stopOrderId(self, value: str):
        ...

    @property
    def ActionFlag(self) -> int:
        ...

    @ActionFlag.setter
    def ActionFlag(self, value: int):
        ...

    @property
    def actionFlag(self) -> int:
        ...

    @actionFlag.setter
    def actionFlag(self, value: int):
        ...

    def Clone(self) -> MomCrypto.Api.MomInputOrderAction:
        ...

    def ToString(self) -> str:
        ...


class MomQryInstrument(System.Object):
    """This class has no documentation."""

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def ProductId(self) -> str:
        ...

    @ProductId.setter
    def ProductId(self, value: str):
        ...


class MomInstrument(System.Object, System.IEquatable[MomCrypto_Api_MomInstrument]):
    """This class has no documentation."""

    @property
    def index(self) -> int:
        ...

    @index.setter
    def index(self, value: int):
        ...

    @property
    def underlyingIndex(self) -> int:
        ...

    @underlyingIndex.setter
    def underlyingIndex(self, value: int):
        ...

    @property
    def productClassIndex(self) -> int:
        ...

    @productClassIndex.setter
    def productClassIndex(self, value: int):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def symbol(self) -> str:
        ...

    @symbol.setter
    def symbol(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def exchange(self) -> str:
        ...

    @exchange.setter
    def exchange(self, value: str):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def market(self) -> str:
        ...

    @market.setter
    def market(self, value: str):
        ...

    @property
    def InstrumentName(self) -> str:
        ...

    @InstrumentName.setter
    def InstrumentName(self, value: str):
        ...

    @property
    def instrumentName(self) -> str:
        ...

    @instrumentName.setter
    def instrumentName(self, value: str):
        ...

    @property
    def ExchangeSymbol(self) -> str:
        ...

    @ExchangeSymbol.setter
    def ExchangeSymbol(self, value: str):
        ...

    @property
    def exchangeSymbol(self) -> str:
        ...

    @exchangeSymbol.setter
    def exchangeSymbol(self, value: str):
        ...

    @property
    def ProductClass(self) -> int:
        ...

    @ProductClass.setter
    def ProductClass(self, value: int):
        ...

    @property
    def productClass(self) -> int:
        ...

    @productClass.setter
    def productClass(self, value: int):
        ...

    @property
    def DeliveryYear(self) -> int:
        ...

    @DeliveryYear.setter
    def DeliveryYear(self, value: int):
        ...

    @property
    def deliveryYear(self) -> int:
        ...

    @deliveryYear.setter
    def deliveryYear(self, value: int):
        ...

    @property
    def DeliveryMonth(self) -> int:
        ...

    @DeliveryMonth.setter
    def DeliveryMonth(self, value: int):
        ...

    @property
    def deliveryMonth(self) -> int:
        ...

    @deliveryMonth.setter
    def deliveryMonth(self, value: int):
        ...

    @property
    def MaxMarketOrderVolume(self) -> float:
        ...

    @MaxMarketOrderVolume.setter
    def MaxMarketOrderVolume(self, value: float):
        ...

    @property
    def maxMarketOrderVolume(self) -> float:
        ...

    @maxMarketOrderVolume.setter
    def maxMarketOrderVolume(self, value: float):
        ...

    @property
    def MinMarketOrderVolume(self) -> float:
        ...

    @MinMarketOrderVolume.setter
    def MinMarketOrderVolume(self, value: float):
        ...

    @property
    def minMarketOrderVolume(self) -> float:
        ...

    @minMarketOrderVolume.setter
    def minMarketOrderVolume(self, value: float):
        ...

    @property
    def MaxLimitOrderVolume(self) -> float:
        ...

    @MaxLimitOrderVolume.setter
    def MaxLimitOrderVolume(self, value: float):
        ...

    @property
    def maxLimitOrderVolume(self) -> float:
        ...

    @maxLimitOrderVolume.setter
    def maxLimitOrderVolume(self, value: float):
        ...

    @property
    def MinLimitOrderVolume(self) -> float:
        ...

    @MinLimitOrderVolume.setter
    def MinLimitOrderVolume(self, value: float):
        ...

    @property
    def minLimitOrderVolume(self) -> float:
        ...

    @minLimitOrderVolume.setter
    def minLimitOrderVolume(self, value: float):
        ...

    @property
    def VolumeMultiple(self) -> float:
        ...

    @VolumeMultiple.setter
    def VolumeMultiple(self, value: float):
        ...

    @property
    def volumeMultiple(self) -> float:
        ...

    @volumeMultiple.setter
    def volumeMultiple(self, value: float):
        ...

    @property
    def PriceTick(self) -> float:
        ...

    @PriceTick.setter
    def PriceTick(self, value: float):
        ...

    @property
    def priceTick(self) -> float:
        ...

    @priceTick.setter
    def priceTick(self, value: float):
        ...

    @property
    def CreateDate(self) -> str:
        ...

    @CreateDate.setter
    def CreateDate(self, value: str):
        ...

    @property
    def createDate(self) -> str:
        ...

    @createDate.setter
    def createDate(self, value: str):
        ...

    @property
    def OpenDate(self) -> str:
        ...

    @OpenDate.setter
    def OpenDate(self, value: str):
        ...

    @property
    def openDate(self) -> str:
        ...

    @openDate.setter
    def openDate(self, value: str):
        ...

    @property
    def ExpireDate(self) -> str:
        ...

    @ExpireDate.setter
    def ExpireDate(self, value: str):
        ...

    @property
    def expireDate(self) -> str:
        ...

    @expireDate.setter
    def expireDate(self, value: str):
        ...

    @property
    def StartDeliveryDate(self) -> str:
        ...

    @StartDeliveryDate.setter
    def StartDeliveryDate(self, value: str):
        ...

    @property
    def startDeliveryDate(self) -> str:
        ...

    @startDeliveryDate.setter
    def startDeliveryDate(self, value: str):
        ...

    @property
    def EndDeliveryDate(self) -> str:
        ...

    @EndDeliveryDate.setter
    def EndDeliveryDate(self, value: str):
        ...

    @property
    def endDeliveryDate(self) -> str:
        ...

    @endDeliveryDate.setter
    def endDeliveryDate(self, value: str):
        ...

    @property
    def InstLifePhase(self) -> int:
        ...

    @InstLifePhase.setter
    def InstLifePhase(self, value: int):
        ...

    @property
    def instLifePhase(self) -> int:
        ...

    @instLifePhase.setter
    def instLifePhase(self, value: int):
        ...

    @property
    def TradingRules(self) -> int:
        ...

    @TradingRules.setter
    def TradingRules(self, value: int):
        ...

    @property
    def tradingRules(self) -> int:
        ...

    @tradingRules.setter
    def tradingRules(self, value: int):
        ...

    @property
    def PositionType(self) -> int:
        ...

    @PositionType.setter
    def PositionType(self, value: int):
        ...

    @property
    def positionType(self) -> int:
        ...

    @positionType.setter
    def positionType(self, value: int):
        ...

    @property
    def UnderlyingSymbol(self) -> str:
        ...

    @UnderlyingSymbol.setter
    def UnderlyingSymbol(self, value: str):
        ...

    @property
    def underlyingSymbol(self) -> str:
        ...

    @underlyingSymbol.setter
    def underlyingSymbol(self, value: str):
        ...

    @property
    def StrikePrice(self) -> float:
        ...

    @StrikePrice.setter
    def StrikePrice(self, value: float):
        ...

    @property
    def strikePrice(self) -> float:
        ...

    @strikePrice.setter
    def strikePrice(self, value: float):
        ...

    @property
    def OptionsType(self) -> int:
        ...

    @OptionsType.setter
    def OptionsType(self, value: int):
        ...

    @property
    def optionsType(self) -> int:
        ...

    @optionsType.setter
    def optionsType(self, value: int):
        ...

    @property
    def UnderlyingMultiple(self) -> float:
        ...

    @UnderlyingMultiple.setter
    def UnderlyingMultiple(self, value: float):
        ...

    @property
    def underlyingMultiple(self) -> float:
        ...

    @underlyingMultiple.setter
    def underlyingMultiple(self, value: float):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def quoteCurrency(self) -> str:
        ...

    @quoteCurrency.setter
    def quoteCurrency(self, value: str):
        ...

    @property
    def BaseCurrency(self) -> str:
        ...

    @BaseCurrency.setter
    def BaseCurrency(self, value: str):
        ...

    @property
    def baseCurrency(self) -> str:
        ...

    @baseCurrency.setter
    def baseCurrency(self, value: str):
        ...

    @property
    def TradingClass(self) -> str:
        ...

    @TradingClass.setter
    def TradingClass(self, value: str):
        ...

    @property
    def tradingClass(self) -> str:
        ...

    @tradingClass.setter
    def tradingClass(self, value: str):
        ...

    @property
    def PrimaryExch(self) -> str:
        ...

    @PrimaryExch.setter
    def PrimaryExch(self, value: str):
        ...

    @property
    def primaryExch(self) -> str:
        ...

    @primaryExch.setter
    def primaryExch(self, value: str):
        ...

    def Clone(self) -> MomCrypto.Api.MomInstrument:
        ...

    @overload
    def Equals(self, other: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...


class OrderField(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def timestamp(self) -> datetime.datetime:
        ...

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        ...

    @property
    def FundId(self) -> int:
        ...

    @FundId.setter
    def FundId(self, value: int):
        ...

    @property
    def fundId(self) -> int:
        ...

    @fundId.setter
    def fundId(self, value: int):
        ...

    @property
    def FundAccountId(self) -> str:
        ...

    @FundAccountId.setter
    def FundAccountId(self, value: str):
        ...

    @property
    def fundAccountId(self) -> str:
        ...

    @fundAccountId.setter
    def fundAccountId(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def AccountId(self) -> str:
        ...

    @AccountId.setter
    def AccountId(self, value: str):
        ...

    @property
    def accountId(self) -> str:
        ...

    @accountId.setter
    def accountId(self, value: str):
        ...

    @property
    def StrategyInputId(self) -> int:
        ...

    @StrategyInputId.setter
    def StrategyInputId(self, value: int):
        ...

    @property
    def strategyInputId(self) -> int:
        ...

    @strategyInputId.setter
    def strategyInputId(self, value: int):
        ...

    @property
    def OrderRef(self) -> int:
        ...

    @OrderRef.setter
    def OrderRef(self, value: int):
        ...

    @property
    def orderRef(self) -> int:
        ...

    @orderRef.setter
    def orderRef(self, value: int):
        ...

    @property
    def OrderLocalId(self) -> int:
        ...

    @OrderLocalId.setter
    def OrderLocalId(self, value: int):
        ...

    @property
    def orderLocalId(self) -> int:
        ...

    @orderLocalId.setter
    def orderLocalId(self, value: int):
        ...

    @property
    def InputLocalId(self) -> int:
        ...

    @InputLocalId.setter
    def InputLocalId(self, value: int):
        ...

    @property
    def inputLocalId(self) -> int:
        ...

    @inputLocalId.setter
    def inputLocalId(self, value: int):
        ...

    @property
    def OrderSysId(self) -> str:
        ...

    @OrderSysId.setter
    def OrderSysId(self, value: str):
        ...

    @property
    def orderSysId(self) -> str:
        ...

    @orderSysId.setter
    def orderSysId(self, value: str):
        ...

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def instrumentId(self) -> str:
        ...

    @instrumentId.setter
    def instrumentId(self, value: str):
        ...

    @property
    def ProductClass(self) -> int:
        ...

    @ProductClass.setter
    def ProductClass(self, value: int):
        ...

    @property
    def productClass(self) -> int:
        ...

    @productClass.setter
    def productClass(self, value: int):
        ...

    @property
    def ExchangeSymbol(self) -> str:
        ...

    @ExchangeSymbol.setter
    def ExchangeSymbol(self, value: str):
        ...

    @property
    def exchangeSymbol(self) -> str:
        ...

    @exchangeSymbol.setter
    def exchangeSymbol(self, value: str):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def exchangeId(self) -> str:
        ...

    @exchangeId.setter
    def exchangeId(self, value: str):
        ...

    @property
    def OrderPriceType(self) -> int:
        ...

    @OrderPriceType.setter
    def OrderPriceType(self, value: int):
        ...

    @property
    def orderPriceType(self) -> int:
        ...

    @orderPriceType.setter
    def orderPriceType(self, value: int):
        ...

    @property
    def Direction(self) -> int:
        ...

    @Direction.setter
    def Direction(self, value: int):
        ...

    @property
    def direction(self) -> int:
        ...

    @direction.setter
    def direction(self, value: int):
        ...

    @property
    def LimitPrice(self) -> float:
        ...

    @LimitPrice.setter
    def LimitPrice(self, value: float):
        ...

    @property
    def limitPrice(self) -> float:
        ...

    @limitPrice.setter
    def limitPrice(self, value: float):
        ...

    @property
    def VolumeTotalOriginal(self) -> float:
        ...

    @VolumeTotalOriginal.setter
    def VolumeTotalOriginal(self, value: float):
        ...

    @property
    def volumeTotalOriginal(self) -> float:
        ...

    @volumeTotalOriginal.setter
    def volumeTotalOriginal(self, value: float):
        ...

    @property
    def TimeCondition(self) -> int:
        ...

    @TimeCondition.setter
    def TimeCondition(self, value: int):
        ...

    @property
    def timeCondition(self) -> int:
        ...

    @timeCondition.setter
    def timeCondition(self, value: int):
        ...

    @property
    def VolumeCondition(self) -> int:
        ...

    @VolumeCondition.setter
    def VolumeCondition(self, value: int):
        ...

    @property
    def volumeCondition(self) -> int:
        ...

    @volumeCondition.setter
    def volumeCondition(self, value: int):
        ...

    @property
    def MinVolume(self) -> float:
        ...

    @MinVolume.setter
    def MinVolume(self, value: float):
        ...

    @property
    def minVolume(self) -> float:
        ...

    @minVolume.setter
    def minVolume(self, value: float):
        ...

    @property
    def ContingentCondition(self) -> int:
        ...

    @ContingentCondition.setter
    def ContingentCondition(self, value: int):
        ...

    @property
    def contingentCondition(self) -> int:
        ...

    @contingentCondition.setter
    def contingentCondition(self, value: int):
        ...

    @property
    def StopPrice(self) -> float:
        ...

    @StopPrice.setter
    def StopPrice(self, value: float):
        ...

    @property
    def stopPrice(self) -> float:
        ...

    @stopPrice.setter
    def stopPrice(self, value: float):
        ...

    @property
    def OrderStatus(self) -> int:
        ...

    @OrderStatus.setter
    def OrderStatus(self, value: int):
        ...

    @property
    def orderStatus(self) -> int:
        ...

    @orderStatus.setter
    def orderStatus(self, value: int):
        ...

    @property
    def OrderSubmitStatus(self) -> int:
        ...

    @OrderSubmitStatus.setter
    def OrderSubmitStatus(self, value: int):
        ...

    @property
    def orderSubmitStatus(self) -> int:
        ...

    @orderSubmitStatus.setter
    def orderSubmitStatus(self, value: int):
        ...

    @property
    def VolumeTraded(self) -> float:
        ...

    @VolumeTraded.setter
    def VolumeTraded(self, value: float):
        ...

    @property
    def volumeTraded(self) -> float:
        ...

    @volumeTraded.setter
    def volumeTraded(self, value: float):
        ...

    @property
    def VolumeTotal(self) -> float:
        ...

    @VolumeTotal.setter
    def VolumeTotal(self, value: float):
        ...

    @property
    def volumeTotal(self) -> float:
        ...

    @volumeTotal.setter
    def volumeTotal(self, value: float):
        ...

    @property
    def InsertDate(self) -> str:
        ...

    @InsertDate.setter
    def InsertDate(self, value: str):
        ...

    @property
    def insertDate(self) -> str:
        ...

    @insertDate.setter
    def insertDate(self, value: str):
        ...

    @property
    def InsertTime(self) -> str:
        ...

    @InsertTime.setter
    def InsertTime(self, value: str):
        ...

    @property
    def insertTime(self) -> str:
        ...

    @insertTime.setter
    def insertTime(self, value: str):
        ...

    @property
    def UpdateTime(self) -> str:
        ...

    @UpdateTime.setter
    def UpdateTime(self, value: str):
        ...

    @property
    def updateTime(self) -> str:
        ...

    @updateTime.setter
    def updateTime(self, value: str):
        ...

    @property
    def CancelTime(self) -> str:
        ...

    @CancelTime.setter
    def CancelTime(self, value: str):
        ...

    @property
    def cancelTime(self) -> str:
        ...

    @cancelTime.setter
    def cancelTime(self, value: str):
        ...

    @property
    def StatusMsg(self) -> str:
        ...

    @StatusMsg.setter
    def StatusMsg(self, value: str):
        ...

    @property
    def statusMsg(self) -> str:
        ...

    @statusMsg.setter
    def statusMsg(self, value: str):
        ...

    @property
    def USD(self) -> float:
        ...

    @USD.setter
    def USD(self, value: float):
        ...

    @property
    def usd(self) -> float:
        ...

    @usd.setter
    def usd(self, value: float):
        ...

    @property
    def Triggered(self) -> bool:
        ...

    @Triggered.setter
    def Triggered(self, value: bool):
        ...

    @property
    def triggered(self) -> bool:
        ...

    @triggered.setter
    def triggered(self, value: bool):
        ...

    @property
    def TriggerType(self) -> int:
        ...

    @TriggerType.setter
    def TriggerType(self, value: int):
        ...

    @property
    def triggerType(self) -> int:
        ...

    @triggerType.setter
    def triggerType(self, value: int):
        ...

    @property
    def StopOrderId(self) -> str:
        ...

    @StopOrderId.setter
    def StopOrderId(self, value: str):
        ...

    @property
    def stopOrderId(self) -> str:
        ...

    @stopOrderId.setter
    def stopOrderId(self, value: str):
        ...

    @property
    def StopWorkingType(self) -> int:
        ...

    @StopWorkingType.setter
    def StopWorkingType(self, value: int):
        ...

    @property
    def stopWorkingType(self) -> int:
        ...

    @stopWorkingType.setter
    def stopWorkingType(self, value: int):
        ...

    @property
    def Version(self) -> int:
        ...

    @Version.setter
    def Version(self, value: int):
        ...

    @property
    def version(self) -> int:
        ...

    @version.setter
    def version(self, value: int):
        ...

    def UpdateVersion(self) -> None:
        ...


class MomOrder(MomCrypto.Api.OrderField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomOrder:
        ...

    def ToString(self) -> str:
        ...


class TradeField(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def timestamp(self) -> datetime.datetime:
        ...

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        ...

    @property
    def FundId(self) -> int:
        ...

    @FundId.setter
    def FundId(self, value: int):
        ...

    @property
    def fundId(self) -> int:
        ...

    @fundId.setter
    def fundId(self, value: int):
        ...

    @property
    def FundAccountId(self) -> str:
        ...

    @FundAccountId.setter
    def FundAccountId(self, value: str):
        ...

    @property
    def fundAccountId(self) -> str:
        ...

    @fundAccountId.setter
    def fundAccountId(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def AccountId(self) -> str:
        ...

    @AccountId.setter
    def AccountId(self, value: str):
        ...

    @property
    def accountId(self) -> str:
        ...

    @accountId.setter
    def accountId(self, value: str):
        ...

    @property
    def StrategyInputId(self) -> int:
        ...

    @StrategyInputId.setter
    def StrategyInputId(self, value: int):
        ...

    @property
    def strategyInputId(self) -> int:
        ...

    @strategyInputId.setter
    def strategyInputId(self, value: int):
        ...

    @property
    def TradeLocalId(self) -> int:
        ...

    @TradeLocalId.setter
    def TradeLocalId(self, value: int):
        ...

    @property
    def tradeLocalId(self) -> int:
        ...

    @tradeLocalId.setter
    def tradeLocalId(self, value: int):
        ...

    @property
    def InputLocalId(self) -> int:
        ...

    @InputLocalId.setter
    def InputLocalId(self, value: int):
        ...

    @property
    def inputLocalId(self) -> int:
        ...

    @inputLocalId.setter
    def inputLocalId(self, value: int):
        ...

    @property
    def OrderLocalId(self) -> int:
        ...

    @OrderLocalId.setter
    def OrderLocalId(self, value: int):
        ...

    @property
    def orderLocalId(self) -> int:
        ...

    @orderLocalId.setter
    def orderLocalId(self, value: int):
        ...

    @property
    def OrderRef(self) -> int:
        ...

    @OrderRef.setter
    def OrderRef(self, value: int):
        ...

    @property
    def orderRef(self) -> int:
        ...

    @orderRef.setter
    def orderRef(self, value: int):
        ...

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def instrumentId(self) -> str:
        ...

    @instrumentId.setter
    def instrumentId(self, value: str):
        ...

    @property
    def ExchangeSymbol(self) -> str:
        ...

    @ExchangeSymbol.setter
    def ExchangeSymbol(self, value: str):
        ...

    @property
    def exchangeSymbol(self) -> str:
        ...

    @exchangeSymbol.setter
    def exchangeSymbol(self, value: str):
        ...

    @property
    def ProductClass(self) -> int:
        ...

    @ProductClass.setter
    def ProductClass(self, value: int):
        ...

    @property
    def productClass(self) -> int:
        ...

    @productClass.setter
    def productClass(self, value: int):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def exchangeId(self) -> str:
        ...

    @exchangeId.setter
    def exchangeId(self, value: str):
        ...

    @property
    def TradeId(self) -> str:
        ...

    @TradeId.setter
    def TradeId(self, value: str):
        ...

    @property
    def tradeId(self) -> str:
        ...

    @tradeId.setter
    def tradeId(self, value: str):
        ...

    @property
    def Direction(self) -> int:
        ...

    @Direction.setter
    def Direction(self, value: int):
        ...

    @property
    def direction(self) -> int:
        ...

    @direction.setter
    def direction(self, value: int):
        ...

    @property
    def OrderSysId(self) -> str:
        ...

    @OrderSysId.setter
    def OrderSysId(self, value: str):
        ...

    @property
    def orderSysId(self) -> str:
        ...

    @orderSysId.setter
    def orderSysId(self, value: str):
        ...

    @property
    def TradingRole(self) -> int:
        ...

    @TradingRole.setter
    def TradingRole(self, value: int):
        ...

    @property
    def tradingRole(self) -> int:
        ...

    @tradingRole.setter
    def tradingRole(self, value: int):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def price(self) -> float:
        ...

    @price.setter
    def price(self, value: float):
        ...

    @property
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...

    @property
    def volume(self) -> float:
        ...

    @volume.setter
    def volume(self, value: float):
        ...

    @property
    def Margin(self) -> float:
        ...

    @Margin.setter
    def Margin(self, value: float):
        ...

    @property
    def margin(self) -> float:
        ...

    @margin.setter
    def margin(self, value: float):
        ...

    @property
    def Commission(self) -> float:
        ...

    @Commission.setter
    def Commission(self, value: float):
        ...

    @property
    def commission(self) -> float:
        ...

    @commission.setter
    def commission(self, value: float):
        ...

    @property
    def CommissionAsset(self) -> str:
        ...

    @CommissionAsset.setter
    def CommissionAsset(self, value: str):
        ...

    @property
    def commissionAsset(self) -> str:
        ...

    @commissionAsset.setter
    def commissionAsset(self, value: str):
        ...

    @property
    def TradeDate(self) -> str:
        ...

    @TradeDate.setter
    def TradeDate(self, value: str):
        ...

    @property
    def tradeDate(self) -> str:
        ...

    @tradeDate.setter
    def tradeDate(self, value: str):
        ...

    @property
    def TradeTime(self) -> str:
        ...

    @TradeTime.setter
    def TradeTime(self, value: str):
        ...

    @property
    def tradeTime(self) -> str:
        ...

    @tradeTime.setter
    def tradeTime(self, value: str):
        ...

    @property
    def TradeType(self) -> int:
        ...

    @TradeType.setter
    def TradeType(self, value: int):
        ...

    @property
    def tradeType(self) -> int:
        ...

    @tradeType.setter
    def tradeType(self, value: int):
        ...

    @property
    def PriceSource(self) -> int:
        ...

    @PriceSource.setter
    def PriceSource(self, value: int):
        ...

    @property
    def priceSource(self) -> int:
        ...

    @priceSource.setter
    def priceSource(self, value: int):
        ...

    @property
    def TradeSource(self) -> int:
        ...

    @TradeSource.setter
    def TradeSource(self, value: int):
        ...

    @property
    def tradeSource(self) -> int:
        ...

    @tradeSource.setter
    def tradeSource(self, value: int):
        ...

    @property
    def BuyVolume(self) -> float:
        ...

    @BuyVolume.setter
    def BuyVolume(self, value: float):
        ...

    @property
    def buyVolume(self) -> float:
        ...

    @buyVolume.setter
    def buyVolume(self, value: float):
        ...

    @property
    def SellVolume(self) -> float:
        ...

    @SellVolume.setter
    def SellVolume(self, value: float):
        ...

    @property
    def sellVolume(self) -> float:
        ...

    @sellVolume.setter
    def sellVolume(self, value: float):
        ...

    @property
    def IsTaker(self) -> bool:
        ...

    @IsTaker.setter
    def IsTaker(self, value: bool):
        ...

    @property
    def isTaker(self) -> bool:
        ...

    @isTaker.setter
    def isTaker(self, value: bool):
        ...

    @property
    def Amount(self) -> float:
        ...

    @Amount.setter
    def Amount(self, value: float):
        ...

    @property
    def amount(self) -> float:
        ...

    @amount.setter
    def amount(self, value: float):
        ...

    @property
    def Version(self) -> int:
        ...

    @Version.setter
    def Version(self, value: int):
        ...

    @property
    def version(self) -> int:
        ...

    @version.setter
    def version(self, value: int):
        ...

    def UpdateVersion(self) -> None:
        ...


class MomTrade(MomCrypto.Api.TradeField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomTrade:
        ...

    def ToString(self) -> str:
        ...


class MomAccount(MomCrypto.Api.AccountField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomAccount:
        ...

    def ToString(self) -> str:
        ...


class PositionField(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def FundId(self) -> int:
        ...

    @FundId.setter
    def FundId(self, value: int):
        ...

    @property
    def fundId(self) -> int:
        ...

    @fundId.setter
    def fundId(self, value: int):
        ...

    @property
    def FundAccountId(self) -> str:
        ...

    @FundAccountId.setter
    def FundAccountId(self, value: str):
        ...

    @property
    def fundAccountId(self) -> str:
        ...

    @fundAccountId.setter
    def fundAccountId(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def AccountId(self) -> str:
        ...

    @AccountId.setter
    def AccountId(self, value: str):
        ...

    @property
    def accountId(self) -> str:
        ...

    @accountId.setter
    def accountId(self, value: str):
        ...

    @property
    def PositionId(self) -> int:
        ...

    @PositionId.setter
    def PositionId(self, value: int):
        ...

    @property
    def positionId(self) -> int:
        ...

    @positionId.setter
    def positionId(self, value: int):
        ...

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def instrumentId(self) -> str:
        ...

    @instrumentId.setter
    def instrumentId(self, value: str):
        ...

    @property
    def ExchangeSymbol(self) -> str:
        ...

    @ExchangeSymbol.setter
    def ExchangeSymbol(self, value: str):
        ...

    @property
    def exchangeSymbol(self) -> str:
        ...

    @exchangeSymbol.setter
    def exchangeSymbol(self, value: str):
        ...

    @property
    def ProductClass(self) -> int:
        ...

    @ProductClass.setter
    def ProductClass(self, value: int):
        ...

    @property
    def productClass(self) -> int:
        ...

    @productClass.setter
    def productClass(self, value: int):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def exchangeId(self) -> str:
        ...

    @exchangeId.setter
    def exchangeId(self, value: str):
        ...

    @property
    def Position(self) -> float:
        ...

    @Position.setter
    def Position(self, value: float):
        ...

    @property
    def position(self) -> float:
        ...

    @position.setter
    def position(self, value: float):
        ...

    @property
    def SellFrozen(self) -> float:
        ...

    @SellFrozen.setter
    def SellFrozen(self, value: float):
        ...

    @property
    def sellFrozen(self) -> float:
        ...

    @sellFrozen.setter
    def sellFrozen(self, value: float):
        ...

    @property
    def BuyFrozen(self) -> float:
        ...

    @BuyFrozen.setter
    def BuyFrozen(self, value: float):
        ...

    @property
    def buyFrozen(self) -> float:
        ...

    @buyFrozen.setter
    def buyFrozen(self, value: float):
        ...

    @property
    def SellUnfrozen(self) -> float:
        ...

    @SellUnfrozen.setter
    def SellUnfrozen(self, value: float):
        ...

    @property
    def sellUnfrozen(self) -> float:
        ...

    @sellUnfrozen.setter
    def sellUnfrozen(self, value: float):
        ...

    @property
    def BuyUnfrozen(self) -> float:
        ...

    @BuyUnfrozen.setter
    def BuyUnfrozen(self, value: float):
        ...

    @property
    def buyUnfrozen(self) -> float:
        ...

    @buyUnfrozen.setter
    def buyUnfrozen(self, value: float):
        ...

    @property
    def BuyVolume(self) -> float:
        ...

    @BuyVolume.setter
    def BuyVolume(self, value: float):
        ...

    @property
    def buyVolume(self) -> float:
        ...

    @buyVolume.setter
    def buyVolume(self, value: float):
        ...

    @property
    def SellVolume(self) -> float:
        ...

    @SellVolume.setter
    def SellVolume(self, value: float):
        ...

    @property
    def sellVolume(self) -> float:
        ...

    @sellVolume.setter
    def sellVolume(self, value: float):
        ...

    @property
    def BuyAmount(self) -> float:
        ...

    @BuyAmount.setter
    def BuyAmount(self, value: float):
        ...

    @property
    def buyAmount(self) -> float:
        ...

    @buyAmount.setter
    def buyAmount(self, value: float):
        ...

    @property
    def SellAmount(self) -> float:
        ...

    @SellAmount.setter
    def SellAmount(self, value: float):
        ...

    @property
    def sellAmount(self) -> float:
        ...

    @sellAmount.setter
    def sellAmount(self, value: float):
        ...

    @property
    def PositionCost(self) -> float:
        ...

    @PositionCost.setter
    def PositionCost(self, value: float):
        ...

    @property
    def positionCost(self) -> float:
        ...

    @positionCost.setter
    def positionCost(self, value: float):
        ...

    @property
    def UseMargin(self) -> float:
        ...

    @UseMargin.setter
    def UseMargin(self, value: float):
        ...

    @property
    def useMargin(self) -> float:
        ...

    @useMargin.setter
    def useMargin(self, value: float):
        ...

    @property
    def Commission(self) -> float:
        ...

    @Commission.setter
    def Commission(self, value: float):
        ...

    @property
    def commission(self) -> float:
        ...

    @commission.setter
    def commission(self, value: float):
        ...

    @property
    def CloseProfit(self) -> float:
        ...

    @CloseProfit.setter
    def CloseProfit(self, value: float):
        ...

    @property
    def closeProfit(self) -> float:
        ...

    @closeProfit.setter
    def closeProfit(self, value: float):
        ...

    @property
    def PositionProfit(self) -> float:
        ...

    @PositionProfit.setter
    def PositionProfit(self, value: float):
        ...

    @property
    def positionProfit(self) -> float:
        ...

    @positionProfit.setter
    def positionProfit(self, value: float):
        ...

    @property
    def OpenCost(self) -> float:
        ...

    @OpenCost.setter
    def OpenCost(self, value: float):
        ...

    @property
    def openCost(self) -> float:
        ...

    @openCost.setter
    def openCost(self, value: float):
        ...

    @property
    def CashPosition(self) -> float:
        ...

    @CashPosition.setter
    def CashPosition(self, value: float):
        ...

    @property
    def cashPosition(self) -> float:
        ...

    @cashPosition.setter
    def cashPosition(self, value: float):
        ...

    @property
    def Version(self) -> int:
        ...

    @Version.setter
    def Version(self, value: int):
        ...

    @property
    def version(self) -> int:
        ...

    @version.setter
    def version(self, value: int):
        ...

    def UpdateVersion(self) -> None:
        ...


class MomPosition(MomCrypto.Api.PositionField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomPosition:
        ...

    def ToString(self) -> str:
        ...


class MomRspUserLogin(System.Object):
    """This class has no documentation."""

    @property
    def TradingDay(self) -> str:
        ...

    @TradingDay.setter
    def TradingDay(self, value: str):
        ...

    @property
    def LoginTime(self) -> str:
        ...

    @LoginTime.setter
    def LoginTime(self, value: str):
        ...

    @property
    def BrokerID(self) -> str:
        ...

    @BrokerID.setter
    def BrokerID(self, value: str):
        ...

    @property
    def UserID(self) -> str:
        ...

    @UserID.setter
    def UserID(self, value: str):
        ...

    @property
    def SystemName(self) -> str:
        ...

    @SystemName.setter
    def SystemName(self, value: str):
        ...

    @property
    def MaxOrderRef(self) -> str:
        ...

    @MaxOrderRef.setter
    def MaxOrderRef(self, value: str):
        ...

    @property
    def SHFETime(self) -> str:
        ...

    @SHFETime.setter
    def SHFETime(self, value: str):
        ...

    @property
    def DCETime(self) -> str:
        ...

    @DCETime.setter
    def DCETime(self, value: str):
        ...

    @property
    def CZCETime(self) -> str:
        ...

    @CZCETime.setter
    def CZCETime(self, value: str):
        ...

    @property
    def FFEXTime(self) -> str:
        ...

    @FFEXTime.setter
    def FFEXTime(self, value: str):
        ...

    @property
    def INETime(self) -> str:
        ...

    @INETime.setter
    def INETime(self, value: str):
        ...


class MomReqUserLogin(System.Object):
    """This class has no documentation."""

    @property
    def UserID(self) -> str:
        ...

    @UserID.setter
    def UserID(self, value: str):
        ...

    @property
    def Password(self) -> str:
        ...

    @Password.setter
    def Password(self, value: str):
        ...

    @property
    def UserProductInfo(self) -> str:
        ...

    @UserProductInfo.setter
    def UserProductInfo(self, value: str):
        ...

    @property
    def ClientIPAddress(self) -> str:
        ...

    @ClientIPAddress.setter
    def ClientIPAddress(self, value: str):
        ...

    @property
    def LoginRemark(self) -> str:
        ...

    @LoginRemark.setter
    def LoginRemark(self, value: str):
        ...


class MomQryField(System.Object):
    """This class has no documentation."""


class MomQryOrder(MomCrypto.Api.MomQryField):
    """This class has no documentation."""

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def OrderSysId(self) -> str:
        ...

    @OrderSysId.setter
    def OrderSysId(self, value: str):
        ...

    @property
    def InsertTimeStart(self) -> str:
        ...

    @InsertTimeStart.setter
    def InsertTimeStart(self, value: str):
        ...

    @property
    def InsertTimeEnd(self) -> str:
        ...

    @InsertTimeEnd.setter
    def InsertTimeEnd(self, value: str):
        ...


class MomQryTrade(MomCrypto.Api.MomQryField):
    """This class has no documentation."""

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...

    @property
    def TradeId(self) -> str:
        ...

    @TradeId.setter
    def TradeId(self, value: str):
        ...

    @property
    def TradeTimeStart(self) -> str:
        ...

    @TradeTimeStart.setter
    def TradeTimeStart(self, value: str):
        ...

    @property
    def TradeTimeEnd(self) -> str:
        ...

    @TradeTimeEnd.setter
    def TradeTimeEnd(self, value: str):
        ...


class MomQryAccount(MomCrypto.Api.MomQryField):
    """This class has no documentation."""

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...


class MomQryPosition(MomCrypto.Api.MomQryField):
    """This class has no documentation."""

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def InstrumentId(self) -> str:
        ...

    @InstrumentId.setter
    def InstrumentId(self, value: str):
        ...

    @property
    def ExchangeId(self) -> str:
        ...

    @ExchangeId.setter
    def ExchangeId(self, value: str):
        ...


class MomFund(System.Object):
    """This class has no documentation."""

    @property
    def FundId(self) -> int:
        ...

    @FundId.setter
    def FundId(self, value: int):
        ...

    @property
    def fundId(self) -> int:
        ...

    @fundId.setter
    def fundId(self, value: int):
        ...

    @property
    def FundName(self) -> str:
        ...

    @FundName.setter
    def FundName(self, value: str):
        ...

    @property
    def fundName(self) -> str:
        ...

    @fundName.setter
    def fundName(self, value: str):
        ...

    @property
    def InitialCapital(self) -> float:
        ...

    @InitialCapital.setter
    def InitialCapital(self, value: float):
        ...

    @property
    def initialCapital(self) -> float:
        ...

    @initialCapital.setter
    def initialCapital(self, value: float):
        ...

    @property
    def CreatedDate(self) -> str:
        ...

    @CreatedDate.setter
    def CreatedDate(self, value: str):
        ...

    @property
    def createdDate(self) -> str:
        ...

    @createdDate.setter
    def createdDate(self, value: str):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def description(self) -> str:
        ...

    @description.setter
    def description(self, value: str):
        ...

    def Clone(self) -> MomCrypto.Api.MomFund:
        ...


class MomFundOrder(MomCrypto.Api.OrderField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomFundOrder:
        ...

    def ToString(self) -> str:
        ...


class MomFundAccount(MomCrypto.Api.AccountField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomFundAccount:
        ...

    def ToString(self) -> str:
        ...


class MomFundPosition(MomCrypto.Api.PositionField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomFundPosition:
        ...

    def ToString(self) -> str:
        ...


class MomUserAction(System.Object):
    """This class has no documentation."""


class MomChangeLeverage(System.Object):
    """This class has no documentation."""

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def Exchange(self) -> str:
        ...

    @Exchange.setter
    def Exchange(self, value: str):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def Leverage(self) -> int:
        ...

    @Leverage.setter
    def Leverage(self, value: int):
        ...


class MomCashJournal(System.Object):
    """This class has no documentation."""

    @property
    def inserted(self) -> int:
        ...

    @inserted.setter
    def inserted(self, value: int):
        ...

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def operatorId(self) -> str:
        ...

    @operatorId.setter
    def operatorId(self, value: str):
        ...

    @property
    def market(self) -> str:
        ...

    @market.setter
    def market(self, value: str):
        ...

    @property
    def cashJournalType(self) -> int:
        ...

    @cashJournalType.setter
    def cashJournalType(self, value: int):
        ...

    @property
    def rollInAccountId(self) -> str:
        ...

    @rollInAccountId.setter
    def rollInAccountId(self, value: str):
        ...

    @property
    def rollOutAccountId(self) -> str:
        ...

    @rollOutAccountId.setter
    def rollOutAccountId(self, value: str):
        ...

    @property
    def amount(self) -> float:
        ...

    @amount.setter
    def amount(self, value: float):
        ...

    @property
    def description(self) -> str:
        ...

    @description.setter
    def description(self, value: str):
        ...

    @property
    def actionDate(self) -> str:
        ...

    @actionDate.setter
    def actionDate(self, value: str):
        ...

    @property
    def currencyType(self) -> str:
        ...

    @currencyType.setter
    def currencyType(self, value: str):
        ...

    @property
    def Inserted(self) -> int:
        ...

    @Inserted.setter
    def Inserted(self, value: int):
        ...

    @property
    def ActionDate(self) -> str:
        ...

    @ActionDate.setter
    def ActionDate(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def OperatorId(self) -> str:
        ...

    @OperatorId.setter
    def OperatorId(self, value: str):
        ...

    @property
    def RollInAccountId(self) -> str:
        ...

    @RollInAccountId.setter
    def RollInAccountId(self, value: str):
        ...

    @property
    def RollOutAccountId(self) -> str:
        ...

    @RollOutAccountId.setter
    def RollOutAccountId(self, value: str):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def CashJournalType(self) -> int:
        ...

    @CashJournalType.setter
    def CashJournalType(self, value: int):
        ...

    @property
    def Amount(self) -> float:
        ...

    @Amount.setter
    def Amount(self, value: float):
        ...

    @property
    def CurrencyType(self) -> str:
        ...

    @CurrencyType.setter
    def CurrencyType(self, value: str):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    def Clone(self) -> MomCrypto.Api.MomCashJournal:
        ...


class MomAny(System.Object):
    """This class has no documentation."""

    @property
    def refValue(self) -> System.Object:
        """This field is protected."""
        ...

    @property
    def marketData(self) -> MomCrypto.Api.MomDepthMarketData:
        """This field is protected."""
        ...

    @property
    def IntValue(self) -> int:
        ...

    @property
    def StringArray(self) -> typing.List[str]:
        ...

    @property
    def AsSpecificInstrument(self) -> MomCrypto.Api.MomSpecificInstrument:
        ...

    @property
    def AsInputOrder(self) -> MomCrypto.Api.MomInputOrder:
        ...

    @property
    def AsInputOrderAction(self) -> MomCrypto.Api.MomInputOrderAction:
        ...

    @property
    def AsQryInstrument(self) -> MomCrypto.Api.MomQryInstrument:
        ...

    @property
    def AsInstrument(self) -> MomCrypto.Api.MomInstrument:
        ...

    @property
    def AsInstrumentList(self) -> System.Collections.Generic.IList[MomCrypto.Api.MomInstrument]:
        ...

    @property
    def AsOrder(self) -> MomCrypto.Api.MomOrder:
        ...

    @property
    def AsTrade(self) -> MomCrypto.Api.MomTrade:
        ...

    @property
    def AsAccount(self) -> MomCrypto.Api.MomAccount:
        ...

    @property
    def AsPosition(self) -> MomCrypto.Api.MomPosition:
        ...

    @property
    def AsRspUserLogin(self) -> MomCrypto.Api.MomRspUserLogin:
        ...

    @property
    def AsReqUserLogin(self) -> MomCrypto.Api.MomReqUserLogin:
        ...

    @property
    def AsQryOrder(self) -> MomCrypto.Api.MomQryOrder:
        ...

    @property
    def AsQryTrade(self) -> MomCrypto.Api.MomQryTrade:
        ...

    @property
    def AsQryAccount(self) -> MomCrypto.Api.MomQryAccount:
        ...

    @property
    def AsQryPosition(self) -> MomCrypto.Api.MomQryPosition:
        ...

    @property
    def AsFund(self) -> MomCrypto.Api.MomFund:
        ...

    @property
    def AsFundOrder(self) -> MomCrypto.Api.MomFundOrder:
        ...

    @property
    def AsFundAccount(self) -> MomCrypto.Api.MomFundAccount:
        ...

    @property
    def AsFundPosition(self) -> MomCrypto.Api.MomFundPosition:
        ...

    @property
    def AsUserAction(self) -> MomCrypto.Api.MomUserAction:
        ...

    @property
    def AsChangeLeverage(self) -> MomCrypto.Api.MomChangeLeverage:
        ...

    @property
    def AsCashJournal(self) -> MomCrypto.Api.MomCashJournal:
        ...

    @overload
    def __init__(self, value: int) -> None:
        ...

    @overload
    def __init__(self, value: MomCrypto.Api.MomDepthMarketData) -> None:
        ...

    @overload
    def __init__(self, value: typing.List[str]) -> None:
        ...

    @overload
    def __init__(self, value: typing.Any) -> None:
        ...

    @overload
    def __init__(self) -> None:
        ...

    def GetMarketData(self, value: typing.Optional[MomCrypto.Api.MomDepthMarketData]) -> typing.Union[None, MomCrypto.Api.MomDepthMarketData]:
        ...


class MomResponse(System.Object):
    """This class has no documentation."""

    @property
    def Identity(self) -> typing.List[int]:
        ...

    @Identity.setter
    def Identity(self, value: typing.List[int]):
        ...

    @property
    def MsgId(self) -> int:
        ...

    @MsgId.setter
    def MsgId(self, value: int):
        ...

    @property
    def Last(self) -> bool:
        ...

    @Last.setter
    def Last(self, value: bool):
        ...

    @property
    def Index(self) -> int:
        ...

    @Index.setter
    def Index(self, value: int):
        ...

    @property
    def Data(self) -> MomCrypto.Api.MomAny:
        ...

    @Data.setter
    def Data(self, value: MomCrypto.Api.MomAny):
        ...

    @property
    def RspInfo(self) -> MomCrypto.Api.MomRspInfo:
        ...

    @RspInfo.setter
    def RspInfo(self, value: MomCrypto.Api.MomRspInfo):
        ...


class ErrorHelper(System.Object):
    """This class has no documentation."""

    Ok: MomCrypto.Api.MomRspInfo = ...

    InternalError: MomCrypto.Api.MomRspInfo = ...

    InvalidLogin: MomCrypto.Api.MomRspInfo = ...

    SingleUserSessionExceedLimit: MomCrypto.Api.MomRspInfo = ...

    NotLoginYet: MomCrypto.Api.MomRspInfo = ...

    BadField: MomCrypto.Api.MomRspInfo = ...

    BadPriceField: MomCrypto.Api.MomRspInfo = ...

    InstrumentNotFound: MomCrypto.Api.MomRspInfo = ...

    AccountNotFound: MomCrypto.Api.MomRspInfo = ...

    ChannelNotFound: MomCrypto.Api.MomRspInfo = ...

    ChannelIndexError: MomCrypto.Api.MomRspInfo = ...

    DuplicateSubscribe: MomCrypto.Api.MomRspInfo = ...

    InstrumentNotTrading: MomCrypto.Api.MomRspInfo = ...

    UserNotFound: MomCrypto.Api.MomRspInfo = ...

    UserNotActive: MomCrypto.Api.MomRspInfo = ...

    OverClosePosition: MomCrypto.Api.MomRspInfo = ...

    InsufficientMoney: MomCrypto.Api.MomRspInfo = ...

    NoValidTraderAvailable: MomCrypto.Api.MomRspInfo = ...

    OverRequestPerSecond: MomCrypto.Api.MomRspInfo = ...

    OrderNotFound: MomCrypto.Api.MomRspInfo = ...

    ShortSell: MomCrypto.Api.MomRspInfo = ...

    UnsupportedFunction: MomCrypto.Api.MomRspInfo = ...

    DuplicateOrderRef: MomCrypto.Api.MomRspInfo = ...

    PriceOverRange: MomCrypto.Api.MomRspInfo = ...

    UnsuitableOrderStatus: MomCrypto.Api.MomRspInfo = ...

    MarketClosed: MomCrypto.Api.MomRspInfo = ...

    OrderCancelPending: MomCrypto.Api.MomRspInfo = ...

    @staticmethod
    def Error(msg: str, id: int = -1) -> MomCrypto.Api.MomRspInfo:
        ...

    @staticmethod
    def IsOk(rsp: MomCrypto.Api.MomRspInfo) -> bool:
        ...

    @staticmethod
    def NewRspError(identity: typing.List[int], info: MomCrypto.Api.MomRspInfo) -> MomCrypto.Api.MomResponse:
        ...


class SafeExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def ToPlainString(secureStr: System.Security.SecureString) -> str:
        ...

    @staticmethod
    def ToSecureString(plainStr: str) -> System.Security.SecureString:
        ...


class PositionExtension(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetPosition(position: MomCrypto.Api.PositionField) -> float:
        ...

    @staticmethod
    def IsLong(position: MomCrypto.Api.PositionField) -> bool:
        ...

    @staticmethod
    def IsShort(position: MomCrypto.Api.PositionField) -> bool:
        ...


class TradeExtension(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetVolume(trade: MomCrypto.Api.TradeField) -> float:
        ...

    @staticmethod
    def IsBuy(trade: MomCrypto.Api.TradeField) -> bool:
        ...

    @staticmethod
    def IsLong(trade: MomCrypto.Api.TradeField) -> bool:
        ...

    @staticmethod
    def IsSell(trade: MomCrypto.Api.TradeField) -> bool:
        ...

    @staticmethod
    def IsShort(trade: MomCrypto.Api.TradeField) -> bool:
        ...


class OrderExtension(System.Object):
    """This class has no documentation."""

    @staticmethod
    def IsCancelled(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsDone(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsFilled(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsMarket(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsNoTrade(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsPartCanceled(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsPartiallyFilled(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsStopMarket(order: MomCrypto.Api.OrderField) -> bool:
        ...

    @staticmethod
    def IsStopOrder(input: MomCrypto.Api.OrderField) -> bool:
        ...


class InputOrderExtension(System.Object):
    """This class has no documentation."""

    @staticmethod
    def Buy(input: MomCrypto.Api.InputOrderField) -> None:
        ...

    @staticmethod
    def GetBuySell(input: MomCrypto.Api.InputOrderField) -> System.ValueTuple[bool, bool]:
        ...

    @staticmethod
    def IsAllTraded(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsBuy(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsCanceled(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsDone(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsLimit(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsLimitOrder(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsMarket(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsMomSettlement(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsNoSend(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsPartCanceled(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsRejected(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsSell(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsSettlement(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsStopLimit(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsStopMarket(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsStopOrder(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def IsUserSettlement(input: MomCrypto.Api.InputOrderField) -> bool:
        ...

    @staticmethod
    def Sell(input: MomCrypto.Api.InputOrderField) -> None:
        ...

    @staticmethod
    def SetLimitPrice(input: MomCrypto.Api.InputOrderField, price: float) -> MomCrypto.Api.InputOrderField:
        ...

    @staticmethod
    def SetMarketPrice(input: MomCrypto.Api.InputOrderField) -> MomCrypto.Api.InputOrderField:
        ...


class InstrumentExtension(System.Object):
    """This class has no documentation."""

    @staticmethod
    def CloseTodayFirst(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def EnableCloseToday(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def EnableShort(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def EnableTrading(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def Expired(instrument: MomCrypto.Api.MomInstrument) -> None:
        ...

    @staticmethod
    def GetDateTime(data: MomCrypto.Api.MomDepthMarketData) -> datetime.datetime:
        ...

    @staticmethod
    def GetExpiredDateTime(instrument: MomCrypto.Api.MomInstrument) -> datetime.datetime:
        ...

    @staticmethod
    def IsCall(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def IsExpired(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def IsOption(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def IsPut(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def IsStarted(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def LockCloseToday(instrument: MomCrypto.Api.MomInstrument) -> bool:
        ...

    @staticmethod
    def SetCloseTodayFirst(instrument: MomCrypto.Api.MomInstrument, value: bool = True) -> None:
        ...

    @staticmethod
    def SetEnableCloseToday(instrument: MomCrypto.Api.MomInstrument, value: bool = True) -> None:
        ...

    @staticmethod
    def SetEnableShort(instrument: MomCrypto.Api.MomInstrument, value: bool = True) -> None:
        ...

    @staticmethod
    def SetEnableTrading(instrument: MomCrypto.Api.MomInstrument, value: bool = True) -> None:
        ...

    @staticmethod
    def SetExpiredDateTime(instrument: MomCrypto.Api.MomInstrument, datetime: typing.Union[datetime.datetime, datetime.date]) -> None:
        ...

    @staticmethod
    def SetLockCloseToday(instrument: MomCrypto.Api.MomInstrument, value: bool = True) -> None:
        ...

    @staticmethod
    def Started(instrument: MomCrypto.Api.MomInstrument) -> None:
        ...


class Convert(System.Object):
    """This class has no documentation."""

    @staticmethod
    def DirectionToPositionDirection(direction: int) -> int:
        ...


class IIdGenerator(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def Next(self) -> int:
        ...


class TickIdGenLocked(System.Object, MomCrypto.Api.IIdGenerator):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    def Next(self) -> int:
        ...


class TickBaseIdGen(System.Object, MomCrypto.Api.IIdGenerator):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    def Next(self) -> int:
        ...


class TickIdGen(System.Object, MomCrypto.Api.IIdGenerator):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    def Next(self) -> int:
        ...


class IdGenerator(System.Object, MomCrypto.Api.IIdGenerator):
    """This class has no documentation."""

    def __init__(self, baseValue: int, seriesValue: int) -> None:
        ...

    def Next(self) -> int:
        ...


class MomAccountTypeType(System.Object):
    """This class has no documentation."""

    Futures: str = "Futures"

    Crypto: str = "Spot"


class MomActionFlag(System.Object):
    """This class has no documentation."""

    Delete: int = ...

    Modify: int = ...


class MomCashJournalTypeType(System.Object):
    """This class has no documentation."""

    FundTransfer: int = ...

    SubAccountTransfer: int = ...

    MainToUsdtFuture: int = ...

    MainToCoinFuture: int = ...

    UsdtFutureToMain: int = ...

    CoinFutureToMain: int = ...


class MomRequest(System.Object):
    """This class has no documentation."""

    @property
    def Identity(self) -> typing.List[int]:
        ...

    @Identity.setter
    def Identity(self, value: typing.List[int]):
        ...

    @property
    def MsgId(self) -> int:
        ...

    @MsgId.setter
    def MsgId(self, value: int):
        ...

    @property
    def Data(self) -> MomCrypto.Api.MomAny:
        ...

    @Data.setter
    def Data(self, value: MomCrypto.Api.MomAny):
        ...


class MomClient(System.Object):
    """This class has no documentation."""

    @property
    def logger(self) -> typing.Any:
        """This field is protected."""
        ...

    @property
    def UserInfo(self) -> MomCrypto.Api.MomRspUserLogin:
        ...

    @UserInfo.setter
    def UserInfo(self, value: MomCrypto.Api.MomRspUserLogin):
        ...

    @property
    def Address(self) -> str:
        ...

    @property
    def Connected(self) -> bool:
        ...

    @property
    def OnConnected(self) -> _EventContainer[typing.Callable[[], None], None]:
        ...

    @OnConnected.setter
    def OnConnected(self, value: _EventContainer[typing.Callable[[], None], None]):
        ...

    @property
    def OnDisconnected(self) -> _EventContainer[typing.Callable[[bool], None], None]:
        ...

    @OnDisconnected.setter
    def OnDisconnected(self, value: _EventContainer[typing.Callable[[bool], None], None]):
        ...

    @property
    def OnRspUserLogin(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomRspUserLogin, MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @OnRspUserLogin.setter
    def OnRspUserLogin(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomRspUserLogin, MomCrypto.Api.MomRspInfo], None], None]):
        ...

    @property
    def OnRspError(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @OnRspError.setter
    def OnRspError(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomRspInfo], None], None]):
        ...

    @property
    def OnResponse(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomResponse], None], None]:
        ...

    @OnResponse.setter
    def OnResponse(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomResponse], None], None]):
        ...

    def __init__(self, address: str, logger: typing.Any, debugMode: bool = False) -> None:
        """This method is protected."""
        ...

    def Init(self) -> None:
        ...

    @overload
    def Login(self, username: str, password: str) -> None:
        ...

    @overload
    def Login(self, req: MomCrypto.Api.MomReqUserLogin) -> None:
        ...

    def ProcessResponse(self, rsp: MomCrypto.Api.MomResponse) -> None:
        """This method is protected."""
        ...

    def Release(self) -> None:
        ...

    def Send(self, request: MomCrypto.Api.MomRequest) -> None:
        """This method is protected."""
        ...


class MomContingentConditionType(System.Object):
    """This class has no documentation."""

    Immediately: int = ...

    Touch: int = ...

    TouchProfit: int = ...

    ParkedOrder: int = ...

    LastPriceGreaterThanStopPrice: int = ...

    LastPriceGreaterEqualStopPrice: int = ...

    LastPriceLesserThanStopPrice: int = ...

    LastPriceLesserEqualStopPrice: int = ...

    AskPriceGreaterThanStopPrice: int = ...

    AskPriceGreaterEqualStopPrice: int = ...

    AskPriceLesserThanStopPrice: int = ...

    AskPriceLesserEqualStopPrice: int = ...

    BidPriceGreaterThanStopPrice: int = ...

    BidPriceGreaterEqualStopPrice: int = ...

    BidPriceLesserThanStopPrice: int = ...

    BidPriceLesserEqualStopPrice: int = ...


class MomCurrencyClassType(System.Object):
    """This class has no documentation."""

    Usd: str = "USD"

    Btc: str = "BTC"

    Eth: str = "ETH"

    Usdt: str = "USDT"

    Usdc: str = "USDC"

    Busd: str = "BUSD"

    @staticmethod
    def GetIndex(type: str) -> int:
        ...


class MomDirectionType(System.Object):
    """This class has no documentation."""

    Buy: int = 48

    Sell: int = 49


class MomFundAction(System.Object):
    """This class has no documentation."""


class MomFundInputOrder(MomCrypto.Api.InputOrderField):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    def Clone(self) -> MomCrypto.Api.MomFundInputOrder:
        ...

    def ToInputOrder(self) -> MomCrypto.Api.MomInputOrder:
        ...

    def ToString(self) -> str:
        ...


class MomFundTrade(MomCrypto.Api.TradeField):
    """This class has no documentation."""

    def Clone(self) -> MomCrypto.Api.MomFundTrade:
        ...

    def ToString(self) -> str:
        ...


class MomHisFundPosition(MomCrypto.Api.PositionField):
    """This class has no documentation."""

    @property
    def TradingDay(self) -> str:
        ...

    @TradingDay.setter
    def TradingDay(self, value: str):
        ...

    @property
    def tradingDay(self) -> str:
        ...

    @tradingDay.setter
    def tradingDay(self, value: str):
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, position: MomCrypto.Api.MomFundPosition) -> None:
        ...


class MomHisPosition(MomCrypto.Api.PositionField):
    """This class has no documentation."""

    @property
    def TradingDay(self) -> str:
        ...

    @TradingDay.setter
    def TradingDay(self, value: str):
        ...

    @property
    def tradingDay(self) -> str:
        ...

    @tradingDay.setter
    def tradingDay(self, value: str):
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, position: MomCrypto.Api.MomPosition) -> None:
        ...


class MomInstLifePhaseType(System.Object):
    """This class has no documentation."""

    NotStart: int = 48

    Started: int = 49

    Pause: int = 50

    Expired: int = 51


class MomInstrumentFeeRate(System.Object):
    """This class has no documentation."""

    @property
    def instrumentIndex(self) -> int:
        ...

    @instrumentIndex.setter
    def instrumentIndex(self, value: int):
        ...

    @property
    def Symbol(self) -> str:
        ...

    @Symbol.setter
    def Symbol(self, value: str):
        ...

    @property
    def symbol(self) -> str:
        ...

    @symbol.setter
    def symbol(self, value: str):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def TakerCommission(self) -> float:
        ...

    @TakerCommission.setter
    def TakerCommission(self, value: float):
        ...

    @property
    def takerCommission(self) -> float:
        ...

    @takerCommission.setter
    def takerCommission(self, value: float):
        ...

    @property
    def MakerCommission(self) -> float:
        ...

    @MakerCommission.setter
    def MakerCommission(self, value: float):
        ...

    @property
    def makerCommission(self) -> float:
        ...

    @makerCommission.setter
    def makerCommission(self, value: float):
        ...


class MomInstrumentMarginRate(System.Object):
    """This class has no documentation."""

    @property
    def InstrumentID(self) -> str:
        ...

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        ...

    @property
    def InvestorRange(self) -> int:
        ...

    @InvestorRange.setter
    def InvestorRange(self, value: int):
        ...

    @property
    def BrokerID(self) -> str:
        ...

    @BrokerID.setter
    def BrokerID(self, value: str):
        ...

    @property
    def InvestorID(self) -> str:
        ...

    @InvestorID.setter
    def InvestorID(self, value: str):
        ...

    @property
    def HedgeFlag(self) -> int:
        ...

    @HedgeFlag.setter
    def HedgeFlag(self, value: int):
        ...

    @property
    def LongMarginRatioByMoney(self) -> float:
        ...

    @LongMarginRatioByMoney.setter
    def LongMarginRatioByMoney(self, value: float):
        ...

    @property
    def LongMarginRatioByVolume(self) -> float:
        ...

    @LongMarginRatioByVolume.setter
    def LongMarginRatioByVolume(self, value: float):
        ...

    @property
    def ShortMarginRatioByMoney(self) -> float:
        ...

    @ShortMarginRatioByMoney.setter
    def ShortMarginRatioByMoney(self, value: float):
        ...

    @property
    def ShortMarginRatioByVolume(self) -> float:
        ...

    @ShortMarginRatioByVolume.setter
    def ShortMarginRatioByVolume(self, value: float):
        ...

    @property
    def IsRelative(self) -> int:
        ...

    @IsRelative.setter
    def IsRelative(self, value: int):
        ...

    @property
    def ExchangeID(self) -> str:
        ...

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        ...

    @property
    def InvestUnitID(self) -> str:
        ...

    @InvestUnitID.setter
    def InvestUnitID(self, value: str):
        ...


class MomMarketDataApi(MomCrypto.Api.MomClient):
    """This class has no documentation."""

    @property
    def ReturnData(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomDepthMarketData], None], None]:
        ...

    @ReturnData.setter
    def ReturnData(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomDepthMarketData], None], None]):
        ...

    @property
    def RspSubscribe(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomSpecificInstrument, MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @RspSubscribe.setter
    def RspSubscribe(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomSpecificInstrument, MomCrypto.Api.MomRspInfo], None], None]):
        ...

    @property
    def RspUnsubscribe(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomSpecificInstrument, MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @RspUnsubscribe.setter
    def RspUnsubscribe(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomSpecificInstrument, MomCrypto.Api.MomRspInfo], None], None]):
        ...

    def __init__(self, address: str, logger: typing.Any, debugMode: bool = False) -> None:
        ...

    def ProcessResponse(self, rsp: MomCrypto.Api.MomResponse) -> None:
        """This method is protected."""
        ...

    @overload
    def Subscribe(self, symbols: typing.List[str]) -> None:
        ...

    @overload
    def Subscribe(self, symbol: str) -> None:
        ...

    @overload
    def Unsubscribe(self, symbols: typing.List[str]) -> None:
        ...

    @overload
    def Unsubscribe(self, symbol: str) -> None:
        ...


class MomMarkets(System.Object):
    """This class has no documentation."""

    Ftx: str = "ftx"

    Mexc: str = "mexc"

    Binance: str = "binance"

    BinanceSpot: str = "binance-spot"

    BinanceFutures: str = "binance-futures"

    Deribit: str = "deribit"


class MomMessageType(System.Object):
    """This class has no documentation."""

    Ping: int = 1

    Pong: int = 2

    Close: int = 3

    Connected: int = 4

    Disconnected: int = 5

    RspError: int = 6

    UserLogin: int = 7

    RspUserLogin: int = 8

    Subscribe: int = 9

    RspSubscribe: int = 10

    RtnDepthMarketData: int = 11

    Unsubscribe: int = 12

    RspUnsubscribe: int = 13

    QryInstrument: int = 14

    RspQryInstrument: int = 15

    QryOrder: int = 16

    RspQryOrder: int = 17

    RtnOrder: int = 18

    QryTrade: int = 19

    RspQryTrade: int = 20

    RtnTrade: int = 21

    QryAccount: int = 22

    RspQryAccount: int = 23

    QryPosition: int = 24

    RspQryPosition: int = 25

    QryPositionDetail: int = 26

    RspQryPositionDetail: int = 27

    InputOrder: int = 28

    RspInputOrder: int = 29

    OrderAction: int = 30

    RspOrderAction: int = 31

    QryFund: int = 32

    RspQryFund: int = 33

    QryFundAccount: int = 34

    RspQryFundAccount: int = 35

    QryFundPosition: int = 36

    RspQryFundPosition: int = 37

    RtnPosition: int = 38

    RtnAccount: int = 39

    RtnFundAccount: int = 40

    RtnFundPosition: int = 41

    UserAction: int = 42

    RspUserAction: int = 43

    FundAction: int = 44

    RspFundAction: int = 45

    QryUser: int = 46

    RspQryUser: int = 47

    DataSync: int = 48

    RspDataSync: int = 49

    UpdatePositionProfit: int = 50

    QryExchangePosition: int = 51

    RspQryExchangePosition: int = 52

    QryExchangeOrder: int = 53

    RspQryExchangeOrder: int = 54

    QryExchangeAccount: int = 55

    RspQryExchangeAccount: int = 56

    InstrumentExpired: int = 57

    ChangeLeverage: int = 58

    RspChangeLeverage: int = 59

    CashJournal: int = 60

    RspCashJournal: int = 61

    SyncAccount: int = 62

    InstrumentListed: int = 63


class MomOffsetFlagType(System.Object):
    """This class has no documentation."""

    Open: int = ...

    Close: int = ...

    CloseToday: int = ...

    AutoOpenClose: int = ...


class MomOptionsTypeType(System.Object):
    """This class has no documentation."""

    CallOptions: int = 49

    PutOptions: int = 50


class MomOrderPriceTypeType(System.Object):
    """This class has no documentation."""

    AnyPrice: int = ...

    LimitPrice: int = ...

    BestPrice: int = ...

    LastPrice: int = ...

    LastPricePlusOneTicks: int = ...

    LastPricePlusTwoTicks: int = ...

    LastPricePlusThreeTicks: int = ...

    AskPrice1: int = ...

    AskPrice1PlusOneTicks: int = ...

    AskPrice1PlusTwoTicks: int = ...

    AskPrice1PlusThreeTicks: int = ...

    BidPrice1: int = ...

    BidPrice1PlusOneTicks: int = ...

    BidPrice1PlusTwoTicks: int = ...

    BidPrice1PlusThreeTicks: int = ...

    FiveLevelPrice: int = ...

    StopLimit: int = ...

    StopMarket: int = ...

    SettlementPrice: int = ...

    MomSettlementPrice: int = ...


class MomOrderStatusType(System.Object):
    """This class has no documentation."""

    PartTradedQueueing: int = ...

    PartTradedNotQueueing: int = ...

    NoTradeQueueing: int = ...

    NoTradeNotQueueing: int = ...

    Untriggered: int = ...

    Triggered: int = ...

    Canceled: int = ...

    Rejected: int = ...

    PartCanceled: int = ...

    Closed: int = ...

    AllTraded: int = ...

    Expired: int = ...


class MomOrderSubmitStatusType(System.Object):
    """This class has no documentation."""

    InsertSubmitted: int = ...

    CancelSubmitted: int = ...

    ModifySubmitted: int = ...

    Accepted: int = ...

    InsertRejected: int = ...

    CancelRejected: int = ...

    ModifyRejected: int = ...


class PerformanceField(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def TradingDay(self) -> str:
        ...

    @TradingDay.setter
    def TradingDay(self, value: str):
        ...

    @property
    def AccountId(self) -> str:
        ...

    @AccountId.setter
    def AccountId(self, value: str):
        ...

    @property
    def AccountType(self) -> str:
        ...

    @AccountType.setter
    def AccountType(self, value: str):
        ...

    @property
    def Equity(self) -> float:
        ...

    @Equity.setter
    def Equity(self, value: float):
        ...

    @property
    def EquityBySettle(self) -> float:
        ...

    @EquityBySettle.setter
    def EquityBySettle(self, value: float):
        ...

    @property
    def Commission(self) -> float:
        ...

    @Commission.setter
    def Commission(self, value: float):
        ...

    @property
    def CloseProfit(self) -> float:
        ...

    @CloseProfit.setter
    def CloseProfit(self, value: float):
        ...

    @property
    def PositionProfit(self) -> float:
        ...

    @PositionProfit.setter
    def PositionProfit(self, value: float):
        ...

    @property
    def PositionProfitBySettle(self) -> float:
        ...

    @PositionProfitBySettle.setter
    def PositionProfitBySettle(self, value: float):
        ...

    @property
    def UseMargin(self) -> float:
        ...

    @UseMargin.setter
    def UseMargin(self, value: float):
        ...

    @property
    def PremiumIn(self) -> float:
        ...

    @PremiumIn.setter
    def PremiumIn(self, value: float):
        ...

    @property
    def PremiumOut(self) -> float:
        ...

    @PremiumOut.setter
    def PremiumOut(self, value: float):
        ...

    @property
    def Available(self) -> float:
        ...

    @Available.setter
    def Available(self, value: float):
        ...

    @property
    def MarketValue(self) -> float:
        ...

    @MarketValue.setter
    def MarketValue(self, value: float):
        ...

    @property
    def MarketValueSettle(self) -> float:
        ...

    @MarketValueSettle.setter
    def MarketValueSettle(self, value: float):
        ...

    @property
    def Deposit(self) -> float:
        ...

    @Deposit.setter
    def Deposit(self, value: float):
        ...

    @property
    def Withdraw(self) -> float:
        ...

    @Withdraw.setter
    def Withdraw(self, value: float):
        ...


class MomPerformance(MomCrypto.Api.PerformanceField):
    """This class has no documentation."""

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def FundAccountId(self) -> str:
        ...

    @FundAccountId.setter
    def FundAccountId(self, value: str):
        ...


class MomFundPerformance(MomCrypto.Api.PerformanceField):
    """This class has no documentation."""


class MomPosiDirectionType(System.Object):
    """This class has no documentation."""

    Net: int = 49

    Long: int = 50

    Short: int = 51


class MomPositionTypeType(System.Object):
    """This class has no documentation."""

    Net: int = 49

    Gross: int = 50


class MomProductClassType(System.Object):
    """This class has no documentation."""

    All: int = ...

    Futures: int = ...

    Options: int = ...

    Stock: int = ...

    FuturesOptions: int = ...

    IndexOptions: int = ...

    Index: int = ...

    Etf: int = ...

    Crypto: int = ...

    CoinFutures: int = ...

    CoinOptions: int = ...

    @staticmethod
    def GetIndex(value: int) -> int:
        ...


class MomReqInstrument(System.Object):
    """This class has no documentation."""

    @property
    def InstrumentID(self) -> str:
        ...

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        ...

    @property
    def ExchangeID(self) -> str:
        ...

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        ...

    @property
    def ExchangeInstID(self) -> str:
        ...

    @ExchangeInstID.setter
    def ExchangeInstID(self, value: str):
        ...

    @property
    def ProductID(self) -> str:
        ...

    @ProductID.setter
    def ProductID(self, value: str):
        ...


class MomStopWorkingTypeType(System.Object):
    """This class has no documentation."""

    MarkPrice: int = ...

    ContractPrice: int = ...

    IndexPrice: int = ...


class MomTimeConditionType(System.Object):
    """This class has no documentation."""

    IOC: int = ...

    GFS: int = ...

    GFD: int = ...

    GTD: int = ...

    GTC: int = ...

    GFA: int = ...

    FOK: int = ...


class MomTraderApi(MomCrypto.Api.MomClient):
    """This class has no documentation."""

    @property
    def InstrumentReady(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomInstrument, bool], None], None]:
        ...

    @InstrumentReady.setter
    def InstrumentReady(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomInstrument, bool], None], None]):
        ...

    @property
    def InstrumentListed(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomInstrument, bool], None], None]:
        ...

    @InstrumentListed.setter
    def InstrumentListed(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomInstrument, bool], None], None]):
        ...

    @property
    def InstrumentExpired(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomInstrument, bool], None], None]:
        ...

    @InstrumentExpired.setter
    def InstrumentExpired(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomInstrument, bool], None], None]):
        ...

    @property
    def RspInputOrder(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomInputOrder, MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @RspInputOrder.setter
    def RspInputOrder(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomInputOrder, MomCrypto.Api.MomRspInfo], None], None]):
        ...

    @property
    def RspOrderAction(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomInputOrderAction, MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @RspOrderAction.setter
    def RspOrderAction(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomInputOrderAction, MomCrypto.Api.MomRspInfo], None], None]):
        ...

    @property
    def ReturnOrder(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomOrder, int], None], None]:
        ...

    @ReturnOrder.setter
    def ReturnOrder(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomOrder, int], None], None]):
        ...

    @property
    def ReturnTrade(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomTrade, int], None], None]:
        ...

    @ReturnTrade.setter
    def ReturnTrade(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomTrade, int], None], None]):
        ...

    @property
    def ReturnAccount(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomAccount], None], None]:
        ...

    @ReturnAccount.setter
    def ReturnAccount(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomAccount], None], None]):
        ...

    @property
    def ReturnFundAccount(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomFundAccount], None], None]:
        ...

    @ReturnFundAccount.setter
    def ReturnFundAccount(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomFundAccount], None], None]):
        ...

    @property
    def ReturnPosition(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomPosition], None], None]:
        ...

    @ReturnPosition.setter
    def ReturnPosition(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomPosition], None], None]):
        ...

    @property
    def RspQryOrder(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomOrder, MomCrypto.Api.MomRspInfo, bool], None], None]:
        ...

    @RspQryOrder.setter
    def RspQryOrder(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomOrder, MomCrypto.Api.MomRspInfo, bool], None], None]):
        ...

    @property
    def RspQryTrade(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomTrade, MomCrypto.Api.MomRspInfo, bool], None], None]:
        ...

    @RspQryTrade.setter
    def RspQryTrade(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomTrade, MomCrypto.Api.MomRspInfo, bool], None], None]):
        ...

    @property
    def RspQryPosition(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomPosition, MomCrypto.Api.MomRspInfo, bool], None], None]:
        ...

    @RspQryPosition.setter
    def RspQryPosition(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomPosition, MomCrypto.Api.MomRspInfo, bool], None], None]):
        ...

    @property
    def RspQryAccount(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomAccount, MomCrypto.Api.MomRspInfo, bool], None], None]:
        ...

    @RspQryAccount.setter
    def RspQryAccount(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomAccount, MomCrypto.Api.MomRspInfo, bool], None], None]):
        ...

    @property
    def RspQryExchangeOrder(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomFundOrder, MomCrypto.Api.MomRspInfo, bool], None], None]:
        ...

    @RspQryExchangeOrder.setter
    def RspQryExchangeOrder(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomFundOrder, MomCrypto.Api.MomRspInfo, bool], None], None]):
        ...

    @property
    def RspQryExchangePosition(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomFundPosition, MomCrypto.Api.MomRspInfo, bool], None], None]:
        ...

    @RspQryExchangePosition.setter
    def RspQryExchangePosition(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomFundPosition, MomCrypto.Api.MomRspInfo, bool], None], None]):
        ...

    @property
    def RspQryExchangeAccount(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomFundAccount, MomCrypto.Api.MomRspInfo, bool], None], None]:
        ...

    @RspQryExchangeAccount.setter
    def RspQryExchangeAccount(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomFundAccount, MomCrypto.Api.MomRspInfo, bool], None], None]):
        ...

    @property
    def RspChangeLeverage(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @RspChangeLeverage.setter
    def RspChangeLeverage(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomRspInfo], None], None]):
        ...

    @property
    def RspCashJournal(self) -> _EventContainer[typing.Callable[[MomCrypto.Api.MomCashJournal, MomCrypto.Api.MomRspInfo], None], None]:
        ...

    @RspCashJournal.setter
    def RspCashJournal(self, value: _EventContainer[typing.Callable[[MomCrypto.Api.MomCashJournal, MomCrypto.Api.MomRspInfo], None], None]):
        ...

    def __init__(self, address: str, logger: typing.Any, debugMode: bool = False) -> None:
        ...

    @overload
    def CancelOrder(self, userId: str, orderRef: int) -> None:
        ...

    @overload
    def CancelOrder(self, action: MomCrypto.Api.MomInputOrderAction) -> None:
        ...

    def ChangeLeverage(self, symbol: str, leverage: int, exchange: str = ...) -> None:
        ...

    def DataSync(self) -> None:
        ...

    def FuturesToSpot(self, amount: float, userId: str = ..., market: str = ..., currency: str = "USDT") -> None:
        ...

    def InputOrder(self, order: MomCrypto.Api.MomInputOrder) -> None:
        ...

    def ProcessResponse(self, rsp: MomCrypto.Api.MomResponse) -> None:
        """This method is protected."""
        ...

    def QueryAccount(self, userId: str) -> None:
        ...

    def QueryExchangeAccount(self, exchangeAccountId: str) -> None:
        ...

    def QueryExchangeOrder(self, exchangeAccountId: str) -> None:
        ...

    def QueryExchangePosition(self, exchangeAccountId: str) -> None:
        ...

    def QueryInstrument(self) -> None:
        ...

    def QueryOrder(self, userId: str, orderRef: int = 0) -> None:
        ...

    def QueryPosition(self, userId: str) -> None:
        ...

    def QueryTrade(self, userId: str, tradeLocalId: int = 0) -> None:
        ...

    def SpotToFutures(self, amount: float, userId: str = ..., market: str = ..., currency: str = "USDT") -> None:
        ...

    def Transfer(self, transferType: int, amount: float, userId: str = ..., market: str = ..., currency: str = "USDT") -> None:
        ...


class MomTradeSourceType(System.Object):
    """This class has no documentation."""

    Exchange: int = ...

    Manual: int = ...


class MomTradeTypeType(System.Object):
    """This class has no documentation."""

    Common: int = ...

    Execution: int = ...

    Expiration: int = ...


class MomUserType(System.Enum):
    """This class has no documentation."""

    Strategy = 0

    Manager = 1


class MomUser(System.Object):
    """This class has no documentation."""

    @property
    def index(self) -> int:
        ...

    @index.setter
    def index(self, value: int):
        ...

    @property
    def UserId(self) -> str:
        ...

    @UserId.setter
    def UserId(self, value: str):
        ...

    @property
    def userId(self) -> str:
        ...

    @userId.setter
    def userId(self, value: str):
        ...

    @property
    def Password(self) -> str:
        ...

    @Password.setter
    def Password(self, value: str):
        ...

    @property
    def password(self) -> str:
        ...

    @password.setter
    def password(self, value: str):
        ...

    @property
    def Enabled(self) -> bool:
        ...

    @Enabled.setter
    def Enabled(self, value: bool):
        ...

    @property
    def enabled(self) -> bool:
        ...

    @enabled.setter
    def enabled(self, value: bool):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def description(self) -> str:
        ...

    @description.setter
    def description(self, value: str):
        ...

    @property
    def UserType(self) -> int:
        """This property contains the int value of a member of the MomCrypto.Api.MomUserType enum."""
        ...

    @UserType.setter
    def UserType(self, value: int):
        """This property contains the int value of a member of the MomCrypto.Api.MomUserType enum."""
        ...

    @property
    def userType(self) -> MomCrypto.Api.MomUserType:
        ...

    @userType.setter
    def userType(self, value: MomCrypto.Api.MomUserType):
        ...

    @property
    def StrategyManager(self) -> str:
        ...

    @StrategyManager.setter
    def StrategyManager(self, value: str):
        ...

    @property
    def strategyManager(self) -> str:
        ...

    @strategyManager.setter
    def strategyManager(self, value: str):
        ...

    @property
    def StrategyName(self) -> str:
        ...

    @StrategyName.setter
    def StrategyName(self, value: str):
        ...

    @property
    def strategyName(self) -> str:
        ...

    @strategyName.setter
    def strategyName(self, value: str):
        ...

    def Clone(self) -> MomCrypto.Api.MomUser:
        ...

    def ToString(self) -> str:
        ...


class MomVolumeConditionType(System.Object):
    """This class has no documentation."""

    AnyVolume: int = ...

    MinVolume: int = ...

    CompleteVolume: int = ...


class ISpscLinkOptions(System.Object):
    """This class has no documentation."""

    @property
    def CpuCore(self) -> int:
        ...

    @CpuCore.setter
    def CpuCore(self, value: int):
        ...


class ISpscTargetBlock(typing.Generic[MomCrypto_Api_ISpscTargetBlock_TInput], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def OfferMessage(self, messageValue: MomCrypto_Api_ISpscTargetBlock_TInput, source: MomCrypto.Api.ISpscSourceBlock[MomCrypto_Api_ISpscTargetBlock_TInput]) -> None:
        ...


class ISpscSourceBlock(typing.Generic[MomCrypto_Api_ISpscSourceBlock_TOutput], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def ConsumeMessage(self, output: typing.Optional[MomCrypto_Api_ISpscSourceBlock_TOutput]) -> typing.Union[bool, MomCrypto_Api_ISpscSourceBlock_TOutput]:
        ...

    def LinkTo(self, target: MomCrypto.Api.ISpscTargetBlock[MomCrypto_Api_ISpscSourceBlock_TOutput], options: MomCrypto.Api.ISpscLinkOptions = None) -> System.IDisposable:
        ...


class SpscBufferBlock(typing.Generic[MomCrypto_Api_SpscBufferBlock_TOutput], System.Object, MomCrypto.Api.ISpscSourceBlock[MomCrypto_Api_SpscBufferBlock_TOutput]):
    """This class has no documentation."""

    @property
    def Count(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def ConsumeMessage(self, output: typing.Optional[MomCrypto_Api_SpscBufferBlock_TOutput]) -> typing.Union[bool, MomCrypto_Api_SpscBufferBlock_TOutput]:
        ...

    def LinkTo(self, target: MomCrypto.Api.ISpscTargetBlock[MomCrypto_Api_SpscBufferBlock_TOutput], options: MomCrypto.Api.ISpscLinkOptions = None) -> System.IDisposable:
        ...

    def Post(self, output: MomCrypto_Api_SpscBufferBlock_TOutput) -> None:
        ...


class SpscBroadcastBlock(typing.Generic[MomCrypto_Api_SpscBroadcastBlock_TOutput], System.Object, MomCrypto.Api.ISpscSourceBlock[MomCrypto_Api_SpscBroadcastBlock_TOutput], System.IDisposable):
    """This class has no documentation."""

    def __init__(self, cloneFunc: typing.Callable[[MomCrypto_Api_SpscBroadcastBlock_TOutput], MomCrypto_Api_SpscBroadcastBlock_TOutput]) -> None:
        ...

    def ConsumeMessage(self, output: typing.Optional[MomCrypto_Api_SpscBroadcastBlock_TOutput]) -> typing.Union[bool, MomCrypto_Api_SpscBroadcastBlock_TOutput]:
        ...

    def Dispose(self) -> None:
        ...

    def LinkTo(self, target: MomCrypto.Api.ISpscTargetBlock[MomCrypto_Api_SpscBroadcastBlock_TOutput], options: MomCrypto.Api.ISpscLinkOptions = None) -> System.IDisposable:
        ...

    def Post(self, output: MomCrypto_Api_SpscBroadcastBlock_TOutput) -> None:
        ...


class SpscActionBlock(typing.Generic[MomCrypto_Api_SpscActionBlock_TInput], System.Object, MomCrypto.Api.ISpscTargetBlock[MomCrypto_Api_SpscActionBlock_TInput]):
    """This class has no documentation."""

    def __init__(self, action: typing.Callable[[MomCrypto_Api_SpscActionBlock_TInput], None]) -> None:
        ...

    def OfferMessage(self, messageValue: MomCrypto_Api_SpscActionBlock_TInput, source: MomCrypto.Api.ISpscSourceBlock[MomCrypto_Api_SpscActionBlock_TInput]) -> None:
        ...


class SpscBufferAction(typing.Generic[MomCrypto_Api_SpscBufferAction_TInput], System.Object, System.IDisposable):
    """This class has no documentation."""

    def __init__(self, action: typing.Callable[[MomCrypto_Api_SpscBufferAction_TInput], None]) -> None:
        ...

    def Dispose(self) -> None:
        ...

    def Post(self, input: MomCrypto_Api_SpscBufferAction_TInput) -> None:
        ...


class SpscQueue(typing.Generic[MomCrypto_Api_SpscQueue_T], System.Object, typing.Iterable[MomCrypto_Api_SpscQueue_T]):
    """Provides a producer/consumer queue safe to be used by only one producer and one consumer concurrently."""

    @property
    def IsEmpty(self) -> bool:
        """Gets whether the collection is currently empty."""
        ...

    @property
    def Count(self) -> int:
        """Gets the number of items in the collection."""
        ...

    def __init__(self) -> None:
        """Initializes the queue."""
        ...

    def Enqueue(self, item: MomCrypto_Api_SpscQueue_T) -> None:
        """
        Enqueues an item into the queue.
        
        :param item: The item to enqueue.
        """
        ...

    @overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[MomCrypto_Api_SpscQueue_T]:
        """Gets an enumerable for the collection."""
        ...

    @overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    def TryDequeue(self, result: typing.Optional[MomCrypto_Api_SpscQueue_T]) -> typing.Union[bool, MomCrypto_Api_SpscQueue_T]:
        """
        Attempts to dequeue an item from the queue.
        
        :param result: The dequeued item.
        :returns: true if an item could be dequeued; otherwise, false.
        """
        ...


class _EventContainer(typing.Generic[MomCrypto_Api__EventContainer_Callable, MomCrypto_Api__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> MomCrypto_Api__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: MomCrypto_Api__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: MomCrypto_Api__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


