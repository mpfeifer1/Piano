import unittest
from testhelper import TestHelp
TestHelp().chwd()
from semanticanalyzer import Semantic
from lark import Tree
from lark import lexer

Token = lexer.Token

class TestSignalGen(unittest.TestCase):

    def setUp(self):
        self.help = TestHelp()
        self.semantic = Semantic(Tree('start', []))


    def test_measureSigGen(self):
        input_measure = Tree('measure', [])
        expected = [{'type':'measure','start':True},{'type':'measure','start':False}]
        signal = self.semantic.measure_to_signal(input_measure)
        self.assertEqual(expected, signal, "Measure signal not valid")

    def test_MismatchMeasureSigGen(self):
        input_measure = Tree('measure', [Tree('instrumentation', [Token('INSTRUMENT', 'acousticgrandpiano'), Tree('noteitem', [Tree('inlinedynamic', [Token('__ANON_5', 'ff')])])])])
        expected = [{'type':'measure','start':True},{'type':'measure','start':False}]
        signal = self.semantic.measure_to_signal(input_measure)
        self.assertNotEqual(expected, signal, "Measure signal valid when it shouldn't be")


    def test_veryComplexMeasure(self):
        very_Complex_Input = Tree('measure', [Tree('instrumentation', [Token('INSTRUMENT', 'acousticgrandpiano'), Tree('noteitem', [Tree('note', [Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_0', '2')])]), Tree('notename', [Token('__ANON_0', 'C'), Tree('number', [Token('__ANON_0', '4')])])])]), Tree('noteitem', [Tree('note', [Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_0', '4')])]), Token('REST', '--')])]), Tree('noteitem', [Tree('note', [Tree('division', [Tree('number', [Token('__ANON_0', '1')]), Tree('number', [Token('__ANON_0', '4')])]), Tree('chord', [Tree('notename', [Token('__ANON_0', 'C'), Tree('number', [Token('__ANON_0', '4')])]), Tree('notename', [Token('__ANON_0', 'E'), Tree('number', [Token('__ANON_0', '4')])]), Tree('notename', [Token('__ANON_0', 'G'), Tree('number', [Token('__ANON_0', '4')])])])])])])])

        expected = [{'type':'measure','start':True},
                    {'type':'instrument', 'name':'acousticgrandpiano'},
                    {'type':'note', 'note_name':'C4', 'length_num':1, 'length_denom':2},
                    {'type':'rest', 'length_num':1, 'length_denom':4},
                    {'type':'chord', 'notes':['C4','E4','G4'], 'length_num':1, 'length_denom':4},
                    {'type':'measure','start':False}]

        signal = self.semantic.measure_to_signal(very_Complex_Input)
        self.assertEqual(expected, signal, "Very complex measure signal not valid")

    def test_instrumentationSigGen(self):
        input_instrumentation = Tree('instrumentation', [Token('INSTRUMENT', 'trumpet')])
        expected = [{'type':'instrument', 'name':'trumpet'}]
        signal = self.semantic.instrumentation_to_signal(input_instrumentation)
        self.assertEqual(expected, signal, "Instrumentation signal not valid")

    def test_noteitemSigGen(self):
        noteitem = Tree('noteitem', [Tree('note', [Tree('division', [Tree('number', [Token('__ANON_3', '1')]), Tree('number', [Token('__ANON_3', '2')])]), Tree('notename', [Token('__ANON_2', 'C'), Tree('number', [Token('__ANON_3', '4')])])])])
        expected = [{'type':'note', 'length_num':1, 'length_denom':2, 'note_name':'C4'}]
        signal = self.semantic.noteitem_to_signal(noteitem)

        self.assertEqual(expected, signal, "Noteitem signal not valid")

    def test_noteSigGen(self):
        input_note = Tree('note', [Tree('division', [Tree('number', [Token('__ANON_3', '1')]), Tree('number', [Token('__ANON_3', '2')])]), Tree('notename', [Token('__ANON_2', 'C'), Tree('number', [Token('__ANON_3', '4')])])])
        expected = [{'type':'note', 'length_num':1, 'length_denom':2, 'note_name':'C4'}]
        signal = self.semantic.note_to_signal(input_note)
        self.assertEqual(expected, signal, "Note (note) signal not valid")

    def test_MismatchNoteSigGen(self):
        input_note = Tree('note', [Tree('division', [Tree('number', [Token('__ANON_3', '1')]), Tree('number', [Token('__ANON_3', '4')])]), Tree('notename', [Token('__ANON_2', 'C'), Tree('number', [Token('__ANON_3', '4')])])])
        expected = [{'type':'note', 'length_num':1, 'length_denom':2, 'note_name':'C4'}]
        signal = self.semantic.note_to_signal(input_note)
        self.assertNotEqual(expected, signal, "Note (note) signal valid when it shouldn't be")

    def test_restSigGen(self):
        input_rest= Tree('note', [ Tree('division', [ Tree('number', [ Token('__ANON_3', '1') ]),  Tree('number', [ Token('__ANON_3', '2') ]) ]),  Token('REST', '--') ])
        expected = [{'type':'rest','length_num':1, 'length_denom':2}]
        signal = self.semantic.note_to_signal(input_rest)
        self.assertEqual(expected, signal, "Note (rest) signal not valid")

    def test_notenameCollection(self):
        input_notename = Tree('notename', [Token('__ANON_0', 'A'),  Tree('number', [Token('__ANON_1', '4')])])
        expected = "A4"
        signal = self.semantic.collect_notename(input_notename)
        self.assertEqual(expected, signal, "Collected notename not valid")

    def test_inlineDynamicSigGen(self):
        input_dynamic = Tree('inlinedynamic', [Token('__ANON_0', 'mp')])
        expected = [{'type':'dynamic', 'volume':'mp'}]
        signal = self.semantic.inlinedynamic_to_signal(input_dynamic)
        self.assertEqual(expected, signal, "Inline dynamic signal not valid.")

    def test_chordSigGen(self):
        input_chord = Tree('chord', [Tree('notename', [Token('__ANON_2', 'C'), Tree('number', [Token('__ANON_3', '4')])]), Tree('notename', [Token('__ANON_1', 'E'), Tree('number', [Token('__ANON_3', '4')])]), Tree('notename', [Token('__ANON_1', 'G'), Tree('number', [Token('__ANON_3', '4')])])])
        expected = ['C4', 'E4', 'G4']
        signal = self.semantic.chord_to_signal(input_chord)
        self.assertEqual(expected, signal, "Chord signal not valid")


if __name__ == '__main__':
    unittest.main()
