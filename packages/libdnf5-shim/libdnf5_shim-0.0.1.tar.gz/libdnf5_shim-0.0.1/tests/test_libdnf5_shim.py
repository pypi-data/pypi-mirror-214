# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys
from types import ModuleType

import pytest
from pytest_mock import MockerFixture


def basic(mod: ModuleType):
    assert mod.__name__ == "libdnf5"
    base = mod.base.Base()
    base.load_config_from_file()
    base.get_config()
    base.setup()


def test_libdnf5_import(mocker: MockerFixture):
    import _libdnf5_shim._impl

    initializes = mocker.spy(_libdnf5_shim._impl, "initialize")

    # Import libdnf5 for the first time
    import libdnf5

    # Check that the shim was used
    initializes.assert_called_once()
    assert "libdnf5" in sys.modules
    assert "_libdnf5_shim.initialize" in sys.modules

    # Run basic tests to make sure the imported libdnf5 works
    basic(libdnf5)

    # Import again
    import libdnf5

    basic(libdnf5)

    # Ensure that initialize was only called once
    initializes.assert_called_once()


def test_libdnf5_import_fail(mocker: MockerFixture):
    import _libdnf5_shim._impl

    initializes = mocker.spy(_libdnf5_shim._impl, "initialize")

    # Set the INTERPRETERS to an empty tuple to cause a failure
    inters = _libdnf5_shim._impl.INTERPRETERS
    _libdnf5_shim._impl.INTERPRETERS = ()

    # Check failure
    try:
        with pytest.raises(ImportError, match=_libdnf5_shim._impl.FAILURE_MSG):
            import libdnf5
    finally:
        _libdnf5_shim._impl.INTERPRETERS = inters

    # Check that shim was used
    initializes.assert_called_once()

    # Try to import libdnf5
    import libdnf5  # noqa: F811

    # Check that it works now
    basic(libdnf5)
    assert initializes.call_count == 2
