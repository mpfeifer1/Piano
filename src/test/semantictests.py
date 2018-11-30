import unittest
from lark import Tree
from lark import lexer

from testhelper import TestHelp
TestHelp().chwd()

import exceptions
from semanticanalyzer import Semantic

Token = lexer.Token

class TestSemantics(unittest.TestCase):

    def setUp(self):
        self.help = TestHelp()
        self.semantic = Semantic(Tree('start', []))


    def test_validDivision(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '4')])])
        flag = True
        res = True
        try:
            res = self.semantic.is_valid_division(division)
        except:
            flag = False
        self.assertTrue(res, 'Valid Division found invalid')
        self.assertTrue(flag, 'Valid Division threw exception')

    def test_invalidDivisionNoDivision(self):
        division = [Tree('number', [])]
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_division, division)

    def test_invalidDivisionNoNumberOnLeft(self):
        division = Tree('division', [Tree('division', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_division, division)

    def test_invalidDivisionNoNumberOnRight(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('division', [Token('__ANON_1', '4')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_division, division)

    def test_invalidDivisionNumerator(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '-1')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_division, division)

    def test_invalidDivisionDenominator(self):
        division = Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_1', '5')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_division, division)

    def test_validNoteName(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'),  Tree('number', [Token('__ANON_1', '4')])])
        self.assertTrue(self.semantic.is_valid_notename(notename))

    def test_validNoteNameAccidental(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'), Tree('accidental', [Token('__ANON_1', '#')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertTrue(self.semantic.is_valid_notename(notename))

    def test_invalidNoteName(self):
        notename = Tree('notename', [Token('__ANON_0', 'H'),  Tree('number', [Token('__ANON_1', '4')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_notename, notename)

    def test_invalidNoteNameAccidental(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'), Tree('accidental', [Token('__ANON_1', '@')]), Tree('number', [Token('__ANON_1', '4')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_notename, notename)

    def test_invalidNoteNameAccidentalLength(self):
        notename = Tree('notename', [Token('__ANON_0', 'C'), Tree('accidental', [Token('__ANON_1', '@')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_notename, notename)

    def test_validNoteItem(self):
        noteitem = Tree('noteitem', [Tree('note', [Tree('division', [Tree('number', [Token('__ANON_3', '1')]), Tree('number', [Token('__ANON_3', '2')])]), Tree('notename', [Token('__ANON_2', 'C'), Tree('number', [Token('__ANON_3', '4')])])])])
        self.assertTrue(self.semantic.is_valid_noteitem(noteitem))

    def test_validInlineDynamic(self):
        dynamic = Tree('inlinedynamic', [Token('__ANON_0', 'MP')])
        self.assertTrue(self.semantic.is_valid_inlinedynamic(dynamic))

    def test_invalidInlineDynamic(self):
        dynamic = Tree('inlinedynamic', [Token('__ANON_0', 'mpp')])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_inlinedynamic, dynamic)

    def test_validDynamic(self):
        dynamic = Tree('dynamic', [Tree('inlinedynamic', [Token('__ANON_0', 'fff')])])
        self.assertTrue(self.semantic.is_valid_dynamic(dynamic), 'Valid dynamic found invalid')

    def test_invalidDynamic(self):
        dynamic = Tree('dynamic', [Tree('number', [Token('__ANON_0', 'fff')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_dynamic, dynamic)

    def test_validId(self):
        iden = Tree('id', [Token('__ANON_0', '$tpt_in-out')])
        self.assertTrue(self.semantic.is_valid_identifier(iden), 'Valid identifier found invalid')

    def test_invalidIdNoStart(self):
        iden = Tree('id', [Token('__ANON_0', 'tpt')])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_identifier, iden)

    def test_invalidIdBadSymbol(self):
        iden = Tree('id', [Token('__ANON_0', '$tp$t')])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_identifier, iden)


    def test_validTree(self):
        tree = Tree('start', [Tree('compose', [])])
        self.assertTrue(self.semantic.is_valid_tree(tree), 'Valid Tree found invalid')


    def test_invalidTreeNoCompose(self):
        tree = Tree('start', [Tree('id', [Token('__ANON_0', '$gp')]), Tree('rhs', [Token('__ANON_1', 'acousticgrandpiano')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_tree, tree)

    def test_invalidTreeNoStart(self):
        tree = Tree('compose', [])
        self.assertFalse(self.semantic.is_valid_tree(tree))

    def test_invalidTreeIdNoRHS(self):
        tree = Tree('start', [Tree('id', Token('__ANON_0', '$gp')), Tree('compose', [Token('__ANON_1', 'acousticgrandpiano')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_tree, tree)

    def test_invalidTreeRHSNoId(self):
        tree = Tree('start', [Tree('rhs', Token('__ANON_0', 'acousticgrandpiano')), Tree('compose', [Token('__ANON_1', 'acousticgrandpiano')])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_tree, tree)

    def test_instrumentationInvalidChild(self):
        tree = Tree('instrumentation', [Tree('trumpet', [])])
        self.assertRaises(exceptions.SemanticError, self.semantic.is_valid_instrumentation, tree)

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
        self.assertFalse(self.semantic.is_valid_measure(tree))

    def test_validMeasureWithInstrumentation(self):
        tree = Tree('measure', [Tree('instrumentation', [Token('INSTRUMENT', 'trumpet')])])
        self.assertTrue(self.semantic.is_valid_measure(tree), 'Valid measure found invalid')
        pass

    def test_variableInstrument(self):
        lhs = Token('__ANON_9', '$tpt')
        rhs = Tree('rhs', [Token('INSTRUMENT', 'trumpet')])
        expected = {'$tpt': Token('INSTRUMENT', 'trumpet')}
        self.semantic.set_variable(lhs, rhs)

        self.assertEqual(expected, self.semantic.variables, "Instrument variables not set correctly!")

    def test_variableMeasure(self):
        lhs = Token('__ANON_9', '$testMeasure')
        rhs = Tree('rhs', [Tree('measure', [Tree('instrumentation', [Token('INSTRUMENT', 'trumpet')])])])
        expected = {'$testMeasure': Tree('measure', [Tree('instrumentation', [Token('INSTRUMENT', 'trumpet')])])}
        self.semantic.set_variable(lhs, rhs)

        self.assertEqual(expected, self.semantic.variables, "Measure variables not set correctly!")


if __name__ == '__main__':
    unittest.main()

