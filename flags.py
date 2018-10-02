
from argparse import ArgumentParser
import sys

# Take in compilation arguments
# Stuff like -o for output file name
parser = ArgumentParser(description='Compile a .pno file to a .midi file')
parser.add_argument('-o', nargs=1,  help='Choose a new file name')


output = parser.parse_args(sys.argv)
print(output)



