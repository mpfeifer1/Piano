'''
This file handles the flags and command line arguments.
'''

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

def getcommandlineargs():
    # Take in compilation arguments
    parser = ArgumentParser(description='Compile a .pno file to a .midi file')
    parser.add_argument('-p', type=pno_type, required=True, help='A .pno file is needed for input')
    parser.add_argument('-o', default='song.midi', type=midi_type, help='A .midi or .mid file is optional for output')
    parser.add_argument('-t', action='store_true', help='An optional flag for creating a .txt file of the grammar tree')
    parser.add_argument('-s', action='store_true', help='An optional flag for creating a .sig (text) file of the generated signals')
    args = parser.parse_args()

    midi_file = args.o
    piano_file = args.p
    tree_file = args.t
    signal_file = args.s

    returnvals = {'midi_file': midi_file, 'piano_file': piano_file, 'tree_file': tree_file, 'signal_file': signal_file}

    return returnvals
