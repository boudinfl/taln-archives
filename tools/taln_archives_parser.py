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
        self.current_name = {}

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

        if name == 'nom':
            self.current_name['nom'] = self.buffer.strip()

        elif name == 'prenom':
            self.current_name['prenom'] = self.buffer.strip()

        # Récupère les auteurs des papiers
        elif name == 'auteur':
            if not self.info.has_key('auteurs'):
                self.info['auteurs'] = []
            self.info['auteurs'].append( ( self.current_name['prenom'], \
                                           self.current_name['nom'] ) )

        # Récupère les noms des présidents de la conférence
        if name == 'president':
            if not self.info.has_key('presidents'):
                self.info['presidents'] = []
            self.info['presidents'].append( ( self.current_name['prenom'], \
                                           self.current_name['nom'] ) )

        # Récupère les différents types de papiers de la conférence
        elif name == 'type' and self.tree[-1][0] == 'typeArticles':
            if not self.info.has_key('typeArticles'):
                self.info['typeArticles'] = []
            self.info['typeArticles'].append((attrs['id'], self.buffer.strip()))

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