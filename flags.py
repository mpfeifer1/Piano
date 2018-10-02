
from argparse import ArgumentParser
import sys

# Take in compilation arguments
# Stuff like -o for output file name
parser = ArgumentParser(description='Compile a .pno file to a .midi file')


parser.add_argument("python",  nargs=1, help='A .py file is needed for input')
parser.add_argument("midi",  nargs=1, help='A .midi or .mid file is needed for input')
parser.add_argument("piano",  nargs=1, help='A .pno file is needed for input')



args = parser.parse_args(sys.argv)


print("------------------")
print(args.python[0])
print(args.midi[0])
print(args.piano[0])
#if args.piano[0] == "sample.pno":
#    print("I DID IT")
#else:
#    print("Did not get correct name")
if  args.piano[0].endswith('.pno'):
    print("YAY PART 2") 
else:
    print("Incorrect file type.  Requires .pno file")


print("*******************")


