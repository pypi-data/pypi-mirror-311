"""
File: main.py
Creation Date: 2024-11-25
Last Update: 2024-11-25
Creator: eis-x
Github: https://github.com/eis-x/pytreebuilder
"""

import unittest
import os
from pytreebuilder.pytreebuilder import PyTreeBuilder

class TestTreeBuilder(unittest.TestCase):
    def setUp(self):
        self.tree_file = 'trees/any_project_tree.txt'  # Nom du fichier de description de structure existant

    def test_create_project_structure(self):
        builder = PyTreeBuilder(self.tree_file)
        builder.create_project_structure()
        self.assertTrue(os.path.isdir('anyproject'))
        self.assertTrue(os.path.isfile('anyproject/anyproject/__init__.py'))
        self.assertTrue(os.path.isfile('anyproject/anyproject/anyproject.py'))
        self.assertTrue(os.path.isdir('anyproject/tests'))
        self.assertTrue(os.path.isfile('anyproject/tests/__init__.py'))
        self.assertTrue(os.path.isfile('anyproject/tests/test_anyproject.py'))
        self.assertTrue(os.path.isfile('anyproject/setup.py'))
        self.assertTrue(os.path.isfile('anyproject/README.md'))
        self.assertTrue(os.path.isfile('anyproject/LICENSE'))

    def tearDown(self):
        import shutil
        if os.path.exists('anyproject'):
            shutil.rmtree('anyproject')

if __name__ == '__main__':
    unittest.main()
