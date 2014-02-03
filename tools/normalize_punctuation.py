#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import unicodedata


if len(sys.argv) != 3:
    print "Usage : extract_references.py input output"
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read file
f = codecs.open(input_file, 'r', 'utf-8')
document = ''.join(f.readlines())
f.close()

# Combine accentuated characters
document = unicodedata.normalize('NFKD', document)
document = ''.join(c for i, c in enumerate(document) if c!=' ' or unicodedata.combining(document[i+1])==0)
document = unicodedata.normalize('NFC', document)

# Write the txt file
f = codecs.open(output_file, 'w', 'utf-8')
f.write(document)
f.close()

