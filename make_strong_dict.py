#!/usr/bin/env python3

import argparse
import sys
#import sqlite3

from utils import (
    load_yaml, load_wordset, get_morphgnt, parse_verse_ranges)

argparser = argparse.ArgumentParser()
argparser.add_argument("verses", help="verses to cover (e.g. 'John 18:1-11')")
argparser.add_argument("--exclude", help="exclusion list file")
argparser.add_argument(
    "--lexicon", dest="lexemes",
    default="../morphological-lexicon/lexemes.yaml",
    help="path to morphological-lexicon lexemes.yaml file "
    "(defaults to ../morphological-lexicon/lexemes.yaml)")
argparser.add_argument(
    "--output", dest="output",
    default=sys.stdout,
    help="output (defaults to standard output)")

args = argparser.parse_args()

verses = parse_verse_ranges(args.verses)

if args.exclude:
    exclusions = load_wordset(args.exclude)
else:
    exclusions = set()

lexemes = load_yaml(args.lexemes)

output = args.output

strong_dict = dict()


for (lemma, metadata) in lexemes.items():
    if lemma not in exclusions:
        assert metadata["strongs"] not in strong_dict
        strong_dict[metadata["strongs"]] = lemma

for entry in get_morphgnt(verses):
    pass
#     if entry[0] == "WORD":
#         lemma = entry[1]["lemma"]
#         if lemma not in exclusions:
#             if "strongs" in lexemes[lemma]:
#                 assert lexemes[lemma]["strongs"] not in strong_dict, "lemma %r with Strong number % is not the only lemma with such Strong number - see lemma %r" % (lemma, lexemes[lemma]["strongs"], strong_dict[lexemes[lemma]["strongs"]])
#                 strong_dict[lexemes[lemma]["strongs"]] = lemma

for (strong, lemma) in strong_dict.items():
    print("{}: {}".format(strong, lemma, file=output))
