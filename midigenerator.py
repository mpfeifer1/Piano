import mido

class MidiGenerator:
    # Take in the list of signals, build a midi file
    def __init__(self, signals):
        # Save the signals the user passed in
        self.signals = signals

    # Take the list of signals, and build a midi file
    def generate(self):
        # Here, iterate over every midi signal, and
        # convert them into a midi file
        # You may need to match each starting signal
        # with its corresponding end signal
        pass
