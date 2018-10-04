from argparse import ArgumentParser
import argparse
import sys

#Define the needed file types
def pno_type(path):
    if not path.endswith('.pno'):
         raise argparse.ArgumentTypeError('A .pno file is required for input')
    return path

def midi_type(path):
    if not path.endswith('.midi') and not path.endswith('.mid'):
        raise argparse.ArgumentTypeError('A .midi or .mid file is required for the output name')
    return path

# Take in compilation arguments
parser = ArgumentParser(description='Compile a .pno file to a .midi file')
parser.add_argument('-p', type=pno_type, required=True, help='A .pno file is needed for input')
parser.add_argument('-o', default='song.midi', type=midi_type, help='A .midi or .mid file is optional for output')

args = parser.parse_args()

midi_file = args.o
piano_file = args.p


print('\n--- Outputting to a file called: ', midi_file, '---\n')

