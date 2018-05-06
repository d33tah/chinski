#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The goal of this project is to find an answer to the question: how much of
Chinese can I actually know if I restrict myself to KangXi radicals? How could
I quickly improve?
"""

import sys

import zhon.hanzi
import progressbar
import progressbar.widgets as PBW
from cjklib import characterlookup


def zhon_regex_to_items(regex):
    ranges = []
    regex_chrs = list(regex)
    for n, item in enumerate(regex_chrs):
        if item == '-':
            ranges.append((regex_chrs[n-1], regex_chrs[n+1]))
    return [unichr(x) for c1, c2 in ranges for x in range(ord(c1), ord(c2)+1)]


def get_HANZI_CHARACTERS():
    return zhon_regex_to_items(zhon.hanzi.characters)


def get_HANZI_RADICALS_and_variations():
    return zhon_regex_to_items(zhon.hanzi.radicals)


HANZI_CHARACTERS = get_HANZI_CHARACTERS()
HANZI_RADICALS = get_HANZI_RADICALS_and_variations()


def is_made_of_radicals_only(decomposition):
    return all(c in HANZI_RADICALS or c not in HANZI_CHARACTERS
               for c in decomposition)


class Decomposer:

    def __init__(self):
        self.cjk = characterlookup.CharacterLookup('T')

    def decompose(self, c):
        ret = self.cjk.getDecompositionEntries(c)
        if ret:
            for x in ret[0]:
                yield x[0]


def main():
    decomposer = Decomposer()
    print("Loaded %d characters." % len(HANZI_CHARACTERS))
    if not is_made_of_radicals_only(u'我'):
        sys.exit('ERROR: 我 is not made of radicals, wtf?')
    total_characters = len(HANZI_CHARACTERS)
    matching_characters = 0
    pb = progressbar.ProgressBar(widgets=[
        PBW.Counter(), PBW.Bar(), PBW.ETA()
    ])
    for char in pb(set(HANZI_CHARACTERS)):
        decomposition = decomposer.decompose(char)
        if is_made_of_radicals_only(decomposition):
            matching_characters = 1
    print("Matched %d characters out of %d" %
          (matching_characters, total_characters))


if __name__ == '__main__':
    main()
