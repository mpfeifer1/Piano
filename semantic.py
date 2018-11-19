from instrumentToNumber import instrumentToNumber

class Semantic:
    # Take in the tree from the user
    def __init__(self, tree):
        # Save the tree the user passed in
        self.tree = tree

        # Keep track of current 'state' of song
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

    def get_dynamic_signal(self, tree):
        pass

    def get_tempo_signal(self, tree):
        pass

    def get_timesig_signal(self, tree):
        pass

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

        signals = []
        signals.append({'type':'measure'})
        
        for i in tree.children:
            if i.data == 'instrumentation':
                signals += (self.instrumentation_to_signal(i))
        
        #for x in signals:
        #    print(x)
        
        return signals

    def instrumentation_to_signal(self, tree):
        if tree.data != 'instrumentation':
            print('error: not an instrumentation')
            return False

        signals = []
        name = tree.children[0]
        
        signals.append({'type':'instrument', 'name':str(name)})
        
        if tree.children[0] in instrumentToNumber:
            for i in tree.children[1:]:
                signals += (self.noteitem_to_signal(i))
        else:
            print('invalid instrument')

        return signals

    def noteitem_to_signal(self,tree):
        if tree.data != 'noteitem':
            print('error: invalid noteitem')
        
        signals = []

        for i in tree.children:
            # possible noteitem children : note , inlinedynamic
            if i.data == 'note':
                signals += (self.note_to_signal(i))
            elif i.data == 'inlinedynamic':
                signals += (self.inlinedynmaic_to_signal(i))
            else:
                print('invalid noteitem child')
   
        return signals
 
    def note_to_signal(self, tree):
        if tree.data != 'note':
            print('error: not a note!')

        signals = []
        notesig = {'type': 'note', 'note_name':'', 'length_num':0, 'length_denom':0}        
        chordsig = {'type': 'chord', 'notes':[], 'length_num':0, 'length_denom':0}
        restsig = {'type': 'rest', 'length_num':0, 'length_denom':0}        

        num = 0
        den = 0
        
        for i in tree.children:
            # children of a note: division, notename, --, chord, tuple
            if i == "--":
                restsig['length_num'] = int(num)
                restsig['length_denom'] = int(den)
                signals.append(restsig)
            elif i.data == 'division':
                print("collecting divisions")
                num = i.children[0].children[0]
                den = i.children[1].children[0]
            elif i.data == 'notename':
                notesig['note_name'] = self.notename_to_signal(i)
                notesig['length_num'] = int(num)
                notesig['length_denom'] = int(den)
                signals.append(notesig)
            elif i.data == "chord":
                chordsig['notes'] = self.chord_to_signal(i)
                chordsig['length_num'] = int(num)
                chordsig['length_denom'] = int(den)
                signals.append(chordsig)
            elif i.data == "tuple":
                signals += self.tuple_to_signal(i)
            else:
                print("invalid note child")

        return signals

    def notename_to_signal(self, tree):
        print('notename to signal')
        name = ""
        for i in tree.children:
            if 'Token' in str(type(i)):
                name += str(i)
            elif 'Tree' in str(type(i)): #it's a token
                name+=i.children[0]
            else:
                print('invalid notename child')
        
        return name

    def inlinedynmaic_to_signal(self, tree):
        return [{'type':'dynamic', 'volume':str(tree.children[0])}]
        
    def chord_to_signal(self, tree):
        if tree.data != 'chord':
            print('error! not a chord')
        
        notes = []

        for i in tree.children:
            # only children of a chord are notenames
            if i.data == 'notename':
                notes.append(self.notename_to_signal(i))
            else:
                print('invalid chord child')
        
        return notes

    def tuple_to_signal(self, tree):
        if tree.data != 'tuple':
            print('error: not a tuple')
        # put dummy data in a tuple signal because we don't like them much
        return [{'type':'tuple', 'length_num':0, 'length_denom':0, 'notes':[]}]

        for i in tree.children:
            if i.data == 'notename':
                self.notename_to_signal(i)
            elif i.data == 'chord':
                self.chord_to_signal(i)
            else:
                print('invalid tuple child')


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
