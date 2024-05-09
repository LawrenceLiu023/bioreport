import re
from typing import Hashable, Self

import pandas as pd

from bioreport import _config
from bioreport._base_module import BaseModule
from bioreport.report import Report
from bioreport.report_sum import ReportSum

_MODULE_NAME = "bismark"


class BioReportModule(BaseModule):
    """A class for parsing report."""

    def __init__(self: Self) -> None:
        super(BioReportModule, self).__init__(
            name=_MODULE_NAME, submodules=_config.MODULE_DICT[_MODULE_NAME], configs={}
        )
        self.SUBMODULE_ALIGN_INFO_LINE_PATTERN: re.Pattern = re.compile(
            r"(?P<key>^[^:^\n]+):\s*(?P<value>[\d\%\.]+)\s*(?P<bracket>\(.+\))?\s*$"
        )
        self.SUBMODULE_DEDUPLICATE_INFO_LINE_PATTERN: re.Pattern = re.compile(
            r"(?P<key>^[^:^\n]+):\s*(?P<value>[\d\%\.]+)\s*(?P<bracket>\(.+\))?\s*$"
        )

    def parse(self: Self, report: Report, name: Hashable | None = None) -> ReportSum:
        """
        Parse a bismark report.

        Parameters
        ----------
        report : Report
            A bismark report.
        name : Hashable | None
            The name of `report_sum`. Default is `None`, which means `report_sum` will be named as the report file name.

        Returns
        -------
        report_sum : ReportSum
            A summary of the bismark report.
        """
        if len(report.module) != 2:
            raise ValueError(
                f"The module of the report is not supported by {_MODULE_NAME} module: {str(report)}. Expected module name: {_MODULE_NAME}. Expected submodule names: {self.submodules}"
            )
        report_submodule: str = report.module[1]
        if report_submodule not in self.submodules:
            raise ValueError(
                f"The submodule of the report is not supported by {_MODULE_NAME} module: {str(report)}. Expected submodule names: {self.submodules}"
            )

        report_sum_series: pd.Series
        match report_submodule:
            case "align":
                report_sum_series = self._submodule_align_parse(report)
            case "deduplicate":
                report_sum_series = self._submodule_deduplicate_parse(report)
            case _:
                raise ValueError(
                    f"The submodule of the report is not supported by {_MODULE_NAME} module: {str(report)}. Expected submodule names: {self.submodules}"
                )
        if name is None:
            report_sum_series.name = report.path.name
        elif isinstance(name, str):
            report_sum_series.name = name
        else:
            raise ValueError(f"The name of the report is not supported: {str(name)}")

        report_sum: ReportSum = ReportSum(module=report.module, data=report_sum_series)

        return report_sum

    def _submodule_align_parse(self: Self, report: Report) -> pd.Series:
        """
        Parse a bismark alignment report.

        Parameters
        ----------
        report : Report
            A bismark alignment report.

        Returns
        -------
        report_sum_series : pd.Series
            The summary of the report.
        """
        report_sum_dict: dict[str, str] = {}
        with open(report.path, "r") as file:
            for line in file:
                line_match: re.Match[str] | None = (
                    self.SUBMODULE_ALIGN_INFO_LINE_PATTERN.match(line)
                )
                if line_match is None:
                    continue
                key: str = line_match.group("key")
                value: str = line_match.group("value")
                report_sum_dict.update({key: value})
        report_sum_series: pd.Series = pd.Series(report_sum_dict)
        return report_sum_series

    def _submodule_deduplicate_parse(self: Self, report: Report) -> pd.Series:
        """
        Parse a bismark deduplicate report.

        Parameters
        ----------
        report : Report
            A bismark deduplicate report.

        Returns
        -------
        report_sum_series : pd.Series
            The summary of the report.
        """
        report_sum_dict: dict = {}
        with open(report.path, "r") as file:
            for line in file:
                line_match: re.Match[str] | None = (
                    self.SUBMODULE_ALIGN_INFO_LINE_PATTERN.match(line)
                )
                if line_match is None:
                    continue
                key: str = line_match.group("key")
                value: str = line_match.group("value")
                report_sum_dict.update({key: value})
        report_sum_series: pd.Series = pd.Series(report_sum_dict)
        return report_sum_series
