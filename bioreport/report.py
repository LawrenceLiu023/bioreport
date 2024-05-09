"""Process bioinformatics report."""

import pathlib
import re
from importlib import import_module
from typing import Any, Hashable, Self

from bioreport import _config
from bioreport.report_sum import ReportSum


class Report:
    """
    A class represent different types of report files.

    Attributes
    ----------
    path : pathlib.Path
        The path to the report file.
    module : tuple[str, ...]
        The type of the file. The length of the tuple could be 0, 1 or 2.

    Methods
    -------
    with_empty_module() -> None
        Check if the module is empty.
    match_file(file_name: str) -> Report
        Match a single file. Determine which type of report it is and return a `Report` object.
    with_matched_module() -> bool
        Check if the `module` of the `Report` object is matched with the actual pattern of the file specified by `path`. Return `True` if the `module` is matched, otherwise return `False`.
    update_module() -> None
        Update the `module` of the `Report` object with the actual pattern of the file specified by `path`.
    parse(update_module: bool = False, *, name: Hashable | None = None) -> ReportSum
        Parse the report file. Return a `ReportSum` object.
    """

    def __init__(
        self: Self, path: str | pathlib.Path, module: tuple[str, ...] = tuple()
    ) -> None:
        self.path: pathlib.Path
        if isinstance(path, str):
            self.path = pathlib.Path(path).absolute()
        elif isinstance(path, pathlib.Path):
            self.path = path.absolute()
        else:
            raise TypeError(f"Invalid type of path: {type(path)}")
        self.module: tuple[str, ...] = module

    def __repr__(self: Self) -> str:
        report_string: str = (
            f'{self.__class__.__name__}(path: "{str(self.path)}", type: "{self.module}")'
        )
        return report_string

    def __eq__(self: Self, other: Any) -> bool:
        is_eq: bool
        if not isinstance(other, Report):
            is_eq = False
            return is_eq
        is_eq = self.path == other.path and self.module == other.module
        return is_eq

    def with_empty_module(self: Self) -> bool:
        """
        Check if the module is empty.

        Returns
        -------
        with_empty_module : bool
            The `module` is empty.
        """
        return len(self.module) == 0

    @classmethod
    def match_file(cls, file: str | pathlib.Path) -> Self:
        """
        Match a single file. Determine which type of report it is and return a `Report` object.

        Parameters
        ----------
        file : str | pathlib.Path
            The file to match.

        Returns
        -------
        report : Report
            The type of the file. The length of the tuple could be 0, 1 or 2.
        """
        file_path: pathlib.Path
        if isinstance(file, str):
            file_path = pathlib.Path(file).absolute()
        elif isinstance(file, pathlib.Path):
            file_path = file.absolute()
        else:
            raise TypeError("file must be a string or pathlib.Path object")

        file_module_match: tuple[str, ...] = tuple()

        report: Report
        if not file_path.is_file():
            report = Report(path=file_path, module=file_module_match)
            return report

        def file_name_glob_check(
            file_path: pathlib.Path, module_patterns: dict[str, str]
        ) -> bool:
            pass_check: bool = True
            if (key_file_name_glob := "pattern_glob") in module_patterns.keys():
                file_path_glob_match_list: list = list(
                    file_path.parent.glob(module_patterns[key_file_name_glob])
                )
                if file_path not in file_path_glob_match_list:
                    pass_check = False
            return pass_check

        def file_name_regex_check(
            file_path: pathlib.Path, module_patterns: dict[str, str]
        ) -> bool:
            pass_check: bool = True
            if (key_file_name_regex := "pattern_regex") in module_patterns.keys():
                file_path_regex_match: re.Match[str] | None = re.match(
                    pattern=module_patterns[key_file_name_regex],
                    string=str(file_path.name),
                )
                if file_path_regex_match is None:
                    pass_check = False
            return pass_check

        def file_content_regex_check(
            file_path: pathlib.Path, module_patterns: dict[str, str]
        ) -> bool:
            pass_check: bool = True
            if (key_context_regex := "content_regex") in module_patterns.keys():
                module_content_regex_line_list: list[str] = module_patterns[
                    key_context_regex
                ].splitlines()
                module_content_regex_line_num: int = len(module_content_regex_line_list)
                with open(file_path, "r") as f:
                    file_content_line_list: list[str] = f.readlines(
                        module_content_regex_line_num
                    )
                content_regex_match: re.Match[str] | None = re.match(
                    pattern=r"\s+".join(module_content_regex_line_list),
                    string="\n".join(file_content_line_list),
                )
                if content_regex_match is None:
                    pass_check = False
            return pass_check

        # match all report patterns
        module_name_matched_set: set[str] = set()
        module_name: str
        module_patterns: dict[str, str]
        for module_name, module_patterns in _config.REPORT_PATTERN.items():
            module_patterns_check: bool = (
                file_name_glob_check(
                    file_path=file_path, module_patterns=module_patterns
                )
                and file_name_regex_check(
                    file_path=file_path, module_patterns=module_patterns
                )
                and file_content_regex_check(
                    file_path=file_path, module_patterns=module_patterns
                )
            )
            if module_patterns_check:
                module_name_matched_set.add(module_name)

        if len(module_name_matched_set) == 0:
            report = Report(path=file_path, module=file_module_match)
            return report
        elif len(module_name_matched_set) > 1:
            raise ValueError(
                f"Too many types of report has been matched: {file_path} -> {module_name_matched_set}. This error could be due to incorrect configuration of report patterns."
            )

        file_module_match = tuple(
            list(module_name_matched_set)[0].split(_config.REPORT_PATTERN_NAME_SEP)
        )
        report = Report(path=file_path, module=file_module_match)
        return report

    def with_matched_module(self: Self) -> bool:
        """
        Check if the `module` of the `Report` object is matched with the actual pattern of the file specified by `path`. Return `True` if the `module` is matched, otherwise return `False`.

        Returns
        -------
        is_matched : bool
            Whether the `module` is matched. `True` if the `module` is matched, otherwise return `False`.
        """
        is_matched: bool
        actual_match_result: Report = self.match_file(file=self.path)
        if actual_match_result.module == self.module:
            is_matched = True
        else:
            is_matched = False
        return is_matched

    def update_module(self: Self) -> None:
        """Update the `module` of the `Report` object with the actual pattern of the file specified by `path`."""
        updated_report: Report = self.match_file(file=self.path)
        self.module = updated_report.module

    def parse(
        self: Self, update_module: bool = False, *, name: Hashable | None = None
    ) -> ReportSum:
        """
        Parse the report file. Return a `ReportSum` object.

        Parameters
        ----------
        update_module : bool
            Whether update the `module` of the `Report` object with the actual pattern of the file specified by `path`.

        Returns
        -------
        report_sum : ReportSum
            The parsed report.
        """
        # update the `module`
        if update_module:
            updated_report: Report = self.match_file(file=self.path)
            self.module = updated_report.module
        # check `module`
        if not self.with_matched_module():
            raise ValueError(
                f"The report file pattern does not match the module specified: {str(self)}"
            )
        # empty `module`
        if self.with_empty_module():
            raise ValueError(
                f"The report file does not match any module pattern: {str(self)}"
            )

        module_name: str = self.module[0]
        module = import_module(
            name=f".{_config.MODULES_DIR_BASENAME}.{module_name}",
            package=_config.PACKAGE_NAME,
        )
        report_sum: ReportSum = module.BioReportModule().parse(report=self, name=name)

        return report_sum
