
import os

import hotswapping

import unittest


class TestCreateDescriptorFromFs(unittest.TestCase):

    def setUp(self):
        self.module_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testdata', '1.0.2', 'foobar.py')
        )

    def test_nonExistingPath_expectNothingImported(self):
        self.assertFalse(hotswapping.create_descriptor_from_fs(''))

    def test_givenDirectoryPath_expectNothingImported(self):
        self.assertFalse(hotswapping.create_descriptor_from_fs(
            os.path.dirname(self.module_path)
        ))

    def test_expectModuleDescriptor(self):
        m = hotswapping.create_descriptor_from_fs(self.module_path)
        self.assertTrue(m)


class TestRenew(unittest.TestCase):

    def setUp(self):
        self.timer_rule = hotswapping.MaxAge(-1)
        self.search_rule = hotswapping.NewerSemanticVersion()

    def test_newerVersionAvaiable_expectRenewed(self):
        module_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testdata', '1.0.2', 'foobar.py')
        )
        m = hotswapping.create_descriptor_from_fs(module_path)
        self.assertFalse(m.deprecated)
        new_m = hotswapping.renew(m, self.search_rule, self.timer_rule)
        self.assertTrue(new_m)
        self.assertTrue(m.deprecated)

    def test_noNewerVersion_expectNotRenewed(self):
        module_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testdata', '2.1.0', 'foobar.py')
        )
        m = hotswapping.create_descriptor_from_fs(module_path)
        self.assertFalse(m.deprecated)
        new_m = hotswapping.renew(m, self.search_rule, self.timer_rule)
        self.assertFalse(new_m)
        self.assertFalse(m.deprecated)


class TestLoadUnload(unittest.TestCase):

    def setUp(self):
        self.module_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testdata', '1.0.2', 'foobar.py')
        )

    def test_load_unload_expectSymbol(self):
        m = hotswapping.create_descriptor_from_fs(self.module_path)
        mod_ = hotswapping.load(m)
        self.assertEqual(3, mod_.FOOBAR)
        self.assertEqual(3, hotswapping.unload(m))

    def test_reload_expectNewValue(self):
        m = hotswapping.create_descriptor_from_fs(self.module_path)
        self.assertEqual(3, hotswapping.load(m).FOOBAR)
        hotswapping.unload(m)
        m = hotswapping.renew(m,
                              hotswapping.NewerSemanticVersion(check_existence=True),
                              hotswapping.MaxAge(-1))
        self.assertEqual(39, hotswapping.load(m).FOOBAR)
        hotswapping.unload(m)


class TestSymbolGetter(unittest.TestCase):

    def setUp(self):
        self.module_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testdata', '1.0.2', 'foobar.py')
        )

    def test_reloadEveryTime(self):
        getter = hotswapping.SymbolGetter(self.module_path, max_age=-1)
        self.assertEqual(39, getter('FOOBAR'))
        self.assertEqual(None, getter('aaa'))

    def test_reloadEveryTwoHours(self):
        getter = hotswapping.SymbolGetter(self.module_path, max_age=3600)
        self.assertEqual(3, getter('FOOBAR'))

    def test_getAllSymbols(self):
        getter = hotswapping.SymbolGetter(self.module_path, max_age=-1)
        d = getter.get_all(['FOOBAR', 'Doer', 'not_there'])
        self.assertEqual(2, len(d))
        self.assertTrue(d['FOOBAR'])
        self.assertTrue(d['Doer'])
        self.assertNotIn('not_there', d)


if __name__ == '__main__':
    unittest.main()
