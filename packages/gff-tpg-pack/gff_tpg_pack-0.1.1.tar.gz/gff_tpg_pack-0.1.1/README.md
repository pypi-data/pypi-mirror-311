# **Documentation du Projet : Analyseur d'Annotations GFF**

Ce projet est un outil conçu pour analyser, manipuler et visualiser des données biologiques au format GFF. Il permet de représenter les gènes, transcrits et exons, de les manipuler (fusion, exportation), et d'extraire des statistiques ou des visualisations utiles.

---

## **Présentation Générale**

Le projet est structuré en plusieurs modules et fonctionnalités :
1. **Modélisation biologique** : Les entités biologiques telles que les gènes, transcrits, et exons sont représentées par des classes.
2. **Fusion et manipulation des annotations** : Combine des annotations provenant de différents fichiers GFF.
3. **Exportation et statistiques** : Génère des fichiers résumant les informations et calcule des statistiques.
4. **Visualisation** : Produit des graphiques (boxplots) pour représenter la distribution des longueurs d'ARN.

---

## **Structure du Code**

### **Classes Principales**

1. **`Gene`**  
   Représente un gène et gère ses transcrits associés. Il permet la fusion avec d'autres gènes ayant le même identifiant.

2. **`Transcrit`**  
   Représente un transcrit (ARNm) et gère ses exons associés. Un transcrit est toujours lié à un gène parent.

3. **`Exon`**  
   Représente un exon associé à un transcrit. Chaque exon est défini par sa position sur le génome.

4. **`Annotation`**  
   Gère l'ensemble des annotations (gènes, transcrits, exons). Elle offre des fonctionnalités pour :
   - Ajouter et récupérer des gènes.
   - Fusionner deux annotations.
   - Générer des fichiers au format GFF.
   - Créer des statistiques et des visualisations.

---

### **Méthodes Clés**

1. **`parser_gff`**  
   Parse un fichier GFF et construit une instance de la classe `Annotation`.

2. **Fusion des annotations**  
   Combine deux annotations via la surcharge de l'opérateur `+`.

3. **Statistiques**  
   Génère des résumés statistiques sur les annotations :
   - Nombre de transcrits par gène.
   - Nombre d'exons par transcrit.

4. **Visualisation**  
   Crée un boxplot représentant la distribution des longueurs totales des exons pour chaque gène.

5. **Exportation**  
   Permet de sauvegarder les annotations dans un fichier GFF compatible ou un fichier texte résumant les informations.

---

## **Utilisation en Ligne de Commande**

Le script propose plusieurs options via des arguments de ligne de commande :

- **Fichier d'entrée GFF** : Spécifiez le fichier à analyser.  
  ```bash
  annotation fichier.gff
  ```

- **Fusionner deux fichiers GFF** :  
  Combine deux annotations et génère un fichier fusionné.  
  ```bash
  annotation fichier1.gff -f fichier2.gff -o fichier_fusionne.gff
  ```

- **Générer un boxplot** :  
  Produit une visualisation des longueurs d'ARN.  
  ```bash
  annotation fichier.gff -i
  ```

- **Afficher les statistiques** :  
  Crée un fichier texte contenant un résumé des annotations.  
  ```bash
  annotation fichier.gff -s stats.txt
  ```

- **Extraire des informations sur un gène spécifique** :  
  Génère un fichier texte avec les détails d'un gène.  
  ```bash
  annotation fichier.gff -g ID_du_gene
  ```

---

## **Exemple d'Exécution**

Pour analyser un fichier `annotations.gff`, fusionner avec un autre fichier, produire un boxplot et générer des statistiques :

```bash
annotation annotations.gff --fusion autre_fichier.gff --output fusion.gff --image --stats statistiques.txt
```

---

## **Dépendances**

- **Python 3.8+**
- Bibliothèques nécessaires : 
  - `matplotlib`
  - `argparse`

Installez les dépendances avec :
```bash
pip install matplotlib argparse
```

---

## **Conclusion**

Ce projet offre un ensemble d'outils puissants et flexibles pour analyser des données GFF. Il est conçu pour être extensible et répond aux besoins des biologistes et bio-informaticiens travaillant avec des annotations génomiques.