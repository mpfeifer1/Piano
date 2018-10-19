import unittest
import grammar
from testhelper import TestHelp

import lark
from lark import Tree
from lark import lexer
from lark import exceptions
Token = lexer.Token
LarkError = exceptions.LarkError


class TestGrammar(unittest.TestCase):

    def setUp(self):
        self.l = lark.Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")
        self.help = TestHelp()

    
    def test_variable(self):
        test = '''
        $gp = acousticgrandpiano
        compose{

        }
        '''
        accept = '''
        start
            id $gp
            compose
        '''
        res = self.l.parse(test).pretty()
        #TODO: Fix this test case
        #self.assertEqual(accept, res, 'Variable declaration not properly parsed')

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
        print(self.l.parse(test))
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

'''
    """
    Compose{
        // Nerd Nerd Nerd
        Tempo(60)
        Timesig(4/4)
    }
    """,



    """
    $gp = acousticgrandpiano
    Compose{
    }
    """,

    """
    compose {
        measure {

        }
    }
    """,


    """
    Compose {
        Measure {
        }
    }
    """

]

badstrs = [
    "INVALID%$&",
    "h#4",
    """
    nathan = a5
    """,
    """
    A
    """,
    """
    $    gp = acousticgrandpiano
    Compose{
    }
    """
]

def runtests():
    l = lark.Lark(grammar.getgrammar())

    print("~~~~~~~GOOD~~~~~~~~")
    for i in goodstrs:
        try:
            l.parse(i)
        except:
            print("INCORRECT - didn't accept", i)

    print()

    print("~~~~~~~BAD~~~~~~~~")
    for i in badstrs:
        try:
            l.parse(i)
            print("INCORRECT - accepted", i)
        except:
            pass
'''

if __name__ == '__main__':
    unittest.main()
