"""Unittests for collapse package

Presently only a dummy test to confirm repo setup and CI integration
"""

import pathlib

import collapse
from collapse import tests


class TestCollapse:
    """Test Collapse package"""

    def test_package_version(self):
        """Consistency test for version numbers"""
        exp = (0, 1, 0)
        msg = 'Collapse Package {comp} Version Mismatch: Expected {exp:d}, got {got:d}'
        assert collapse.__MAJOR__ == exp[0], msg.format(comp='MAJOR', exp=exp[0], got=collapse.__MAJOR__)
        assert collapse.__MINOR__ == exp[1], msg.format(comp='MINOR', exp=exp[1], got=collapse.__MINOR__)
        assert collapse.__MICRO__ == exp[2], msg.format(comp='MICRO', exp=exp[2], got=collapse.__MICRO__)

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
