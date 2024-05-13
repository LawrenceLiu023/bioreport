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
    parse()
        Parse a report file with the module. Returns the parsed report.
    """

    def __init__(self, name="base", submodules: tuple[str, ...] = tuple(), configs={}):
        self.name: str = name
        self.submodules: tuple[str, ...] = submodules
        self.configs: dict = configs

    @abstractmethod
    def parse(self:Self, report:Report, name:str|None=None) -> ReportSum:
        raise NotImplementedError
