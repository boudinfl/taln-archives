#!/bin/bash

# Ce script utilise poppler-utils pour extraire le contenu textuel des fichiers
# pdfs, et un système d'OCR en cas d'impossibilité d'extraire le texte.

resolution=300
PDF_TO_TEXT=/usr/local/bin/pdftotext

# Extraction par année
for YEAR in {1997..2014}
do
    echo "Extraction du contenu textuel des fichiers de TALN $YEAR"

    TXT_DIR=../TALN/TALN-$YEAR/txt/
    IMG_DIR=$TXT_DIR/img/

    # Creation du répertoire txt
    if [ ! -d "$TXT_DIR" ]; then
        mkdir $TXT_DIR
    fi

    for PDF_FILE in ../TALN/TALN-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")

        # Extraction du contenu textuel avec pdftotext
        PDF2TXT_FILE=$TXT_DIR/${FILENAME%.*}.pdf2txt
        TXT_FILE=$TXT_DIR/${FILENAME%.*}.txt

        if [ -f $TXT_FILE ]
        then
            continue
        fi

        echo "$PDF_TO_TEXT -layout -enc UTF-8 $PDF_FILE $PDF2TXT_FILE"
        $PDF_TO_TEXT -layout -enc UTF-8 $PDF_FILE $PDF2TXT_FILE

        # Test si le contenu textuel n'est pas correct, OCR
        NB_ET=$(grep -c 'et' $PDF2TXT_FILE)

        if (( $NB_ET < 5 ))
        then
            mkdir $IMG_DIR
            rm -f $PDF2TXT_FILE

            # Conversion du fichier pdf en images
            echo "convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg"
            convert -density $resolution $PDF_FILE $IMG_DIR/${FILENAME%.*}.jpg

            # Calcul du nombre de pages
            NUMPAGES=$(ls $IMG_DIR/*.jpg | wc -l)
            NUMPAGES=$((NUMPAGES-1))

            echo "NUMPAGES" $NUMPAGES

            # Si le nombre de page est supérieur à 1
            if (( $NUMPAGES > 1 ))
            then

                # OCR des fichiers images
                for PAGE in $(eval echo {0..$NUMPAGES})
                do
                    IMG_FILE=$IMG_DIR/${FILENAME%.*}-$PAGE.jpg
                    echo "tesseract $IMG_FILE ${IMG_FILE%.*}"
                    tesseract $IMG_FILE ${IMG_FILE%.*}
                    echo "cat ${IMG_FILE%.*}.txt >> $PDF2TXT_FILE"
                    cat ${IMG_FILE%.*}.txt >> $PDF2TXT_FILE
                    rm ${IMG_FILE%.*}.txt
                    rm $IMG_FILE
                done

            # Si il y a une page
            else
                IMG_FILE=$IMG_DIR/${FILENAME%.*}.jpg
                echo "tesseract $IMG_FILE $IMG_FILE"
                tesseract $IMG_FILE $IMG_FILE
                mv $IMG_FILE.txt $PDF2TXT_FILE
                rm $IMG_FILE
            fi

            rmdir $IMG_DIR
        fi

        # Nettoyage du contenu textuel 
        python clean_text_output.py $PDF2TXT_FILE $TXT_FILE
        rm -f $PDF2TXT_FILE

    done

    echo "Extraction du contenu textuel des fichiers de RECITAL $YEAR"

    TXT_DIR=../RECITAL/RECITAL-$YEAR/txt/
    IMG_DIR=$TXT_DIR/img/

    # Creation du répertoire txt
    if [ ! -d "$TXT_DIR" ]; then
        mkdir $TXT_DIR
    fi

    for PDF_FILE in ../RECITAL/RECITAL-$YEAR/actes/*.pdf
    do
        FILENAME=$(basename "$PDF_FILE")

        # Extraction du contenu textuel avec pdftotext
        PDF2TXT_FILE=$TXT_DIR/${FILENAME%.*}.pdf2txt
        TXT_FILE=$TXT_DIR/${FILENAME%.*}.txt

        if [ -f $TXT_FILE ]
        then
            continue
        fi

        echo "$PDF_TO_TEXT -layout -enc UTF-8 $PDF_FILE $PDF2TXT_FILE"
        $PDF_TO_TEXT -layout -enc UTF-8 $PDF_FILE $PDF2TXT_FILE

        # Test si le contenu textuel n'est pas correct, OCR
        NB_ET=$(grep -c 'et' $PDF2TXT_FILE)

        if (( $NB_ET < 5 ))
        then
            mkdir $IMG_DIR
            rm -f $PDF2TXT_FILE

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
                    echo "cat ${IMG_FILE%.*}.txt >> $PDF2TXT_FILE"
                    cat ${IMG_FILE%.*}.txt >> $PDF2TXT_FILE
                    rm ${IMG_FILE%.*}.txt
                    rm $IMG_FILE
                done

            # Si il y a une page
            else
                IMG_FILE=$IMG_DIR/${FILENAME%.*}.jpg
                echo "tesseract $IMG_FILE $IMG_FILE"
                tesseract $IMG_FILE $IMG_FILE
                mv $IMG_FILE.txt $PDF2TXT_FILE
                rm $IMG_FILE
            fi

            rmdir $IMG_DIR
        fi

        # Nettoyage du contenu textuel 
        python clean_text_output.py $PDF2TXT_FILE $TXT_FILE
        rm -f $PDF2TXT_FILE

    done

done

