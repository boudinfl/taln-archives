#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.sax
import sys
import codecs
import re
import cgi
import os
import shutil
import taln_archives_parser as parser

from mako.template import Template
editionTemplate = Template(filename='templates/edition.html')
indexTemplate = Template(filename='templates/index.html')
paperTemplate = Template(filename='templates/article.html')
rechTemplate = Template(filename='templates/recherche.html')
confTemplate = Template(filename='templates/conference.html')

root = '../'
conf_paths = ['TALN/', 'RECITAL/']
# conf_paths = ['RECITAL/']
ws_dir = 'ateliers/'
ws_paths = ['2015/']

output = "../www/"
conferences = {}
ateliers = {}
nb_pdfs = 0
nb_papers = 0
mots_cles = {}
auteurs = {}

################################################################################

################################################################################
# Création du fichier html de chaque conférence
################################################################################
for path in conf_paths:

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

        # Création du nom du fichier html de la conférence
        fichier_html = rep_edition + 'index.html'

        # Parsing du fichier xml de la conférence
        current_conf = parser.content_handler(fichier)

        # Récupération de l'année de la conférence à partir de la date de début
        annee = re.sub('^(\d{4})-.+$', '\g<1>', current_conf.meta['dateDebut'])

        # Ajout de la conférence (eg TALN pour TALN'2010) dans les meta
        current_conf.meta['conference'] = re.sub('\'?(\d{4})$', '', \
                                             current_conf.meta['acronyme'])

        current_conf.meta['atelier'] = False 

        ########################################################################
        # Copie des fichiers d'actes
        src_dir = root + path + edition + '/actes/'
        for fichier_pdf in os.listdir(src_dir):
            if re.search('\.pdf$', fichier_pdf):
                shutil.copy(src_dir+fichier_pdf, rep_edition+fichier_pdf)

        ########################################################################
        # Copie des fichiers bibtex
        src_dir = root + path + edition +'/bib/'
        for fichier_bibtex in os.listdir(src_dir):
            if re.search('\.bib$', fichier_bibtex):
                shutil.copy(src_dir+fichier_bibtex, rep_edition+fichier_bibtex)


        # Ajout de la conférence au conteneur des différentes conférences pour
        # les liens de la page d'acceuil
        info = {}
        info['annee'] = annee
        info['path'] =  path + edition + '/index.html'
        info['lieu'] = current_conf.meta['ville'] +' (' \
                       + current_conf.meta['pays'] + ')'
        conferences[conference].append(info)

        # Comptage du nombre de papiers dans TALN Archives
        nb_papers += len(current_conf.articles)
        
        # Extraction des mots clés et des auteurs de la base
        for a in range(len(current_conf.articles)):
            article = current_conf.articles[a]
            lien_article = path + edition + "/" + article['id'] + '.pdf'

            if article['mots_cles'] != "":
                article_keywords = article['mots_cles'].lower().split(',')

                titre = ""
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

                for prenom, nom in article['auteurs']:
                    auteur = nom+', '+prenom
                    if not auteurs.has_key(auteur):
                        auteurs[auteur] = []
                    auteurs[auteur].append(article_info)

            # Ajout du lien vers le fichier pdf
            current_conf.articles[a]['pdf'] = False
            if os.path.isfile(output+lien_article):
                current_conf.articles[a]['pdf'] = True
                nb_pdfs += 1

            ####################################################################
            # Création du fichier html de l'article
            ####################################################################
            fichier_article = rep_edition+article['id']+'.html'
            handle = codecs.open(fichier_article, 'w', 'utf-8')
            handle.write(paperTemplate.render(meta=current_conf.meta, \
                         article=article))
            handle.close()

        ########################################################################
        # Création du fichier html de la page principale
        ########################################################################
        handle = codecs.open(fichier_html, 'w', 'utf-8')
        handle.write(editionTemplate.render(meta=current_conf.meta, \
            articles=current_conf.articles))
        handle.close()

################################################################################

################################################################################
# Création du fichier html de chaque atelier
################################################################################
for path in ws_paths:

    # Année de l'atelier
    annee_atelier = re.sub('\/$', '', path)

    # Lister les ateliers de l'année
    noms_ateliers = os.listdir(root+ws_dir+path)

    # memoriser les ateliers de l'année
    ateliers[annee_atelier] = []

    # Pour toutes le éditions de la conférence
    for atelier in noms_ateliers:

        if not re.search('^[A-Za-z0-9]+$', atelier):
            continue

        # Nom du fichier meta
        fichier = root + ws_dir + path + atelier + '/' 
        fichier += atelier.lower() + '-' + annee_atelier + '.xml'
        
        # Nom du répertoire de l'atelier
        rep_atelier = output + ws_dir + path + atelier + "/"

        # Création du répertoire de l'atelier
        if not os.path.exists(rep_atelier):
            os.makedirs(rep_atelier)

        # Création du nom du fichier html de l'atelier
        fichier_html = rep_atelier + 'index.html'

        # Parsing du fichier xml de l'atelier
        current_ws = parser.content_handler(fichier)

        # Récupération de l'année de l'atelier à partir de la date de début
        annee = re.sub('^(\d{4})-.+$', '\g<1>', current_ws.meta['dateDebut'])

        current_ws.meta['conference'] = annee
        # current_ws.meta['acronyme'] = current_ws.meta['conference']
        

        # Ajout de l'atelier (eg TALN pour TALN'2010) dans les meta
        # current_ws.meta['conference'] = re.sub('\'?(\d{4})$', '', \
        #                                      current_ws.meta['acronyme'])
        current_ws.meta['atelier'] = True 

        ########################################################################
        # Copie des fichiers d'actes
        src_dir = root + ws_dir + path + atelier +'/actes/'
        for fichier_pdf in os.listdir(src_dir):
            if re.search('\.pdf$', fichier_pdf):
                shutil.copy(src_dir+fichier_pdf, rep_atelier+fichier_pdf)

        ########################################################################
        # Copie des fichiers bibtex
        src_dir = root + ws_dir + path + atelier +'/bib/'
        for fichier_bibtex in os.listdir(src_dir):
            if re.search('\.bib$', fichier_bibtex):
                shutil.copy(src_dir+fichier_bibtex, rep_atelier+fichier_bibtex)


        # Ajout de la conférence au conteneur des différentes conférences pour
        # les liens de la page d'acceuil
        info = {}
        info['annee'] = annee
        info['atelier'] = atelier
        info['path'] = ws_dir + path + atelier + '/index.html'
        info['lieu'] = current_ws.meta['ville'] +' (' \
                       + current_ws.meta['pays'] + ')'
        ateliers[annee_atelier].append(info)

        # Comptage du nombre de papiers dans TALN Archives
        nb_papers += len(current_ws.articles)
        
        # Extraction des mots clés et des auteurs de la base
        for a in range(len(current_ws.articles)):
            article = current_ws.articles[a]
            lien_article = ws_dir + path + atelier + "/" + article['id'] + '.pdf'

            if article['mots_cles'] != "":
                article_keywords = article['mots_cles'].lower().split(',')

                titre = ""
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

                for prenom, nom in article['auteurs']:
                    auteur = nom+', '+prenom
                    if not auteurs.has_key(auteur):
                        auteurs[auteur] = []
                    auteurs[auteur].append(article_info)

            # Ajout du lien vers le fichier pdf
            current_ws.articles[a]['pdf'] = False
            if os.path.isfile(output+lien_article):
                current_ws.articles[a]['pdf'] = True
                nb_pdfs += 1

            ####################################################################
            # Création du fichier html de l'article
            ####################################################################
            fichier_article = rep_atelier+article['id']+'.html'
            handle = codecs.open(fichier_article, 'w', 'utf-8')
            handle.write(paperTemplate.render(meta=current_ws.meta, \
                         article=article))
            handle.close()

        ########################################################################
        # Création du fichier html de la page principale
        ########################################################################
        handle = codecs.open(fichier_html, 'w', 'utf-8')
        handle.write(editionTemplate.render(meta=current_ws.meta, \
            articles=current_ws.articles))
        handle.close()

################################################################################


################################################################################
# Création du fichier html de la page principale
################################################################################
handle = codecs.open(output+'index.html', 'w', 'utf-8')
handle.write(indexTemplate.render( conferences=conferences,
                                   ateliers=ateliers,
                                   nb_papers=nb_papers, 
                                   nb_pdfs=nb_pdfs))
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

################################################################################
# Création des fichiers html des conférences
################################################################################
for conference in conferences:
    lien_conference = output + conference + "/index.html"
    for i in range(len(conferences[conference])):
        conferences[conference][i]['path'] = \
                 re.sub(conference+"/", "", conferences[conference][i]['path'])

    handle = codecs.open(lien_conference, 'w', 'utf-8')
    handle.write(confTemplate.render(editions=conferences[conference],
                                     conference=conference))
    handle.close()

for atelier in ateliers:
    lien_conference = output + ws_dir + atelier + "/index.html"
    for i in range(len(ateliers[atelier])):
        ateliers[atelier][i]['path'] = \
                 re.sub(ws_dir+atelier+"/", "", ateliers[atelier][i]['path'])

    handle = codecs.open(lien_conference, 'w', 'utf-8')
    handle.write(confTemplate.render(editions=ateliers[atelier],
                                     conference=atelier,
                                     atelier=True))
    handle.close()


