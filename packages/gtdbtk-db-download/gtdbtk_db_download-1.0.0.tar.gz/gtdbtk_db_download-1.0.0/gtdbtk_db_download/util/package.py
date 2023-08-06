import os
import sys
from pathlib import Path


def get_module_path() -> Path:
    """
    Returns the path to the module.

    https://docs.python.org/3/library/pkgutil.html#pkgutil.get_data
    """
    module_path = Path(os.path.dirname(sys.modules['gtdbtk_db_download'].__file__))
    return module_path
