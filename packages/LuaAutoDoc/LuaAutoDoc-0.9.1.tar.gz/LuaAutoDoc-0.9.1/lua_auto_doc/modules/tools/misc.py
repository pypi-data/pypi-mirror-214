""" This module contains minor supporting functions not designed specific for a single task."""

import os
from contextlib import contextmanager

# pylint: disable=unused-variable
# Terminal colours
g_warning_colour = '\033[93m'
g_error_colour = '\033[91m'
g_success_colour = '\033[92m'
g_code_field_colour = '\033[100m\033[97m'
g_code_field_end_colour = '\033[0m\033[0m'
g_end_colour = '\033[0m'


@contextmanager
def cd(newdir: str) -> None:
    """ Context manager for changing the current working directory.

    :param newdir: The new directory to change to.
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
# pylint: enable=unused-variable
