from __future__ import print_function
import os
import sys
import re
import logging
import unicodedata
from codecs import open
from random import shuffle, randint, choice

replacement_pattern = re.compile(ur'\$\{(?P<token>[^}]+)\}')

unicode_min, unicode_max = 0, 0x10ffff
unicode_cat_blacklist = ['Mn', 'Mc', 'Me', 'Cc', 'Cf', 'Cs', 'Co', 'Cn']

profile = {}

with open('profile.properties', encoding='utf-8') as infile:
    for line in infile:
        key, value = line.strip().split('=')
        profile[key] = value

adjectives = []
people = []

def load_words(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read().splitlines()
    else:
        print(filename + ' not found. Generate it.')
        sys.exit(1)

adjectives = load_words('adjectives.txt')

def _character():
    while True:
        i = randint(unicode_min, unicode_max)
        c = unichr(i)
        if unicodedata.category(c) not in unicode_cat_blacklist:
            return c

def _indefinite_adjective():
    adj = _adjective()
    article = 'an' if adj.lower()[0] in 'aeiou' else 'a'
    return '%s %s' % (article, adj)

def _adjective():
    return choice(adjectives)

def _fix_capitalization(text, location):
    return text[0].upper() + text[1:] if location == 0 else text

def _dispatch(match):
    res = globals()['_%s' % match.group('token')]()
    return _fix_capitalization(res, match.start())

def randomize(text):
    return replacement_pattern.sub(_dispatch, text) if text else ''

def randomized_profile():
    return {key: randomize(value) for key, value in profile.iteritems()}

def main():
    print('\n'.join(['%s=%s' % (k, v) for k, v in randomized_profile().iteritems()]))


if __name__ == '__main__':
    import sys
    if '-v' in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
    main()
