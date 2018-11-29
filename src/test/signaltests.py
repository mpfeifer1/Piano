import unittest
import lark
from lark import lexer

Token = lexer.Token

class TestSignalGeneration(unittest.TestCase):

    def setUp(self):
        self.l = lark.Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")
        self.measureTest = '''
        Compose {
            Measure {
                acousticgrandpiano {
                    1/2 C4; 1/2 --;
                }
                trumpet {
                    1/4 E4; 1/4 (C4 E4); 1/4 (E4 G4); fff; 1/4 tuplet(C4 D4 E4 F4 G4);
                }
            }
        }
        '''

        self.tree = self.l.parse(self.measureTest)
        self.testMeasure = self.tree.children[0].children[0].children[0]

        self.semantic = Semantic(self.testMeasure)
        self.help = TestHelp()

    def test_measure_to_signal(self):
        self.semantic.measure_to_signal(self.testMeasure)



