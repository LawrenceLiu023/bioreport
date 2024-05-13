"""
bioreport
=========

Bioreport is a Python package for parsing and searching reports generated by bioinformatics programmes.
"""

__version__ = "1.1.2"

from .report import Report
from .report_sum import ReportSum
from .search import scan_dir

__all__: list[str] = [
    "Report",
    "ReportSum",
    "scan_dir",
]