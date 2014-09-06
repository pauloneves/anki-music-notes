#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
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
# clef: treble|bass

solfege = {
    'c': 'do',
    'd': 're',
    'e': 'mi',
    'f': 'fa',
    'g': 'sol',
    'a': 'la',
    'b': 'si',
}


def gen_output_path(note, octave, level):
    path = os.path.join('generated', level, note.upper() + str(octave))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def gen_lily_score(clef, note, octave):
    diff_octave = octave - 3
    symbol_octave = "'"
    if diff_octave < 0:
        symbol_octave = ","
        diff_octave = abs(diff_octave)
    return LY_NOTE.substitute(clef=clef, note=note, octave=(symbol_octave * diff_octave))


def gen_score(clef, note, octave, level):
    lily_score = gen_lily_score(clef, note, octave)

    output_file = os.path.join(gen_output_path(note, octave, level),
                               clef + note.upper() + str(octave))
    cmd = 'lilypond -s -dbackend=eps -dresolution=300 --png ' + \
          '-o ' + output_file + \
          ' -'
    pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE).stdin
    pipe.write(lily_score)
    pipe.close()


def link_other_files(note, octave, level):
    mp3 = 'short-Piano.ff.{note}{octave}.mp3'.format(note=note.upper(),
                                                     octave=str(octave))
    dest = os.path.join(gen_output_path(note, octave, level), mp3)
    if not os.path.exists(dest):
        os.link(os.path.join('audio-notes', mp3), dest)

    keyboard = 'keyboard-{solfege}.png'.format(solfege=solfege[note])
    dest = os.path.join(gen_output_path(note, octave, level), keyboard)
    if not os.path.exists(dest):
        os.link(keyboard, dest)


def gen_card(clef, note, octave, level):
    gen_score(clef, note, octave, level)
    link_other_files(note, octave, level)


def gen_basic_files():
    level = 'basic'
    clef = 'treble'
    for note in solfege.keys():
        for octave in (4, 5):
            gen_card(clef, note, octave, level)
    gen_card(clef, 'c', 6, level)

    clef = 'bass'
    for note in solfege.keys():
        for octave in (2, 3):
            gen_card(clef, note, octave, level)
    gen_card(clef, 'c', 4, level)

if __name__ == '__main__':
    gen_basic_files()
