import pathlib
from shutil import rmtree

from setuptools import find_packages, setup

# remove build directory
CURR_DIR_PATH: pathlib.Path = pathlib.Path(__file__).absolute().parent
BUILD_DIR_PATH: pathlib.Path = CURR_DIR_PATH / "build"
if BUILD_DIR_PATH.is_dir():
    rmtree(BUILD_DIR_PATH)


setup(
    name="bioreport",
    author="liujiahuan",
    version="1.1.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    exclude_package_data={},
    install_requires=[
        "pandas>=2.0.0",
        "rich>=13.0.0",
        "beautifulsoup4>=4.12.0",
    ],
)
