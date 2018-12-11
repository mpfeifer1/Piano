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

    # Create a text file of the grammar tree if the -t flag is set
    if inputflags['tree_file']:
        out_tree = open('tree.txt', 'w')
        out_tree.write(tree.pretty())
        out_tree.close()

    # Convert the parse tree into a list of sound signals
    analyzer = semantic.Semantic(tree)
    signals = analyzer.analyze()

    # Create a text file of the signals if the -s flag is set
    if inputflags['signal_file']:
        out_sig = open('signal.sig', 'w')
        pretty_sig = '\n'.join(str(i) for i in signals)
        out_sig.write(pretty_sig)
        out_sig.close()

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
