from json import load
from typing import Hashable, Self

import pandas as pd
from bs4 import BeautifulSoup, Tag

from bioreport import _config
from bioreport._base_module import BaseModule
from bioreport.report import Report
from bioreport.report_sum import ReportSum

_MODULE_NAME = "fastp"


class BioReportModule(BaseModule):
    """A class for parsing report."""

    def __init__(self: Self) -> None:
        super(BioReportModule, self).__init__(
            name=_MODULE_NAME, submodules=_config.MODULE_DICT[_MODULE_NAME], configs={}
        )

    def parse(self: Self, report: Report, name: Hashable | None = None) -> ReportSum:
        """
        Parse a fastp report.

        Parameters
        ----------
        report : Report
            A fastp report.
        name : Hashable | None
            The name of `report_sum`. Default is `None`, which means `report_sum` will be named as the report file name.

        Returns
        -------
        report_sum : ReportSum
            A summary of the fastp report.
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
            case "html":
                report_sum_series = self._submodule_html_parse(report)
            case "json":
                report_sum_series = self._submodule_json_parse(report)
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

    def _submodule_html_parse(self: Self, report: Report) -> pd.Series:
        """
        Parse a fastp report in html format.

        Parameters
        ----------
        report : Report
            A fastp html report.

        Returns
        -------
        report_sum_series : pd.Series
            The summary of the report.
        """
        with open(report.path, "r") as file:
            html_content: str = file.read()

        soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")

        DIV_ID_LIST: list[str] = [
            "general",
            "before_filtering_summary",
            "after_filtering_summary",
            "filtering_result",
        ]

        div_list: list[Tag] = [soup.find("div", id=div_id) for div_id in DIV_ID_LIST]

        def _summary_table_parse(table) -> dict[str, str]:
            info_dict: dict[str, str] = {}
            row_list: list[Tag] = table.find_all("tr")
            for row in row_list:
                col_list: list[Tag] = row.find_all("td")
                row_text_list: list[str] = [col.text.strip() for col in col_list]
                if len(row_text_list) != 2:
                    raise ValueError(f"Unexpected table row: \n{row}")
                row_text_list[0] = row_text_list[0].removesuffix(":")
                info_dict.update({row_text_list[0]: row_text_list[1]})
            return info_dict

        table_info_dict_list: list[dict[str, str]] = [
            {} for _ in range(len(DIV_ID_LIST))
        ]
        for div_index, div in enumerate(div_list):
            if not div:
                continue

            summary_table_list: list[Tag] = div.find_all(
                "table", class_="summary_table"
            )

            for table in summary_table_list:
                table_info_dict: dict[str, str] = _summary_table_parse(table)
                table_info_dict_list[div_index] = table_info_dict

        report_sum_dict: dict[tuple[str, str], str] = {}
        for table_index in range(len(DIV_ID_LIST)):
            table_info_type: str = DIV_ID_LIST[table_index]
            table_info_dict = table_info_dict_list[table_index]
            report_sum_dict.update(
                {
                    (table_info_type, key): value
                    for key, value in table_info_dict.items()
                }
            )
        report_sum_series: pd.Series = pd.Series(report_sum_dict)
        return report_sum_series

    def _submodule_json_parse(self: Self, report: Report) -> pd.Series:
        """
        Parse a json report in html format.

        Parameters
        ----------
        report : Report
            A json html report.

        Returns
        -------
        report_sum_series : pd.Series
            The summary of the report.
        """
        with open(report.path, "r") as file:
            json_dict: dict = load(file)
        summary_dict: dict | None = json_dict.get("summary")
        if summary_dict is None:
            raise ValueError("Invalid JSON report.")
        before_filtering_dict: dict | None = summary_dict.get("before_filtering")
        after_filtering_dict: dict | None = summary_dict.get("after_filtering")
        filtering_result_dict: dict | None = json_dict.get("filtering_result")
        if (
            before_filtering_dict is None
            or after_filtering_dict is None
            or filtering_result_dict is None
        ):
            raise ValueError("Invalid JSON report.")
        before_filtering_dict = {
            ("before_filtering", key): value
            for key, value in before_filtering_dict.items()
        }
        after_filtering_dict = {
            ("after_filtering", key): value
            for key, value in after_filtering_dict.items()
        }
        filtering_result_dict = {
            ("filtering_result", key): value
            for key, value in filtering_result_dict.items()
        }
        result_sum_dict: dict = {
            **before_filtering_dict,
            **after_filtering_dict,
            **filtering_result_dict,
        }
        result_sum_series: pd.Series = pd.Series(result_sum_dict)
        return result_sum_series
