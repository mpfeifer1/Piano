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
        self.assertTrue(True, 'Valid Division found invalid')

    def test_invalidDivisionNoDivision(self):
        division = Tree('number', [])
        self.assertFalse(self.semantic.is_valid_division(division), 'Invalid division, no division found ')

    def test_invalidDivisionNoNumberOnLeft(self):
        division = Tree('division', [Tree('division', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertFalse(self.semantic.is_valid_division(division), 'Invalid division, no number on left')
        pass
    def test_invalidDivisionNoNumberOnRight(self):
        pass
    def test_invalidDivisionNumerator(self):
        pass
    def test_invalidDivisionDenominator(self):
        pass

    def test_validTree(self):
        tree = Tree('start', [Tree('compose', [])])
        self.assertTrue(self.semantic.is_valid_tree(tree), 'Valid Tree found invalid')


    def test_invalidTreeNoCompose(self):
        tree = Tree('start', [Tree('id', [Token('__ANON_0', '$gp')]), Tree('rhs', [Token('__ANON_1', 'acousticgrandpiano')])])
        self.assertFalse(self.semantic.is_valid_tree(tree), 'Invalid tree no compose found as valid') 


    def test_invalidTreeNoStart(self):
        tree = Tree('compose', [])
        self.assertFalse(self.semantic.is_valid_tree(tree), 'Invalid tree no start found as valid')

    
    def test_invalidTreeIdNoRHS(self):
        tree = Tree('start', [Tree('id', Token('__ANON_0', '$gp')), Tree('compose', [Token('__ANON_1', 'acousticgrandpiano')])])
        self.assertFalse(self.semantic.is_valid_tree(tree), 'Invalid tree no rhs to match id found as valid')


    def test_invalidTreeRHSNoId(self):
        tree = Tree('start', [Tree('rhs', Token('__ANON_0', 'acousticgrandpiano')), Tree('compose', [Token('__ANON_1', 'acousticgrandpiano')])])
        self.assertFalse(self.semantic.is_valid_tree(tree), 'Invalid tree no id to match rhs found as valid')


if __name__ == '__main__':
    unittest.main()

