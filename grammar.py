from mido import Message, MidiFile, MidiTrack

import lark
from argparse import ArgumentParser
from lark import Lark
import unittest
import sys

grammar = r'''
    start: compose
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
    compose: digit | accidental | comment | number | notename
    notename: ("a".."g" | "A".."G") accidental? number
    comment: "//"
    lhs: NAME
        | compose
    number: digit+

    %import common.CNAME -> NAME
    %import common.WS_INLINE

    %ignore WS_INLINE
'''

'''
    start: lhs "=" rhs
    rhs: composeitems
        | instrument
        | instrumentation
        | note
        | tuplet
        | chord
        | tempo
        | timesig
        | inlinedynamic
        | dynamic
'''
# Try a sample grammar recognition
l = lark.Lark(grammar)

print("BUILT GRAMMAR")

goodstrs = [
    "5",
    "5\t5",
    "1 2",
    "1 ",
    " 1",
    "\t67",
    "// hello",
    "A#2",
    "ab3",
    "// hello"
]

badstrs = [
    "INVALID%$&",
    "h#4"
]

print("~~~~~~~GOOD~~~~~~~~")
for i in goodstrs:
    print(i)
    try:
        l.parse(i)
        print("correct")
    except:
        print("INCORRECT - didn't accept")
    print()

print("~~~~~~~BAD~~~~~~~~")
for i in badstrs:
    print(i)
    try:
        l.parse(i)
        print("INCORRECT - accepted")
    except:
        print("correct")
    print()
