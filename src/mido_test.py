from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido
song = MidiFile(type=1, ticks_per_beat=1000)
song.tracks.append(MidiTrack())
song.tracks[0].append(MetaMessage("set_tempo", tempo=3000000))
song.tracks[0].append(Message("program_change", channel=0, program=57, time=0))
song.tracks[0].append(Message("note_on", note=60, channel=0, velocity=127, time=0))
song.tracks[0].append(Message("note_off", note=60, channel=0, velocity=127, time=1000))
song.tracks.append(MidiTrack())
song.tracks[1].append(Message("program_change", channel=1, program=57, time=0))
song.tracks[1].append(Message("note_on", note=60, channel=1, velocity=127, time=0))
song.tracks[1].append(Message("note_off", note=60, channel=1, velocity=127, time=1000))
song.save("ugh.mid")
