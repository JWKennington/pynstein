"""Unittests for collapse package

Presently only a dummy test to confirm repo setup and CI integration
"""

import collapse


class TestCollapse:

    def test_package_version(self):
        """Consistency test for version numbers"""
        EXPECTED = (0, 0, 1)
        MSG = 'Collapse Package {comp} Version Mismatch: Expected {exp:d}, got {got:d}'
        assert collapse.__MAJOR__ == EXPECTED[0], MSG.format(comp='MAJOR', exp=EXPECTED[0], got=collapse.__MAJOR__)
        assert collapse.__MINOR__ == EXPECTED[1], MSG.format(comp='MINOR', exp=EXPECTED[1], got=collapse.__MINOR__)
        assert collapse.__MICRO__ == EXPECTED[2], MSG.format(comp='MICRO', exp=EXPECTED[2], got=collapse.__MICRO__)
