#!/usr/bin/env python3

from mido import Message, MidiFile, MidiTrack

import lark
from argparse import ArgumentParser
from lark import Lark
import unittest
import sys

#TODO add more instruments
grammar = r'''
    start: compose
        | lhs "=" rhs compose

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

    compose: "compose"i "{" composeitems* "}"

    notename: ("a".."g" | "A".."G") accidental? number

    rest: "--"

    number: digit+

    instrument: "trumpet"i | "piano"i | "tuba"i | "acousticgrandpiano"i

    division: number "/" number

    chord: "(" notename+ ")" | lhs

    tuple: "tuplet("i (chord|note)+ ")"

    note: division notename
        | division chord
        | division tuple
        | division rest
        | lhs

    inlinedynamic: "mf"i
        | "mp"i
        | "f"i+
        | "p"i+
        | lhs

    dynamic: "Dynamic("i inlinedynamic ")"

    noteitem: note ";"
        | inlinedynamic ";"

    instrumentation: (instrument | lhs) "{" noteitem+ "}"
        | lhs

    measure: "Measure"i "{" instrumentation* "}"
        | lhs

    tempo: "Tempo("i number ")"
        | lhs

    timesig: "Timesig("i division ")"
        | lhs

    repeat: "Repeat"i composeitems+ "Endr"i

    composeitems: tempo
        | timesig
        | dynamic
        | measure
        | repeat

    lhs: "$" NAME

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

    COMMENT: "//" /[^\n]/*
    WHITESPACE: " " | "\t" | "\n"

    %import common.CNAME -> NAME

    %ignore COMMENT
    %ignore WHITESPACE
'''
'''
'''

# Try a sample grammar recognition
l = lark.Lark(grammar)

print("BUILT GRAMMAR")

goodstrs = [
    """
    Compose{
        // Nathan is a nerd
    }
    """,


    """
    Compose {
        Measure {
            acousticgrandpiano {
                1/4 C4; 1/4 C4; 1/4 G4; 1/4 G4;
            }
            acousticgrandpiano {
                1/4 C4; 1/4 --; 1/4 G4; 1/4 --;
            }
        }
    }
    """,



    """
    Compose{
        // Nerd Nerd Nerd
        Tempo(60)
        Timesig(4/4)
    }
    """,



    """
    $gp = acousticgrandpiano
    Compose{
    }
    """,

    """
    compose {
        measure {

        }
    }
    """,


    """
    Compose {
        Measure {

        }
    }
    """

]

badstrs = [
    "INVALID%$&",
    "h#4",
    """
    nathan = a5
    """,
    """
    A
    """,
    """
    $    gp = acousticgrandpiano
    Compose{
    }
    """
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
