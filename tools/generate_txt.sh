#!/bin/bash

# Ce script génère les versions txt des articles à partir de deux outils:
# 1. Apache PDFBox
# 2. Tesseract OCR (1 PDF -> n JPGs -> n TXTs -> 1 TXT)
#    You need convert (imagemagick) and tesseract (tesseract-ocr-[en|fr|...])

resolution=300
PATH_PDFBOX=/nlp/pdfbox-app-1.8.2.jar

# Extraction du texte des fichiers de RECITAL
for YEAR in {2001..2005} {2007..2013}
do
    echo "Extracting text from RECITAL $YEAR papers"

    # Creation du répertoire txt
    TXT_DIR=../RECITAL/RECITAL-$YEAR/txt/
    IMG_DIR=$TXT_DIR/img/
    mkdir $TXT_DIR
    mkdir $IMG_DIR

    for PDF_FILE in ../RECITAL/RECITAL-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")
        OCR_TXT_FILE=$TXT_DIR/${FILENAME%.*}.ocr
        # rm -f $OCR_TXT_FILE

        # OCR IF FILE DO NOT EXISTS
        if [ ! -f $OCR_TXT_FILE ]
        then

            # Conversion du fichier pdf en images
            echo "convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg"
            convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg

            # Calcul du nombre de pages
            NUMPAGES=$(ls $IMG_DIR/*.jpg | wc -l)
            NUMPAGES=$((NUMPAGES-1))

            # Si le nombre de page est supérieur à 1
            if (( $NUMPAGES > 1 ))
            then

                # OCR des fichiers images
                for PAGE in $(eval echo {0..$NUMPAGES})
                do
                    IMG_FILE=$IMG_DIR/${FILENAME%.*}-$PAGE.jpg
                    echo "tesseract $IMG_FILE ${IMG_FILE%.*}"
                    tesseract $IMG_FILE ${IMG_FILE%.*}
                    echo "cat ${IMG_FILE%.*}.txt >> $OCR_TXT_FILE"
                    cat ${IMG_FILE%.*}.txt >> $OCR_TXT_FILE
                    rm ${IMG_FILE%.*}.txt
                    rm $IMG_FILE
                done

            # Si il y a une page
            else
                IMG_FILE=$IMG_DIR/${FILENAME%.*}.jpg
                echo "tesseract $IMG_FILE $IMG_FILE"
                tesseract $IMG_FILE $IMG_FILE
                mv $IMG_FILE.txt $OCR_TXT_FILE
                rm $IMG_FILE
            fi
        fi

        # Extraction du texte avec PDFBOX
        TXT_FILE=$TXT_DIR/${FILENAME%.*}.txt
        HTML_FILE=$TXT_DIR/${FILENAME%.*}.html
        # rm -f $TXT_FILE
        # rm -f $HTML_FILE

        if [ ! -f $TXT_FILE ]
        then
            echo 'java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 $PDF_FILE $TXT_FILE'
            java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 -sort $PDF_FILE $TXT_FILE
        fi

        if [ ! -f $HTML_FILE ]
        then
            echo 'java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 -html $PDF_FILE $HTML_FILE'
            java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 -html $PDF_FILE $HTML_FILE
        fi
        
    done

    rmdir $IMG_DIR
    
done

# Extraction du texte des fichiers de TALN
for YEAR in {2001..2005} {2007..2013}
do
    echo "Extracting text from TALN $YEAR papers"
    # Creation du répertoire txt
    TXT_DIR=../TALN/TALN-$YEAR/txt/
    IMG_DIR=$TXT_DIR/img/
    mkdir $TXT_DIR
    mkdir $IMG_DIR

    for PDF_FILE in ../TALN/TALN-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")
        OCR_TXT_FILE=$TXT_DIR/${FILENAME%.*}.ocr
        # rm -f $OCR_TXT_FILE

        # OCR IF FILE DO NOT EXISTS
        if [ ! -f $OCR_TXT_FILE ]
        then

            # Conversion du fichier pdf en images
            echo "convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg"
            convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg

            # Calcul du nombre de pages
            NUMPAGES=$(ls $IMG_DIR/*.jpg | wc -l)
            NUMPAGES=$((NUMPAGES-1))

            # Si le nombre de page est supérieur à 1
            if (( $NUMPAGES > 1 ))
            then

                # OCR des fichiers images
                for PAGE in $(eval echo {0..$NUMPAGES})
                do
                    IMG_FILE=$IMG_DIR/${FILENAME%.*}-$PAGE.jpg
                    echo "tesseract $IMG_FILE ${IMG_FILE%.*}"
                    tesseract $IMG_FILE ${IMG_FILE%.*}
                    echo "cat ${IMG_FILE%.*}.txt >> $OCR_TXT_FILE"
                    cat ${IMG_FILE%.*}.txt >> $OCR_TXT_FILE
                    rm ${IMG_FILE%.*}.txt
                    rm $IMG_FILE
                done

            # Si il y a une page
            else
                IMG_FILE=$IMG_DIR/${FILENAME%.*}.jpg
                echo "tesseract $IMG_FILE $IMG_FILE"
                tesseract $IMG_FILE $IMG_FILE
                mv $IMG_FILE.txt $OCR_TXT_FILE
                rm $IMG_FILE
            fi
        fi

        # Extraction du texte avec PDFBOX
        TXT_FILE=$TXT_DIR/${FILENAME%.*}.txt
        HTML_FILE=$TXT_DIR/${FILENAME%.*}.html
        # rm -f $TXT_FILE
        # rm -f $HTML_FILE

        if [ ! -f $TXT_FILE ]
        then
            echo 'java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 $PDF_FILE $TXT_FILE'
            java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 -sort $PDF_FILE $TXT_FILE
        fi

        if [ ! -f $HTML_FILE ]
        then
            echo 'java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 -html $PDF_FILE $HTML_FILE'
            java -jar $PATH_PDFBOX ExtractText -encoding UTF-8 -html $PDF_FILE $HTML_FILE
        fi

    done

    rmdir $IMG_DIR

done

