from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido
from noteToNumber import noteToNumber
from instrumentToNumber import instrumentToNumber

class MidiGenerator:
    # Take in the list of signals, build a midi file
    def __init__(self, signals):
        # Save the signals the user passed in
        self.signals = signals
        self.tempo = 120
        self.measure_start_time = 0
        self.measure_end_time = 0
        self.ticks_per_beat = 0
        self.song = MidiFile(type=1, ticks_per_beat=1000)
        self.max_track = -1
        self.current_track = -1
        self.track_time = []
        self.chord_track = 0
        self.first_instrument = True

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
        types['timesig'] = ['time_num', 'time_denom']
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
                print(curr_type)
                print("Error: Expected " , need , " type paramaters")
                return False

            # Check that all the parameters we have match what we neeed
            for i in types[curr_type]:
                if i not in signal:
                    print("Error: Unexpected parameter " , i , " in " , curr_type)
                    return False

        return True


    # Take the list of signals, and build a midi file
    def generate(self):

        # If the signals passed in aren't valid, return an error
        if not self.validate(self.signals):
            return False

        #add an initial track to the song
        self.add_track()

        self.song.tracks[self.current_track].append(self.midify_tempo({'type': 'tempo', 'bpm': 20}))

        for signal in self.signals:
            print(signal)
            if signal['type'] == 'measure':
                self.midify_measure(signal)
            elif signal['type'] == 'instrument':
                msg = self.midify_instrument(signal)
                self.song.tracks[self.current_track].append(msg)
                print(self.current_track)
            elif signal['type'] == 'note':
                on, off = self.midify_note(signal)
                self.song.tracks[self.current_track].append(on)
                self.song.tracks[self.current_track].append(off)

        for track in self.song.tracks:
            print("track")
            for message in track:
                print(message)

        self.song.save('piano.mid')


    def midify_measure(self, signal):
        self.measure_start_time = self.measure_end_time
        self.current_track = 0
        self.first_instrument = True


    def midify_instrument(self, signal):
        instrumentNumber = instrumentToNumber[signal['name']]

        self.measure_end_time = self.measure_start_time

        if(self.current_track == self.max_track and self.first_instrument == False):
            print('adding a new track')
            self.add_track()
        elif(self.first_instrument == True):
            self.first_instrument = False
        else:
            self.current_track += 1

        return Message('program_change', program=instrumentNumber, time=0)

    def midify_tempo(self, signal):
        if(signal['type'] != 'tempo'):
            print('Error when midifying tempo')
            return ''
        self.ticks_per_beat = mido.bpm2tempo(signal['bpm'])
        return MetaMessage("set_tempo", tempo=self.ticks_per_beat)

    def midify_note(self, signal):
        if(signal['type'] != 'note'):
            print('Error when midifying note')
            return '', ''

        noteNumber = noteToNumber[signal['note_name']]
        length = int(1000 * (signal['length_num']/float(signal['length_denom'])))

        self.measure_end_time = self.measure_start_time + length
        return Message('note_on', note=noteNumber, velocity=127, time=0), Message('note_off',
            note=noteNumber, velocity=127, time=length)


    def add_track(self):
        self.song.tracks.append(MidiTrack())
        self.max_track += 1
        self.current_track = self.max_track
        self.track_time.append(0)

