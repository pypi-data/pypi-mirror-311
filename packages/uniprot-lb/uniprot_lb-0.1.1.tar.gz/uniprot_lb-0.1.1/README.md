
# Projet POO - M1 Bioinformatique

Ce projet offre une collection d'outils pour analyser et manipuler les données issues de fichiers Uniprot. Il inclut des fonctionnalités pour extraire des informations, calculer des propriétés biochimiques, et visualiser des caractéristiques des protéines.
Il a été réalisé dans le cadre d'un projet pour l'UE Programmation Avancée Python du M1 de Bio-Informatique de l'Université Claude Bernard - Lyon 1.

## Structure du dépôt

- **`uniprot.py`** : Contient la classe `Uniprot` qui permet d'analyser des fichiers Uniprot individuels.
- **`uniprot_collection.py`** : Définit la classe `Collection`, conçue pour manipuler et analyser un ensemble d'objets `Uniprot`.
- **`Test.py`** : Script de test pour démontrer l'utilisation des classes et méthodes.
- **Dossier `data/`** : Contient des fichiers de données d'entrée, notamment des entrées Uniprot.
- **Images `.png`** : Générées pour visualiser l'abondance relative des acides aminés (ABRL) des entrées Uniprot.

## Fonctionnalités

### Classe `Uniprot`
- **Extraction d'informations** : Accession number, nom du gène, organisme, séquence peptidique, IDs GO.
- **Export au format FASTA** : Génère un fichier `.fasta` basé sur les informations de la protéine. Ce fichier est enregistré dans le répértoire `fasta_outputs`.
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
   Clonez ce dépôt sur votre machine locale :
   ```
   git clone http://pedago-service.univ-lyon1.fr:2325/briou/uniprot.git
   ```

2. **Exécution des tests** :
   Le fichier `Test.py` contient des exemples d'utilisation. Exécutez-le avec Python :
   ```
   python Test.py
   ```

3. **Visualisation des graphiques** :
   Les graphiques générés seront enregistrés sous forme de fichiers `.png` dans le répertoire `figures`.

## Pré-requis

- Python 3.6 ou plus récent.
- Bibliothèques Python :
  - `matplotlib`
  - (`functools` si besoin de mettre une longueur différente de 500 acides aminés dans le filtre des objets de la `collection`.)

## Exemples rapides

### Objets Uniprots
```python
import uniprot

# Création d'un objet Uniprot à partir d'un fichier
uniprot_obj = uniprot.uniprot_from_file("./data/P05067.txt")

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
import uniprot_collection as collection
from functools import partial

# Création d'un objet Collection à partir d'un fichier contenant plusieurs entrées.
collection_1 = collection.collection_from_file("./data/five_proteins.txt")

# Affichage des informations
print(collection_1)

# Ajout de données dans une collection
collection_2 = collection.collection_from_file("./data/five_proteins.txt")

with open("./data/P05067.txt", "r") as f:
    file_contents = f.read()
    collection_1.add(file_contents)

# Retrait d'éléments dans la collection
collection_1.del_("PGBM_HUMAN")
collection_2.del_("SPRC_BOVIN")

# Fusion de deux collections
collection_3 = collection_2 + collection_1

# Filtrage des objets pour lesquels la séquence peptidique est supérieure à 1000 acide aminés:
print(collection_3.filter(partial(collection.filtre_longueur,n=1000)))

# Création d'un plot pour chacun des objets de collection_3
for element in collection_3:
    collection_3.draw_ABRL(element.id)
```

## Contributeurs

- Baptiste Riou
- Lorcan Brenders

