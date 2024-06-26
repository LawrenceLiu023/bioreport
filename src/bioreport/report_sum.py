"""Summary of bioinformatics report."""

from typing import Hashable, Iterable, Literal, Self

import pandas as pd
from pandas import DataFrame, Series


class ReportSum:
    """
    A class to represent a summary of a report.

    The data is stored based on pandas `Series` in order to be compatible with pandas processing.

    Attributes
    ----------
    module : tuple[str, ...]
        The module of the report.
    data : Series
        The data of the report.
    name : Hashable | None
        The name of the report.

    Methods
    -------
    concat(report_sums: Iterable[Self], join: Literal["inner", "outer"] = "outer") -> DataFrame
        Concatenate multiple `ReportSum` objects into one.
    """

    def __init__(self, module: tuple[str, ...], data: Series) -> None:
        self.module: tuple[str, ...] = module
        self.data: Series = data

    @property
    def name(self) -> Hashable:
        """
        Get the name of the `data`.

        Returns
        -------
        name : Hashable
            _description_
        """
        name: Hashable | None = self.data.name
        return name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(type: "{self.module}", name: "{self.name}")'

    @classmethod
    def concat(
        cls, report_sums: Iterable[Self], join: Literal["inner", "outer"] = "outer"
    ) -> DataFrame:
        """
        Concatenate multiple `ReportSum` objects into one.

        Parameters
        ----------
        report_sums : Iterable[Self]
            Multiple `ReportSum` objects.
        join : Literal["inner", "outer"], default "outer"
            How to handle indexes on other axis (or axes).

        Returns
        -------
        multi_report_sum : DataFrame
            A `DataFrame` containing the concatenated data from all `ReportSum` objects.
        """
        report_sum_module_list: list = [report_sum.module for report_sum in report_sums]
        if len(set(report_sum_module_list)) > 1:
            error_modules_str: str = ",".join(list(map(str, report_sum_module_list)))
            raise ValueError(
                f"All report_sums must have the same module. The modules of the reports are: {error_modules_str}"
            )
        multi_report_sum: DataFrame = pd.concat(
            [report_sum.data for report_sum in report_sums], axis=1, join=join
        )
        multi_report_sum = multi_report_sum.T
        return multi_report_sum

    def rename(self, name: Hashable | None) -> None:
        """
        Change the name of the `data`.

        Parameters
        ----------
        name : Hashable | None
            The new name of the `data` attribute.
        """
        self.data.name = name
