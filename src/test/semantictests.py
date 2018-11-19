import unittest
from testhelper import TestHelp
TestHelp().chwd()
from semanticanalyzer import Semantic
from lark import Tree
from lark import lexer

Token = lexer.Token

class TestSemantics(unittest.TestCase):

    def setUp(self):
        self.help = TestHelp()
        self.semantic = Semantic(Tree('start', []))


    def test_validDivision(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertTrue(self.semantic.is_valid_division(division), 'Valid Division found invalid')

    def test_invalidDivisionNoDivision(self):
        division = [Tree('number', [])]
        self.assertFalse(self.semantic.is_valid_division(division), 'Invalid division, no division found ')

    def test_invalidDivisionNoNumberOnLeft(self):
        division = Tree('division', [Tree('division', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertFalse(self.semantic.is_valid_division(division), 'Invalid division, no number on left')

    def test_invalidDivisionNoNumberOnRight(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('division', [Token('__ANON_1', '4')])])
        self.assertFalse(self.semantic.is_valid_division(division), 'Invalid division, no number on right')

    def test_invalidDivisionNumerator(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '-1')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertFalse(self.semantic.is_valid_division(division), 'Invalid numerator')

    def test_invalidDivisionDenominator(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '5')])])
        self.assertFalse(self.semantic.is_valid_division(division), 'Invalid denominator')

    def test_validNoteName(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'),  Tree('number', [Token('__ANON_1', '4')])])
        self.assertTrue(self.semantic.is_valid_notename(notename), 'Valid notename found invalid')

    def test_validNoteNameAccidental(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'), Tree('accidental', [Token('__ANON_1', '#')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertTrue(self.semantic.is_valid_notename(notename), 'Valid notename found invalid')

    def test_invalidNoteName(self):
        notename = Tree('notename', [Token('__ANON_0', 'H'),  Tree('number', [Token('__ANON_1', '4')])])
        self.assertFalse(self.semantic.is_valid_notename(notename), 'Invalid notename letter')

    def test_invalidNoteNameAccidental(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'), Tree('accidental', [Token('__ANON_1', '@')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertFalse(self.semantic.is_valid_notename(notename), 'Invalid accidental found')

    def test_invalidNoteNameAccidentalLength(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'), Tree('accidental', [Token('__ANON_1', '@')])])
        self.assertFalse(self.semantic.is_valid_notename(notename), 'Invalid number of args after accidental')

    def test_validNoteItem(self):
        noteitem = Tree('noteitem', [Tree('note', [Tree('division', [Tree('number', [Token('__ANON_3', '1')]), Tree('number', [Token('__ANON_3', '2')])]), Tree('notename', [Token('__ANON_2', 'C'), Tree('number', [Token('__ANON_3', '4')])])])])
        self.assertTrue(self.semantic.is_valid_noteitem(noteitem), 'Valid noteitem found invalid')

    def test_validInlineDynamic(self):
        dynamic = Tree('inlinedynamic', [Token('__ANON_0', 'MP')])
        self.assertTrue(self.semantic.is_valid_inlinedynamic(dynamic), 'Valid inline dynamic found invalid')

    def test_invalidInlineDynamic(self):
        dynamic = Tree('inlinedynamic', [Token('__ANON_0', 'mpp')])
        self.assertFalse(self.semantic.is_valid_inlinedynamic(dynamic), 'Invalid inline dynamic found valid')

    def test_validDynamic(self):
        dynamic = Tree('dynamic', [Tree('inlinedynamic', [Token('__ANON_0', 'fff')])])
        self.assertTrue(self.semantic.is_valid_dynamic(dynamic), 'Valid dynamic found invalid')

    def test_invalidDynamic(self):
        dynamic = Tree('dynamic', [Tree('number', [Token('__ANON_0', 'fff')])])
        self.assertFalse(self.semantic.is_valid_dynamic(dynamic), 'Invalid dynamic found valid')

    def test_validId(self):
        iden = Tree('id', [Token('__ANON_0', '$tpt_in-out')])
        self.assertTrue(self.semantic.is_valid_identifier(iden), 'Valid identifier found invalid')

    def test_invalidIdNoStart(self):
        iden = Tree('id', [Token('__ANON_0', 'tpt')])
        self.assertFalse(self.semantic.is_valid_identifier(iden), 'Invalid identifier no $ at start found valid')

    def test_invalidIdBadSymbol(self):
        iden = Tree('id', [Token('__ANON_0', '$tp$t')])
        self.assertFalse(self.semantic.is_valid_identifier(iden), 'Invalid identifier bad symbol found valid')


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

    '''
    def test_validInstrumentation(self):
        div = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '4')])])
        notename = Tree('notename', [Token('__ANON_2', 'B'), \
                   Tree('accidental', [Token('__anon_3', 'b')]), Tree('number', [Token('__ANON_1', '4')])])
        note = Tree('note', [div, notename])
        tree = Tree('instrumentation', [Token('INSTRUMENT', 'acousticgrandpiano'), note])
        self.assertTrue(self.semantic.is_valid_instrumentation(tree), 'Valid instrumentation tree found invalid')
    '''
    '''
    def test_validNoteitem(self):
        tree1 = Tree('noteitem', [ Tree('note', [ Tree('division', [ Tree('number', [ Token('__ANON_3', '1') ]),  Tree('number', [ Token('__ANON_3', '4') ]) ]),  Tree('notename', [ Token('__ANON_1', 'A'),  Tree('accidental', [ Token('__ANON_0', 'b') ]),  Tree('number', [ Token('__ANON_3', '5') ]) ]) ]) ])
        tree2 = Tree('noteitem', [ Tree('note', [ Tree('division', [ Tree('number', [ Token('__ANON_3', '1') ]),  Tree('number', [ Token('__ANON_3', '2') ]) ]),  Token('REST', '--') ]) ])
        tree3 = Tree('noteitem', [ Tree('inlinedynamic', [ Token('__ANON_5', 'mf') ]) ])
        self.assertTrue(self.semantic.is_valid_noteitem(tree1), 'Valid noteitem tree with note found inalid')
        self.assertTrue(self.semantic.is_valid_noteitem(tree2), 'Valid noteitem tree with rest found inalid')
        self.assertTrue(self.semantic.is_valid_noteitem(tree3), 'Valid noteitem tree with dynamic found inalid')
    '''
    def test_validMeasure(self):
        tree = Tree('measure', [])
        self.assertTrue(self.semantic.is_valid_measure(tree), 'Valid measure found invalid')

    def test_invalidMeasure(self):
        tree = Tree('compose', [])
        self.assertFalse(self.semantic.is_valid_measure(tree), 'Valid measure found invalid')

    def test_validMeasureWithInstrumentation(self):
        tree = Tree('measure', [Tree('instrumentation', [Token('INSTRUMENT', 'trumpet')])])
        self.assertTrue(self.semantic.is_valid_measure(tree), 'Valid measure found invalid')
        pass

if __name__ == '__main__':
    unittest.main()

