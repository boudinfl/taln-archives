#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.sax

################################################################################
class content_handler(xml.sax.ContentHandler):
    """ XML sax parser for taln documents """
     #-T-----------------------------------------------------------------------T-
    def __init__(self, path):
        # Tree for pushing/poping tags, attrs
        self.tree = []
        
        # Buffer for xml element
        self.buffer = ''

        self.meta = {}
        self.articles = []
        self.info = {}

        self.tags = ['titre', 'title', 'resume', 'abstract', 'mots_cles',\
         'keywords', 'type', 'acronyme', 'ville', 'pays', 'dateDebut',\
          'dateFin', 'pages']
        
        # Construct an launch the parser
        parser = xml.sax.make_parser()
        parser.setContentHandler(self)
        parser.parse(path)
    #-B-----------------------------------------------------------------------B-
        
    #-T-----------------------------------------------------------------------T-
    def startElement(self, name, attrs):
        self.tree.append((name, attrs))

    #-B-----------------------------------------------------------------------B-
        
    #-T-----------------------------------------------------------------------T-
    def characters(self, data):
        self.buffer += data
    #-B-----------------------------------------------------------------------B-
        
    #-T-----------------------------------------------------------------------T-
    def endElement(self, name):
        tag, attrs = self.tree.pop()

        # Récupère les auteurs des papiers
        if name == 'nom' and self.tree[-1][0] == 'auteur':
            if not self.info.has_key('auteurs'):
                self.info['auteurs'] = []
            self.info['auteurs'].append(self.buffer.strip())

        # Récupère les différents types de papiers de la conférence
        elif name == 'type' and self.tree[-1][0] == 'typeArticles':
            if not self.info.has_key('typeArticles'):
                self.info['typeArticles'] = []
            self.info['typeArticles'].append((attrs['id'], self.buffer.strip()))

        # Récupère les identifiants des meilleurs papiers
        elif name == 'articleId' and self.tree[-1][0] == 'meilleurArticle':
            if not self.info.has_key('meilleurArticle'):
                self.info['meilleurArticle'] = []
            self.info['meilleurArticle'].append(self.buffer.strip())

        # Récupère les statistiques de soumissions de la conférence
        elif name == 'acceptations' and self.tree[-1][0] == 'statistiques':
            if not self.info.has_key('acceptations'):
                self.info['acceptations'] = {}
            self.info['acceptations'][attrs['id']] = \
            round(float(self.buffer.strip()) / \
                float(attrs['soumissions']), 3) * 100

        # Récupère les noms des présidents de la conférence
        if name == 'nom' and self.tree[-1][0] == 'presidents':
            if not self.info.has_key('presidents'):
                self.info['presidents'] = []
            self.info['presidents'].append(self.buffer.strip())

        # Récupère tous les tags terminaux
        elif name in self.tags:
            self.info[name] = self.buffer.strip()

        elif name == 'article':
            self.info['id'] = attrs['id']
            self.articles.append(self.info.copy())
            self.info = {}

        elif name == 'edition':
        	self.meta = self.info
        	self.info = {}
    
        # Flush the buffer
        self.buffer = ''
    #-B-----------------------------------------------------------------------B-

################################################################################