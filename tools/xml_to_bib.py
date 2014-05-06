#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Script de conversion des fichiers au format XML vers Bibtex.
    Auteur : Florian Boudin
    Date : 5 mai 2014
    Version : 1
"""

import os
import re
import sys
import codecs
import datetime
import taln_archives_parser as parser
import unidecode

months = { 1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
           7:'July', 8:'August', 9:'September', 10:'October', 11:'November',
           12:'December' }

www = "http://www.atala.org/taln_archives/"

def bibtexify(text):
    """ Fonction pour préparer les champs bibtex à l'affichage."""
    text = re.sub('\&', '\&', text)
    text = re.sub('\{', '\{', text)
    text = re.sub('\}', '\}', text)
    text = re.sub('\$', '\$', text)
    return text

#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """ Fonction principale réalisant les appels. """

    bib_dir = os.path.dirname(sys.argv[1]) + "/bib/"
    main_bib = re.sub('\.xml', '.bib', sys.argv[1])

    # parsing du fichier xml
    parse = parser.content_handler(sys.argv[1])

    # récupère le nom de la conférence et l'année
    conference, year = parse.meta["acronyme"].split("'")

    # récupère les noms des présidents
    editors = []
    for prenom, nom in parse.meta["presidents"]:
        editors.append(nom.strip()+', '+prenom.strip())

    # récupère le titre de la conférence
    conf_title = "Actes de la "+ parse.meta["titre"]
    if conference == "RECITAL":
        conf_title = "Actes des "+ parse.meta["titre"]

    # récupère l'adresse de la conférence
    address = parse.meta["ville"]+", "+parse.meta["pays"]

    # récupère le mois de la conférence
    month = months[int(parse.meta["dateDebut"].split('-')[1])]

    # récupère l'url de la conférence
    conf_url = www + conference.upper() + '/' + conference.upper() + "-" + year

    # ouvre le handler pour l'écriture du bibtext principal
    f1 = codecs.open(main_bib, 'w', 'utf-8')

    # - Print proceedings
    f1.write("@proceedings{"+conference+":"+str(year)+",\n")
    f1.write("  editor    = {"+' and '.join(editors)+"},\n")
    f1.write("  title     = {"+conf_title+"},\n")
    f1.write("  month     = {"+month+"},\n")
    f1.write("  year      = {"+str(year)+"},\n")
    f1.write("  address   = {"+address+"},\n")
    f1.write("  publisher = {Association pour le Traitement Automatique des Langues},\n")
    f1.write("  url       = {"+conf_url+"}\n")
    f1.write("}")

    # - Print inProceedings
    for article in parse.articles:

        # récupère les noms des auteurs
        authors = []
        for prenom, nom in article['auteurs']:
            authors.append(nom.strip()+', '+prenom.strip())

        # constuction de la clé à la ACL anthology
        key = [ re.sub('[-\s]', '', unidecode.unidecode(u.split(', ')[0])).lower() for u in authors ]
        if len(key) > 3:
            key = key[0]+'-EtAl'
        else:
            key = '-'.join(key)
        key += ':'+str(year)+':'+conference

        # récupère le titre de l'article
        title = ""
        language = ""
        extra_title = ""
        if article.has_key("titre"):
            title = article["titre"]
            language = "french"
            if article.has_key("title"):
                extra_title = article["title"]
        else:
            title = article["title"]
            language = "english"

        # construit l'url de l'article
        url = conf_url + "/" + article['id']

        current_bib = "@inproceedings{"+key+",\n"
        current_bib += "  author    = {"+' and '.join(authors)+"},\n"
        current_bib += "  title     = {"+bibtexify(title)+"},\n"
        current_bib += "  booktitle = {"+conf_title+"},\n"
        current_bib += "  month     = {"+month+"},\n"
        current_bib += "  year      = {"+str(year)+"},\n"
        current_bib += "  address   = {"+address+"},\n"
        current_bib += "  publisher = {Association pour le Traitement Automatique des Langues},\n"
        if article.has_key("pages"):
            pages = re.sub("(\d+)-(\d+)", "\g<1>--\g<2>", article["pages"])
            current_bib += "  pages     = {"+pages+"},\n"
        current_bib += "  url       = {"+url+"},\n"

        # ouvre le handler pour l'écriture du bibtext courant
        f2 = codecs.open(bib_dir+article['id']+".bib", 'w', 'utf-8')
        f2.write(current_bib+"}")
        f2.close()

        current_bib += "  language  = {"+language+"},\n"
        if extra_title != "":
            current_bib += "  note      = {"+bibtexify(extra_title)+"},\n"
        if article.has_key("resume"):
            current_bib += "  resume    = {"+bibtexify(article['resume'])+"},\n"
        if article.has_key("abstract"):
            current_bib += "  abstract  = {"+bibtexify(article['abstract'])+"},\n"
        if article.has_key("mots_cles"):
            current_bib += "  motscles  = {"+bibtexify(article['mots_cles'])+"},\n"
        if article.has_key("keywords"):
            current_bib += "  keywords  = {"+bibtexify(article['keywords'])+"},\n"
        current_bib += "}"

        f1.write('\n\n' + current_bib)

    f1.close()
