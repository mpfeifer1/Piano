#!/usr/bin/env python3.5

# Import system libraries - TODO remove unnecessary ones
from lark import Lark
from argparse import ArgumentParser


# Import our libraries
from core import grammar
from core import semanticanalyzer as semantic
from core import flags

# Get input flags
inputflags = flags.getcommandlineargs()

# Open the input file
with open(inputflags['piano_file'], 'r') as inputfile:
    data = inputfile.read()
try:
    # Build the parse tree using the grammar
    parser = Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")
    tree = parser.parse(data)

    # Debugging print statements
    print(tree.pretty())

    # Convert the parse tree into a list of sound signals
    analyzer = semantic.Semantic(tree)
    signals = analyzer.analyze()

    # Pass the sound signals to Mido, and build a MIDI file
    generator = midigenerator.MidiGenerator(signals)
    midifile = generator.generate()
except Exception as e:
    print(e)
