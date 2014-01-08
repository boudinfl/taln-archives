#!/bin/bash

# Converts pdf to txt
# (1 PDF -> n JPGs -> n TXTs -> 1 TXT)
# You need convert (imagemagick) and tesseract (tesseract-ocr-[en|fr|...])

resolution=300 # default value

# Extraction du texte des fichiers de RECITAL
for YEAR in 2005 {2007..2013}
do
    echo "Extracting text from RECITAL $YEAR papers"

    # Creation du répertoire txt
    TXT_DIR=../RECITAL/RECITAL-$YEAR/txt/
    IMG_DIR=$TXT_DIR/img/
    mkdir -p $TXT_DIR
    mkdir -p $IMG_DIR

    for PDF_FILE in ../RECITAL/RECITAL-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")
        TXT_FILE=$TXT_DIR/${FILENAME%.*}.txt
        rm -f $TXT_FILE
        
        # Conversion du fichier pdf en images
        echo "convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg"
        convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg

        # OCR des fichiers images
        for IMG_FILE in $IMG_DIR/*.jpg
        do
            echo "tesseract $IMG_FILE ${IMG_FILE%.*}"
            tesseract $IMG_FILE ${IMG_FILE%.*}
            echo "cat ${IMG_FILE%.*}.txt >> $TXT_FILE"
            cat ${IMG_FILE%.*}.txt >> $TXT_FILE
            rm ${IMG_FILE%.*}.txt
            rm $IMG_FILE
        done

    done

    rmdir -p $IMG_DIR

done

# Extraction du texte des fichiers de TALN
for YEAR in 2005 {2007..2013}
do
    echo "Extracting text from TALN $YEAR papers"
    # Creation du répertoire txt
    TXT_DIR=../TALN/TALN-$YEAR/txt/
    IMG_DIR=$TXT_DIR/img/
    mkdir -p $TXT_DIR
    mkdir -p $IMG_DIR

    for PDF_FILE in ../TALN/TALN-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")
        TXT_FILE=$TXT_DIR/${FILENAME%.*}.txt
        rm -f $TXT_FILE

        # Conversion du fichier pdf en images
        echo "convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg"
        convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg

        # OCR des fichiers images
        for IMG_FILE in $IMG_DIR/*.jpg
        do
            echo "tesseract $IMG_FILE ${IMG_FILE%.*}"
            tesseract $IMG_FILE ${IMG_FILE%.*}
            echo "cat ${IMG_FILE%.*}.txt >> $TXT_FILE"
            cat ${IMG_FILE%.*}.txt >> $TXT_FILE
            rm ${IMG_FILE%.*}.txt
            rm $IMG_FILE
        done

    done

    rmdir -p $IMG_DIR

done

