from typing import overload
import abc

import Calculators.IO
import System
import System.Collections.Generic

Calculators_IO_AggregatedDataLoader_FetchData_T = typing.TypeVar("Calculators_IO_AggregatedDataLoader_FetchData_T")
Calculators_IO_AggregatedDataWriter_ToCsv_T = typing.TypeVar("Calculators_IO_AggregatedDataWriter_ToCsv_T")
Calculators_IO_CsvDataLoader_FetchData_T = typing.TypeVar("Calculators_IO_CsvDataLoader_FetchData_T")
Calculators_IO_CsvDataWriter_ToCsv_T = typing.TypeVar("Calculators_IO_CsvDataWriter_ToCsv_T")
Calculators_IO_IDataLoader_FetchData_T = typing.TypeVar("Calculators_IO_IDataLoader_FetchData_T")
Calculators_IO_IDataWriter_ToCsv_T = typing.TypeVar("Calculators_IO_IDataWriter_ToCsv_T")


class IDataLoader(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def FetchData(self, location: str) -> System.Collections.Generic.IEnumerable[Calculators_IO_IDataLoader_FetchData_T]:
        ...


class AggregatedDataLoader(System.Object, Calculators.IO.IDataLoader):
    """This class has no documentation."""

    def FetchData(self, location: str) -> System.Collections.Generic.IEnumerable[Calculators_IO_AggregatedDataLoader_FetchData_T]:
        ...


class IDataWriter(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def ToCsv(self, data: System.Collections.Generic.IEnumerable[Calculators_IO_IDataWriter_ToCsv_T], path: str, append: bool) -> None:
        ...


class AggregatedDataWriter(System.Object, Calculators.IO.IDataWriter):
    """This class has no documentation."""

    def ToCsv(self, data: System.Collections.Generic.IEnumerable[Calculators_IO_AggregatedDataWriter_ToCsv_T], path: str, append: bool) -> None:
        ...


class CsvDataLoader(System.Object, Calculators.IO.IDataLoader):
    """This class has no documentation."""

    def FetchData(self, filePath: str) -> System.Collections.Generic.IEnumerable[Calculators_IO_CsvDataLoader_FetchData_T]:
        ...


class CsvDataWriter(System.Object, Calculators.IO.IDataWriter):
    """This class has no documentation."""

    def ToCsv(self, datas: System.Collections.Generic.IEnumerable[Calculators_IO_CsvDataWriter_ToCsv_T], path: str, append: bool) -> None:
        ...


