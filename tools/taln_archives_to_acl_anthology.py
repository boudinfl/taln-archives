#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Script de conversion des actes au format TALN Archives vers celui utilisé
    par l'ACL Anthology
    Auteur : Florian Boudin
    Date : 2 juin 2014
    Version : 1
"""

import os
import re
import sys
import codecs
import datetime
import taln_archives_parser as parser
import unidecode
import shutil

months = { 1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
           7:'July', 8:'August', 9:'September', 10:'October', 11:'November',
           12:'December' }

volumes = [ (u'long', 'Long Papers'), 
            (u'court', 'Short Papers'),
            (u'poster', 'Posters'),
            (u'démonstration', 'System Demonstrations'),
            (u'invite', 'Invited Conferences') ]

www = "http://www.aclweb.org/anthology/"

def bibtexify(text):
    """ Fonction pour préparer les champs bibtex à l'affichage."""
    text = re.sub('\&', '\&', text)
    text = re.sub('\{', '\{', text)
    text = re.sub('\}', '\}', text)
    text = re.sub('\$', '\$', text)
    return text

def xmlify(text):
    """ Fonction pour préparer les champs xml."""
    text = re.sub('&', '&amp;', text)
    text = re.sub('<', '&lt;', text)
    text = re.sub('>', '&gt;', text)
    return text


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """ Fonction principale réalisant les appels. """

    # Fichier de meta-données
    TALN_xml = sys.argv[1]

    # Répertoire TALN
    TALN_dir = os.path.dirname(TALN_xml)

    # Répertoire de sortie
    output_dir = sys.argv[2]

    print TALN_dir
    print TALN_xml

    # Fichier de meta-données de RECITAL (si il existe)
    RECITAL_parse = None
    RECITAL_xml = None
    if len(sys.argv) > 3:
        RECITAL_xml = sys.argv[3]
        RECITAL_parse = parser.content_handler(RECITAL_xml)

    # bib_dir = os.path.dirname(sys.argv[1]) + "/bib/"
    # main_bib = re.sub('\.xml', '.bib', sys.argv[1])

    # parsing du fichier xml
    TALN_parse = parser.content_handler(TALN_xml)

    # Nom de la conférence et l'année
    conference, year = TALN_parse.meta["acronyme"].split("'")

    # Noms des présidents
    editors = TALN_parse.meta["presidents"]

    # Titre de la conférence
    conf_title = "Proceedings of "+ conference + " " + year

    # Adresse de la conférence
    address = TALN_parse.meta["ville"]+", "+TALN_parse.meta["pays"]

    # Mois de la conférence
    month = months[int(TALN_parse.meta["dateDebut"].split('-')[1])]

    # Identifiant ACL Anthology
    ACL_id = 'F' + year[-2:]

    # Url de la conférence
    conf_url = www + ACL_id

    # Création du répertoire
    if not os.path.exists(output_dir+"/"+ACL_id):
        os.makedirs(output_dir+"/"+ACL_id)

    xml_file = output_dir+"/"+ACL_id+"/"+ACL_id+".xml"

    # ouvre le handler pour l'écriture du xml
    f1 = codecs.open(xml_file, 'w', 'utf-8')

    # - Print proceedings
    f1.write(u'<?xml version="1.0" encoding="UTF-8"?>\n')
    f1.write(u'<volume id="'+ACL_id+'">\n')

    # Pour chaque volume
    vol_number = 0
    for vol_type, vol_title in volumes:

        # Articles correspondant à ce volume
        vol_articles = [u for u in TALN_parse.articles if u["type"] == vol_type]

        if len(vol_articles):
            vol_number += 1
            volume = conf_title +' (Volume '+ str(vol_number)+': '+vol_title+')'
            first_id = vol_number*1000

            # Print Volume paper
            f1.write(u'\t<paper id="'+str(first_id)+'">\n')
            f1.write(u'\t\t<title>'+volume+'</title>\n')
            for prenom, nom in editors:
                f1.write(u'\t\t<editor><first>'+prenom+'</first><last>'+nom+'</last></editor>\n')
            f1.write(u'\t\t<month>'+month+'</month>\n')
            f1.write(u'\t\t<year>'+year+'</year>\n')
            f1.write(u'\t\t<address>'+address+'</address>\n')
            f1.write(u'\t\t<publisher>Association pour le Traitement Automatique des Langues</publisher>\n')
            f1.write(u'\t\t<url>'+conf_url+'-'+str(vol_number)+'</url>\n')
            f1.write(u'\t\t<bibtype>book</bibtype>\n')
            f1.write(u'\t\t<bibkey>'+conference+year+':'+vol_type+':'+year+'</bibkey>\n')
            f1.write(u'\t</paper>\n')

            # Print each article
            for article in vol_articles:

                # Identifiant ACL anthology
                acl_id = first_id + int(article['id'][-3:])

                pdf_taln_archives = TALN_dir+'/actes/'+article['id']+'.pdf'
                pdf_acl_format = output_dir + '/' + ACL_id + '/' + ACL_id + '-' + str(acl_id) + '.pdf'
                bib_file = output_dir + '/' + ACL_id + '/' + ACL_id + '-' + str(acl_id) + '.bib'

                if os.path.exists(pdf_taln_archives):
                    shutil.copy(pdf_taln_archives, pdf_acl_format)

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
                if article["title"] != '':
                    title = article["title"]
                    if article["titre"] != '':
                        title += ' ('+article["titre"]+')'
                else:
                    title = article["titre"]
                title += (' [in French]')

                # construit l'url de l'article
                url = conf_url + "/" + article['id']


                f1.write(u'\t<paper id="'+str(acl_id)+'">\n')
                f1.write(u'\t\t<title>'+xmlify(title)+'</title>\n')
                for prenom, nom in article['auteurs']:
                    f1.write(u'\t\t<author><first>'+prenom+'</first><last>'+nom+'</last></author>\n')
                f1.write(u'\t\t<booktitle>'+volume+'</booktitle>\n')
                f1.write(u'\t\t<month>'+month+'</month>\n')
                f1.write(u'\t\t<year>'+year+'</year>\n')
                f1.write(u'\t\t<address>'+address+'</address>\n')
                f1.write(u'\t\t<publisher>Association pour le Traitement Automatique des Langues</publisher>\n')
                if article["pages"] != "":
                    f1.write(u'\t\t<pages>'+article["pages"]+'</pages>\n')
                f1.write(u'\t\t<url>'+conf_url+'-'+str(acl_id)+'</url>\n')
                f1.write(u'\t\t<bibtype>inproceedings</bibtype>\n')
                f1.write(u'\t\t<bibkey>'+key+'</bibkey>\n')
                f1.write(u'\t</paper>\n')

                f2 = codecs.open(bib_file, 'w', 'utf-8')
                f2.write("@inproceedings{"+key+",\n")
                f2.write("  author    = {"+' and '.join(authors)+"},\n")
                f2.write("  title     = {"+bibtexify(title)+"},\n")
                f2.write("  booktitle = {"+volume+"},\n")
                f2.write("  month     = {"+month+"},\n")
                f2.write("  year      = {"+year+"},\n")
                f2.write("  address   = {"+address+"},\n")
                f2.write("  publisher = {Association pour le Traitement Automatique des Langues},\n")
                if article["pages"] != "":
                    pages = re.sub("(\d+)-(\d+)", "\g<1>--\g<2>", article["pages"])
                    f2.write("  pages     = {"+pages+"},\n")
                f2.write("  url       = {"+conf_url+'-'+str(first_id)+"}\n")
                f2.write("}")
                f2.close()


    # Pour le Volume de RECITAL
    if RECITAL_parse is not None:

        vol_number += 1
        first_id = vol_number*1000

        # Nom de la conférence et l'année
        conference, year = RECITAL_parse.meta["acronyme"].split("'")

        # Noms des présidents
        editors = RECITAL_parse.meta["presidents"]

        # Titre de la conférence
        volume = "Proceedings of "+ conference + " " + year

        # Print Volume paper
        f1.write(u'\t<paper id="'+str(first_id)+'">\n')
        f1.write(u'\t\t<title>'+volume+'</title>\n')
        for prenom, nom in editors:
            f1.write(u'\t\t<editor><first>'+prenom+'</first><last>'+nom+'</last></editor>\n')
        f1.write(u'\t\t<month>'+month+'</month>\n')
        f1.write(u'\t\t<year>'+year+'</year>\n')
        f1.write(u'\t\t<address>'+address+'</address>\n')
        f1.write(u'\t\t<publisher>Association pour le Traitement Automatique des Langues</publisher>\n')
        f1.write(u'\t\t<url>'+conf_url+'-'+str(vol_number)+'</url>\n')
        f1.write(u'\t\t<bibtype>book</bibtype>\n')
        f1.write(u'\t\t<bibkey>'+conference+year+':'+year+'</bibkey>\n')
        f1.write(u'\t</paper>\n')

        # Print each article
        for article in RECITAL_parse.articles:

            # Identifiant ACL anthology
            first_id += 1

            pdf_taln_archives = os.path.dirname(RECITAL_xml)+'/actes/'+article['id']+'.pdf'
            pdf_acl_format = output_dir + '/' + ACL_id + '/' + ACL_id + '-' + str(first_id) + '.pdf'
            bib_file = output_dir + '/' + ACL_id + '/' + ACL_id + '-' + str(first_id) + '.bib'


            if os.path.exists(pdf_taln_archives):
                shutil.copy(pdf_taln_archives, pdf_acl_format)

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
            if article["title"] != '':
                title = article["title"]
                if article["titre"] != '':
                    title += ' ('+article["titre"]+')'
            else:
                title = article["titre"]
            title += (' [in French]')

            # construit l'url de l'article
            url = conf_url + "/" + article['id']

            f1.write(u'\t<paper id="'+str(first_id)+'">\n')
            f1.write(u'\t\t<title>'+xmlify(title)+'</title>\n')
            for prenom, nom in article['auteurs']:
                f1.write(u'\t\t<author><first>'+prenom+'</first><last>'+nom+'</last></author>\n')
            f1.write(u'\t\t<booktitle>'+volume+'</booktitle>\n')
            f1.write(u'\t\t<month>'+month+'</month>\n')
            f1.write(u'\t\t<year>'+year+'</year>\n')
            f1.write(u'\t\t<address>'+address+'</address>\n')
            f1.write(u'\t\t<publisher>Association pour le Traitement Automatique des Langues</publisher>\n')
            if article["pages"] != "":
                f1.write(u'\t\t<pages>'+article["pages"]+'</pages>\n')
            f1.write(u'\t\t<url>'+conf_url+'-'+str(first_id)+'</url>\n')
            f1.write(u'\t\t<bibtype>inproceedings</bibtype>\n')
            f1.write(u'\t\t<bibkey>'+key+'</bibkey>\n')
            f1.write(u'\t</paper>\n')

            f2 = codecs.open(bib_file, 'w', 'utf-8')
            f2.write("@inproceedings{"+key+",\n")
            f2.write("  author    = {"+' and '.join(authors)+"},\n")
            f2.write("  title     = {"+bibtexify(title)+"},\n")
            f2.write("  booktitle = {"+volume+"},\n")
            f2.write("  month     = {"+month+"},\n")
            f2.write("  year      = {"+year+"},\n")
            f2.write("  address   = {"+address+"},\n")
            f2.write("  publisher = {Association pour le Traitement Automatique des Langues},\n")
            if article["pages"] != "":
                pages = re.sub("(\d+)-(\d+)", "\g<1>--\g<2>", article["pages"])
                f2.write("  pages     = {"+pages+"},\n")
            f2.write("  url       = {"+conf_url+'-'+str(first_id)+"}\n")
            f2.write("}")
            f2.close()



    f1.write('</volume>\n')

    # # - Print inProceedings
    # for article in TALN_parse.articles:

    #     # récupère les noms des auteurs
    #     authors = []
    #     for prenom, nom in article['auteurs']:
    #         authors.append(nom.strip()+', '+prenom.strip())

    #     # constuction de la clé à la ACL anthology
    #     key = [ re.sub('[-\s]', '', unidecode.unidecode(u.split(', ')[0])).lower() for u in authors ]
    #     if len(key) > 3:
    #         key = key[0]+'-EtAl'
    #     else:
    #         key = '-'.join(key)
    #     key += ':'+str(year)+':'+conference

    #     # récupère le titre de l'article
    #     title = ""
    #     language = ""
    #     extra_title = ""
    #     if article.has_key("titre"):
    #         title = article["titre"]
    #         language = "french"
    #         if article.has_key("title"):
    #             extra_title = article["title"]
    #     else:
    #         title = article["title"]
    #         language = "english"

    #     # construit l'url de l'article
    #     url = conf_url + "/" + article['id']

    #     current_bib = "@inproceedings{"+key+",\n"
    #     current_bib += "  author    = {"+' and '.join(authors)+"},\n"
    #     current_bib += "  title     = {"+bibtexify(title)+"},\n"
    #     current_bib += "  booktitle = {"+conf_title+"},\n"
    #     current_bib += "  month     = {"+month+"},\n"
    #     current_bib += "  year      = {"+str(year)+"},\n"
    #     current_bib += "  address   = {"+address+"},\n"
    #     current_bib += "  publisher = {Association pour le Traitement Automatique des Langues},\n"
    #     if article.has_key("pages"):
    #         pages = re.sub("(\d+)-(\d+)", "\g<1>--\g<2>", article["pages"])
    #         current_bib += "  pages     = {"+pages+"},\n"
    #     current_bib += "  url       = {"+url+"},\n"

    #     # ouvre le handler pour l'écriture du bibtext courant
    #     f2 = codecs.open(bib_dir+article['id']+".bib", 'w', 'utf-8')
    #     f2.write(current_bib+"}")
    #     f2.close()

    #     current_bib += "  language  = {"+language+"},\n"
    #     if extra_title != "":
    #         current_bib += "  note      = {"+bibtexify(extra_title)+"},\n"
    #     if article.has_key("resume"):
    #         current_bib += "  resume    = {"+bibtexify(article['resume'])+"},\n"
    #     if article.has_key("abstract"):
    #         current_bib += "  abstract  = {"+bibtexify(article['abstract'])+"},\n"
    #     if article.has_key("mots_cles"):
    #         current_bib += "  motscles  = {"+bibtexify(article['mots_cles'])+"},\n"
    #     if article.has_key("keywords"):
    #         current_bib += "  keywords  = {"+bibtexify(article['keywords'])+"},\n"
    #     current_bib += "}"

    #     f1.write('\n\n' + current_bib)

    # f1.close()
