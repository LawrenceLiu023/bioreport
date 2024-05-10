# bioreport

A package for processing bioinformatics reports.

Current version supports the following report types:

- fastp-json
- fastp-html
- bismark-align
- bismark-deduplicate

The package is still under development. The framework is designed to be extensible. More report types will be supported in the future.

## Install

```shell
pip install bioreport
```

## Usage

Quick start:

```python
import bioreport
import pandas as pd

# Scan a directory for reports.
report_list = bioreport.scan_dir("/path/to/report/dir")

# Parse all the reports found.
report_sum_list = [r.parse() for r in report_list]

# Combine the parsed reports.
combined_report = bioreport.ReportSum.concat(report_sum_list)
```

For more details, please see the [documentation](https://bioreport.readthedocs.io/en/latest/).
