# SPDX-License-Identifier: MIT
#
# Based on:
#   https://github.com/packit/rpm-shim
#   Copyright Contributors to the Packit project.
# libdnf5-shim itself is:
#   Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>

"""
libdnf5 shim module implmentation
"""

from __future__ import annotations

import importlib
import json
import logging
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

PROJECT_NAME = "libdnf5-shim"
MODULE_NAME = "libdnf5"

INTERPRETERS: tuple[str, ...] = (
    "/usr/libexec/platform-python",
    f"/usr/bin/python{sys.version_info.major}",
    f"/usr/bin/python{sys.version_info.major}.{sys.version_info.minor}",
)
FAILURE_MSG = (
    "Failed to import system libdnf5 module. "
    "Make sure libdnf5 Python bindings installed on your system."
)

LOG = logging.getLogger(PROJECT_NAME)


def query_interp_sitepackages(interpreter) -> list[str]:
    command = (
        interpreter,
        "-c",
        "import json, site; print(json.dumps(site.getsitepackages()))",
    )
    output = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(output.stdout)


def get_system_sitepackages() -> Iterator[str]:
    """
    Gets a list of sitepackages directories of system Python interpreter(s).

    Returns:
        An iterator of paths.
    """

    for interpreter in INTERPRETERS:
        if not Path(interpreter).is_file():
            continue
        sitepackages = query_interp_sitepackages(interpreter)
        LOG.debug("Collected sitepackages for %s:\n%s", interpreter, sitepackages)
        yield from sitepackages


def try_path(path: str) -> bool:
    """
    Tries to load system libdnf5 module from the specified path.

    Returns:
        True if successful, False otherwise.
    """
    if not (Path(path) / MODULE_NAME).is_dir():
        return False
    sys.path.insert(0, path)
    try:
        importlib.reload(sys.modules[MODULE_NAME])
    except Exception as exc:  # pragma: no cover
        LOG.debug("Exception:", exc_info=exc)
        return False
    else:
        return True
    finally:
        del sys.path[0]


def initialize() -> None:
    """
    Initializes the shim. Tries to load system libdnf5 module.
    """
    for path in get_system_sitepackages():
        LOG.debug(f"Trying {path}")
        if try_path(path):
            LOG.debug("Import successful")
            return
    raise ImportError(FAILURE_MSG)
