#!/bin/bash

# Script pour générer les fichiers bibtex

#  RECITAL
for YEAR in {1999..2015}
do

    XML_FILE=../conferences/RECITAL/RECITAL-$YEAR/recital-$YEAR.xml
    BIB_DIR=../conferences/RECITAL/RECITAL-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
   
done

# TALN
for YEAR in {1997..2015}
do

    XML_FILE=../conferences/TALN/TALN-$YEAR/taln-$YEAR.xml
    BIB_DIR=../conferences/TALN/TALN-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done


# DEFT
for YEAR in 2015
do

    XML_FILE=../ateliers/DEFT/DEFT-$YEAR/deft-$YEAR.xml
    BIB_DIR=../ateliers/DEFT/DEFT-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done


# ETeRNAL
for YEAR in 2015
do

    XML_FILE=../ateliers/ETeRNAL/ETeRNAL-$YEAR/eternal-$YEAR.xml
    BIB_DIR=../ateliers/ETeRNAL/ETeRNAL-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done

# ITI
for YEAR in 2015
do

    XML_FILE=../ateliers/ITI/ITI-$YEAR/iti-$YEAR.xml
    BIB_DIR=../ateliers/ITI/ITI-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done

# TALaRE
for YEAR in 2015
do

    XML_FILE=../ateliers/TALaRE/TALaRE-$YEAR/talare-$YEAR.xml
    BIB_DIR=../ateliers/TALaRE/TALaRE-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done

# TASLA
for YEAR in 2015
do

    XML_FILE=../ateliers/TASLA/TASLA-$YEAR/tasla-$YEAR.xml
    BIB_DIR=../ateliers/TASLA/TASLA-$YEAR/bib/

    if [ ! -d "$BIB_DIR" ]; then
        mkdir $BIB_DIR
    fi

    echo "python xml_to_bib.py $XML_FILE"
    python xml_to_bib.py $XML_FILE
    
done


