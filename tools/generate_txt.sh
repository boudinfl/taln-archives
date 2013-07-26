#!/bin/bash

PATH_PDFBOX=/nlp/pdfbox-app-1.8.2.jar


# Extraction du texte des fichiers de RECITAL
for YEAR in {2007..2013}
do
    echo "Extracting text from RECITAL $YEAR papers"
    # Creation du répertoire txt
    mkdir -p ../RECITAL/RECITAL-$YEAR/txt/

    for PDF_FILE in ../RECITAL/RECITAL-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")
        TXT_FILE=../RECITAL/RECITAL-$YEAR/txt/${FILENAME%.*}.txt

        echo 'java -jar $PATH_PDFBOX ExtractText $PDF_FILE $TXT_FILE'
        java -jar $PATH_PDFBOX ExtractText $PDF_FILE $TXT_FILE

    done
done

# Extraction du texte des fichiers de TALN
for YEAR in {2007..2013}
do
    echo "Extracting text from TALN $YEAR papers"
    # Creation du répertoire txt
    mkdir -p ../TALN/TALN-$YEAR/txt/

    for PDF_FILE in ../TALN/TALN-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")
        TXT_FILE=../TALN/TALN-$YEAR/txt/${FILENAME%.*}.txt

        echo 'java -jar $PATH_PDFBOX ExtractText $PDF_FILE $TXT_FILE'
        java -jar $PATH_PDFBOX ExtractText $PDF_FILE $TXT_FILE

    done
done

