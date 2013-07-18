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

from mako.template import Template
confTemplate = Template(filename='templates/conference.mako_template')
mainTemplate = Template(filename='templates/main.mako_template')
rechTemplate = Template(filename='templates/recherche.mako_template')

root = '../'
paths = ['TALN/', 'RECITAL/']
output = "../www/"
conferences = {}
nb_papers = 0
mots_cles = {}
auteurs = {}

################################################################################

################################################################################
# Création du fichier html de chaque conférence
################################################################################
for path in paths:

    # Nom de la conférence
    conference = re.sub('\/$', '', path)

    # Lister les editions de la conférence
    editions = os.listdir(root+path)

    # memoriser les éditions de la conférences
    conferences[conference] = []

    # Pour toutes le éditions de la conférence
    for edition in editions:

        if not re.search(conference, edition):
            continue

        # Nom du fichier meta
        fichier = root + path + edition + '/' + edition.lower() + '.xml'

        # Nom du répertoire de la conférence
        rep_edition = output + path + edition + "/"

        # Création du répertoire de l'édition
        if not os.path.exists(rep_edition):
            os.makedirs(rep_edition)

        # fichier html de la conférence
        fichier_html = rep_edition + '/index.html'

        current_conf = parser.content_handler(fichier)

        annee = re.sub('^(\d{4})-.+$', '\g<1>', current_conf.meta['dateDebut'])
        lien = path + edition + '/index.html'
        chemin_actes = path + edition + '/actes/'
        chemin_bibtex = path + edition + '/bibtex/'

        # Copie des fichiers d'actes
        src_dir = root + path + edition +'/actes/'
        dst_dir = output + chemin_actes
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)

        # Copie des fichiers bibtex
        src_dir = root + path + edition +'/bibtex/'
        dst_dir = output + chemin_bibtex
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)

        conferences[conference].append((annee, lien))

        handle = codecs.open(fichier_html, 'w', 'utf-8')
        handle.write(confTemplate.render(meta=current_conf.meta, \
            articles=current_conf.articles))
        handle.close()

        nb_papers += len(current_conf.articles)

        # Extraction des mots clés et des auteurs de la base
        for article in current_conf.articles:
            if article['mots_cles'] != "":
                article_keywords = article['mots_cles'].lower().split(',')

                titre = ""
                lien_article = chemin_actes+article['id']+'.pdf'
                if article['titre'] != "":
                    titre = article['titre']
                else:
                    titre = article['title']

                article_info = (article['id'], titre, lien_article)

                for i in range(len(article_keywords)):
                    keyword = article_keywords[i].strip()
                    if not mots_cles.has_key(keyword):
                        mots_cles[keyword] = []
                    mots_cles[keyword].append(article_info)

                for auteur in article['auteurs']:
                    if not auteurs.has_key(auteur):
                        auteurs[auteur] = []
                    auteurs[auteur].append(article_info)

################################################################################

################################################################################
# Création du fichier html de la page principale
################################################################################
handle = codecs.open(output+'index.html', 'w', 'utf-8')
handle.write(mainTemplate.render(conferences=conferences, nb_papers=nb_papers))
handle.close()
################################################################################

################################################################################
# Création du fichier html de la recherche par mots clés
################################################################################
handle = codecs.open(output+'mots_cles.html', 'w', 'utf-8')
handle.write(rechTemplate.render(mode_recherche=u"mots clés", dict=mots_cles))
handle.close()
################################################################################

################################################################################
# Création du fichier html de la recherche par auteurs
################################################################################
handle = codecs.open(output+'auteurs.html', 'w', 'utf-8')
handle.write(rechTemplate.render(mode_recherche=u"auteurs", dict=auteurs))
handle.close()
################################################################################


