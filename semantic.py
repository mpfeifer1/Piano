from instrumentToNumber import instrumentToNumber

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
            self.throw()

        # Split up the tree into a list of commands
        commands = self.split_into_commands(self.tree)

        # Process each command in the language
        for command in commands:
            # If it's an assignment, do that
            if command[0] == 'assignment':
                self.set_variable(command[1], command[2], self.variables)
            # If it's a compose, do that
            if command[0] == 'compose':
                signals = self.process_compose(command[1])

        return signals

    # Take in a list of trees with composeitems at their root
    # return a list of signals
    def process_compose(self, trees):
        # Define the signals
        signals = []

        # For each tree, add its signals to the list
        for tree in trees:
            signals += self.process_composeitems(tree)

        return signals

    # Take in a list of trees with a single composeitem
    # return a list of signals
    def process_composeitems(self, tree):
        # Strip out the 'composeitems' tree
        tree = tree.children[0]

        # Define the list of signals
        signals = []

        # Tempo
        if tree.data == 'tempo':
            if self.is_valid_tempo(tree):
                self.apply_tempo(tree)

        # Timesig
        if tree.data == 'timesig':
            if self.is_valid_timesig(tree):
                self.apply_timesig(tree)

        # Dynamic
        if tree.data == 'dynamic':
            if self.is_valid_dynamic(tree):
                self.apply_dynamic(tree)

        # Measure
        if tree.data == 'measure':
            if self.is_valid_measure(tree):
                signals += self.measure_to_signal(tree)

        # Repeat
        if tree.data == 'repeat':
            if self.is_valid_repeat(tree):
                tree = self.expand_repeat(tree)
                signals += self.process_composeitems(tree)

        print(tree)
        print()
        return signals



    # Take the tree, and split it up into a list of commands
    def split_into_commands(self, tree):
        commands = []
        # For each child
        for i in self.tree.children:
            # If it's an identifier, add a new command, add the lhs to it
            if i.data == 'id':
                commands.append(['assignment'])
                commands[-1].append(i.children[0])
            # If it's a rhs, there must already be a command, attach this to it
            if i.data == 'rhs':
                commands[-1].append(i.children[0])
            # Otherwise, if it's a compose, add this to the list of commands
            if i.data == 'compose':
                commands.append(['compose'])
                commands[-1].append(i.children)

        return commands

    # Check that the data has a start symbol
    def is_valid_tree(self, tree):
        return tree.data == 'start'

    # check that the measure is valid
    def is_valid_repeat(self, tree):
        pass

    # check that the measure is valid
    def is_valid_measure(self, tree):
        pass

    # check that the tempo is valid
    def is_valid_tempo(self, tree):
        pass

    def is_valid_timesig(self, tree):
        pass

    def is_valid_dynamic(self, tree):
        pass

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
    def measure_to_signal(self, tree):
        if tree.data != 'measure':
            print('error: not a measure')
            return False
        for i in tree.children:
            if i.data == 'instrumentation':
                self.instrumentation_to_signal(i)

    def instrumentation_to_signal(self, tree):
        if tree.data != 'instrumentation':
            print('error: not an instrumentation')
            return False
        print('\ninstrumentation: ' + tree.children[0])
        if instrumentToNumber.__contains__(tree.children[0]):
            for i in tree.children[1:]:
                self.noteitem_to_signal(i)
        else:
            print('invalid instrument')

    def noteitem_to_signal(self,tree):
        if tree.data != 'noteitem':
            print('error: invalid noteitem')
        
        for i in tree.children:
            if i.data == 'note':
                self.note_to_signal(i)
            elif i.data == 'inlinedynamic':
                self.inlinedynmaic_to_signal(i)
            else:
                print('invalid noteitem child')
    
    def note_to_signal(self, tree):
        pass

    def inlinedynmaic_to_signal(self, tree):
        pass
        
    def chord_to_signal(self, tree):
        pass

    def tuple_to_signal(self, tree):
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

    def throw(self):
        # TODO find a way to throw an exception here
        pass
