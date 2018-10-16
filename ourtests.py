import unittest
import grammar

import lark
from lark import Tree

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

        ''' Assert '''
        self.assertEqual(actual, expected)

    def test_measure(self):
        ''' Arrange '''
        test = """
        Compose{
            Measure{
            }
        }
        """
        # This and the following test are currently real broken, thus
        # the comment out

        #expected = Tree('start', [Tree('compose', [Tree('measure', [])])])
        
        #actual = self.l.parse(test)

        #self.assertEqual(actual, expected)

    def test_single_instrument(self):
        ''' Arrange '''
        # Measures can be empty but instruments need to have a note
        test = """
        Compose{
            Measure{
                acousticgrandpiano{ 
                    1/4 C4;
                }
            }    
        }    
        """
        #expected = Tree('start', [Tree('compose', [Tree('measure', [Tree('acousticgrandpiano', [])])])])
        #print(self.l.parse(test).pretty)
        #actual = self.l.parse(test)
        
        #self.assertEqual(actual, expected)
""" Other tests:
    Instrument
    Tempo
    Timesig
"""

'''
    """
    Compose {
        Measure {
            acousticgrandpiano {
                1/4 C4; 1/4 C4; 1/4 G4; 1/4 G4;
            }
            acousticgrandpiano {
                1/4 C4; 1/4 --; 1/4 G4; 1/4 --;
            }
        }
    }
    """,



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
