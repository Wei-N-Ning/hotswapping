
import hotswapping

import unittest


class MockModuleDescriptor(object):

    def __init__(self, birth_time):
        self.birth_time = birth_time
        self.deprecated = False


class TestMaxAge(unittest.TestCase):

    def setUp(self):
        self.rule = hotswapping.MaxAge(3600)
        self.m = MockModuleDescriptor(1)

    def test_expectRetired(self):
        self.rule.age = lambda(x): 3601
        self.assertTrue(self.rule.retire(self.m))
        self.assertTrue(self.m.deprecated)

    def test_expectNotRetired(self):
        self.rule.age = lambda(x): 10
        self.rule.max_age = 11
        self.assertFalse(self.rule.retire(self.m))
        self.assertFalse(self.m.deprecated)


if __name__ == '__main__':
    unittest.main()
