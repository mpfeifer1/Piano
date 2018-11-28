from mido import Message, MidiFile, MidiTrack

class MidiGenerator:
    # Take in the list of signals, build a midi file
    def __init__(self, signals):
        # Save the signals the user passed in
        self.signals = signals
        self.time = 0
        self.tempo = 120
        self.measure_start_time = 0
        self.measure_end_time = 0
        self.seconds_per_beat = 0
        self.song = MidiFile(type=2)
        self.max_track = 0
        self.current_track = 0

    # Returns a dictionary from each signal type to a list
    # of all the extra fields that type requires
    def get_type_fields(self):
        types = dict()
        types['note'] = ['note_name', 'length_num', 'length_denom']
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
                print('Error: Missing Signal Type')
                return False

            # Find this signal's type
            curr_type = signal['type']

            # Check it's a valid type
            if curr_type not in types:
                print('Error: Invalid Signal Type')
                return False

            # Count how many parameters are needed, and how many we have
            need = len(types[curr_type])
            have = len(signal) - 1
            if have != need:
                print("Error: Expected " + need + " type paramaters")
                return False

            # Check that all the parameters we have match what we neeed
            for i in types[curr_type]:
                if i not in signal:
                    print("Error: Unexpected parameter " + i + " in " + curr_type)
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

        self.add_track()

        self.song.tracks[self.current_track].append(Message('note_on', note=64, velocity=64, time=0))
        self.song.tracks[self.current_track].append(Message('note_off', note=64, velocity=127, time=5000))


        self.song.save('piano.mid')
        for signal in self.signals:
            print(signal)


    def midify_measure(self, signal):
        pass

    def add_track(self):
        self.song.tracks.append(MidiTrack())
        self.max_track += 1
        self.current_track = self.max_track - 1