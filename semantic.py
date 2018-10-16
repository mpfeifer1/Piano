class Semantic:
    # Keep track of current 'state' of song
    self.dynamic = 'mf'
    self.tempo = 120
    self.timesig = (4,4)

    # Take in the tree from the user
    def __init__(self, tree):
        self.tree = tree

    # Take the tree, and convert it into a list of signals
    def analyze(self):
        # so basically here, we're gonna wanna loop through
        # every command in the program, check if it's valid
        # and do it.
        # we gonna need to keep track of variables defined and stuff
        # it should return nice errors, yeah
        # this should keep track of global time, and send that in
        # to each measure
        pass

    # check that all the numbers are powers of 2 and nonzero
    def is_valid_division(self, tree):
        pass

    # check the name exists in our program
    def is_valid_identifier(self, tree):
        pass

    # sets a variable in our memory to its tree
    def set_variable(self, tree):
        pass

    # Check if it has a 'start', and one compose
    def is_valid_program(self, tree):
        pass

    # Takes in a measure, builds a list of signals
    def measure_to_signal(self, tree, time):
        pass

    def chord_to_signal(self, tree, time):
        pass

    def tuple_to_signal(self, tree, time):
        pass

    def note_to_signal(self, tree, time):
        pass

    # given a tree that represents a dynamic, set the new volume
    def apply_dynamic(self, tree):
        pass

    # returns a new tree without the base repeat
    def expand_repeat(self, tree):
        pass

    # given a tree that represents a tempo, set that new tempo
    def apply_tempo(self, tree):
        pass

    # given a tree that represents a time signature, set the timesig
    def apply_timesig(self, tree):
        pass

