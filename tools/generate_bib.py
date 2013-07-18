#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.sax
import sys
import codecs
import re
import cgi
import os
import xml_parser as parser
from nltk.corpus import stopwords

def replace_diacritics(text):

    diacritics = [
        (u"é", u"\\'{e}"),
        (u"É", u"\\'{E}"), 
        (u"è", u"\\`{e}"),
        (u"ë", u'\\"{e}'),
        (u"ê", u'\\^{e}'),
        (u"à", u"\\`{a}"),
        (u"á", u"\\'{a}"),
        (u"â", u"\\^{a}"),
        (u"ä", u'\\"{a}'),
        (u"ç", u"\\c{c}"),
        (u"ù", u"\\`{u}"),
        (u"ï", u'\\"{\i}'),
        (u"ì", u'\\`{\i}'),
        (u"î", u'\\^{\i}'),
        (u"ö", u'\\"{o}'),
        (u"ş", u'\\c{s}'),
        (u"š", u'\\v{s}')
    ]
    protected_text = text

    for a, b in diacritics:
        protected_text = re.sub(a, b, protected_text)

    protected_text = re.sub(u"(?u)[’]", "'", protected_text)

    return protected_text

def rm_diacritics(text):
    protected_text = re.sub(u'(?u)[éèëê]', u'e', text)
    protected_text = re.sub(u'(?u)[ïìî]', u'i', protected_text)
    protected_text = re.sub(u'(?u)[ç]', u'c', protected_text)
    protected_text = re.sub(u'(?u)[ù]', u'u', protected_text)
    protected_text = re.sub(u'(?u)[àáäâ]', u'a', protected_text)
    protected_text = re.sub(u'(?u)[ö]', u'o', protected_text)
    protected_text = re.sub(u'(?u)[šş]', u's', protected_text)
    return protected_text

from mako.template import Template
bibTemplate = Template(filename='templates/bibtex.mako_template')

root = '../'
paths = ['TALN/', 'RECITAL/']

################################################################################
# Création des fichiers bibtex de chaque conférence
################################################################################
for path in paths:

    # Nom de la conférence
    conference = re.sub('\/$', '', path)

    # Lister les editions de la conférence
    editions = os.listdir(root+path)

    # Pour toutes le éditions de la conférence
    for edition in editions:

        if not re.search(conference, edition):
            continue

        # Nom du fichier meta
        fichier = root + path + edition + '/' + edition.lower() + '.xml'

        # Chemin du répertoire bibtex
        bib_rep = root + path + edition + '/bibtex/'

        # Création du répertoire bibtex
        if not os.path.exists(bib_rep):
            os.makedirs(bib_rep)

        current_conf = parser.content_handler(fichier)

        # Annee de la conférence
        annee = re.sub('^(\d{4})-.+$', '\g<1>', current_conf.meta['dateDebut'])
        current_conf.meta['annee'] = annee

        for article in current_conf.articles:

            current_bibtex = bib_rep + article['id'] + '.bib'

            ####################################################################
            # Génération de la clé bibtex
            # 1. nom du premier auteur (e.g. boudin)
            # 2. premier mot non vide du titre (e.g. résumé)
            # 3. acronyme de la conférence (e.g. taln)
            # 4. annee de la conférence (e.g. 12 pour 2012)
            ####################################################################
            bibkey = ""

            # 1. nom du premier auteur (e.g. boudin)
            bibkey = article['auteurs'][0].split(' ')[-1]

            # 2. premier mot non vide du titre (e.g. résumé)
            titre = article['title']
            if article['titre'] != "" :
                titre = article['titre']
            mots = re.split('(?iu)\W+', titre.lower())
            mots_vides = set(stopwords.words('french'))

            index = 0
            for i in range(len(mots)):
                if mots[i] in mots_vides or len(mots[i]) < 2:
                    index += 1
                else:
                    break
            bibkey += ':' + mots[index]

            # 3. acronyme de la conférence (e.g. taln)
            bibkey += ':'+re.sub("'\d+", '', current_conf.meta['acronyme'])

            # 4. annee de la conférence (e.g. 12 pour 2012)
            bibkey += str(current_conf.meta['annee'][2:4])
        
            # Mise en minuscules
            bibkey = rm_diacritics(bibkey.lower())

            ####################################################################
            # Néttoyage des accents pour Latex
            ####################################################################

            article['titre'] = replace_diacritics(article['titre'])
            for i in range(len(article['auteurs'])):
                article['auteurs'][i] = replace_diacritics(article['auteurs'][i])

            current_conf.meta['titre'] = replace_diacritics(current_conf.meta['titre'])
            current_conf.meta['ville'] = replace_diacritics(current_conf.meta['ville'])
            current_conf.meta['pays'] = replace_diacritics(current_conf.meta['pays'])

            # Ajout d'un double tiret pour les numéros de pages
            if article['pages'] != "":
                article['pages'] = re.sub('^(\d+)-(\d+)$', '\g<1>--\g<2>', article['pages'])

            handle = codecs.open(current_bibtex, 'w', 'utf-8')
            handle.write(bibTemplate.render(article=article, meta=current_conf.meta, bibkey=bibkey))
            handle.close()

