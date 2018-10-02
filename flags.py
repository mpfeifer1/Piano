
from argparse import ArgumentParser
import sys

# Take in compilation arguments
# Stuff like -o for output file name
parser = ArgumentParser(description='Compile a .pno file to a .midi file')
#parser.add_argument('-o', nargs=1,  help='Choose a new file name')

#parser.add_argument('--version', help='Current Version of Piano 1.0.0')


#flags_file=sys.argv[0]
#midi_file=sys.argv[2]
#piano_file=sys.argv[3]


#python flags.py out.mid sample.pno
#print "# of args: ", len(sys.argv[1])
#print "Flags python File: ", flags_file 
#print "-o input: ", sys.argv[1]
#print "Midi File: ", midi_file 
#print "Piano File: ", piano_file

#flags_file=sys.argv[0]
#midi_file=sys.argv[2]
#piano_file=sys.argv[3]




parser.add_argument("python",  nargs=1, help='A .py file is needed for input')
parser.add_argument("midi",  nargs=1, help='A .midi or .mid file is needed for input')
parser.add_argument("piano",  nargs=1, help='A .pno file is needed for input')




args = parser.parse_args(sys.argv)


print("------------------")
print(args.python[0])
print(args.midi[0])
print(args.piano[0])
if args.piano[0] == "sample.pno":
    print("I DID IT")
else:
    print("Did not get correct name")
#if '.pno' in args.piano[0]:
if  args.piano[0].endswith('.pno'):
    print("YAY PART 2") 



print("*******************")
#args = parser.parse_args(sys.argv)
print(args)


