
from argparse import ArgumentParser
import argparse
import sys

def pno_type(path):
    if not path.endswith('.pno'):
         raise argparse.ArgumentTypeError('A .pno file is required for input')
    return path

def midi_type(path):
    if not path.endswith('.midi') and not path.endswith('.mid'):
        raise argparse.ArgumentTypeError('A .midi or .mid file is required for the output name')
    return path

# Take in compilation arguments
# Stuff like -o for output file name
parser = ArgumentParser(description='Compile a .pno file to a .midi file')


#parser.add_argument("python",  nargs=1, help='A .py file is needed for input')
parser.add_argument('midi_out', type=midi_type, help='A .midi or .mid file is needed for output')
parser.add_argument('pno_in', type=pno_type, help='A .pno file is needed for input')


args = parser.parse_args()

#if len(sys.argv) != 3:
#    print('usage: flags.py out.midi in.pno\n')

midi_file = args.midi_out
piano_file = args.pno_in



print("------------------")
print "Midi file output: ", midi_file
print "Piano file input: ", piano_file
print("------------------")


