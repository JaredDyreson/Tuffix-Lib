from Tuffix.Configuration import DEBUG_BUILD_CONFIG, read_state, State
from Tuffix.Commands import InitCommand
from Tuffix.Editors import EmacsKeyword

# from UnitTests.BaseEditorTester import BaseTestClass
import unittest

IGNORE_ME = True

# class EmacsKeywordTest(BaseTestClass.BaseEditorsTest):
# @classmethod
# def setUpClass(cls):
# super(BaseTestClass.BaseEditorsTest, cls).setUpClass()
# # cls.Keyword = EmacsKeyword(DEBUG_BUILD_CONFIG)
# # print(f'{cls.__name__} -> {dir(cls)}')


class EmacsKeywordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(DEBUG_BUILD_CONFIG,
                          DEBUG_BUILD_CONFIG.version,
                          [], [])
        cls.Init = InitCommand(DEBUG_BUILD_CONFIG)
        cls.Init.create_state_directory()
        cls.state.write()
        cls.Emacs = EmacsKeyword(DEBUG_BUILD_CONFIG)

    @classmethod
    def tearDownClass(cls):
        cls.state.build_config.state_path.unlink()

    def test_add(self):
        """
        Install emacs and check the state path
        """

        before_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("emacs" not in before_install.editors)
        self.Emacs.add()
        after_install = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("emacs" in after_install.editors)

        try:
            self.assertTrue(self.Emacs.is_deb_package_installed('emacs'))
        except EnvironmentError:
            self.assertTrue(False)

    def test_remove(self):
        """
        Remove emacs and check the state path
        """

        self.Emacs.remove()
        after_removal = read_state(DEBUG_BUILD_CONFIG)
        self.assertTrue("emacs" not in after_removal.editors)

        try:
            self.assertFalse(self.Emacs.is_deb_package_installed('emacs'))
        except EnvironmentError:
            self.assertTrue(False)