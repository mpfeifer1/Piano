#!/usr/bin/env python3

from mido import Message, MidiFile, MidiTrack

import lark
from argparse import ArgumentParser
from lark import Lark
import unittest
import sys

import grammar
import ourtests

l = lark.Lark(grammar.getgrammar(), parser='lalr', lexer="contextual")
