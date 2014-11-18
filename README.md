# taln-archives

TALN Archives est une archive numérique francophone des articles de recherche en
Traitement Automatique de la Langue. Elle contient actuellement les actes des 
conférences RECITAL et TALN de 1997 à 2014.

Une version html est disponible 
[ici](http://www.atala.org/taln_archives/).

Un fichier XML contenant les méta-données a été créé pour chaque édition des 
conférences, ce dernier contient :

- Méta-données de la conférence
  - Titre de la conférence, acronyme, ville, pays
  - Dates de début et de fin de la conférence
  - Noms des présidents du comité de programme
  - Formats des articles publiés (e.g.~court, long)
  - URL du site web de la conférence

- Méta-données pour chaque article
  - Identifiant unique (e.g.~taln-2008-long-001)
  - Noms des auteurs, emails, affiliations
  - Titre, résumé et mots clés (français et anglais si disponible)
  - Format de l'article
  - Numéros des pages
  - Nom de la session dans le programme

Les fichiers bibtex de tous les articles ont été générés automatiquement à 
partir du fichier de méta-données avec la commande :

    cd tools/
    ./generate_bibtex_files.sh

Les fichiers au format texte des articles ont été extraits avec l'outil 
[pdftotext](http://poppler.freedesktop.org/) au format texte ou OCRisés
avec l'outil [tesseract-ocr](http://code.google.com/p/tesseract-ocr/).

    cd tools/
    ./extract_text_from_pdfs.sh

Les méta-données des fichiers pdfs ont été modifiés avec l'outil 
[pdftk](http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) avec la commande :

    cd tools/
    ./update_pdf_metadata.sh

Une version web de l'archive peut être créée avec la commande :

    cd tools/
    python generate_html.py

Si vous utilisez cet ensemble de données, veuillez citer l'article :

 - Florian Boudin, TALN Archives : une archive numérique francophone des 
   articles de recherche en Traitement Automatique de la Langue, Traitement 
   Automatique des Langues Naturelles (TALN), 2013.

Mises à jour
 - 18/11/2014, ajout des titres en anglais pour TALN 2014, RECITAL 2014 et 
   TALN-2011.
 - 09/07/2014, ajout des actes de TALN-RECITAL 2014.
 - 28/06/2014, corrections meta-donnés.
 - 06/05/2015, bug-fixes, ajout des prénoms/noms dans les fichiers de 
   méta-données, modification des bibtex (maintenant en UTF-8), transfert des
   informations sur les meilleurs papiers et les taux de sélection.
 - 07/04/2014, ajout des actes de TALN 1997 et 1998.
 - 02/04/2014, ajout des actes de TALN-RECITAL 1999 et 2000.
 - 28/03/2014, ajout des actes de TALN-RECITAL 2006.
 - 06/02/2014, suppression des fichiers parscit/html/txt et conversion des 
   articles avec pdftotext + nettoyage des header/footer.
 - 03/02/2014, ajout de l'extraction des citations avec ParsCit.
 - 02/02/2014, ajout des actes de RECITAL 2001.
 - 31/01/2014, ajout des actes des conférences TALN-RECITAL 2002 et TALN 2001, 
   modifications des scripts.
 - 29/01/2014, modification du script de conversion pdf->txt et ajout des 
   fichiers txt, html et ocr.
 - 27/01/2014, ajout des actes de TALN/RECITAL 2003, correction de 
   problèmes de case des noms d'auteurs, correction de problèmes de fichiers
   corrompus (recital-2008-long-010), correction de problèmes de fichiers 
   protégés (taln-2010-long-037), modification globale des méta-données des 
   fichiers pdfs à l'aide de pdftk.
 - 24/01/2014, ajout des actes de RECITAL 2004.
 - 23/01/2014, ajout des actes de TALN 2004 et modification des scripts pour la
   génération du site web.
 - 21/01/2014, ajout de méta-données pour TALN et RECITAL 2005 (résumé, mots 
   clés) et modification des pdfs.
 - 15/01/2014, corrections de méta-données.
 - 08/01/2014, ajout des actes des conférences TALN 2005 et RECITAL 2005, 
   ajout des noms des sessions dans TALN 2009.
 - 26/07/2013, ajout des fichiers textes, extraits à partir du contenu des
   articles au format pdf.
 - 18/07/2013, ajout des fichiers de génération de bibtex et du site web.
 - 25/06/2013, ajout des actes des conférences TALN 2013 et RECITAL 2013.

Remerciements
 - Thierry Hamon
 - Patrick Paroubek
 - Gil Francopoulo
 - Amir Hazem
 - Anne Vilnat
 - Cédrick Fairon
 - Pierre Zweigenbaum
