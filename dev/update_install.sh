#!/usr/bin/env bash
# Update and install the latest version of bioreport for development
# execute this script in the root directory of bioreport
python ./setup.py build &&
    echo "** The latest version has been built. **" &&
    pip uninstall -y bioreport &&
    echo "** The old version has been uninstalled. **" &&
    python -m pip install ./ &&
    echo "** The latest version has been installed. **"
