class Semantic:
    # Take in the tree from the user
    def __init__(self, tree):
        # Save the tree the user passed in
        self.tree = tree

        # Keep track of current 'state' of song
        self.dynamic = 'mf'
        self.tempo = 120
        self.timesig = (4,4)
        self.timestamp = 0
        self.variables = {}

    # Take the tree, and convert it into a list of signals
    def analyze(self):
        # so basically here, we're gonna wanna loop through
        # every command in the program, check if it's valid
        # and do it.
        # we gonna need to keep track of variables defined and stuff
        # it should return nice errors, yeah
        # this should keep track of global time, and send that in
        # to each measure

        # Check that the tree is valid
        if not self.is_valid_tree(self.tree):
            throw()

        # Split up the tree into a list of commands
        commands = self.split_into_commands(self.tree)

        # Process each command in the language
        for command in commands:
            # If it's an assignment, do that
            if command[0] == 'assignment':
                self.set_variable(command[1], command[2], self.variables)
            # If it's a compose, do that
            if command[0] == 'compose':
                signals = self.processcompose(command[1])

        return signals

    # Take in a tree representing the compose to use,
    # return a list of signals
    def processcompose(self, tree):
        pass

    # Take the tree, and split it up into a list of commands
    def split_into_commands(self, tree):
        commands = []
        # For each child
        for i in self.tree.children:
            # If it's an identifier, add a new command, add the lhs to it
            if i.data == 'id':
                commands.append(['assignment'])
                commands[-1].append(i.children)
            # If it's a rhs, there must already be a command, attach this to it
            if i.data == 'rhs':
                commands[-1].append(i.children)
            # Otherwise, if it's a compose, add this to the list of commands
            if i.data == 'compose':
                commands.append(['compose'])
                commands[-1].append(i.children)

        return commands


    # Check that the data has a start symbol
    def is_valid_tree(self, tree):
        return tree.data == 'start'

    # check that all the numbers are powers of 2 and nonzero
    def is_valid_division(self, tree):
        pass

    # check the name exists in our program
    def is_valid_identifier(self, tree):
        pass

    # sets a variable in our memory to its tree
    def set_variable(self, lhs, rhs, variables):
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

    def throw():
        # TODO find a way to throw an exception here
        pass
