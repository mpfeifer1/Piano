#!/usr/bin/env python3

# Import system libraries
from lark import Lark
from lark import exceptions as larkexcept
from argparse import ArgumentParser

# Import Piano libraries
from core import grammar
from core import semanticanalyzer as semantic
from core import midigenerator
from core import exceptions
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
    midi_name = inputflags['midi_file']

    midifile.save(midi_name)

#except larkexcept.LarkError as le:
#    print('Encountered error during syntax analysis and tokenizing:')
#    print(le)
#except exceptions.SemanticError as se:
#    print('Encountered error during semantic analysis:')
#    print(se)
#except exceptions.MidiError as me:
#    print('Encountered error during midi generation:')
#    print(me)
#except exceptions.PianoException as pe:
#    print('Unknown Piano error ocurred during compilation:')
#    print(pe)

except Exception as e:
    print('Unknown error ocurred during compilation:')
    print(e)
