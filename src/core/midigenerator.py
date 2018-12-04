from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido
import exceptions
from noteToNumber import noteToNumber
from instrumentToNumber import instrumentToNumber
from dynamicToVelocity import dynamicToVelocity

class MidiGenerator:
    # Take in the list of signals, build a midi file
    def __init__(self, signals):
        # Save the signals the user passed in
        self.signals = signals
        self.timsig = [4,4]
        self.dynamic = 87
        self.measure_start_time = 0
        self.ticks_per_beat = 1000

        self.song = MidiFile(type=1, ticks_per_beat=1000)
        self.track_time = []
        for i in range(32):
            self.song.tracks.append(MidiTrack())
            self.track_time.append(0)

        self.current_track = 0
        self.current_channel = 0

    # Returns a dictionary from each signal type to a list
    # of all the extra fields that type requires
    def get_type_fields(self):
        types = dict()
        types['note'] = ['note_name', 'length_num', 'length_denom']
        types['rest'] = ['length_num', 'length_denom']
        types['tempo'] = ['bpm']
        types['chord'] = ['notes', 'length_num', 'length_denom']
        types['tuple'] = ['notes', 'length_num', 'length_denom']
        types['measure'] = ['start']
        types['dynamic'] = ['volume']
        types['instrument'] = ['name']
        types['timesig'] = ['time_num', 'time_denom']
        return types


    # Check that the list of signals passed in is valid
    def validate(self, signals):
        print('validate')
        # Grab valid types
        types = self.get_type_fields()

        # Check the signal has a type
        for signal in signals:

            # Check the signal has a type
            if 'type' not in signal:
                raise exceptions.SignalError('Signal has no type.')

            # Find this signal's type
            curr_type = signal['type']

            # Check it's a valid type
            if curr_type not in types:
                raise exceptions.SignalError('Signal has improper type.')

            # Count how many parameters are needed, and how many we have
            need = len(types[curr_type])
            have = len(signal) - 1

            if have != need:
                raise exceptions.SignalError('Incorrect number of signal parameters.')

            # Check that all the parameters we have match what we neeed
            for i in types[curr_type]:
                if i not in signal:
                    raise exceptions.SignalError('Missing parameter for signal type.')

        return True


    # Take the list of signals, and build a midi file
    def generate(self):
        print('generate')
        # If the signals passed in aren't valid, return an error
        if not self.validate(self.signals):
            return False

        self.resolve_errors(0)
        for signal in self.signals:
            if signal['type'] == 'measure':
                self.midify_measure(signal)
            elif signal['type'] == 'instrument':
                msg = self.midify_instrument(signal)
                self.song.tracks[self.current_track].append(msg)
            elif signal['type'] == 'note':
                on, off = self.midify_note(signal)
                self.song.tracks[self.current_track].append(on)
                self.song.tracks[self.current_track].append(off)
                self.track_time[self.current_track] += off.time
            elif signal['type'] == 'rest':
                on, off = self.midify_rest(signal)
                self.song.tracks[self.current_track].append(on)
                self.song.tracks[self.current_track].append(off)
                self.track_time[self.current_track] += off.time
            elif signal['type'] == 'chord':
                initialTrack = self.current_track
                for i in range(len(signal['notes'])):
                    note = signal['notes'][i]
                    newSignal = {'type': 'note', 'note_name': note, 'length_num':signal['length_num'], 'length_denom' : signal['length_denom']}
                    on, off = self.midify_note(newSignal)
                    self.song.tracks[self.current_track].append(on)
                    self.song.tracks[self.current_track].append(off)
                    self.track_time[self.current_track] += off.time
                    self.current_track += 1
                    self.current_channel += 1
                self.current_track = initialTrack

            elif signal['type'] == 'dynamic':
                self.midify_dynamic(signal)
            elif signal['type'] == 'timesig':
                self.midify_timesig(signal)
            elif signal['type'] == 'tempo':
                msg = self.midify_tempo(signal)
                self.song.tracks[self.current_track].append(msg)

        self.resolve_errors(0)
        return self.song

    def resolve_errors(self, time):
        print('resolve')
        for i in range(len(self.track_time)):
            if time < self.track_time[i]:
                time = self.track_time[i]

        for i in range(len(self.track_time)):
            if self.track_time[i] < time:
                time_diff = time - self.track_time[i]
                self.song.tracks[i].append(Message("note_on",  note=0, channel=self.current_channel, velocity=0, time=0))
                self.song.tracks[i].append(Message("note_off", note=0, channel=self.current_channel, velocity=0, time=time_diff))
                self.track_time[i] = time


    def midify_measure(self, signal):
        print('measure')
        if signal['start']:
            self.current_track = 0
            self.current_channel = 0
            self.resolve_errors(self.measure_start_time)
        else:
            self.measure_start_time += self.ticks_per_beat * self.timesig[0]
            self.resolve_errors(self.measure_start_time)

    def midify_timesig(self, signal):
        print('timesig')
        if signal['type'] != 'timesig':
            print('Error: invalid timesig signal')

        self.timesig = [int(signal['time_num']), int(signal['time_denom'])]


    def midify_dynamic(self, signal):
        print('dynamic')
        if signal['type'] != 'dynamic':
            print('Error: invalid dynamic signal')

        self.dynamic = dynamicToVelocity[signal['volume']]


    def midify_instrument(self, signal):
        print('instrument')
        instrumentNumber = instrumentToNumber[signal['name']]

        self.current_track += 1
        self.current_channel += 1

        return Message('program_change', channel=self.current_channel, program=instrumentNumber, time=0)


    def midify_tempo(self, signal):
        print('tempo')
        if(signal['type'] != 'tempo'):
            print('Error when midifying tempo')
            return ''
        self.ticks_per_beat = mido.bpm2tempo(int(signal['bpm']) * 18)

        return MetaMessage("set_tempo", tempo=self.ticks_per_beat)


    def midify_note(self, signal):
        print('note')
        if(signal['type'] != 'note'):
            print('Error when midifying note')
            return '', ''

        noteNumber = noteToNumber[signal['note_name']]
        length = int(self.ticks_per_beat * self.timesig[0] * signal['length_num'] / signal['length_denom'])
        length = int(self.ticks_per_beat * self.timesig[1] * signal['length_num'] / signal['length_denom'])
        return Message('note_on', note=noteNumber, channel=self.current_channel, velocity=self.dynamic, time=0), Message('note_off',note=noteNumber, channel=self.current_channel, velocity=self.dynamic, time=length)


    def midify_rest(self, signal):
        print('rest')
        if(signal['type'] != 'rest'):
            print('Error when midifying rest')
            return '', ''

        length = int(self.ticks_per_beat * self.timesig[0] * signal['length_num'] / signal['length_denom'])
        length = int(self.ticks_per_beat * self.timesig[1] * signal['length_num'] / signal['length_denom'])
        return Message('note_on', note=0, channel=self.current_channel, velocity=self.dynamic, time=0), Message('note_off',note=0, channel=self.current_channel, velocity=self.dynamic, time=length)

