"""Unittests for collapse package

Presently only a dummy test to confirm repo setup and CI integration
"""
import pathlib

import collapse
from collapse import tests


class TestCollapse:

    def test_package_version(self):
        """Consistency test for version numbers"""
        EXPECTED = (0, 0, 2)
        MSG = 'Collapse Package {comp} Version Mismatch: Expected {exp:d}, got {got:d}'
        assert collapse.__MAJOR__ == EXPECTED[0], MSG.format(comp='MAJOR', exp=EXPECTED[0], got=collapse.__MAJOR__)
        assert collapse.__MINOR__ == EXPECTED[1], MSG.format(comp='MINOR', exp=EXPECTED[1], got=collapse.__MINOR__)
        assert collapse.__MICRO__ == EXPECTED[2], MSG.format(comp='MICRO', exp=EXPECTED[2], got=collapse.__MICRO__)

    def test_test_root(self):
        EXPECTED = pathlib.Path(__file__).parent.parent
        assert tests.TEST_ROOT == EXPECTED, 'Collapse Test Directory moved. Expected {}, got {}'.format(EXPECTED.as_posix(), tests.TEST_ROOT.as_posix())

    def test_run_tests(self, mocker):
        """The trick here is to duck punch the pytest main function to short-circuit this call"""
        mocker.patch(
            # Don't want to invoke pytest from within build suite
            'pytest.main',
            return_value=None,
        )
        tests.run_tests()