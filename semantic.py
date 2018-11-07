import lark

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

        self.treetype = type(lark.tree.Tree('data', ['children']))

    # Take the tree, and convert it into a list of signals
    def analyze(self):
        # so basically here, we're gonna wanna loop through
        # every command in the program, check if it's valid
        # and do it.
        # we gonna need to keep track of variables defined and stuff
        # it should return nice errors, yeah
        # this should keep track of global time, and send that in
        # to each measure

        if not self.is_valid_tree(self.tree):
            #TODO throw real exception
            print('hey man theres no start')

        # Print children
        for i in self.tree.children:
            print(i.pretty())

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

    # check that all the numbers are powers of 2 and nonzero
    def is_valid_division(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'division':
            return False

        if not tree.children[0].data == 'number':
            return False

        if not tree.children[0].data == 'number':
            return False

        if not int(tree.children[0].children[0].value) > 0:
            return False

        denom = int(tree.children[1].children[0].value)
        if not (denom  == 1 or denom == 2 or denom == 4 or denom == 8 or denom == 16 or denom == 32 or denom == 64 or denom == 128):
            return False

        return True


    def is_valid_noteitem(self):
        if not type(tree) is self.treetype:
            return False

        return True


    # check the name exists in our program
    def is_valid_identifier(self, tree):
        if not type(tree) is self.treetype:
            return False

        pass


    def is_valid_measure(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'measure':
            return False

        return True

    def is_valid_instrumentation(self, tree):
        if not type(tree) is self.treetype:
            return False

        if tree.data != 'instrumentation':
            return False
        child = tree.children
        if child[0].type != 'INSTRUMENT':
            return False
        for x in child[1:]:
            if not is_valid_noteitem:
                return False
        return True

    # sets a variable in our memory to its tree
    def set_variable(self, tree):
        pass

    # Check if it has a 'start', and one compose
    def is_valid_program(self, tree):
        if not type(tree) is self.treetype:
            return False

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

