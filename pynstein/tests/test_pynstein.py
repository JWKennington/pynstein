"""Unittests for pynstein package

Presently only a dummy test to confirm repo setup and CI integration
"""

import pathlib

import pynstein
from pynstein import tests


class TestCollapse:
    """Test Collapse package"""

    def test_package_version(self):
        """Consistency test for version numbers"""
        exp = (0, 2, 0)
        msg = 'Collapse Package {comp} Version Mismatch: Expected {exp:d}, got {got:d}'
        assert pynstein.__MAJOR__ == exp[0], msg.format(comp='MAJOR', exp=exp[0], got=pynstein.__MAJOR__)
        assert pynstein.__MINOR__ == exp[1], msg.format(comp='MINOR', exp=exp[1], got=pynstein.__MINOR__)
        assert pynstein.__MICRO__ == exp[2], msg.format(comp='MICRO', exp=exp[2], got=pynstein.__MICRO__)

    def test_test_root(self):
        """Test test root dir"""
        exp = pathlib.Path(__file__).parent.parent
        assert tests.TEST_ROOT == exp, 'Collapse Test Directory moved. Expected {}, got {}'.format(exp.as_posix(), tests.TEST_ROOT.as_posix())

    def test_run_tests(self, mocker):
        """The trick here is to duck punch the pytest main function to short-circuit this call"""
        mocker.patch(
            # Don't want to invoke pytest from within build suite
            'pytest.main',
            return_value=None,
        )
        tests.run_tests()
