import re
from typing import Hashable, Self

import pandas as pd
from pandas import Series

from bioreport import _config
from bioreport._base_module import BaseModule
from bioreport.report import Report
from bioreport.report_sum import ReportSum

_MODULE_NAME = "bowtie2"


class BioReportModule(BaseModule):
    """A class for parsing report."""

    def __init__(self: Self) -> None:
        super(BioReportModule, self).__init__(
            name=_MODULE_NAME, submodules=_config.MODULE_DICT[_MODULE_NAME], configs={}
        )

    def parse(self: Self, report: Report, name: Hashable | None = None) -> ReportSum:
        """
        Parse a bowtie2 report.

        Parameters
        ----------
        report : Report
            A bowtie2 report.
        name : Hashable | None, default None
            The name of `report_sum`. Default is `None`, which means `report_sum` will be named as the report file name.

        Returns
        -------
        report_sum : ReportSum
            A summary of the bowtie2 report.
        """
        module_tuple_len = 2
        if len(report.module) != module_tuple_len:
            raise ValueError(
                f"The module of the report is not supported by {_MODULE_NAME} module: {str(report)}. Expected module name: {_MODULE_NAME}. Expected submodule names: {self.submodules}"
            )
        report_submodule: str = report.module[1]
        if report_submodule not in self.submodules:
            raise ValueError(
                f"The submodule of the report is not supported by {_MODULE_NAME} module: {str(report)}. Expected submodule names: {self.submodules}"
            )

        report_sum_series: Series
        match report_submodule:
            case "paired":
                report_sum_series = self._submodule_summary_parse(report)
            case "unpaired":
                report_sum_series = self._submodule_summary_parse(report)
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

    def _submodule_summary_parse(self: Self, report: Report) -> Series:
        report_sum_dict: dict[str, str] = {}
        with open(report.path, "r") as file:
            for line in file:
                line_str: str = line.strip()
                if line.endswith("; of these:"):
                    line_str = line.split(";")[0]
                    if (curr_unit := line_str.split(" ")[1]) not in [
                        "reads",
                        "pairs",
                        "mates",
                    ]:
                        curr_unit = "reads"
                line_str_list: list[str] = line_str.split(" ")
                value: str = line_str_list[0].strip()
                percentage: str | None
                key: str
                if line_str_list[1].startswith("("):
                    percentage = line_str_list[1].split("%")[0].strip()
                    key = " ".join(line_str_list[2:])
                else:
                    percentage = None
                    key = " ".join(line_str_list[1:])
                report_sum_dict.update({f"{curr_unit} {key}": value})
                if percentage is not None:
                    report_sum_dict.update({f"percent {curr_unit} {key}": percentage})
        report_sum_series: Series = Series(report_sum_dict)

        return report_sum_series
