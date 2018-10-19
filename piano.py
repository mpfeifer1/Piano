#!/usr/bin/env python3

# Import system libraries - TODO remove unnecessary ones
from lark import Lark
from mido import Message, MidiFile, MidiTrack
from argparse import ArgumentParser

import unittest
import lark
import sys

# Import our libraries
import grammar
import semantic
import ourtests
import flags
import midigenerator

# Get input flags
inputflags = flags.getcommandlineargs()

# Open the input file
with open(inputflags['piano_file'], 'r') as inputfile:
    data = inputfile.read()

# Build the parse tree using the grammar
parser = lark.Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")
tree = parser.parse(data)

# Debugging print statements
print(tree)
print()
print(tree.pretty())

# Convert the parse tree into a list of sound signals
analyzer = semantic.Semantic(tree)
signals = analyzer.analyze()

# Pass the sound signals to Mido, and build a MIDI file
generator = midigenerator.MidiGenerator(signals);
midifile = generator.generate()

