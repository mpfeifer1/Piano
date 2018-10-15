#!/usr/bin/env python3

from mido import Message, MidiFile, MidiTrack

import lark
from argparse import ArgumentParser
from lark import Lark
import unittest
import sys

#TODO add more instruments
grammar = r'''    
    forbidden: notename
        | "compose"i
        | "--"
        | instrument
        | "tuplet"i
        | "tuplet("i
        | "dynamic"i
        | "dynamic("i
        | "measure"i
        | "measure("i
        | "tempo"i
        | "tempo("i
        | "timesig"i
        | "timesig("i
        | "repeat"i
        | "endr"i
        
    start: (id "=" rhs)* compose

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

    chord: "(" notename+ ")"

    tuple: "tuplet("i (chord|note|id)+ ")"

    note: division notename
        | division (chord | id)
        | division (tuple | id)
        | division rest

    inlinedynamic: "mf"i
        | "mp"i
        | "f"i+
        | "p"i+

    dynamic: "Dynamic("i (inlinedynamic | id) ")"

    noteitem: (note|id) ";"
        | inlinedynamic ";"

    instrumentation: (instrument | id) "{" noteitem+ "}"

    measure: "Measure"i "{" (instrumentation | id)* "}"

    tempo: "Tempo("i number ")"

    timesig: "Timesig("i division ")"

    repeat: "Repeat"i composeitems+ "Endr"i

    composeitems: id
        | tempo
        | timesig
        | dynamic
        | measure
        | repeat

    id: /[$][a-zA-Z]+[a-zA-Z0-9_\-]*/

    rhs: instrument
        | tempo
        | timesig
        | dynamic
        | measure
        | repeat
        | instrumentation
        | note
        | tuple
        | chord
        | inlinedynamic
        | id

    INLINECOMMENT: "//" /[^\n]/*
    COMMENTBLOCK: "/*" /(.*[\n])*.*/ "*/"
    WHITESPACE: " " | "\t" | "\n"

    %ignore INLINECOMMENT
    %ignore COMMENTBLOCK
    %ignore WHITESPACE
'''
'''
'''

# Try a sample grammar recognition
l = lark.Lark(grammar, parser='lalr', lexer="contextual")

print("BUILT GRAMMAR")

goodstrs = [
    """
    Compose{
        // Nathan is a nerd
    }
    """,


    """
    /*
    * Testing comment block!
    */
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
    $gp = Measure {
            acousticgrandpiano {
                1/4 a#6;
            }
        }
    Compose{
        $gp
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
        x = l.parse(i)
        #print()
        #print(x)
        #print()
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
