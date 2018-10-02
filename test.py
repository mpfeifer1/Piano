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
    compose: digit | accidental | comment
    comment: "//"

    %import common.WS_INLINE
    %ignore WS_INLINE
'''

# Try a sample grammar recognition
l = lark.Lark(grammar)
strs = [
    "5",
    "INVALID%$&",
    "5\t5",
    "1 2",
    "1 ",
    " 1",
    "\t6",
    "// hello"
]

for i in strs:
    print(i)
    try:
        print(l.parse(i).pretty())
    except:
        print("Didn't work")
    print()
