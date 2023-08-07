from typing import overload
import datetime

import FtxApi.Rest.Models.LeveragedTokens
import System


class LeveragedToken(System.Object):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def Description(self) -> str:
        ...

    @Description.setter
    def Description(self, value: str):
        ...

    @property
    def Underlying(self) -> str:
        ...

    @Underlying.setter
    def Underlying(self, value: str):
        ...

    @property
    def Outstanding(self) -> float:
        ...

    @Outstanding.setter
    def Outstanding(self, value: float):
        ...

    @property
    def PricePerShare(self) -> float:
        ...

    @PricePerShare.setter
    def PricePerShare(self, value: float):
        ...

    @property
    def PositionPerShare(self) -> float:
        ...

    @PositionPerShare.setter
    def PositionPerShare(self, value: float):
        ...

    @property
    def UnderlyingMark(self) -> float:
        ...

    @UnderlyingMark.setter
    def UnderlyingMark(self, value: float):
        ...

    @property
    def ContractAddress(self) -> str:
        ...

    @ContractAddress.setter
    def ContractAddress(self, value: str):
        ...

    @property
    def Change1h(self) -> float:
        ...

    @Change1h.setter
    def Change1h(self, value: float):
        ...

    @property
    def Change24h(self) -> float:
        ...

    @Change24h.setter
    def Change24h(self, value: float):
        ...


class LeveragedTokenBalance(System.Object):
    """This class has no documentation."""

    @property
    def Token(self) -> str:
        ...

    @Token.setter
    def Token(self, value: str):
        ...

    @property
    def Balance(self) -> float:
        ...

    @Balance.setter
    def Balance(self, value: float):
        ...


class LeveragedTokenCreation(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Token(self) -> str:
        ...

    @Token.setter
    def Token(self, value: str):
        ...

    @property
    def RequestedSize(self) -> float:
        ...

    @RequestedSize.setter
    def RequestedSize(self, value: float):
        ...

    @property
    def Pending(self) -> bool:
        ...

    @Pending.setter
    def Pending(self, value: bool):
        ...

    @property
    def CreatedSize(self) -> float:
        ...

    @CreatedSize.setter
    def CreatedSize(self, value: float):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Cost(self) -> float:
        ...

    @Cost.setter
    def Cost(self, value: float):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def RequestedAt(self) -> datetime.datetime:
        ...

    @RequestedAt.setter
    def RequestedAt(self, value: datetime.datetime):
        ...

    @property
    def FulfilledAt(self) -> datetime.datetime:
        ...

    @FulfilledAt.setter
    def FulfilledAt(self, value: datetime.datetime):
        ...


class LeveragedTokenCreationRequest(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Token(self) -> str:
        ...

    @Token.setter
    def Token(self, value: str):
        ...

    @property
    def RequestedSize(self) -> float:
        ...

    @RequestedSize.setter
    def RequestedSize(self, value: float):
        ...

    @property
    def Pending(self) -> bool:
        ...

    @Pending.setter
    def Pending(self, value: bool):
        ...

    @property
    def Cost(self) -> float:
        ...

    @Cost.setter
    def Cost(self, value: float):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def RequestedAt(self) -> datetime.datetime:
        ...

    @RequestedAt.setter
    def RequestedAt(self, value: datetime.datetime):
        ...


class LeveragedTokenRedemption(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Token(self) -> str:
        ...

    @Token.setter
    def Token(self, value: str):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def ProjectedProceeds(self) -> float:
        ...

    @ProjectedProceeds.setter
    def ProjectedProceeds(self, value: float):
        ...

    @property
    def Pending(self) -> bool:
        ...

    @Pending.setter
    def Pending(self, value: bool):
        ...

    @property
    def RequestedAt(self) -> datetime.datetime:
        ...

    @RequestedAt.setter
    def RequestedAt(self, value: datetime.datetime):
        ...


class LeveragedTokenRedemptionRequest(System.Object):
    """This class has no documentation."""

    @property
    def Id(self) -> float:
        ...

    @Id.setter
    def Id(self, value: float):
        ...

    @property
    def Token(self) -> str:
        ...

    @Token.setter
    def Token(self, value: str):
        ...

    @property
    def Size(self) -> float:
        ...

    @Size.setter
    def Size(self, value: float):
        ...

    @property
    def Pending(self) -> bool:
        ...

    @Pending.setter
    def Pending(self, value: bool):
        ...

    @property
    def Price(self) -> float:
        ...

    @Price.setter
    def Price(self, value: float):
        ...

    @property
    def Proceeds(self) -> float:
        ...

    @Proceeds.setter
    def Proceeds(self, value: float):
        ...

    @property
    def Fee(self) -> float:
        ...

    @Fee.setter
    def Fee(self, value: float):
        ...

    @property
    def RequestedAt(self) -> datetime.datetime:
        ...

    @RequestedAt.setter
    def RequestedAt(self, value: datetime.datetime):
        ...

    @property
    def FulfilledAt(self) -> datetime.datetime:
        ...

    @FulfilledAt.setter
    def FulfilledAt(self, value: datetime.datetime):
        ...


