#!/bin/bash

# Script pour générer les fichiers bibtex

#  RECITAL
for YEAR in {1999..2015}
do

    XML_FILE=../RECITAL/RECITAL-$YEAR/recital-$YEAR.xml
    BIB_DIR=../RECITAL/RECITAL-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
   
done

# TALN
for YEAR in {1997..2015}
do

    XML_FILE=../TALN/TALN-$YEAR/taln-$YEAR.xml
    BIB_DIR=../TALN/TALN-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done

# Ateliers
for YEAR in 2015
do
    for ATELIER in ../ateliers/$YEAR/*
    do
        XML_FILE=$ATELIER/`basename $ATELIER | tr '[A-Z]' '[a-z]'`-$YEAR.xml
        BIB_DIR=$ATELIER/bib/

        if [ ! -d "$BIB_DIR" ]; then
            mkdir $BIB_DIR
        fi

        echo "python xml_to_bib.py $XML_FILE"
        python xml_to_bib.py $XML_FILE

    done
done