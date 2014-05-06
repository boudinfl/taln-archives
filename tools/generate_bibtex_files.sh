#!/bin/bash

# Script pour générer les fichiers bibtex

#  RECITAL
for YEAR in {1999..2013}
do

    XML_FILE=../RECITAL/RECITAL-$YEAR/recital-$YEAR.xml
    BIB_DIR=../RECITAL/RECITAL-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
   
done

# Extraction du texte des fichiers de TALN
for YEAR in {1997..2013}
do

    XML_FILE=../TALN/TALN-$YEAR/taln-$YEAR.xml
    BIB_DIR=../TALN/TALN-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done