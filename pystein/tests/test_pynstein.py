"""Unittests for pystein package

Presently only a dummy test to confirm repo setup and CI integration
"""

import pathlib

import pystein
from pystein import tests


class TestPyStein:
    """Test pystein package"""

    def test_package_version(self):
        """Consistency test for version numbers"""
        exp = (0, 5, 2)
        msg = 'Collapse Package {comp} Version Mismatch: Expected {exp:d}, got {got:d}'
        assert pystein.__MAJOR__ == exp[0], msg.format(comp='MAJOR', exp=exp[0], got=pystein.__MAJOR__)
        assert pystein.__MINOR__ == exp[1], msg.format(comp='MINOR', exp=exp[1], got=pystein.__MINOR__)
        assert pystein.__MICRO__ == exp[2], msg.format(comp='MICRO', exp=exp[2], got=pystein.__MICRO__)

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
