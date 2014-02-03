#!/bin/bash

# Ce script extrait les citations des articles avec l'outil ParsCit
PATH_PARSCIT=/nlp/ParsCit/bin

# Extraction des citations des articles de RECITAL
for YEAR in {2001..2005} {2007..2013}
do
    echo "Extracting citations from RECITAL $YEAR papers"

    TXT_DIR=../RECITAL/RECITAL-$YEAR/txt/

    for TXT_FILE in $TXT_DIR/*.txt
    do
        FILENAME=$(basename "$TXT_FILE")
        TMP_TXT_FILE=$TXT_DIR/${FILENAME%.*}.tmp
        PARSCIT_FILE=$TXT_DIR/${FILENAME%.*}.parscit.xml
        OCR_TXT_FILE=$TXT_DIR/${FILENAME%.*}.ocr

        cp $TXT_FILE $TMP_TXT_FILE
        echo "$PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE"
        $PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE

        NUM_LINES=$(cat $PARSCIT_FILE | wc -l)

        if (( $NUM_LINES < 10 ))
        then
            echo "failed for", $FILENAME
            cp $OCR_TXT_FILE $TMP_TXT_FILE
            echo "$PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE"
            $PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE
        fi

        rm -f $TMP_TXT_FILE

    done
    
done

# Extraction des citations des articles de TALN
for YEAR in {2001..2005} {2007..2013}
do
    echo "Extracting citations from TALN $YEAR papers"

    TXT_DIR=../TALN/TALN-$YEAR/txt/

    for TXT_FILE in $TXT_DIR/*.txt
    do
        FILENAME=$(basename "$TXT_FILE")
        TMP_TXT_FILE=$TXT_DIR/${FILENAME%.*}.tmp
        PARSCIT_FILE=$TXT_DIR/${FILENAME%.*}.parscit.xml
        OCR_TXT_FILE=$TXT_DIR/${FILENAME%.*}.ocr

        cp $TXT_FILE $TMP_TXT_FILE
        echo "$PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE"
        $PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE

        NUM_LINES=$(cat $PARSCIT_FILE | wc -l)

        if (( $NUM_LINES < 10 ))
        then
            echo "failed for", $FILENAME
            cp $OCR_TXT_FILE $TMP_TXT_FILE
            echo "$PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE"
            $PATH_PARSCIT/citeExtract.pl $TMP_TXT_FILE $PARSCIT_FILE
        fi

        rm -f $TMP_TXT_FILE

    done

done

