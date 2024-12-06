# Xomics
## Description du projet : 
Le projet Xomics consiste à analyser et visualiser des données génomiques, à partir d'un ou plusieurs fichiers gff. 
Les fonctionnalités principales sont donc :
- importation de fichiers gff, 
- gestion des objets gènes, transcrits, et exons
- fusion des annotations pour générer un nouveau fichier gff à partir des données d'annotation fusionnées, 
- visualisation de la distribution de la longueurs des transcrits pour les gènes, avec une représentation graphique en boxplot.

## Prérequis 
Les prérequis suivants sont demandés avant toute installation : 
- python 3
- module python matplotlib (pour la visualisation). Il peut être installé avec la commande :
```bash
pip install matplotlib
```

## Installation
L'installation se fait se fait en réalisant un "fork" à partir de ce gitlab sur le votre. Ensuite, il faut cloner le projet depuis le terminal en faisant : 
```bash
git clone [URL du clone du projet, http]
```

## Utilisation

Le répertoire xomics contient tous les scripts nécessaires : 

- script_annot_visu_final.py : contient les classes et méthodes essentielles. inutile de modifier ce script.

- script_execution.py : permet de réaliser la fusion des annotations des fichiers gff (en entrée), retourne le fichier gff d'annotations fusionnées et une visualisation graphique de la taille des transcrits additionnées par gène.

- script_get_gene.py : permet de réaliser une recherche de gène (ID du gène cherché en entrée) et retourne les informations concernant le gène contenues dans le fichier gff.

### Fusion des annotations, et visualisation

Vous devez d'abord placer les fichiers gff que vous souhaitez analyser dans le fichier "data". 

Ensuite, accédez au script "script_execution.py" et modifiez le chemin des variables path_gff1 et path_gff2 en fonction du nom de vos fichiers d'annotations.
Vous pouvez également renommer le fichier fusionné gff de sortie, nommé par défaut "merge_annotation.gff", ainsi que la représentation graphique nommée par défaut "output_graph.png".


Afin de lancer ce script :

```bash
python3 script_execution.py
```

Un exemple est fourni dans le répertoire : "Exemple_merge_annotation.gff" et "Exemple_output_graph.png".

### Recherche d'un gène spécifique
Pour rechercher un gène à partir de son identifiant, utilisez le script suivant dans votre terminal :

```bash
python3 script_get_gene.py
```

Entrez ensuite l'ID du gène recherché, et les informations concernant le gène vous seront retournées.


## Classes, méthodes
Classes principales :
Gene :
- représente un gène.
- gère les transcrits associés.
- calcule la longueur totale des transcrits.

Transcript :
- représente un transcrit associé à un gène.
- gère les exons associés.
- calcule la longueur totale des exons.

Exon :
-représente un exon associé à un transcrit.

Annotation :
- parse les fichiers gff pour construire une annotation.
- gère la fusion des annotations.
- permet l'exportation des annotations au format GFF.
- génère des visualisations sous forme de boxplots.

Méthodes Clés :

- get_gene(gene_id) : Recherche un gène à partir de son ID.
- to_gff(output_path) : Exporte les annotations dans un fichier GFF.
- rna_lens(fichier_output) : Génère un boxplot des longueurs des transcrits.



## NB
Après multiples essais, il semblerait que la méthode get_gene ne fonctionne pas (souci de dictionnaire, qui est vide lorsque cette méthode est utilisée mais fonctionne mais le dictionnaire semble rempli avec get_gff... Un peu de mal à comprendre.


Autrices : Centa Clara, El Khattabi Mariam (M1 Bio-informatique, Université Lyon 1)


 
