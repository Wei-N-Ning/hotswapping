
import unittest

import packageFoo


class TestPackageFoo(unittest.TestCase):

    def setUp(self):
        self.dao = packageFoo.PackageFoo()

    def test_getPackages(self):
        self.assertFalse(self.dao.get_all('doom2'))
        self.assertEqual(
            ['doom-1.0', 'doom-1.1', 'doom-1.2'],
            self.dao.get_all('doom')
        )

    def test_resolve(self):
        self.assertTrue(
            self.dao.resolve(['doom-1.0'])
        )

    def test_split(self):
        self.assertSequenceEqual(('doom', '1.0'), self.dao.split('doom-1.0'))

    def test_comparePackages(self):
        self.assertEqual(0, self.dao.compare_packages('doom-1.0', 'doom-1.0'))
        self.assertEqual(0, self.dao.compare_packages('doom-1.0.0', 'doom-1'))
        self.assertEqual(1, self.dao.compare_packages('doom-1.3', 'doom-1.0'))
        self.assertEqual(-1, self.dao.compare_packages('doom-0.99', 'doom-1.0'))
        self.assertEqual(1, self.dao.compare_packages('doom2-1.0', 'doom-1.0'))
        self.assertEqual(0, self.dao.compare_packages('doom-1.0', 'hexen-1.0'))
        self.assertEqual(1, self.dao.compare_packages('doom-1.0', 'doom'))


if __name__ == '__main__':
    unittest.main()
