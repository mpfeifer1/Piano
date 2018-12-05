import sys
sys.path.append(r'core')
from instrumentToNumber import instrumentToNumber
import exceptions
import lark
from lark import lexer

Token = lexer.Token

class Semantic:

    # Take in the tree from the user
    def __init__(self, tree):
        # Save the tree the user passed in
        self.tree = tree

        # Keep track of current 'state' of song
        self.variables = {}

        self.treetype = type(lark.tree.Tree('data', ['children']))
        self.tokentype = type(Token('data1', 'data2'))

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
        #if not self.is_valid_tree(self.tree):
        #    raise exceptions.SemanticError('Invalid parse tree.')

        # Split up the tree into a list of commands
        commands = self.split_into_commands(self.tree)

        # Grab the initial signals
        signals = self.get_default_signals()

        # Process each command in the language
        for command in commands:
            # If it's an assignment, do that
            if command[0] == 'assignment':
                self.set_variable(command[1], command[2])
            # If it's a compose, do that
            if command[0] == 'compose':
                newsig = self.process_compose(command[1])
                signals += self.process_compose(command[1])
        return signals


    # Return a list of signals with all the default settings
    def get_default_signals(self):
        tempo_sig = {"type":"tempo",
                     "bpm":120}
        timesig_sig = {"type": "timesig",
                       "time_num": 4,
                       "time_denom": 4}
        dynamic_sig = {"type": "dynamic",
                       "volume": "mf"}

        signals = []
        signals.append(tempo_sig)
        signals.append(timesig_sig)
        signals.append(dynamic_sig)

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
            else:
                raise exceptions.TempoError('Invalid Tempo structure.')

        # Timesig
        if tree.data == 'timesig':
            if self.is_valid_timesig(tree):
                signals += self.get_timesig_signal(tree)
            else:
                raise exceptions.TimesigError('Invalid Timesig structure.')

        # Dynamic
        if tree.data == 'dynamic':
            if self.is_valid_dynamic(tree):
                signals += self.get_dynamic_signal(tree)
            else:
                raise exceptions.DynamicError('Invalid Dynamic Structure.')

        # Measure
        if tree.data == 'measure':
            if self.is_valid_measure(tree):
                signals += self.measure_to_signal(tree)
            else:
                raise exceptions.MeasureError('Invalid Measure Structure')

        # Repeat
        if tree.data == 'repeat':
            if self.is_valid_repeat(tree):
                newtree = tree.children[0]
                print("Calling with ", newtree)

                repeatedsignals = self.process_composeitems(newtree)
                signals += repeatedsignals
                signals += repeatedsignals

                print("Repeated signals: ", repeatedsignals)
            else:
                raise exceptions.RepeatError('Invalid Repeat Structure.')

        # Variable measures
        if tree.data == 'id':
            if self.is_valid_measure(self.variables[tree.children[0]]):
                signals += self.measure_to_signal(self.variables[tree.children[0]])
        return signals


    def get_dynamic_signal(self, tree):
        signal = {"type":"dynamic"}
        signal["volume"] = tree.children[0].children[0].value
        return [signal]

    def get_tempo_signal(self, tree):
        signal = {"type":"tempo"}
        signal["bpm"] = tree.children[0].children[0].value
        return [signal]

    def get_timesig_signal(self, tree):
        signal = {"type":"timesig"}
        signal["time_num"] = tree.children[0].children[0].children[0].value
        signal["time_denom"] = tree.children[0].children[1].children[0].value
        return [signal]

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
            elif i.data == 'rhs':
                commands[-1].append(i.children[0])
            # Otherwise, if it's a compose, add this to the list of commands
            elif i.data == 'compose':
                commands.append(['compose'])
                commands[-1].append(i.children)
        return commands

    # TODO order these checks in a better order


    # Check that the data has a start symbol
    def is_valid_tree(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if tree.data != 'start':
            return False

        for i in range(len(tree.children[:-1])):
            if tree.children[i].data == 'id':
                if tree.children[i+1].data != 'rhs':
                    raise exceptions.ValidationError('Assignment right-hand side not found.')
            if tree.children[i].data == 'rhs':
                if tree.children[i-1].data != 'id':
                    raise exceptions.ValidationError('Assignment identifier not found.')
        if tree.children[-1].data != 'compose':
            raise exceptions.SemanticError('Compose statement not found.')
        return True


    def is_valid_dynamic(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')
        if tree.data != 'dynamic':
            return False

        item = tree.children[0].data
        if item == 'inlinedynamic':
            d = tree.children[0].children[0].lower()
            if d not in self.valid_levels:
                raise exceptions.DynamicError('Incorrect inline dynamic.')
        elif item == 'id':
            return Semantic.is_valid_identifier(self, tree)
        else:
            raise exceptions.SemanticError('Inline dynamic or identifier expected, not given.')

        return True


    def is_valid_inlinedynamic(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')
        if tree.data != 'inlinedynamic':
            return False

        d = tree.children[0].lower()
        if d not in self.valid_levels:
            raise exceptions.DynamicError('Incorrect inline dynamic.')

        return True


    def is_valid_note(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if tree.data != 'note':
            return False

        if len(tree.children[0].children) != 2:
            raise exceptions.SemanticError('2 children expected, ' + len(tree.children[0].children) + ' given.')

        if tree.children[0].data != 'division':
            raise exceptions.ValidationError('Tree prefix incorrect: ' + str(tree.data) + ' given, division expected.')

        if not self.is_valid_division(tree.children[0]):
            raise exceptions.SemanticError("Invalid Division")

        if type(tree.children[1]) == self.tokentype and tree.children[1].type == 'REST':
            return True

        if not self.is_valid_notename(tree.children[1]) and not self.is_valid_chord(tree.children[1]) and not self.is_valid_tuple(tree.children[1]):
            raise exceptions.SemanticError("Invalid notename or chord")

        return True

    def is_valid_chord(self, tree):
        return True


    # check that the measure is valid
    def is_valid_repeat(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'repeat':
            return False

        try:
            for subtree in tree.children:
                if not subtree.data == 'composeitems':
                    return False
        except:
            return False

        return True


    # check that the tempo is valid
    def is_valid_tempo(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'tempo':
            return False

        tempoval = int(tree.children[0].children[0].value)
        if tempoval < 40 or tempoval > 240:
            return False

        return True


    def is_valid_timesig(self, tree):
        if not type(tree) is self.treetype:
            return False

        if not tree.data == 'timesig':
            return False

        if not tree.children[0].data == 'division':
            return False

        return self.is_valid_division(tree.children[0])

    # check that all the numbers are powers of 2 and nonzero
    def is_valid_division(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'division':
            return False

        if not tree.children[0].data == 'number':
            raise exceptions.ValidationError('Tree prefix incorrect: ' + str(tree.data) + ' given, number expected.')

        if not tree.children[1].data == 'number':
            raise exceptions.ValidationError('Tree prefix incorrect: ' + str(tree.data) + ' given, number expected.')

        if not len(tree.children) == 2:
            raise exceptions.SemanticError('2 children expected, ' + len(tree.children[0].children) + ' given.')

        if not int(tree.children[0].children[0].value) > 0:
            raise exceptions.SemanticError('Positive/nonzero value needed for division numerator.')

        denom = int(tree.children[1].children[0].value)
        validDenoms = [1, 2, 4, 8, 16, 32, 64, 128]
        if denom not in validDenoms:
            raise exceptions.DivisionError('Division denominator must be power of 2.')

        return True


    def is_valid_noteitem(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'noteitem':
            return False

        if not len(tree.children) == 1:
            raise exceptions.SemanticError('1 child expected, ' + len(tree.children[0].children) + ' given.')

        item = tree.children[0].data
        if item == 'note':
            return Semantic.is_valid_note(self, tree.children[0])
        elif item  == 'id':
            return Semantic.is_valid_identifier(self, tree.children[0])
        elif item == 'inlinedynamic':
            d = tree.children[0].children[0].lower()
            if d not in self.valid_levels:
                raise exceptions.DynamicError('Incorrect inline dynamic.')
        else:
            raise exceptions.SemanticError('Note, inline dynamic, or identifier expected, not given.')

        return True


    def is_valid_tuple(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'tuple':
            return False

        try:
            for child in tree.children:
                if child.data == 'notename':
                    if not self.is_valid_notename(child):
                        raise SemanticError
                elif child.data == 'chord':
                    if not self.is_valid_chord(child):
                        raise SemanticError
                elif child.data == 'rest':
                    if not self.is_valid_rest(child):
                        raise SemanticError
                else:
                    raise SemanticError
        except:
            raise SemanticError('Tuples may only contian notes, chords, and rests.')

        return True


    def is_valid_rest(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'rest':
            return False

        return True


    def is_valid_chord(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'chord':
            return False

        try:
            for child in tree.children:
                if not child.data == 'notename':
                    return False
                if not self.is_valid_notename(child):
                    raise SemanticError
        except:
            raise exceptions.SemanticError('Chords should only contain notes.')

        return True


    def is_valid_notename(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'notename':
            return False

        if not (len(tree.children) == 3 or len(tree.children) == 2):
            raise exceptions.SemanticError('2 or 3 children expected, ' + len(tree.children[0].children) + ' given.')

        n = tree.children[0]
        n.upper()
        validNoteLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        if n not in validNoteLetters:
            raise exceptions.NoteError('Invalid note letter.')

        if len(tree.children) == 3:
            #Has accidental
            if tree.children[1].data != 'accidental':
                raise exceptions.NoteError('Accidental expected, not given.')
            if tree.children[2].data != 'number':
                raise exceptions.NoteError('Octave number expected, not given')

            acc = tree.children[1].children[0].value
            if acc != ('#' or 'b'):
                raise exceptions.NoteError('Incorrect accidental symbol given, \'b\' or \'#\' expected.')
            octave = int(tree.children[2].children[0].value)
            if 9 > octave < 0:
                raise exceptions.NoteError('Invalid note octave.')

        elif len(tree.children) == 2:
            #No accidental or rest
            if tree.children[1].data != 'number':
                raise exceptions.NoteError('Octave number expected, not given')
            octave = int(tree.children[1].children[0].value)
            if 9 > octave < 0:
                raise exceptions.NoteError('Invalid note octave.')
        else:
            #Invalid length
            raise exceptions.NoteError('Invalid note syntax')
            return False

        return True


    # check the name exists in our program
    def is_valid_identifier(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'id':
            return False

        theID = tree.children[0]
        length = len(theID)

        if length < 2:
            raise exceptions.SemanticError('At least 2 children expected, ' + len(tree.children[0].children) + ' given.')

        if theID[0] != '$':
            raise exceptions.SemanticError('Identifier must begin with \'$\'')

        if not theID[1].isalpha():
            raise exceptions.SemanticError('Identifier first non-$ must be alpha-non-numeric.')

        for i in range(2, length):
            idChar = theID[i]
            if not(idChar.isalnum() or idChar == '_' or idChar == '-'):
                raise exceptions.SemanticError('Identifier may only contain alphanumeric, _, and -.')

        return True


    def is_valid_measure(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if not tree.data == 'measure':
            return False
        for subtree in tree.children:
            isInstr = self.is_valid_instrumentation(subtree)
            isId = self.is_valid_identifier(subtree)
            if (not isInstr) and (not isId):
                raise exceptions.MeasureError('Instrument or identifier required.')
        return True


    def is_valid_instrumentation(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(tree)) + ' is not ' + str(self.treetype) + '.')

        if tree.data != 'instrumentation':
            return False
        if len(tree.children) < 1:
            raise exceptions.SemanticError('At least 1 child expected, ' + len(tree.children[0].children) + ' given.')

        child = tree.children
        if type(child[0]) == self.treetype:
            if not self.is_valid_identifier(child[0]):
                return False
            child[0] = self.variables[child[0].children[0]]
        if type(child[0]) != self.tokentype:
            raise exceptions.ValidationError('Type mismatch: ' + str(type(child[0])) + ' is not ' + str(self.tokentype) + '.')
        if child[0].type != 'INSTRUMENT':
            raise exceptions.ValidationError('Type mismatch: ' + child[0].type + ' is not INSTRUMENT.')

        for x in child[1:]:
            if not self.is_valid_noteitem(x):
                raise exceptions.SemanticError('Invalid Noteitem.')
        return True


    # sets a variable in our memory to its tree
    def set_variable(self, lhs, rhs):
        self.variables[lhs.value] = rhs

    # Check if it has a 'start', and one compose
    def is_valid_program(self, tree):
        if not type(tree) is self.treetype:
            raise exceptions.SemanticError("Not a tree")

    # Takes in a measure, builds a list of signals
    def measure_to_signal(self, tree):
        if not self.is_valid_measure(tree):
            raise exceptions.SemanticError("Invalid measure")
            return []

        signals = []
        signals.append({'type':'measure', 'start':True})
        for i in tree.children:
            if i.data == 'instrumentation':
                signals += self.instrumentation_to_signal(i)

        signals.append({'type':'measure', 'start':False})

        return signals


    def instrumentation_to_signal(self, tree):
        if not self.is_valid_instrumentation(tree):
            raise exceptions.SemanticError(tree.data + ' given where instrumentation is expected.')

        signals = []
        name = tree.children[0]

        signals.append({'type':'instrument', 'name':str(name)})

        if tree.children[0] in instrumentToNumber:
            for i in tree.children[1:]:
                signals += self.noteitem_to_signal(i)
        else:
            raise exceptions.SignalConversionError('Invalid instrument given.')


        return signals


    def noteitem_to_signal(self,tree):
        if not self.is_valid_noteitem(tree):
            raise exceptions.SemanticError(tree.data + ' given where noteitem is expected.')
            return False

        signals = []

        for i in tree.children:
            # possible noteitem children : note , inlinedynamic
            if i.data == 'note':
                signals += (self.note_to_signal(i))
            elif i.data == 'inlinedynamic':
                signals += (self.inlinedynamic_to_signal(i))
            else:
                raise exceptions.SignalConversionError('Invalid noteitem given.')

        return signals


    def note_to_signal(self, tree):
        if not self.is_valid_note(tree):
            raise exceptions.SemanticError(tree.data + ' given where note is expected.')

        signals = []
        # this function loops through the note's children and fills
        # out the necessary fields when it finds them.`
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
                num = i.children[0].children[0]
                den = i.children[1].children[0]
            elif i.data == 'notename':
                notesig['note_name'] = self.collect_notename(i)
                notesig['length_num'] = int(num)
                notesig['length_denom'] = int(den)
                signals.append(notesig)
            elif i.data == "chord":
                chordsig['notes'] = self.chord_to_signal(i)
                chordsig['length_num'] = int(num)
                chordsig['length_denom'] = int(den)
                signals.append(chordsig)
            elif i.data == "tuple":
                tupleItems = self.tuple_to_signal(i)
                itemCount = len(tupleItems)
                newDen = int(den) * itemCount
                for item in tupleItems:
                    print(item)
                    if item['type'] == 'note':
                        tnotesig = {'type': 'note', 'note_name':'', 'length_num':0, 'length_denom':0}
                        tnotesig['note_name'] = item['value']
                        tnotesig['length_num'] = int(num)
                        tnotesig['length_denom'] = newDen
                        signals.append(tnotesig)
                    elif item['type'] == 'chord':
                        tchordsig = {'type': 'chord', 'notes':[], 'length_num':0, 'length_denom':0}
                        tchordsig['notes'] = item['value']
                        tchordsig['length_num'] = int(num)
                        tchordsig['length_denom'] = newDen
                        signals.append(tchordsig)
            else:
                raise exceptions.SignalConversionError('Invalid note given.')

        return signals

    def collect_notename(self, tree):
        if not self.is_valid_notename:
            print("invalid notename")

        name = ""
        for i in tree.children:
            if 'Token' in str(type(i)):
                name += str(i)
            elif 'Tree' in str(type(i)): #it's a token
                name+=i.children[0]
            else:
                raise exceptions.SignalConversionError('Invalid notename given.')

        return name

    def inlinedynamic_to_signal(self, tree):
        if not self.is_valid_inlinedynamic:
            print('invalid inlinedynamic')

        return [{'type':'dynamic', 'volume':str(tree.children[0])}]


    def chord_to_signal(self, tree):
        if tree.data != 'chord':
            raise exceptions.SemanticError(tree.data + ' given where chord is expected.')

        notes = []

        for i in tree.children:
            # only children of a chord are notenames
            if i.data == 'notename':
                notes.append(self.collect_notename(i))
            else:
                raise exceptions.SignalConversionError('Invalid chord contents.')

        return notes


    def tuple_to_signal(self, tree):
        if tree.data != 'tuple':
            raise exceptions.SemanticError(tree.data + ' given where tuple is expected.')

        # put dummy data in a tuple signal because we don't like them much

        notes = []

        for i in tree.children:
            if i.data == 'notename':
                notes.append({'type' : 'note', 'value' : self.collect_notename(i)})
            elif i.data == 'chord':
                notes.append({'type' : 'chord', 'value' : self.chord_to_signal(i)})
            else:
                raise exceptions.SignalConversionError('Invalid tuple contents.')

        return notes


    # given a tree that represents a dynamic, set the new volume
    def apply_dynamic(self, tree):
        raise exceptions.NotImplementedException('Oops! This hasn\'t been implemented yet!')


    # given a tree that represents a tempo, set that new tempo
    def apply_tempo(self, tree):
        raise exceptions.NotImplementedException('Oops! This hasn\'t been implemented yet!')


    # given a tree that represents a time signature, set the timesig
    def apply_timesig(self, tree):
        raise exceptions.NotImplementedException('Oops! This hasn\'t been implemented yet!')

