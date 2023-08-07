from typing import overload
import FtxApi.Rest.Enums
import System


class OptionType(System.Enum):
    """This class has no documentation."""

    put = 0

    call = 1


class OrderType(System.Enum):
    """This class has no documentation."""

    limit = 0

    market = 1


class SideType(System.Enum):
    """This class has no documentation."""

    buy = 0

    sell = 1


class TriggerType(System.Enum):
    """This class has no documentation."""

    stop = 0

    trailingStop = 1

    takeProfit = 2


