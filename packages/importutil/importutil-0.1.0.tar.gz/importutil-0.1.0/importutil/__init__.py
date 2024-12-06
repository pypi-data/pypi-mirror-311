import importlib.util
import sys
from pathlib import Path


def is_package_installed(package_name: str) -> bool:
    """
    Check if a Python package is installed.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    return importlib.util.find_spec(package_name) is not None


def import_module(file: str):
    file = Path(file).resolve()
    path = str(file.parent)

    original_sys_path = None

    if path not in sys.path:
        original_sys_path = sys.path.copy()
        # append to front
        sys.path = [path, *sys.path]

    module = importlib.import_module(file.stem)

    # restore sys path
    if original_sys_path is not None:
        sys.path = original_sys_path

    return module
