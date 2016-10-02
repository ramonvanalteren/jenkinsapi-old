import unittest
import jenkinsapi


class TestMisc(unittest.TestCase):

    def test_jenkinsapi_version(self):
        """Verify that we can get the jenkinsapi version number from the
        package's __version__ property.
        """
        v = jenkinsapi.__version__
        parts = [int(x) for x in v.split('.')]
        for p in parts:
            assert p >= 0, "Implausible version number: %r" % v

if __name__ == '__main__':
    unittest.main()
