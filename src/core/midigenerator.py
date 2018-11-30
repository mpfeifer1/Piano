import mido

class MidiGenerator:
    # Take in the list of signals, build a midi file
    def __init__(self, signals):
        # Save the signals the user passed in
        self.signals = signals

    # Returns a dictionary from each signal type to a list
    # of all the extra fields that type requires
    def get_type_fields(self):
        types = dict()
        types['note'] = ['notename', 'length_num', 'length_denom']
        types['rest'] = ['length_num', 'length_denom']
        types['tempo'] = ['bpm']
        types['chord'] = ['notes', 'length_num', 'length_denom']
        types['tuple'] = ['notes', 'length_num', 'length_denom']
        types['measure'] = []
        types['dynamic'] = ['volume']
        types['instrument'] = ['name']
        return types



    # Check that the list of signals passed in is valid
    def validate(self, signals):
        # Grab valid types
        types = self.get_type_fields()

        # Check the signal has a type
        for signal in signals:
            # Check the signal has a type
            if 'type' not in signal:
                return False

            # Find this signal's type
            curr_type = signal['type']

            # Check it's a valid type
            if curr_type not in types:
                return False

            # Count how many parameters are needed, and how many we have
            need = len(types[curr_type])
            have = len(signal) - 1
            if have != need:
                return False

            # Check that all the parameters we have match what we neeed
            for i in types[curr_type]:
                if i not in signal:
                    return False

        return True



    # Take the list of signals, and build a midi file
    def generate(self):
        # Here, iterate over every midi signal, and
        # convert them into a midi file
        # You may need to match each starting signal
        # with its corresponding end signal

        # If the signals passed in aren't valid, return an error
        if not self.validate(self.signals):
            return False

        pass
