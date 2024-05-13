"""Search for report files."""

import logging
import pathlib

from rich.logging import RichHandler
from rich.progress import track

from bioreport import _config
from bioreport.report import Report

_logger: logging.Logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_rich_handler = RichHandler(level=logging.INFO, show_path=False, rich_tracebacks=True)
_logger.addHandler(_rich_handler)


def scan_dir(dir: str | pathlib.Path) -> list[Report]:
    """
    Scan a directory to find all the report files.

    Parameters
    ----------
    dir : str | pathlib.Path
        The directory to scan.

    Returns
    -------
    report_list : list[Report]
        A list of `Report` objects. `Report.path` is the report file path. `Report.module` is a tuple of the type of the report.
    """
    dir_path: pathlib.Path
    if isinstance(dir, str):
        dir_path = pathlib.Path(dir).absolute()
    elif isinstance(dir, pathlib.Path):
        dir_path = dir.absolute()
    _logger.info(f"Scanning directory: {str(dir_path)}")

    report_path_to_module_dict: dict[pathlib.Path, tuple[str, ...]] = {}
    file_found_list: list[pathlib.Path] = []
    for curr_root, _, curr_files in dir_path.walk():
        curr_file_path_list: list[pathlib.Path] = [
            pathlib.Path(curr_root) / f for f in curr_files
        ]
        file_found_list.extend(curr_file_path_list)
    _logger.info(f"Total number of files to match: {len(file_found_list)}")
    candidate_report_list: list[Report] = [
        Report.match_file(f)
        for f in track(sequence=file_found_list, description="Matching files...")
    ]
    report_list: list[Report] = list(
        filter(lambda x: not x.with_empty_module(), candidate_report_list)
    )
    return report_list
