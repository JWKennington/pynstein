"""Tests subpackage"""
import pathlib

import pytest

TEST_ROOT = pathlib.Path(__file__).parent.parent


def run_tests():
    """Helper function for invoking pytest suite
    Returns:
        None
    """
    return pytest.main(['-x', TEST_ROOT.as_posix()])
