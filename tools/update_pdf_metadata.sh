#!/bin/bash

# Script pour mettre à jour les méta-données des fichiers pdfs avec celles des
# fichiers de méta-données en xml

# Extraction du texte des fichiers de RECITAL
for YEAR in {2003..2005} {2007..2013}
do

    XML_FILE=../RECITAL/RECITAL-$YEAR/recital-$YEAR.xml

    for PDF_FILE in ../RECITAL/RECITAL-$YEAR/actes/*.pdf
    do
        echo "updating meta-data from " $PDF_FILE

        # Récupération des méta-données
        META_FILE=${PDF_FILE%.*}.metadata
        echo "pdftk $PDF_FILE dump_data_utf8 > $META_FILE"
        pdftk $PDF_FILE dump_data_utf8 > $META_FILE

        # Création du nouveau fichier de méta-données
        NEW_META_FILE=${PDF_FILE%.*}.updated_metadata
        echo "python generate_pdf_metadata.py $XML_FILE $META_FILE $NEW_META_FILE"
        python generate_pdf_metadata.py $XML_FILE $META_FILE $NEW_META_FILE
        
        # Modification des méta-données
        echo "pdftk $PDF_FILE update_info_utf8 $NEW_META_FILE output $PDF_FILE.updated"
        pdftk $PDF_FILE update_info_utf8 $NEW_META_FILE output $PDF_FILE.updated

        # Suppression des fichiers temporaires
        rm -f $META_FILE
        rm -f $NEW_META_FILE
        rm -f $PDF_FILE
        mv $PDF_FILE.updated $PDF_FILE

    done

done

# Extraction du texte des fichiers de TALN
for YEAR in {2003..2005} {2007..2013}
do

    XML_FILE=../TALN/TALN-$YEAR/taln-$YEAR.xml

    for PDF_FILE in ../TALN/TALN-$YEAR/actes/*.pdf
    do
        echo "updating meta-data from " $PDF_FILE

        # Récupération des méta-données
        META_FILE=${PDF_FILE%.*}.metadata
        echo "pdftk $PDF_FILE dump_data_utf8 > $META_FILE"
        pdftk $PDF_FILE dump_data_utf8 > $META_FILE

        # Création du nouveau fichier de méta-données
        NEW_META_FILE=${PDF_FILE%.*}.updated_metadata
        echo "python generate_pdf_metadata.py $XML_FILE $META_FILE $NEW_META_FILE"
        python generate_pdf_metadata.py $XML_FILE $META_FILE $NEW_META_FILE
        
        # Modification des méta-données
        echo "pdftk $PDF_FILE update_info_utf8 $NEW_META_FILE output $PDF_FILE.updated"
        pdftk $PDF_FILE update_info_utf8 $NEW_META_FILE output $PDF_FILE.updated

        # Suppression des fichiers temporaires
        rm -f $META_FILE
        rm -f $NEW_META_FILE
        rm -f $PDF_FILE
        mv $PDF_FILE.updated $PDF_FILE

    done

done

