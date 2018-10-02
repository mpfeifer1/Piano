from mido import Message, MidiFile, MidiTrack

import lark
from argparse import ArgumentParser
from lark import Lark
import unittest
import sys

#TODO add more instruments
grammar = r'''
    start: compose
        | lhs "=" rhs
    digit: "0"
        | "1"
        | "2"
        | "3"
        | "4"
        | "5"
        | "6"
        | "7"
        | "8"
        | "9"
    accidental: "#" | "b"
    compose: "Compose" "{" composeitems* "}"
    notename: ("a".."g" | "A".."G") accidental? number
    comment: "//"
    rest: "--"
    lhs: NAME
        | compose
    number: digit+
    instrument: "trumpet" | "piano" | "tuba"
    division: number "/" number
    chord: "(" notename+ ")" | lhs
    tuple: "tuplet(" (chord|note)+ ")"

    note: division notename
        | division chord
        | division tuple
        | division rest
        | lhs

    inlinedynamic: "mf"
        | "mp"
        | "f"+
        | "p"+
        | lhs

    dynamic: "Dynamic(" inlinedynamic ")"

    noteitem: note ";"
        | inlinedynamic ";"

    instrumentation: (instrument | lhs) "{" noteitem+ "}"
        | lhs

    measure: "Measure" "{" instrumentation* "}"
        | lhs

    tempo: "Tempo(" number ")"
        | lhs

    timesig: "Timesig(" division ")"
        | lhs

    repeat: "Repeat" composeitems+ "Endr"

    composeitems: tempo
        | timesig
        | dynamic
        | measure
        | repeat

    rhs: composeitems
        | instrument
        | instrumentation
        | note
        | tuple
        | chord
        | tempo
        | timesig
        | inlinedynamic
        | dynamic

    %import common.CNAME -> NAME
    %import common.WS_INLINE

    %ignore WS_INLINE
'''

# Try a sample grammar recognition
l = lark.Lark(grammar)

print("BUILT GRAMMAR")

goodstrs = [
    "Compose{}"
]

badstrs = [
    "INVALID%$&",
    "h#4"
]

print("~~~~~~~GOOD~~~~~~~~")
for i in goodstrs:
    try:
        l.parse(i)
    except:
        print("INCORRECT - didn't accept", i)

print()

print("~~~~~~~BAD~~~~~~~~")
for i in badstrs:
    try:
        l.parse(i)
        print("INCORRECT - accepted", i)
    except:
        pass
