#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import codecs
import unicodedata


if len(sys.argv) != 3:
    print "Usage : extract_references.py input output"
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

document = []

for line in codecs.open(input_file, 'r', 'utf-8'):

    line = line.strip()

    # remove 2013 footer line
    if re.search(u'(?i)^\d+.+ATALA$', line):
        # print "----> delete", line
        continue

    # remove 2013 header line
    elif re.search(u'(?i)TALN-R[ÉE]CITAL 2013, 17-21 ?[JI]uin, Les Sables d[’\']Olonne', line):
        # print "----> delete", line
        continue
        
    # remove 2012 footer 1
    elif re.search(u'(?i)Actes de la conf[ée]rence conjointe JEP-TALN-RECITAL 2012, .+\d+,?$', line):
        # print "----> delete", line
        continue
        
    # remove 2012 footer 2
    elif re.search(u'(?i)Grenoble, 4 au 8 juin 2012.+2012 ATALA \& AFCP', line):
        # print "----> delete", line
        continue
        
    # remove header 2011
    elif re.search(u'(?i)TALN 2011, Montpellier, 27 juin.+1er juillet ?2011', line):
        # print "----> delete", line
        continue
        
    # remove header 2010
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2010.+Montr(é|é|e)al, 19.+23 ?juillet 2010', line):
        # print "----> delete", line
        continue
        
    # remove header 2009
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2009.+Senlis, 24.+26 ?juin 2009', line):
        # print "----> delete", line
        continue
        
    # remove header 2008
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2008.+Avignon, 9.+13 ?juin 2008', line):
        # print "----> delete", line
        continue
        
    # remove header 2007
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2007.+Toulouse, 5.+8 ?juin 2007', line):
        # print "----> delete", line
        continue
        
    # remove header 2005
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2005.+Dourdan, 6.+10 ?juin 2005', line):
        # print "----> delete", line
        continue
        
    # remove header 2004
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2004.+F(è|é|e)s, 19.+21 ?avril 2004', line):
        # print "----> delete", line
        continue
        
    # remove header 2003
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2003.+Batz.+sur.+Mer, 11.+14 ?juin 2003', line):
        # print "----> delete", line
        continue
        
    # remove header 2002
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2002.+Nancy, 24.+27 ?juin 2002', line):
        # print "----> delete", line
        continue
        
    # remove header 2001
    elif re.search(u'(?i)(TALN|RECITAL|RÉCITAL) 2001.+Tours, 2.+5 ?juillet 2001', line):
        # print "----> delete", line
        continue
        
    elif re.search(u'^[^\w]$', line):
        # print "----> delete", line
        continue
        
    else:
        document.append(line)

# create document buffer
document = u'\n'.join(document)

# remove double lines
document = re.sub(u'\n{3,}', u'\n', document)

# combining diacritics
if re.search(u'´e', document):

    # print '---> bad diacritics for', input_file

    # Combine accentuated characters
    document = unicodedata.normalize('NFKD', document)
    document = ''.join(c for i, c in enumerate(document) if c!=' ' or unicodedata.combining(document[i+1])==0)
    # document = unicodedata.normalize('NFC', document)

    # document = re.sub(u'(^| )e´ ', u'é', document)
    document = re.sub(u'(?i)́e', u'é', document)
    document = re.sub(u'(?i)(^|\s)é ', u' é', document)
    document = re.sub(u'(?i)a`', u'à', document)
    document = re.sub(u'(?i)`a', u'à', document)
    document = re.sub(u'(?i)`e', u'è', document)
    document = re.sub(u'(?i)e`', u'è', document)
    document = re.sub(u'(?i)e[ˆ^]', u'ê', document)
    document = re.sub(u'(?i)o[ˆ^]', u'ô', document)
    document = re.sub(u'(?i)i[ˆ^]', u'î', document)
    document = re.sub(u'(?i)ˆı', u'î', document)
    document = re.sub(u'(?i)ˆe', u'ê', document)
    document = re.sub(u'(?i)ˆo', u'ô', document)
    document = re.sub(u'(?i)ç', u'ç', document)


# Write the txt file
f = codecs.open(output_file, 'w', 'utf-8')
f.write(document)
f.close()



# # Read file
# f = codecs.open(input_file, 'r', 'utf-8')
# document = ''.join(f.readlines())
# f.close()

# # Combine accentuated characters
# document = unicodedata.normalize('NFKD', document)
# document = ''.join(c for i, c in enumerate(document) if c!=' ' or unicodedata.combining(document[i+1])==0)
# document = unicodedata.normalize('NFC', document)



