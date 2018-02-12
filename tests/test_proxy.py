"""
A quick demo showing how to write a proxy class that wraps the self-loading object
"""

import os
import time
import unittest

import hotswapping


class Proxy(object):

    def __init__(self, path, cls_name, max_age=3600.0):
        self._path = path
        self._cls_name = cls_name
        self._getter = hotswapping.SymbolGetter(self._path, max_age=max_age)

    def do(self):
        cls = self._getter(self._cls_name)
        return cls().do()


class TestProxy(unittest.TestCase):

    def setUp(self):
        self.module_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testdata', '1.0.2', 'foobar.py')
        )

    def test_expectSelfReloading(self):
        p = Proxy(self.module_path, 'Doer', max_age=0.1)
        self.assertEqual(0, p.do())
        time.sleep(0.2)
        self.assertEqual(1, p.do())


if __name__ == '__main__':
    unittest.main()
