# taln-archives

Mises à jour
 - 26 juillet 2013, ajout des fichiers textes, extraits à partir du contenu des
   articles au format pdf.
 - 18 juillet 2013, ajout des fichiers de génération de bibtex et du site web
 - 25 juin 2013, ajout des actes des conférences TALN 2013 et RECITAL 2013

TALN Archives est une archive numérique francophone des articles de recherche en
Traitement Automatique de la Langue. Elle contient actuellement les actes des 
conférences RECITAL et TALN de 2007 à 2012.

Un fichier XML contenant les méta-données a été créé pour chaque édition des 
conférences, ce dernier contient :

- Méta-données de la conférence
  - Titre de la conférence, acronyme, ville, pays
  - Dates de début et de fin de la conférence
  - Noms des présidents du comité de programme
  - Formats des articles publiés (e.g.~court, long)
  - Nombre d'articles soumis et nombre d'articles acceptés
  - URL du site web de la conférence
  - Identifiant(s) du(des) meilleur(s) article(s)

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
    python generate_bib.py

Les fichiers au format texte des articles ont été extraits avec l'outil 
[PDFBox](http://pdfbox.apache.org/).

    cd tools/
    ./generate_txt.sh

Une version web de l'archive peut être créée avec la commande :

    cd tools/
    python generate_html.py


Si vous utilisez cet ensemble de données, veuillez citer l'article :

 - Florian Boudin, TALN Archives : une archive numérique francophone des 
   articles de recherche en Traitement Automatique de la Langue, Traitement 
   Automatique des Langues Naturelles (TALN), 2013, papier court
