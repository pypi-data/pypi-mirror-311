
# uniprot_lb_poo

`uniprot_lb_poo` est un package Python qui permet d'analyser et manipuler des données issues de fichiers Uniprot. Il offre des outils pour extraire des informations biologiques, calculer des propriétés biochimiques, et visualiser des caractéristiques des protéines.

Ce projet a été développé dans le cadre de l'UE Programmation Avancée Python du Master 1 Bio-Informatique à l'Université Claude Bernard - Lyon 1.

## Structure du package

- **`uniprot.py`** : Contient la classe `Uniprot` qui permet d'analyser des fichiers Uniprot individuels.
- **`uniprot_collection.py`** : Définit la classe `Collection`, conçue pour manipuler et analyser un ensemble d'objets `Uniprot`.
- **Images `.png`** : Générées pour visualiser l'abondance relative des acides aminés (ABRL) des entrées Uniprot.

## Fonctionnalités

### Classe `Uniprot`
- **Extraction d'informations** : Accession number, nom du gène, organisme, séquence peptidique, IDs GO.
- **Export au format FASTA** : Génère un fichier `.fasta` basé sur les informations de la protéine. Ce fichier est enregistré dans le répertoire `fasta_outputs` (créé s'il n'existe pas déjà).
- **Calcul de propriétés** :
  - Poids moléculaire.
  - Hydrophobicité moyenne.

### Classe `Collection`
- **Organisation de données** : Permet de regrouper plusieurs objets `Uniprot` pour des analyses globales.
- **Méthodes principales** :
  - Tri des protéines par longueur de séquence.
  - Filtrage basé sur l'hydrophobicité.
  - Analyse des IDs GO présents dans le groupe.
  - Génération de graphiques spécifiques (ABRL).

## Utilisation

1. **Installation** :

   Installez le package avec pip :
   ```
   pip install uniprot_lb_poo
   ```

2. **Visualisation des graphiques** :
   Les graphiques générés seront enregistrés sous forme de fichiers `.png` dans le répertoire `figures` (créé s'il n'existe pas déjà).

## Pré-requis

- Python 3.10 ou plus récent.
- Bibliothèques Python :
  - `matplotlib>=3.9.2`

## Exemples rapides

### Test simple
```python
from uniprot_lb_poo import hello

hello.main()
# Hello from uniprot_lb_poo !

```

### Objets Uniprot
```python
from uniprot_lb_poo import uniprot

# Création d'un objet Uniprot à partir d'un fichier
uniprot_obj = uniprot.uniprot_from_file("your/file/path.txt")

# Affichage des informations
print(uniprot_obj)

# Calcul de propriétés
print("Poids moléculaire :", uniprot_obj.molecular_weight())
print("Hydrophobicité moyenne :", uniprot_obj.average_hydrophobicity())

# Export au format FASTA
uniprot_obj.fasta_dump()
```

### Objets Collections
```python
import uniprot_lb_poo
from uniprot_lb_poo import uniprot_collection as collection
from functools import partial

# Création d'un objet Collection à partir d'un fichier contenant plusieurs entrées.
collection_1 = collection.collection_from_file("your/file/path/multiple_entries.txt")

# Affichage des informations
print(collection_1)

# Ajout de données dans une collection
collection_2 = collection.collection_from_file("your/file/path/multiple_entries.txt")

with open("your/file/path/single_entry.txt", "r") as f:
    file_contents = f.read()
    collection_1.add(file_contents)

# Retrait d'éléments dans la collection
collection_1.del_("PGBM_HUMAN")
collection_2.del_("SPRC_BOVIN")

# Fusion de deux collections
collection_3 = collection_2 + collection_1

# Filtrage des objets pour lesquels la séquence peptidique est supérieure à 1000 acides aminés:
print(collection_3.filter(partial(collection.filtre_longueur, n=1000)))

# Création d'un plot pour chacun des objets de collection_3
for element in collection_3:
    collection_3.draw_ABRL(element.id)
```

## Auteurs-Etudiants

- Baptiste Riou
- Lorcan Brenders

## Contributeurs-Professeurs

- Arnaud Mary
- Guillaume Launay
