import pathlib
from collections import defaultdict

import tomllib

# package directories
PACKAGE_DIR_PATH: pathlib.Path = pathlib.Path(__file__).absolute().parent
PACKAGE_NAME: str = PACKAGE_DIR_PATH.name

# search patterns
_report_pattern_file_basename: str = "report_pattern.toml"
REPORT_PATTERN_KEYS: list[str] = ["pattern_glob", "pattern_regex", "content_regex"]
_report_pattern_path: pathlib.Path = PACKAGE_DIR_PATH / _report_pattern_file_basename
with open(_report_pattern_path, "rb") as report_pattern_file:
    REPORT_PATTERN: dict = tomllib.load(report_pattern_file)
REPORT_PATTERN_NAME_SEP: str = "-"  # separator of key, i.e. "fastp-json"

# modules
MODULES_DIR_BASENAME: str = "_modules"
MODULES_DIR_PATH: pathlib.Path = PACKAGE_DIR_PATH / MODULES_DIR_BASENAME
_modules_dict: defaultdict[str, list[str]] = defaultdict(list)
for _curr_key in REPORT_PATTERN.keys():
    _curr_key_split_list: list[str] = _curr_key.split(REPORT_PATTERN_NAME_SEP)
    _curr_module_name: str = _curr_key_split_list[0]
    if len(_curr_key_split_list) == 2:
        _curr_submodule_name: str = _curr_key_split_list[1]
        _modules_dict[_curr_module_name].append(_curr_submodule_name)
    elif (
        len(_curr_key_split_list) == 1 and _curr_module_name not in _modules_dict.keys()
    ):
        _modules_dict[_curr_module_name] = []
    elif len(_curr_key_split_list) == 1 and _curr_module_name in _modules_dict.keys():
        raise ValueError(
            f"Conflict of report pattern keys: {_curr_module_name} <-> {_curr_key}"
        )
    else:
        raise ValueError(f"Invalid report pattern key: {_curr_key}")
MODULE_DICT: dict[str, tuple[str, ...]] = {
    m: tuple(sm) for m, sm in _modules_dict.items()
}

if __name__ == "__main__":
    print(MODULE_DICT)
