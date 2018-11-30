from testhelper import TestHelp
TestHelp().chwd()

import unittest
import midigenerator

class TestGeneration(unittest.TestCase):

    def setUp(self):
        self.generator = midigenerator.MidiGenerator([])

    def test_validateEmptySignals(self):
        signals = []
        self.assertTrue(self.generator.validate(signals), 'Valid signal list found invalid')

    def test_validateFirstSignalEmpty(self):
        signals = [dict()]
        self.assertFalse(self.generator.validate(signals), 'Invalid signal list found valid')

    def test_validateProperSignal(self):
        signals = [{"type":"measure", 'start':True}]
        self.assertTrue(self.generator.validate(signals), 'Valid signal list found invalid')
        signals = [{"type":"note", "note_name":"C4", "length_denom":1, "length_num":1}]
        self.assertTrue(self.generator.validate(signals), 'Valid signal list found invalid')

    def test_validateWrongNumberFields(self):
        signals = [{"type":"dynamic"}]
        self.assertFalse(self.generator.validate(signals), 'Invalid signal list found valid')

    def test_validateSignalWrongFields(self):
        signals = [{"type":"dynamic", "BADFIELD":"data"}]
        self.assertFalse(self.generator.validate(signals), 'Invalid signal list found valid')

if __name__ == '__main__':
    unittest.main()

