# Xomics

## Le fichier GFF
Le format de fichier GFF, similaire au format GTF, est un format de fichier utilisé pour représenter des annotations de génomes. Il contient tous les gènes annotés avec leurs positions et différentes informations connues à leurs sujet.
En plus des gènes, ces fichiers contiennent également d'autres "features" comme par exemple les différents transcrits connus d'un gène ainsi que les différents exons qui les composent.
Les fichiers `data/Human_sample1.gff` et `data/Human_sample2.gff` contiennent l'annotation des quelques gènes du génome humain hg38 ainsi que quelques uns de leurs transcrits.
Pour simplifier les choses, seul 3 types de "features" sont représentées dans ce fichier:  "gene", "mRNA" et "exon". Dans de vrai fichiers d'annotations il peut y avoir beaucoup plus de features différents (CDS, codon, lncRNA, UTR...).
Le fichier est sous format tabulé et organisé sous forme arborescente qui représente l'appartenance : un "exon" appartient à un "mRNA" qui lui même appartient à un "gene".
Ainsi, toutes les lignes qui suivent une ligne "gene" correspondent à des features qui appartiennent à ce gene, et ce,  jusqu'à la prochaine ligne "gene". De même toutes les lignes "exon" qui suivent une ligne "mRNA" sont des exons qui appartiennent à ce transcrit.
On peut résumer les choses de la manière suivante :

```
Ligne "gene" du gène 1
Ligne "mRNA" du transcrit 1 du gène 1
Ligne "exon" de l'exon 1 du transcrit 1 du gène 1
Ligne "exon" de l'exon 2 du transcrit 1 du gène 1
Ligne "exon" de l'exon 3 du transcrit 1 du gène 1
Ligne "exon" de l'exon 4 du transcrit 1 du gène 1
...
Ligne "mRNA" du transcrit 2 du gène 1
Ligne "exon" de l'exon 1 du transcrit 2 du gène 1
Ligne "exon" de l'exon 2 du transcrit 2 du gène 1
Ligne "exon" de l'exon 3 du transcrit 2 du gène 1
...

Ligne "gene" du gène 2
Ligne "mRNA" du transcrit 1 du gène 2
Ligne "exon" de l'exon 1 du transcrit 1 du gène 2
Ligne "exon" de l'exon 2 du transcrit 1 du gène 2
Ligne "exon" de l'exon 3 du transcrit 1 du gène 1
...
Ligne "mRNA" du transcrit 2 du gène 2
Ligne "exon" de l'exon 1 du transcrit 2 du gène 2
Ligne "exon" de l'exon 2 du transcrit 2 du gène 2
Ligne "exon" de l'exon 3 du transcrit 2 du gène 2
...

```


Pour les significations des différentes colonnes, elles sont similaires à celles du format GTF. La spécification exacte se trouve [ici](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md).
Comme pour le format GTF, chaque ligne est découpée en 9 colonnes, les huits première étant bien spécifiées et la dernière étant une colonne "attributs" dans laquelle plusieurs informations peuvent être renseignées.

## Modèle de classe

Notre objectif sera de proposer une implémentation des classes `Gene`, `Transcrit` et `Exon` représentant respectivement des gènes, des transcrits et des exons. Ces objets auront vocation à être créée à partir d'un fichier GFF tels que ceux présents dans le répertoire `data`. Autrement dit les informations que nous aurons sous la main pour créer des objets Gene, Transcrit et Exon seront celles présentes dans le fichier GFF. 
Le code implémentant ces classes sera écrit dans le module `annotation[.py]`.
Un fichier contenant les informations d'un unique gène  vous est fourni sous `data/ADGRB2.gff`.
Une fois ces classes écrites, il vous faudra écrire classe `Annotation` qui représente un ensemble de gènes tel que le représente un fichier GFF.

### Détail des classes `Gene`, `Transcrit` et `Exon`

Le choix des différents attributs et méthodes que vous utiliserez dans vos classes est libre mais quelques spécifications vous sont imposées.
* À partir d'un objet de type `Gene`, il faudra que l'utilisateur puisse avoir accès à tous les objets de type `Transcrit` qui correspondent aux transcrits de ce gène. 
* De même, à partir d'un objet de type `Transcrit`, il faudra que l'utilisateur puisse avoir accès à tous les objets de type `Exon` qui correspondent aux exons de ce transcrit. 
* À partir d'un objet de type `Gene`, il faudra que l'utilisateur puisse avoir accès à son nom et à son identifiant (le `GeneID` présent dans la section `Dbxref`).
* Les objets de type `Transcrit` devront connaître leur identifiant (le champs `transcript_id`).
* À partir d'un objet de type `Transcrit`, il faudra que l'utilisateur puisse avoir accès à l'identifiant du gène auquel il appartient.
* De même à partir d'un objet de type `Exon`, il faudra que l'utilisateur puisse avoir accès à l'identifiant du transcrit et du gène auquel il appartient.

## Méthodes

### Égalité de transcrits

Lorqu'on écrit une classe, python nous laisse la possibilité de redéfinir les opérations usuelles sur les objet de cette classe telle que l'addition, la soustraction, ou encore les tests d'égalité ou de comparaisons.
Pour cela on doit définir ce que signifie ces opérations dans le contexte de la classe qu'on est en train d'écrire. Par exemple si on souhaite pouvoir tester l'égalité entre deux objets de la façon suivante :
```python
if objet1 == objet2:
    ...
```
il faut implémenter la méthode `__eq__` dans la classe. Cette méthode doit prendre `self` en paramètre ainsi qu'un autre objet de même type (celui avec lequel on veut tester l'égalité de notre objet `self`) et renvoyer un  booléen.
C'est alors cette méthode qui sera automatiquement appelée lorsqu'on teste l'égalité entre les deux objets.
* Implémentez la méthode `__eq__` de la classe `Transcit` pour que deux objets `Transcrit` soit considérés égaux s'ils ont le même "transcript_id" et le même "GeneID".

### Fusion de gènes

Étant donnés deux objets de type `Gene` représentant le même gène mais issus d'annotations différentes, on souhaiterait pouvoir créer un nouvel objet de type `Gene` correspondant à la fusion des deux objets initiaux.
On se placera ici dans un cas simple où on considère que les deux objets ne diffèreront que par leur liste de transcrits. Autrement dit étant donnés deux objet de type `Gene` représentant le même gène on souhaiterait en créer un nouveau dont la liste des transcrits correspond à l'union des deux ensembles de transcrits des deux objets `Gene`.
Pour savoir si un transcrit d'un des objets est présent dans l'autre, on ne regardera que l'identifiant du transcrit (pas besoin d'aller vérifier la liste des exons). On pourra donc utiliser le test d'égalité entre les transcrits comme implémenté précédemment.
Pour fusionner les deux gènes nous alons utiliser le symbole "+" de l'addition, on pourra donc écrire:
```python
gene_fusionné = gene1 + gene2

```
Pour pouvoir définir l'addition entre deux objets d'une même classe, il faut implémenter la méthode `__add__` dans la classe. Cette méthode prend en paramètre `self` et un autre objet de même type et retourne un nouvel objet de la classe.

* Implémentez la méthode `__add__` pour la classe gène qui lèvera une exeptions si les deux gènes (self et l'autre) n'ont pas le même "GeneID" et retournera un nouvel objet `Gene` qui contiendra les transcrits présents dans les deux gènes initiaux.


## Classe Annotation

Implémentez maintenant une classe `Annotation` qui représentera une collection de gène telle que celle présente dans un fichier GFF.
Le constructeur de la classe devra prendre un fichier GFF et créer tous les objets `Gene`, `Transcit` et `Exon` correspondant. 
À partir d'un objet annotation, l'utilisateur devra être capable d'avoir accès aux gènes présents à l'intérieur.

### Fusion d'annotation

Implémentez la méthode `__add__` de la classe annotation pour que l'on puisse fusionner deux annotations en utilisant le symbole "+" de l'addition. Dans la fusion des annotations, si un gène n'apparait que dans une seule des deux annotations alors il sera présent tel quel dans l'annotation résultat, sinon le gène présent dans la fusion sera la fusion des deux gènes telle que définie précédemment avec la méthode `__add__` de la classe `Gene`.
Vous pouvez tester votre méthode avec les deux fichier `data/Human_sample1.gff` et  `data/Human_sample2.gff`.

### Méthode get_gene
Implémentez une méthode `get_gene` qui, étant donné un GeneID passé en paramètre sous forme de chaîne de caractères, retourne l'objet `Gene` de l'annotation qui correspond à cet identifiant et lève une exception si aucun gène ne possède cet identifiant dans l'annotation.

### Exporter en gff

Écrire une méthode `to_gff` qui prend un chemin de fichier en paramètre et écrit sous format GFF le contenu de l'objet annotation 
Astuce : Vous pouvez enregistrer dans les objets `Gene`, `Transcrit` et `Exon` leur ligne de fichier GFF à partir desquelles ils ont été créés.

## Visualisation de données

On souhaite visualiser la distribution des longueurs des transcrits pour des gènes. Étant donné un transcrit, sa longueur sera la somme de la longueur des exons qui le compose. 
On souhaite dessiner un boxplot (boite à moustache) ayant une boite par gène, et la boite d'un gène sera définie par les longueurs des différents transcrits de ce gène. 

Vous dessinerez ce boxplot grâce à la librarie matplotlib (à installer) en vous basant sur l'exemple suivant.
### 

```python
from matplotlib import figure

fig = figure.Figure()
ax   = fig.subplots(1, 1)
RNAlens = [
            [300, 1558, 845, 130, 200 ], # longueur des transcrits du gène 1 
            [400, 650, 768],  # longueur des transcrits du gène 2 
            [658, 825, 1154, 478] # longueur des transcrits du gène 3 
            ]
nom_des_genes = ["gene1", "gene2", "gene3"]
ax.boxplot(RNAlegnth, tick_labels=nom_des_genes)
fig.savefig("test.png")
```

* Écrire la méthode `rna_lens` dans la classe `Annotation` qui prendra un nom de fichier en paramètre et qui sauvegardera le boxplot dans le fichier des longueurs des transcrits pour tous les gène de l'annotation dans ce fichier.


