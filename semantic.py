#in this file, we may want a global state object
# That, or make this a class like normal people

def analyze(tree):
    # so basically here, we're gonna wanna loop through
    # every command in the program, check if it's valid
    # and do it.
    # we gonna need to keep track of variables defined and stuff
    # it should return nice errors, yeah
    # this should keep track of global time, and send that in
    # to each measure
    pass

# check that all the numbers are powers of 2 and nonzero
def is_valid_division(tree):
    pass

# check the name exists in our program
def is_valid_identifier(tree):
    pass

# Check if it has a 'start', and one compose
def is_valid_program(tree):
    pass

# Takes in a measure, builds a list of signals
def measure_to_signal(tree, time):
    pass

def chord_to_signal(tree, time):
    pass

def tuple_to_signal(tree, time):
    pass

def note_to_signal(tree, time):
    pass

# given a tree that represents a dynamic, set the new volume
def apply_dynamic(tree):
    pass

# returns a new tree without the base repeat
def expand_repeat(tree):
    pass

# given a tree that represents a tempo, set that new tempo
def apply_tempo(tree):
    pass

# given a tree that represents a time signature, set the timesig
def apply_timesig(tree):
    pass

