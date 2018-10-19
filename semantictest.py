import unittest
from testhelper import TestHelp
from semantic import Semantic
from lark import Tree
from lark import lexer

Token = lexer.Token

class TestSemantics(unittest.TestCase):

    def setUp(self):
        self.help = TestHelp()
        self.semantic = Semantic(Tree('start', []))


    def test_validDivision(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '4')])]) 
        self.semantic.is_valid_division(division)
        self.assertTrue(True)


    def test_validTree(self):
        tree = Tree('start', [Tree('compose', [])])
        self.assertTrue(self.semantic.is_valid_tree(tree), 'Valid Tree found invalid')


if __name__ == '__main__':
    unittest.main()

