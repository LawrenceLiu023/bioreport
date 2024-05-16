from abc import abstractmethod
from typing import Self

from bioreport.report import Report
from bioreport.report_sum import ReportSum


class BaseModule:
    """
    A base class for all modules. Defines the basic structure of a module.

    Attributes
    ----------
    name : str
        The name of the module.
    submodules : tuple[str, ...]
        The submodules of the module. `()` if there are no submodules.
    configs : dict
        The configurations of the module.

    Methods
    -------
    parse(report: Report, name: str | None = None)
        Parse a report file with the module. Returns the parsed report.
    """

    def __init__(
        self, name="base", submodules: tuple[str, ...] = tuple(), configs={}
    ) -> None:
        self.name: str = name
        self.submodules: tuple[str, ...] = submodules
        self.configs: dict = configs

    @abstractmethod
    def parse(self: Self, report: Report, name: str | None = None) -> ReportSum:
        """
        Parse a report.

        Parameters
        ----------
        report : Report
            A report.
        name : Hashable | None, default None
            The name of `report_sum`. Default is `None`, which means `report_sum` will be named as the report file name.

        Returns
        -------
        report_sum : ReportSum
            A summary of the report.
        """
        raise NotImplementedError
