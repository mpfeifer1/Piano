#!/usr/bin/env python3

from lark import Lark
from mido import Message, MidiFile, MidiTrack
from argparse import ArgumentParser

import unittest
import lark
import sys

import grammar
import semantic
import ourtests
import flags

inputflags = flags.getcommandlineargs()
print(inputflags)

with open(inputflags['piano_file'], 'r') as inputfile:
    data = inputfile.read()

l = lark.Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")
tree = l.parse(data);
result = semantic.analyze(tree)
