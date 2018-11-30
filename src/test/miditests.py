from testhelper import TestHelp
import unittest

TestHelp().chwd()

import exceptions
import midigenerator

class TestGeneration(unittest.TestCase):

    def setUp(self):
        self.generator = midigenerator.MidiGenerator([])

    def test_validateEmptySignals(self):
        signals = []
        self.assertTrue(self.generator.validate(signals), 'Valid signal list found invalid')

    def test_validateFirstSignalEmpty(self):
        signals = [dict()]
        self.assertRaises(SignalError, self.generator.validate, signals)

    def test_validateProperSignal(self):
        signals = [{"type":"measure"}]
        self.assertTrue(self.generator.validate(signals), 'Valid signal list found invalid')
        signals = [{"type":"note", "notename":"C4", "length_denom":1, "length_num":1}]
        self.assertTrue(self.generator.validate(signals), 'Valid signal list found invalid')

    def test_validateWrongNumberFields(self):
        signals = [{"type":"dynamic"}]
        self.assertRaises(SignalError, self.generator.validate, signals)
        pass

    def test_validateSignalWrongFields(self):
        signals = [{"type":"dynamic", "BADFIELD":"data"}]
        self.assertRaises(SignalError, self.generator.validate, signals)
        pass

if __name__ == '__main__':
    unittest.main()

