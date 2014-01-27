#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.sax
import sys
import codecs
import re
import cgi
import os
import shutil
import xml_parser as parser


xml_file = sys.argv[1]
meta_file = sys.argv[2]
output_file = sys.argv[3]

# Parsing du fichier xml de la conférence
current_conf = parser.content_handler(xml_file)

# Récupération de l'identifiant du papier
paper_id = re.sub('^.+\/([^\/]+)\.metadata$', '\g<1>', meta_file)

# Récupération des méta-données du papier dans le xml
article_metadata = {}
for article in current_conf.articles:
    if article['id'] == paper_id:
        article_metadata = article
        break

# Stop en cas de problème
if len(article_metadata) == 0:
    print "Erreur, article", paper_id, "non trouvé dans le fichier", xml_file
    sys.exit(0)

# Récupération des informations utiles
titre = article_metadata['titre']
if len(titre) == 0:
    titre = article_metadata['title']
auteurs = ', '.join(article_metadata['auteurs'])

# Complétion du nouveau fichier de méta-données
meta_buffer = 'InfoBegin\n'
meta_buffer += 'InfoKey: Creator\n'
meta_buffer += 'InfoValue: Florian Boudin pour TALN Archives\n'
meta_buffer += 'InfoBegin\n'
meta_buffer += 'InfoKey: Title\n'
meta_buffer += 'InfoValue: ' + titre + '\n'
meta_buffer += 'InfoBegin\n'
meta_buffer += 'InfoKey: Author\n'
meta_buffer += 'InfoValue: ' + auteurs + '\n'
meta_buffer += 'InfoBegin\n'
meta_buffer += 'InfoKey: Producer\n'
meta_buffer += 'InfoValue: Florian Boudin via pdftk\n'

# Lecture du fichier de méta-données pdf
for line in codecs.open(meta_file, 'r', 'utf-8'):
    if not re.search('^Info', line):
         meta_buffer += line

# Ecriture du nouveau fichier de méta-données
handle = codecs.open(output_file, 'w', 'utf-8')
handle.write(meta_buffer)
handle.close()

# print paper_id
# print meta_buffer
# print article_metadata
