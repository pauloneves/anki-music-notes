#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import popen2
import os
from string import Template

LY_NOTE = Template(r"""\version "2.14.1"
\include "croped-paper.ly"
\include "english.ly"
\score {
  \new Staff \with {
\remove "Time_signature_engraver"
\clef $clef
}
   $note$octave
}
""")

defaultNoteOctave = 3
#clef: treble|bass

def getOutputPath(note, octave):
    path = os.path.join('generated', note.upper() + str(octave))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def genLilyScore(clef, note, octave):
    diffOctave = octave - 3
    symbolOctave = "'"
    if diffOctave < 0:
        symbolOctave = ","
        diffOctave = abs(diffOctave)
    return LY_NOTE.substitute(clef=clef, note=note, octave=(symbolOctave * diffOctave))


def genScore(clef, note, octave):
    lilyScore =  genLilyScore(clef, note, octave)

    outputFile = os.path.join(getOutputPath(note, octave),
                              clef+note.upper()+str(octave))
    cmd = 'lilypond -s -dbackend=eps -dresolution=300 --png ' + \
          '-o ' + outputFile + \
          ' -'
    stdout, stdin = popen2.popen2(cmd)

    stdin.write(lilyScore)
    stdin.close()
