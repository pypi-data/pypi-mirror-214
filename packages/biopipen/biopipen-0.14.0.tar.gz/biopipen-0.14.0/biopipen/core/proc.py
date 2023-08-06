"""Provides a base class for the processes to subclass"""
from diot import Diot
from liquid.defaults import SEARCH_PATHS
from pipen import Proc as PipenProc

from .filters import filtermanager
from .defaults import BIOPIPEN_DIR, REPORT_DIR


def _repr(x):
    if isinstance(x, Diot):
        return repr(x.to_dict())
    return repr(x)


filtermanager.register("repr")(_repr)


class Proc(PipenProc):
    """Base class for all processes in biopipen to subclass"""

    template_opts = {
        "globals": {"biopipen_dir": str(BIOPIPEN_DIR)},
        "filters": filtermanager.filters.copy(),
        "search_paths": SEARCH_PATHS + [str(REPORT_DIR)],
    }
