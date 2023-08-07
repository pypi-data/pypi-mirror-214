from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.Interfaces
import QuantConnect.Parameters
import QuantConnect.Securities
import System
import System.Collections.Generic
import System.Reflection


class ParameterAttribute(System.Attribute):
    """
    Specifies a field or property is a parameter that can be set
    from an AlgorithmNodePacket.Parameters dictionary
    """

    BindingFlags: System.Reflection.BindingFlags = ...
    """Specifies the binding flags used by this implementation to resolve parameter attributes"""

    @property
    def Name(self) -> str:
        """Gets the name of this parameter"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Gets the name of this parameter"""
        ...

    def __init__(self, name: str = None) -> None:
        """
        Initializes a new instance of the ParameterAttribute class
        
        :param name: The name of the parameter. If null is specified then the field or property name will be used
        """
        ...

    @staticmethod
    def ApplyAttributes(parameters: System.Collections.Generic.Dictionary[str, str], instance: typing.Any) -> None:
        """
        Uses reflections to inspect the instance for any parameter attributes.
        If a value is found in the parameters dictionary, it is set.
        
        :param parameters: The parameters dictionary
        :param instance: The instance to set parameters on
        """
        ...

    @staticmethod
    def GetParametersFromAssembly(assembly: System.Reflection.Assembly) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Resolves all parameter attributes from the specified compiled assembly path
        
        :param assembly: The assembly to inspect
        :returns: Parameters dictionary keyed by parameter name with a value of the member type.
        """
        ...

    @staticmethod
    def GetParametersFromType(type: typing.Type) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, str]]:
        """
        Resolves all parameter attributes from the specified type
        
        :param type: The type to inspect
        :returns: Parameters dictionary keyed by parameter name with a value of the member type.
        """
        ...


class PerformanceAnalysisFrequency(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Weekly = 1

    Daily = 2

    Custom = 3


class PerformanceAnalyserAttribute(System.Attribute):
    """
    Specifies a field or property is a parameter that can be set
    from an AlgorithmNodePacket.Parameters dictionary
    """

    @property
    def LiveAlgorithmID(self) -> str:
        """The live algorithm name that the performance analyser will be applied to"""
        ...

    @LiveAlgorithmID.setter
    def LiveAlgorithmID(self, value: str):
        """The live algorithm name that the performance analyser will be applied to"""
        ...

    @property
    def BenchmarkBacktest(self) -> str:
        """The name of this benchmark backtesting algorithm"""
        ...

    @BenchmarkBacktest.setter
    def BenchmarkBacktest(self, value: str):
        """The name of this benchmark backtesting algorithm"""
        ...

    @property
    def StartDate(self) -> typing.Optional[datetime.datetime]:
        """Start date of the expected period of this performance analysis"""
        ...

    @StartDate.setter
    def StartDate(self, value: typing.Optional[datetime.datetime]):
        """Start date of the expected period of this performance analysis"""
        ...

    @property
    def EndDate(self) -> typing.Optional[datetime.datetime]:
        """End date of the expected period of this performance analysis"""
        ...

    @EndDate.setter
    def EndDate(self, value: typing.Optional[datetime.datetime]):
        """End date of the expected period of this performance analysis"""
        ...

    @property
    def DestOutputFolder(self) -> str:
        """The desstination output directory for the performance analysis results"""
        ...

    @DestOutputFolder.setter
    def DestOutputFolder(self, value: str):
        """The desstination output directory for the performance analysis results"""
        ...

    @property
    def DestOutputFileName(self) -> str:
        """The desstination output file name based on the start and end date"""
        ...

    @DestOutputFileName.setter
    def DestOutputFileName(self, value: str):
        """The desstination output file name based on the start and end date"""
        ...

    @property
    def InitialCashBook(self) -> QuantConnect.Securities.CashBook:
        ...

    @InitialCashBook.setter
    def InitialCashBook(self, value: QuantConnect.Securities.CashBook):
        ...

    @property
    def InitialHoldings(self) -> System.Collections.Generic.Dictionary[str, QuantConnect.Holding]:
        ...

    @InitialHoldings.setter
    def InitialHoldings(self, value: System.Collections.Generic.Dictionary[str, QuantConnect.Holding]):
        ...

    @property
    def Frequency(self) -> int:
        """This property contains the int value of a member of the QuantConnect.Parameters.PerformanceAnalysisFrequency enum."""
        ...

    @Frequency.setter
    def Frequency(self, value: int):
        """This property contains the int value of a member of the QuantConnect.Parameters.PerformanceAnalysisFrequency enum."""
        ...

    @overload
    def __init__(self, StartDate: typing.Union[datetime.datetime, datetime.date], EndDate: typing.Union[datetime.datetime, datetime.date], BenchmarkBacktest: str = ..., DestOutputFolder: str = ..., LiveAlgorithmID: str = ...) -> None:
        """
        Initializes a new instance of the PerformanceAnalyserAttribute class
        
        :param StartDate: the specified start date of this analysis job
        :param EndDate: the specified end date of this analysis job
        :param BenchmarkBacktest: the target backtesting algorithm name to compare with in this analysis job
        :param DestOutputFolder: the destination output folder for live results of this analysis job
        :param LiveAlgorithmID: the live algorithm name that need an analysis
        """
        ...

    @overload
    def __init__(self, BenchmarkBacktest: str = ..., Frequency: QuantConnect.Parameters.PerformanceAnalysisFrequency = ..., DestOutputFolder: str = ..., LiveAlgorithmID: str = ...) -> None:
        """
        Initializes a new instance of the PerformanceAnalyserAttribute class
        
        :param BenchmarkBacktest: the target backtesting algorithm name to compare with in this analysis job
        :param Frequency: the frequency of this performance analysis job
        :param DestOutputFolder: the destination output folder for live results of this analysis job
        :param LiveAlgorithmID: the live algorithm name that need an analysis
        """
        ...

    def InitRolloverPeriod(self) -> None:
        ...

    def IsInvokingBacktest(self) -> bool:
        ...

    def TakePortfolioSnapshot(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        ...

    def UpdateRolloverPeriod(self) -> None:
        ...


