# Standard imports
import lark
import unittest
from lark import Tree
from lark import lexer
from lark import exceptions

Token = lexer.Token
LarkError = exceptions.LarkError

# Local imports
from testhelper import TestHelp

# Change directory for imports
TestHelp().chwd()

# Core imports
import grammar

class TestGrammar(unittest.TestCase):

    def setUp(self):
        self.l = lark.Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")
        self.help = TestHelp()


    def test_variable(self):
        test = '''
        compose{
            measure {
                acousticgrandpiano {
                    mf;
                }
            }
        }
        '''
        accept = Tree('start', [Tree('compose', [Tree('composeitems', [Tree('measure', [Tree('instrumentation', [Token('INSTRUMENT', 'acousticgrandpiano'), Tree('noteitem', [Tree('inlinedynamic', [Token('__ANON_5', 'mf')])])])])])])])

        res = self.l.parse(test)#.pretty()
        self.assertEqual(accept, res, 'Variable declaration not properly parsed')


    def test_comment(self):
        ''' Arrange '''
        test = """
        Compose{
            // Nathan is a nerd
        }
        """
        expected ='''
        start
            compose
        '''
        actual = self.l.parse(test).pretty()
        self.assertTrue(self.help.prettyTreeComp(actual, expected), 'Comments not parsed correctly')


    def test_basicMeasure(self):
        test="""
        Compose {
            Measure {
                acousticgrandpiano {
                    1/4 Bb4;
                }
            }
        }
        """

        accept = '''
        start
          compose
            composeitems
              measure
                instrumentation
                  acousticgrandpiano
                  noteitem
                    note
                      division
                        number 1
                        number 4
                      notename
                        B
                        accidental b
                        number 4
        '''

        testtree = self.l.parse(test).pretty()
        self.assertTrue(self.help.prettyTreeComp(testtree, accept), 'Basic Measure syntax parsed incorrectly')


    def test_repeat(self):
        test='''
        Compose {
            Repeat
            Tempo(72)
            Endr
        }
        '''
        accept = '''
        start
            compose
                composeitems
                    repeat
                        composeitems
                            tempo
                                number 72
        '''
        testtree = self.l.parse(test).pretty()
        self.assertTrue(self.help.prettyTreeComp(testtree, accept), 'Basic repeat tree incorrect')


    def test_repeatFail(self):
        test='''
        Compose {
            Repeat
            Tempo(72)
        }
        '''
        reject = '''
        start
            compose
                composeitems
                    repeat
                        composeitems
                            tempo
                                number 72
        '''
        # Lark throws an exception if the test string doesn't match the grammar.
        try:
            testtree = self.l.parse(test).pretty()
            testfail = False
        except LarkError as e:
            testfail = True
        self.assertTrue(testfail, 'Incorrect repeat structure accepted (no Endr)')


if __name__ == '__main__':
    unittest.main()

