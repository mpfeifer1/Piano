import unittest
import grammar
from testhelper import TestHelp

import lark
from lark import Tree
from lark import lexer

Token = lexer.Token


class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.l = lark.Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")


    def test_comment(self):
        ''' Arrange '''
        test = """
        Compose{
            // Nathan is a nerd
        }
        """
        expected = Tree('start', [Tree('compose', [])])

        ''' Act '''
        actual = self.l.parse(test)
        #print(actual)

        ''' Assert '''
        self.assertEqual(actual, expected, 'Comments not parsed correctly')


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
        
        x = TestHelp()
        res = x.prettyTreeComp(testtree, accept)
        
        self.assertTrue(res, 'Basic Measure syntax parsed incorrectly')

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
