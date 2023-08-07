from typing import overload
import datetime
import typing

import FtxApi.Rest.Models
import System
import System.Collections.Generic

FtxApi_Rest_Models_FtxResult_T = typing.TypeVar("FtxApi_Rest_Models_FtxResult_T")


class Position(System.Object):
    """This class has no documentation."""

    @property
    def CollateralUsed(self) -> typing.Optional[float]:
        ...

    @CollateralUsed.setter
    def CollateralUsed(self, value: typing.Optional[float]):
        ...

    @property
    def Cost(self) -> typing.Optional[float]:
        ...

    @Cost.setter
    def Cost(self, value: typing.Optional[float]):
        ...

    @property
    def EntryPrice(self) -> typing.Optional[float]:
        ...

    @EntryPrice.setter
    def EntryPrice(self, value: typing.Optional[float]):
        ...

    @property
    def EstimatedLiquidationPrice(self) -> typing.Optional[float]:
        ...

    @EstimatedLiquidationPrice.setter
    def EstimatedLiquidationPrice(self, value: typing.Optional[float]):
        ...

    @property
    def Future(self) -> str:
        ...

    @Future.setter
    def Future(self, value: str):
        ...

    @property
    def InitialMarginRequirement(self) -> typing.Optional[float]:
        ...

    @InitialMarginRequirement.setter
    def InitialMarginRequirement(self, value: typing.Optional[float]):
        ...

    @property
    def LongOrderSize(self) -> typing.Optional[float]:
        ...

    @LongOrderSize.setter
    def LongOrderSize(self, value: typing.Optional[float]):
        ...

    @property
    def MaintenanceMarginRequirement(self) -> typing.Optional[float]:
        ...

    @MaintenanceMarginRequirement.setter
    def MaintenanceMarginRequirement(self, value: typing.Optional[float]):
        ...

    @property
    def NetSize(self) -> typing.Optional[float]:
        ...

    @NetSize.setter
    def NetSize(self, value: typing.Optional[float]):
        ...

    @property
    def OpenSize(self) -> typing.Optional[float]:
        ...

    @OpenSize.setter
    def OpenSize(self, value: typing.Optional[float]):
        ...

    @property
    def RealizedPnl(self) -> typing.Optional[float]:
        ...

    @RealizedPnl.setter
    def RealizedPnl(self, value: typing.Optional[float]):
        ...

    @property
    def ShortOrderSize(self) -> typing.Optional[float]:
        ...

    @ShortOrderSize.setter
    def ShortOrderSize(self, value: typing.Optional[float]):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Size(self) -> typing.Optional[float]:
        ...

    @Size.setter
    def Size(self, value: typing.Optional[float]):
        ...

    @property
    def UnrealizedPnl(self) -> typing.Optional[float]:
        ...

    @UnrealizedPnl.setter
    def UnrealizedPnl(self, value: typing.Optional[float]):
        ...


class AccountInfo(System.Object):
    """This class has no documentation."""

    @property
    def BackstopProvider(self) -> bool:
        ...

    @BackstopProvider.setter
    def BackstopProvider(self, value: bool):
        ...

    @property
    def Collateral(self) -> float:
        ...

    @Collateral.setter
    def Collateral(self, value: float):
        ...

    @property
    def FreeCollateral(self) -> float:
        ...

    @FreeCollateral.setter
    def FreeCollateral(self, value: float):
        ...

    @property
    def InitialMarginRequirement(self) -> float:
        ...

    @InitialMarginRequirement.setter
    def InitialMarginRequirement(self, value: float):
        ...

    @property
    def Liquidating(self) -> bool:
        ...

    @Liquidating.setter
    def Liquidating(self, value: bool):
        ...

    @property
    def MaintenanceMarginRequirement(self) -> float:
        ...

    @MaintenanceMarginRequirement.setter
    def MaintenanceMarginRequirement(self, value: float):
        ...

    @property
    def MakerFee(self) -> float:
        ...

    @MakerFee.setter
    def MakerFee(self, value: float):
        ...

    @property
    def MarginFraction(self) -> typing.Optional[float]:
        ...

    @MarginFraction.setter
    def MarginFraction(self, value: typing.Optional[float]):
        ...

    @property
    def OpenMarginFraction(self) -> typing.Optional[float]:
        ...

    @OpenMarginFraction.setter
    def OpenMarginFraction(self, value: typing.Optional[float]):
        ...

    @property
    def TakerFee(self) -> float:
        ...

    @TakerFee.setter
    def TakerFee(self, value: float):
        ...

    @property
    def TotalAccountValue(self) -> float:
        ...

    @TotalAccountValue.setter
    def TotalAccountValue(self, value: float):
        ...

    @property
    def TotalPositionSize(self) -> float:
        ...

    @TotalPositionSize.setter
    def TotalPositionSize(self, value: float):
        ...

    @property
    def Username(self) -> str:
        ...

    @Username.setter
    def Username(self, value: str):
        ...

    @property
    def Leverage(self) -> float:
        ...

    @Leverage.setter
    def Leverage(self, value: float):
        ...

    @property
    def Positions(self) -> System.Collections.Generic.List[FtxApi.Rest.Models.Position]:
        ...

    @Positions.setter
    def Positions(self, value: System.Collections.Generic.List[FtxApi.Rest.Models.Position]):
        ...


class AccountLeverage(System.Object):
    """This class has no documentation."""

    @property
    def Leverage(self) -> int:
        ...

    @Leverage.setter
    def Leverage(self, value: int):
        ...


class Balance(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def Free(self) -> float:
        ...

    @Free.setter
    def Free(self, value: float):
        ...

    @property
    def Total(self) -> float:
        ...

    @Total.setter
    def Total(self, value: float):
        ...


class Candle(System.Object):
    """This class has no documentation."""

    @property
    def Close(self) -> float:
        ...

    @Close.setter
    def Close(self, value: float):
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
    def Open(self) -> float:
        ...

    @Open.setter
    def Open(self, value: float):
        ...

    @property
    def StartTime(self) -> datetime.datetime:
        ...

    @StartTime.setter
    def StartTime(self, value: datetime.datetime):
        ...

    @property
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...


class Coin(System.Object):
    """This class has no documentation."""

    @property
    def CanDeposit(self) -> bool:
        ...

    @CanDeposit.setter
    def CanDeposit(self, value: bool):
        ...

    @property
    def CanWithdraw(self) -> bool:
        ...

    @CanWithdraw.setter
    def CanWithdraw(self, value: bool):
        ...

    @property
    def HasTag(self) -> bool:
        ...

    @HasTag.setter
    def HasTag(self, value: bool):
        ...

    @property
    def Id(self) -> str:
        ...

    @Id.setter
    def Id(self, value: str):
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...


class DepositAddress(System.Object):
    """This class has no documentation."""

    @property
    def Address(self) -> str:
        ...

    @Address.setter
    def Address(self, value: str):
        ...

    @property
    def Tag(self) -> str:
        ...

    @Tag.setter
    def Tag(self, value: str):
        ...


class DepositHistory(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def Confirmations(self) -> float:
        ...

    @Confirmations.setter
    def Confirmations(self, value: float):
        ...

    @property
    def ConfirmedTime(self) -> datetime.datetime:
        ...

    @ConfirmedTime.setter
    def ConfirmedTime(self, value: datetime.datetime):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def SentTime(self) -> datetime.datetime:
        ...

    @SentTime.setter
    def SentTime(self, value: datetime.datetime):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def TxId(self) -> str:
        ...

    @TxId.setter
    def TxId(self, value: str):
        ...

    @property
    def Notes(self) -> str:
        ...

    @Notes.setter
    def Notes(self, value: str):
        ...


class Fill(System.Object):
    """This class has no documentation."""

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def FeeCurrency(self) -> str:
        ...

    @FeeCurrency.setter
    def FeeCurrency(self, value: str):
        ...

    @property
    def FeeRate(self) -> typing.Optional[float]:
        ...

    @FeeRate.setter
    def FeeRate(self, value: typing.Optional[float]):
        ...

    @property
    def Future(self) -> str:
        ...

    @Future.setter
    def Future(self, value: str):
        ...

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Liquidity(self) -> str:
        ...

    @Liquidity.setter
    def Liquidity(self, value: str):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def BaseCurrency(self) -> str:
        ...

    @BaseCurrency.setter
    def BaseCurrency(self, value: str):
        ...

    @property
    def QuoteCurrency(self) -> str:
        ...

    @QuoteCurrency.setter
    def QuoteCurrency(self, value: str):
        ...

    @property
    def OrderId(self) -> int:
        ...

    @OrderId.setter
    def OrderId(self, value: int):
        ...

    @property
    def TradeId(self) -> int:
        ...

    @TradeId.setter
    def TradeId(self, value: int):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...


class FtxOption(System.Object):
    """This class has no documentation."""

    @property
    def Underlying(self) -> str:
        ...

    @Underlying.setter
    def Underlying(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def Strike(self) -> float:
        ...

    @Strike.setter
    def Strike(self, value: float):
        ...

    @property
    def Expiry(self) -> datetime.datetime:
        ...

    @Expiry.setter
    def Expiry(self, value: datetime.datetime):
        ...

    def Parse(self, symbol: str) -> None:
        ...

    @staticmethod
    def ParseExpiry(expiry: str) -> datetime.datetime:
        ...

    def ToString(self) -> str:
        ...


class FtxResult(typing.Generic[FtxApi_Rest_Models_FtxResult_T], System.Object):
    """This class has no documentation."""

    @property
    def Success(self) -> bool:
        ...

    @Success.setter
    def Success(self, value: bool):
        ...

    @property
    def Result(self) -> FtxApi_Rest_Models_FtxResult_T:
        ...

    @Result.setter
    def Result(self, value: FtxApi_Rest_Models_FtxResult_T):
        ...

    @property
    def Error(self) -> str:
        ...

    @Error.setter
    def Error(self, value: str):
        ...

    @property
    def Request(self) -> str:
        ...

    @Request.setter
    def Request(self, value: str):
        ...


class FundingPayment(System.Object):
    """This class has no documentation."""

    @property
    def Future(self) -> str:
        ...

    @Future.setter
    def Future(self, value: str):
        ...

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Payment(self) -> float:
        ...

    @Payment.setter
    def Payment(self, value: float):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...


class FundingRate(System.Object):
    """This class has no documentation."""

    @property
    def Future(self) -> str:
        ...

    @Future.setter
    def Future(self, value: str):
        ...

    @property
    def Rate(self) -> float:
        ...

    @Rate.setter
    def Rate(self, value: float):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...


class Future(System.Object):
    """This class has no documentation."""

    @property
    def Ask(self) -> typing.Optional[float]:
        """best ask on the orderbook"""
        ...

    @Ask.setter
    def Ask(self, value: typing.Optional[float]):
        """best ask on the orderbook"""
        ...

    @property
    def Bid(self) -> typing.Optional[float]:
        """best bid on the orderbook"""
        ...

    @Bid.setter
    def Bid(self, value: typing.Optional[float]):
        """best bid on the orderbook"""
        ...

    @property
    def Change1H(self) -> float:
        """price change in the last hour"""
        ...

    @Change1H.setter
    def Change1H(self, value: float):
        """price change in the last hour"""
        ...

    @property
    def Change24H(self) -> float:
        """price change in the last 24 hours"""
        ...

    @Change24H.setter
    def Change24H(self, value: float):
        """price change in the last 24 hours"""
        ...

    @property
    def ChangeBod(self) -> float:
        """price change since midnight UTC (beginning of day)"""
        ...

    @ChangeBod.setter
    def ChangeBod(self, value: float):
        """price change since midnight UTC (beginning of day)"""
        ...

    @property
    def VolumeUsd24H(self) -> float:
        """USD volume in the last 24 hours"""
        ...

    @VolumeUsd24H.setter
    def VolumeUsd24H(self, value: float):
        """USD volume in the last 24 hours"""
        ...

    @property
    def Volume(self) -> float:
        """quantity traded in the last 24 hours"""
        ...

    @Volume.setter
    def Volume(self, value: float):
        """quantity traded in the last 24 hours"""
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def Enabled(self) -> bool:
        ...

    @Enabled.setter
    def Enabled(self, value: bool):
        ...

    @property
    def Expired(self) -> bool:
        ...

    @Expired.setter
    def Expired(self, value: bool):
        ...

    @property
    def Expiry(self) -> typing.Optional[datetime.datetime]:
        ...

    @Expiry.setter
    def Expiry(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def Index(self) -> float:
        """average of the Market Prices for the constituent markets in the index"""
        ...

    @Index.setter
    def Index(self, value: float):
        """average of the Market Prices for the constituent markets in the index"""
        ...

    @property
    def ImfFactor(self) -> float:
        ...

    @ImfFactor.setter
    def ImfFactor(self, value: float):
        ...

    @property
    def Last(self) -> typing.Optional[float]:
        """last price the future traded at"""
        ...

    @Last.setter
    def Last(self, value: typing.Optional[float]):
        """last price the future traded at"""
        ...

    @property
    def LowerBound(self) -> float:
        """the lowest price the future can trade at"""
        ...

    @LowerBound.setter
    def LowerBound(self, value: float):
        """the lowest price the future can trade at"""
        ...

    @property
    def Mark(self) -> float:
        """mark price of the future"""
        ...

    @Mark.setter
    def Mark(self, value: float):
        """mark price of the future"""
        ...

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def Perpetual(self) -> bool:
        """whether or not this is a perpetual contract"""
        ...

    @Perpetual.setter
    def Perpetual(self, value: bool):
        """whether or not this is a perpetual contract"""
        ...

    @property
    def PositionLimitWeight(self) -> float:
        ...

    @PositionLimitWeight.setter
    def PositionLimitWeight(self, value: float):
        ...

    @property
    def PostOnly(self) -> bool:
        ...

    @PostOnly.setter
    def PostOnly(self, value: bool):
        ...

    @property
    def PriceIncrement(self) -> float:
        ...

    @PriceIncrement.setter
    def PriceIncrement(self, value: float):
        ...

    @property
    def SizeIncrement(self) -> float:
        ...

    @SizeIncrement.setter
    def SizeIncrement(self, value: float):
        ...

    @property
    def Underlying(self) -> str:
        ...

    @Underlying.setter
    def Underlying(self, value: str):
        ...

    @property
    def UpperBound(self) -> float:
        """the highest price the future can trade at"""
        ...

    @UpperBound.setter
    def UpperBound(self, value: float):
        """the highest price the future can trade at"""
        ...

    @property
    def Type(self) -> str:
        """One of future, perpetual, or move"""
        ...

    @Type.setter
    def Type(self, value: str):
        """One of future, perpetual, or move"""
        ...

    @property
    def MoveStart(self) -> str:
        ...

    @MoveStart.setter
    def MoveStart(self, value: str):
        ...


class FutureStats(System.Object):
    """This class has no documentation."""

    @property
    def Volume(self) -> float:
        ...

    @Volume.setter
    def Volume(self, value: float):
        ...

    @property
    def NextFundingRate(self) -> float:
        ...

    @NextFundingRate.setter
    def NextFundingRate(self, value: float):
        ...

    @property
    def NextFundingTime(self) -> str:
        ...

    @NextFundingTime.setter
    def NextFundingTime(self, value: str):
        ...

    @property
    def ExpirationPrice(self) -> float:
        ...

    @ExpirationPrice.setter
    def ExpirationPrice(self, value: float):
        ...

    @property
    def PredictedExpirationPrice(self) -> float:
        ...

    @PredictedExpirationPrice.setter
    def PredictedExpirationPrice(self, value: float):
        ...

    @property
    def OpenInterest(self) -> float:
        ...

    @OpenInterest.setter
    def OpenInterest(self, value: float):
        ...

    @property
    def StrikePrice(self) -> float:
        ...

    @StrikePrice.setter
    def StrikePrice(self, value: float):
        ...


class OptionFill(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Option(self) -> FtxApi.Rest.Models.FtxOption:
        ...

    @Option.setter
    def Option(self, value: FtxApi.Rest.Models.FtxOption):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def Liquidity(self) -> str:
        ...

    @Liquidity.setter
    def Liquidity(self, value: str):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def FeeRate(self) -> float:
        ...

    @FeeRate.setter
    def FeeRate(self, value: float):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...


class OptionPosition(System.Object):
    """This class has no documentation."""

    @property
    def NetSize(self) -> float:
        ...

    @NetSize.setter
    def NetSize(self, value: float):
        ...

    @property
    def EntryPrice(self) -> float:
        ...

    @EntryPrice.setter
    def EntryPrice(self, value: float):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Option(self) -> FtxApi.Rest.Models.FtxOption:
        ...

    @Option.setter
    def Option(self, value: FtxApi.Rest.Models.FtxOption):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def PessimisticValuation(self) -> typing.Optional[float]:
        ...

    @PessimisticValuation.setter
    def PessimisticValuation(self, value: typing.Optional[float]):
        ...

    @property
    def PessimisticIndexPrice(self) -> typing.Optional[float]:
        ...

    @PessimisticIndexPrice.setter
    def PessimisticIndexPrice(self, value: typing.Optional[float]):
        ...

    @property
    def PessimisticVol(self) -> typing.Optional[float]:
        ...

    @PessimisticVol.setter
    def PessimisticVol(self, value: typing.Optional[float]):
        ...


class OptionQuote(System.Object):
    """This class has no documentation."""

    @property
    def Collateral(self) -> float:
        ...

    @Collateral.setter
    def Collateral(self, value: float):
        ...

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Option(self) -> FtxApi.Rest.Models.FtxOption:
        ...

    @Option.setter
    def Option(self, value: FtxApi.Rest.Models.FtxOption):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def QuoteExpiry(self) -> typing.Optional[datetime.datetime]:
        ...

    @QuoteExpiry.setter
    def QuoteExpiry(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def QuoterSide(self) -> str:
        ...

    @QuoterSide.setter
    def QuoterSide(self, value: str):
        ...

    @property
    def RequestId(self) -> typing.Optional[int]:
        ...

    @RequestId.setter
    def RequestId(self, value: typing.Optional[int]):
        ...

    @property
    def RequestSide(self) -> str:
        ...

    @RequestSide.setter
    def RequestSide(self, value: str):
        ...

    @property
    def Size(self) -> typing.Optional[float]:
        ...

    @Size.setter
    def Size(self, value: typing.Optional[float]):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    def ToString(self) -> str:
        ...


class Order(System.Object):
    """This class has no documentation."""

    @property
    def CreatedAt(self) -> datetime.datetime:
        ...

    @CreatedAt.setter
    def CreatedAt(self, value: datetime.datetime):
        ...

    @property
    def FilledSize(self) -> typing.Optional[float]:
        ...

    @FilledSize.setter
    def FilledSize(self, value: typing.Optional[float]):
        ...

    @property
    def Future(self) -> str:
        ...

    @Future.setter
    def Future(self, value: str):
        ...

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def Price(self) -> typing.Optional[float]:
        ...

    @Price.setter
    def Price(self, value: typing.Optional[float]):
        ...

    @property
    def AvgFillPrice(self) -> typing.Optional[float]:
        ...

    @AvgFillPrice.setter
    def AvgFillPrice(self, value: typing.Optional[float]):
        ...

    @property
    def RemainingSize(self) -> typing.Optional[float]:
        ...

    @RemainingSize.setter
    def RemainingSize(self, value: typing.Optional[float]):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Size(self) -> typing.Optional[float]:
        ...

    @Size.setter
    def Size(self, value: typing.Optional[float]):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def ReduceOnly(self) -> bool:
        ...

    @ReduceOnly.setter
    def ReduceOnly(self, value: bool):
        ...

    @property
    def Ioc(self) -> bool:
        ...

    @Ioc.setter
    def Ioc(self, value: bool):
        ...

    @property
    def PostOnly(self) -> bool:
        ...

    @PostOnly.setter
    def PostOnly(self, value: bool):
        ...

    @property
    def ClientId(self) -> str:
        ...

    @ClientId.setter
    def ClientId(self, value: str):
        ...


class QuoteRequest(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> int:
        ...

    @Id.setter
    def Id(self, value: int):
        ...

    @property
    def Option(self) -> FtxApi.Rest.Models.FtxOption:
        ...

    @Option.setter
    def Option(self, value: FtxApi.Rest.Models.FtxOption):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Time(self) -> datetime.datetime:
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        ...

    @property
    def RequestExpiry(self) -> datetime.datetime:
        ...

    @RequestExpiry.setter
    def RequestExpiry(self, value: datetime.datetime):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def HideLimitPrice(self) -> typing.Optional[bool]:
        ...

    @HideLimitPrice.setter
    def HideLimitPrice(self, value: typing.Optional[bool]):
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        ...

    @LimitPrice.setter
    def LimitPrice(self, value: typing.Optional[float]):
        ...

    @property
    def Quotes(self) -> typing.List[FtxApi.Rest.Models.OptionQuote]:
        ...

    @Quotes.setter
    def Quotes(self, value: typing.List[FtxApi.Rest.Models.OptionQuote]):
        ...

    def ToString(self) -> str:
        ...


class TriggerOrder(System.Object):
    """This class has no documentation."""

    @property
    def CreatedAt(self) -> datetime.datetime:
        ...

    @CreatedAt.setter
    def CreatedAt(self, value: datetime.datetime):
        ...

    @property
    def Future(self) -> str:
        ...

    @Future.setter
    def Future(self, value: str):
        ...

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Market(self) -> str:
        ...

    @Market.setter
    def Market(self, value: str):
        ...

    @property
    def TriggerPrice(self) -> typing.Optional[float]:
        ...

    @TriggerPrice.setter
    def TriggerPrice(self, value: typing.Optional[float]):
        ...

    @property
    def OrderId(self) -> typing.Optional[float]:
        ...

    @OrderId.setter
    def OrderId(self, value: typing.Optional[float]):
        ...

    @property
    def Side(self) -> str:
        ...

    @Side.setter
    def Side(self, value: str):
        ...

    @property
    def Size(self) -> typing.Optional[float]:
        ...

    @Size.setter
    def Size(self, value: typing.Optional[float]):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Type(self) -> str:
        ...

    @Type.setter
    def Type(self, value: str):
        ...

    @property
    def OrderPrice(self) -> typing.Optional[float]:
        ...

    @OrderPrice.setter
    def OrderPrice(self, value: typing.Optional[float]):
        ...

    @property
    def Error(self) -> str:
        ...

    @Error.setter
    def Error(self, value: str):
        ...

    @property
    def TriggeredAt(self) -> typing.Optional[datetime.datetime]:
        ...

    @TriggeredAt.setter
    def TriggeredAt(self, value: typing.Optional[datetime.datetime]):
        ...

    @property
    def ReduceOnly(self) -> bool:
        ...

    @ReduceOnly.setter
    def ReduceOnly(self, value: bool):
        ...

    @property
    def OrderType(self) -> str:
        ...

    @OrderType.setter
    def OrderType(self, value: str):
        ...

    @property
    def RetryUntilFilled(self) -> bool:
        ...

    @RetryUntilFilled.setter
    def RetryUntilFilled(self, value: bool):
        ...


class WithdrawalHistory(System.Object):
    """This class has no documentation."""

    @property
    def Coin(self) -> str:
        ...

    @Coin.setter
    def Coin(self, value: str):
        ...

    @property
    def Address(self) -> str:
        ...

    @Address.setter
    def Address(self, value: str):
        ...

    @property
    def Tag(self) -> str:
        ...

    @Tag.setter
    def Tag(self, value: str):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Status(self) -> str:
        ...

    @Status.setter
    def Status(self, value: str):
        ...

    @property
    def Time(self) -> str:
        ...

    @Time.setter
    def Time(self, value: str):
        ...

    @property
    def TxId(self) -> str:
        ...

    @TxId.setter
    def TxId(self, value: str):
        ...


