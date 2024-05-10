import pathlib
from shutil import rmtree

from setuptools import setup

# remove build directory
CURR_DIR_PATH: pathlib.Path = pathlib.Path(__file__).absolute().parent
BUILD_DIR_PATH: pathlib.Path = CURR_DIR_PATH / "build"
if BUILD_DIR_PATH.is_dir():
    rmtree(BUILD_DIR_PATH)

setup()
