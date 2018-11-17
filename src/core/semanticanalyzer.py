import lark

class Semantic:
    # Take in the tree from the user
    def __init__(self, tree):
        # Save the tree the user passed in
        self.tree = tree

        # Keep track of current 'state' of song
        self.variables = {}

        self.treetype = type(lark.tree.Tree('data', ['children']))

        # Build all of the valid dynamic levels
        self.valid_levels = ["mp", "mf"]
        soft = ""
        loud = ""
        for i in range(4):
            soft = soft + "p"
            loud = loud + "f"
            self.valid_levels.append(loud)
            self.valid_levels.append(soft)


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

        # Grab the initial signals
        signals = self.get_default_signals()

        # Process each command in the language
        for command in commands:
            # If it's an assignment, do that
            if command[0] == 'assignment':
                self.set_variable(command[1], command[2], self.variables)
            # If it's a compose, do that
            if command[0] == 'compose':
                signals += self.process_compose(command[1])

        return signals

    # Return a list of signals with all the default settings
    def get_default_signals(self):
        signals = []
        # send default instrument
        # " tempo
        # " timesig
        # " dynamic
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
                signals += self.get_tempo_signal(tree)

        # Timesig
        if tree.data == 'timesig':
            if self.is_valid_timesig(tree):
                signals += self.get_timesig_signal(tree)

        # Dynamic
        if tree.data == 'dynamic':
            if self.is_valid_dynamic(tree):
                signals += self.get_dynamic_signal(tree)

        # Measure
        if tree.data == 'measure':
            if self.is_valid_measure(tree):
                signals += self.measure_to_signal(tree)

        # Repeat
        if tree.data == 'repeat':
            if self.is_valid_repeat(tree):
                repeatedsignals = self.process_composeitems(tree)
                signals += repeatedsignals
                signals += repeatedsignals

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

    # TODO order these checks in a better order

    # Check that the data has a start symbol
    def is_valid_tree(self, tree):
        if not type(tree) is self.treetype:
            return False

        if tree.data != 'start':
            return False
        for i in range(len(tree.children[:-1])):
            if tree.children[i].data == 'id':
                if tree.children[i+1].data != 'rhs':
                    return False
            if tree.children[i].data == 'rhs':
                if tree.children[i-1].data != 'id':
                    return False
        if tree.children[-1].data != 'compose':
            return False
        return True

    def is_valid_dynamic(self, tree):
        if not type(tree) is self.treetype:
            return False
        if tree.data != 'dynamic':
            return False

        item = tree.children[0].data
        if item == 'inlinedynamic':
            d = tree.children[0].children[0].lower()
            if d not in self.valid_levels:
                return False
        elif item == 'id':
            return Semantic.is_valid_identifier(self, tree)
        else:
            return False

        return True

    def is_valid_inlinedynamic(self, tree):
        if not type(tree) is self.treetype:
            return False
        if tree.data != 'inlinedynamic':
            return False

        d = tree.children[0].lower()
        if d not in self.valid_levels:
            return False

        return True

    def is_valid_note(self, tree):
        if not type(tree) is self.treetype:
            return False

        if len(tree.children[0].children) != 2:
            return False

        if tree.children[0].children[0].data != 'division':
            return False
        else:
            n = tree.children[0].children[1].data
            if not ( n == 'notename' or n == 'chord' or n == 'tuple' or n == 'id' or n == 'REST'):
                return False

            if tree.children[0].children[1].data == 'REST':
                if tree.children[0].children[1].children[0].value != '--':
                    print('rest is not good')
                    return False

        return True

    # check that the measure is valid
    def is_valid_repeat(self, tree):
        pass

    # check that the measure is valid
    def is_valid_measure(self, tree):
        pass

    # check that the tempo is valid
    def is_valid_tempo(self, tree):
        pass

    # check that all the numbers are powers of 2 and nonzero
    def is_valid_division(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'division':
            return False

        if not tree.children[0].data == 'number':
            return False

        if not tree.children[1].data == 'number':
            return False

        if not len(tree.children) == 2:
            return False

        if not int(tree.children[0].children[0].value) > 0:
            return False

        denom = int(tree.children[1].children[0].value)
        if not (denom  == 1 or denom == 2 or denom == 4 or denom == 8 or denom == 16 or denom == 32 or denom == 64 or denom == 128):
            return False

        return True

    def is_valid_noteitem(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'noteitem':
            return False

        if not len(tree.children) == 1:
            return False

        item = tree.children[0].data
        if item == 'note':
            return Semantic.is_valid_note(self, tree)
        elif item  == 'id':
            return Semantic.is_valid_identifier(self, tree)
        elif item == 'inlinedynamic':
            d = tree.children[0].lower()
            if d not in self.valid_levels:
                return False
        else:
            return False

        return True

    def is_valid_notename(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'notename':
            return False

        if not (len(tree.children) == 3 or len(tree.children) == 2):
            return False

        n = tree.children[0]
        n.upper()
        if not (n  == 'A' or n == 'B' or n == 'C' or n == 'D' or n == 'E' or n == 'F' or n == 'G'):
            return False

        if len(tree.children) == 3:
            #Has accidental
            if tree.children[1].data != 'accidental':
                return False
            if tree.children[2].data != 'number':
                return False

            acc = tree.children[1].children[0].value
            if acc != ('#' or 'b'):
                return False
            octave = int(tree.children[2].children[0].value)
            if 9 > octave < 0:
                return False

        elif len(tree.children) == 2:
            #No accidental
            if tree.children[1].data != 'number':
                return False
            octave = int(tree.children[1].children[0].value)
            if 9 > octave < 0:
                return False
        else:
            #Invalid length
            return False

        return True


    # check the name exists in our program
    def is_valid_identifier(self, tree):
        if not type(tree) is self.treetype:
            return False
        if not tree.data == 'id':
            return False
        theID = tree.children[0]
        length = len(theID)
        if length < 2:
            return False
        if theID[0] != '$':
            return False
        if not theID[1].isalpha():
            return False

        for i in range(2, length):
            idChar = theID[i]
            if not(idChar.isalnum() or idChar == '_' or idChar == '-'):
                return False

        return True


    def is_valid_measure(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'measure':
            return False

        for subtree in tree.children:
            isInstr = self.is_valid_instrumentation(subtree)
            isId = self.is_valid_identifier(subtree)
            if (not isInstr) and (not isId):
                return False

        return True

    def is_valid_instrumentation(self, tree):
        if not type(tree) is self.treetype:
            return False

        if tree.data != 'instrumentation':
            return False

        if len(tree.children) < 1:
            return False

        child = tree.children
        if child[0].type != 'INSTRUMENT':
            return False

        for x in child[1:]:
            if not self.is_valid_noteitem(x):
                return False
        return True

    # sets a variable in our memory to its tree
    def set_variable(self, lhs, rhs, variables):
        pass

    # Check if it has a 'start', and one compose
    def is_valid_program(self, tree):
        if not type(tree) is self.treetype:
            return False

        pass

    # Takes in a measure, builds a list of signals
    def measure_to_signal(self, tree):
        pass

    def chord_to_signal(self, tree):
        pass

    def tuple_to_signal(self, tree):
        pass

    def note_to_signal(self, tree):
        pass

    # given a tree that represents a dynamic, set the new volume
    def apply_dynamic(self, tree):
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
