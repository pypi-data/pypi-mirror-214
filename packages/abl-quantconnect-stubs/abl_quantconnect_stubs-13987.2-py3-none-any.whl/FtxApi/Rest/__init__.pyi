from typing import overload
import datetime
import typing

import FtxApi
import FtxApi.Rest
import FtxApi.Rest.Enums
import FtxApi.Rest.Models
import FtxApi.Rest.Models.LeveragedTokens
import FtxApi.Rest.Models.Markets
import System
import System.Collections.Generic
import System.Threading.Tasks


class FtxRestApi(System.Object):
    """This class has no documentation."""

    def __init__(self, client: FtxApi.Client) -> None:
        ...

    def AcceptRequestQuoteAsync(self, quoteId: int) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.OptionQuote]]:
        ...

    def CancelAllOrdersAsync(self, instrument: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[str]]:
        ...

    def CancelOrderAsync(self, id: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[str]]:
        ...

    def CancelOrderByClientIdAsync(self, clientOrderId: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[str]]:
        ...

    def CancelQuoteRequestAsync(self, requestId: int) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.QuoteRequest]]:
        ...

    def ChangeAccountLeverageAsync(self, leverage: int) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.AccountLeverage]:
        ...

    def CreateQuoteRequestAsync(self, side: FtxApi.Rest.Enums.SideType, type: FtxApi.Rest.Enums.OptionType, strike: float, size: float, expiry: typing.Optional[datetime.datetime] = None, limitPrice: typing.Optional[float] = None, hideLimitPrice: typing.Optional[bool] = None, requestExpiry: typing.Optional[datetime.datetime] = None, counterPartyId: typing.Optional[int] = None) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.QuoteRequest]]:
        ...

    def GetAccountInfoAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.AccountInfo]]:
        ...

    def GetAllFuturesAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Future]]]:
        ...

    def GetBalancesAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Balance]]]:
        ...

    def GetCoinAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Coin]]]:
        ...

    def GetCoinsAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Coin]]]:
        ...

    def GetDepositAddressAsync(self, coin: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.DepositAddress]]:
        ...

    def GetDepositHistoryAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.DepositHistory]]]:
        ...

    @overload
    def GetFillsAsync(self, market: str, limit: int, start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date]) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Fill]]]:
        ...

    @overload
    def GetFillsAsync(self, limit: int, start: typing.Union[datetime.datetime, datetime.date]) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Fill]]]:
        ...

    def GetFundingPaymentAsync(self, start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date]) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.FundingPayment]]]:
        ...

    def GetFundingRatesAsync(self, start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date]) -> System.Threading.Tasks.Task[System.Collections.Generic.List[FtxApi.Rest.Models.FundingRate]]:
        ...

    def GetFutureAsync(self, future: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.Future]]:
        ...

    def GetFutureStatsAsync(self, future: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.FutureStats]]:
        ...

    def GetHistoricalPricesAsync(self, marketName: str, resolution: int, start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date]) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Candle]]]:
        ...

    def GetLeveragedTokenBalancesAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.LeveragedTokens.LeveragedTokenBalance]]]:
        ...

    def GetLeveragedTokenCreationListAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.LeveragedTokens.LeveragedTokenCreation]]]:
        ...

    def GetLeveragedTokenRedemptionListAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.LeveragedTokens.LeveragedTokenRedemptionRequest]]]:
        ...

    def GetLeveragedTokensListAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.LeveragedTokens.LeveragedToken]]]:
        ...

    def GetMarketOrderBookAsync(self, marketName: str, depth: int = 20) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.Markets.Orderbook]]:
        ...

    def GetMarketsAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Markets.Market]]]:
        ...

    def GetMarketTradesAsync(self, marketName: str, limit: int, start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date]) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Markets.Trade]]]:
        ...

    def GetMyQuoteRequestsAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.QuoteRequest]]]:
        ...

    def GetOpenOrdersAsync(self, instrument: str = None) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Order]]]:
        ...

    def GetOptionsPositionsAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.OptionPosition]]]:
        ...

    def GetOrderFillsAsync(self, orderId: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Fill]]]:
        ...

    def GetOrderStatusAsync(self, id: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.Order]]:
        ...

    def GetOrderStatusByClientIdAsync(self, clientOrderId: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.Order]]:
        ...

    def GetPositionsAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.Position]]]:
        ...

    def GetQuoteRequestsAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.QuoteRequest]]]:
        ...

    def GetRequestQuotesAsync(self, requestId: int) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.OptionQuote]]]:
        ...

    def GetSingleMarketsAsync(self, marketName: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.Markets.Market]]:
        ...

    def GetTokenInfoAsync(self, tokenName: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.LeveragedTokens.LeveragedToken]]:
        ...

    def GetWithdrawalHistoryAsync(self) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[System.Collections.Generic.List[FtxApi.Rest.Models.WithdrawalHistory]]]:
        ...

    def PlaceOrderAsync(self, instrument: str, side: FtxApi.Rest.Enums.SideType, price: float, orderType: FtxApi.Rest.Enums.OrderType, amount: float, clientId: str = None, ioc: bool = False, reduceOnly: typing.Optional[bool] = False) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.Order]]:
        ...

    def PlaceStopOrderAsync(self, instrument: str, side: FtxApi.Rest.Enums.SideType, type: FtxApi.Rest.Enums.TriggerType, triggerPrice: float, amount: float, orderPrice: typing.Optional[float] = None, reduceOnly: typing.Optional[bool] = None, retryUntilFilled: typing.Optional[bool] = None) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.TriggerOrder]]:
        ...

    def RequestLeveragedTokenCreationAsync(self, tokenName: str, size: float) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.LeveragedTokens.LeveragedTokenCreationRequest]]:
        ...

    def RequestLeveragedTokenRedemptionAsync(self, tokenName: str, size: float) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.LeveragedTokens.LeveragedTokenRedemption]]:
        ...

    def RequestWithdrawalAsync(self, coin: str, size: float, address: str, tag: str, pass: str, code: str) -> System.Threading.Tasks.Task[FtxApi.Rest.Models.FtxResult[FtxApi.Rest.Models.WithdrawalHistory]]:
        ...


class FtxRestApiFactory(System.Object):
    """This class has no documentation."""

    @staticmethod
    def CreateClient(apiKey: str, apiSecret: str) -> FtxApi.Rest.FtxRestApi:
        ...


