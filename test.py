from mido import Message, MidiFile, MidiTrack
from lark import Lark
from argparse import ArgumentParser
import unittest
import sys

# Take in compilation arguments
# Stuff like -o for output file name
parser = ArgumentParser(description='Compile a .pno file to a .midi file')
parser.add_argument('-o', nargs=1,  help='Choose a new file name')

thing = parser.parse_args(sys.argv)
print(thing)

# Build Midi file and tracks
mid = MidiFile()
track1 = MidiTrack()
track2 = MidiTrack()
track3 = MidiTrack()
track4 = MidiTrack()
mid.tracks.append(track1)
mid.tracks.append(track2)
mid.tracks.append(track3)
mid.tracks.append(track4)

#track.append(Message('program_change', program=12, time=0))

# Add notes to tracks
track1.append(Message('note_on', note=64, velocity=64, time=0))
track1.append(Message('note_off', note=64, velocity=64, time=1024))
track2.append(Message('note_on', note=68, velocity=64, time=128))
track2.append(Message('note_off', note=68, velocity=64, time=1024))
track3.append(Message('note_on', note=71, velocity=64, time=256))
track3.append(Message('note_off', note=71, velocity=64, time=1024))
track4.append(Message('note_on', note=76, velocity=64, time=384))
track4.append(Message('note_off', note=76, velocity=64, time=1024))

# Try a sample grammar recognition
l = Lark('''start: WORD "," WORD "!"
            %import common.WORD
            %ignore " "
         ''')
print(l.parse("Hello, World!").pretty())


# Sample output
print(mid.length)
mid.save('song.midi')
