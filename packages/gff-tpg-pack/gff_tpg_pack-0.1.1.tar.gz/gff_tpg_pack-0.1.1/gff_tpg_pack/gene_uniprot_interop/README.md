# Gene Uniprot Interop


## Un laboratoire pas très rangé

Bonjour cher stagiaire, soyez le bienvenu dans notre laboratoire. Nous avons besoin de vos compétences, de toute urgence !

Des années de travail de recherche en biologie du developpement sont sur le point de révolutionner notre compréhension du vivant. Seuls quelques analyses complémentaires sont exigées par un éditeur un peu tatillon...

Malheuresement, le post-doctorant qui était la cheville ouvrière de cette étude, est parti vers une position des plus prestigieuse. Dans sa hâte, il a malencontreusement melangé les tubes contenant les extraits tissulaires necessaires aux analyses complémentaires.

Je ne dispose donc que de 5 tubes et de 5 étiquettes sans leurs correspondances. Nous sommes experts en biologie moléculaire et nous avons effectué une analyse bulk RNASeq sur nos 5 précieux échantillons.
Chacune des analyses RNASeq est écrite dans un fichier texte nommé d'après le numéro du tube (`countings1.tsv, ..., countings5.txt`).

Pour nous permettre d'aller plus loin, nous avons desespérement besoin de VOTRE analyse bionformatique de ces fichiers résultats afin d'assigner les étiquettes aux bons échantillons.
Les financements de l'étude arrivant à leurs termes, **Vous être notre seul espoir !**

## Euh ...

Pas de panique! Un ancien étudiant du Master avait participé à cette étude et avait constitué un jeux de protéines depuis la base de données uniprot.

Par ailleurs, l'entreprise sollicitée pour l'analyse RNASeq, a fourni le fichier `gff` utilisé pour la quantification.

Les affaires reprennent ! D'une part, les protéines sont très bien annotées en terme de fonctions et de localisation et d'autre par le fichier `gff` devrait vous permettre de relier les comptages de transcrit avec le gène correspondant !!!

Mais le temps presse, vous ne pourrez pas parser/organiser les données gff du génome de référence **ET** les données annotées des protéines **ET** évaluer les comptages.

Vous vous rappelez vaguement avoir développé, lors d'une UE de M1, un parser pour l'une de ces tâches. Si seulement, un autre binome avait publié le package publique permettant de réaliser une autre de ces taches. Vous pourriez alors consacrer tout votre temps à l'analyse des fonctions des protéines dont les gènes sont surexprimés dans les différents échantillons. Et, avec un peu de chance, faire correspondre les 5 échantillons à leurs étiquettes.

## Communication d'un package

Travailler sur une autre branche `publish` de votre repo.
Organiser les fichiers dans cette nouvelle branche en suivant le patron ci dessous, (on suppose que votre répo est un repertoire local `notre_repo`).

### Structure des repertoires
```
notre_repo
├── README.md
└── hello
    ├── __init__.py
    ├── utils
    │   ├── __init__.py
    │   └── translate.py
    └── world.py
```
On notera:
-  la présence d'un fichier `README.md` qui contiendra la documentation des fonctions publiques de votre package.
- un repertoire portant le nom de votre package `hello/`
- sous ce repertoire une organisation du code en sous repertoires si necessaire.
- chaque repertoire sous `hello/` **doit** contenir un fichier `__init__.py` qui peut être vide.

### Fichier de documentation
A ce stade, il est primordial de commencer à renseigner les fonctions que vous souhaitez rendre publiques, en éditant le fichier `README.md`. 
On utilise le language [markdown](https://www.markdownguide.org/basic-syntax/) pour écrire cette documentation en proposant notamment des lignes d'exemples, par exemple à l'aide de [*codes-fences*](https://www.markdownguide.org/basic-syntax/#code).

### Installation d'un gestionnaire de paquets
Ce programme va nous aider à prendre en charge les dépendances de notre package et à detailler sa description. Différents progammes existent, nous allons [installer et utiliser uv](https://docs.astral.sh/uv/getting-started/installation/).
Nous allons commencer par demander à `uv` dec créer le fichier `pyproject.toml`, en tapant `uv init` dans le repertoire de notre repo.
Attention par défaut, le nom de notre package porte celui du repertoire (ex: `notre_repo`), editez le fichier `toml` pour le corriger si nécessaire.
Notre package ayant besoin de la librarie matplotlib pour fonctionner, on va l'ajouter à la liste de dépendances via la commande: `uv add matplotlib`.
* Il est inutile d'ajouter les modules de la librarie standard (`sys`, `json`, etc..) aux dépendances.
* Les dépendances seront automatiquement installés préalablement à notre package.
* La liste des dépendances est écrite et modfiable à tout moment dans le fichier `pyproject.toml`.

### Declaration des informations du package
Le fichier `pyproject.toml` peut contenir [beaucoup d'autres informations](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml) comme le numéro de version (fixé à 0.1.0 pour commencer). Editer ce fichier, pour ajouter votre binôme en tant qu'auteurs, un lien vers le répo gitlab et profitez en pour déclarer les mots-clés appropriés. Enfin, déclarer bien le fichier `README.md` comme documentation; ainsi celle-ci sera formatée et affichée lors de la (future) mise en ligne de votre package.

### Test local du package
Il est temps de nous assurer que votre package fonctionne localement. La commande `uv run python` va démarrer un environnement virtuel qui va nous permettre de tester votre module (comme si notre package était 'déjà' installé).
```sh
notre_repo$ uv run python
Python 3.12.4 (main, Jun 13 2024, 21:31:44) [Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import hello.world
>>> hello.world.tell()
Hello from world!
>>> 
```
Sur la base de l'organisation en repertoire illustrée precemment, le prompt python permet de valider les correspondances entre l'arborescence du package et ses modules et commandes.

### Création de la distribution
La distribution d'un package est l'ensemble des fichiers qui sera effectivement téléchargé par l'utilisateur lors de son intallation. Ces fichiers sont regroupés dans une seule archive à l'extension `.whl`. En fait, cette archive sera simplement décompréssée dans le répertoire `site-packages` lors de l'installation du package avec `pip`.

Dans le répertoire racine de notre package exécutons la commande: `uv build`. Un répertoire `dist/` est alors créé. Inspecter son contenu, essayer de lister le contenu de ce fichier `.whl` (`tar -tf dist/*whl`). En quoi consiste-t-il ?

### Publication, mise en ligne
PyPI est le serveur d'indexation de packages publiques principal du language Python.
Ce serveur permet de lister et ou de télécharger la plupart des packages Python, `pip` utilise d'ailleurs PyPI  pour obtenir les fichiers d'un package lors d'un `pip install <package>`.

Il va nous uploader notre fichier `dist/*.whl` sur PyPI !!

1. Creer un compte PyPI
2. Obtenir un token PyPI pour nous authentifier lors de l'upload
3. Déclarer localement la valeur du toke, `export UV_PUBLISH_TOKEN=<token_PyPI>`
4. Uploader notre package: `uv publish`
5. Apprecier le moment, en consultant `https://pypi.org/project/<mon_package>/`

### Tester l'installation
Il est temps de nous assurer que notre package peut être installé et utilisé dans un environnement vierge. Dans un tout autre repertoire que votre répo:
1. Créer un [environnement virtuel](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments): `python[3] -m venv <nom_de_votre_environnemnt de test>`
2. Activer l'environnement: `source <nom_de_votre_environnemnt de test>/bin/activate`
3. Installer votre package: `(<nom_de_votre_environnemnt de test>) pip install <mon_package>`
4. Démarrer un prompt Python dans cet environnement et tester les appels aux modules de votre package.


#### Corrections et numéro de version
Si vous êtes amené.e.s à modifier votre package pour réussir à le publier, à l'installer, ou simplement si vous decouvrez des bugs à corriger ou des fonctionnalités à ajouter; vous devrez régulierement `build` votre package pour le re-uploader sur PyPI. **Attention, vous devrez alors incrementer son numéro de version dans `pyproject.toml` AVANT de `uv build` et `uv publish`**.

## Tableau de bord 

Binome | Fonctionalité | Nom du package | Url GitLab| Version
---    | ---          | ---            | ---       | ---
Magloire/Severin |  gff  |                |           |
Elsa/Salma |  uniprot |   uniprot_xplorer|  [branche publish](http://pedago-service.univ-lyon1.fr:2325/ebaligand/uniprot.git)| 0.1.1
Lorcan/Baptiste | uniprot| uniprot_lb_poo | [branche publish](http://pedago-service.univ-lyon1.fr:2325/briou/uniprot.git)    | 0.1.7
Clara/Mariam |    |                |           |
Thomas/Paul | gff | gff_tpg_pack| [branche publish](http://pedago-service.univ-lyon1.fr:2325/tgagnieu/xomics/-/tree/publish?ref_type=heads) |1.0.1
Maya/Thibaud |  uniprot | uniproj_2024|[branche publish](http://pedago-service.univ-lyon1.fr:2325/tguiramand/uniprot/-/tree/publish?ref_type=heads) | 0.1.3
Ndeye/Imene |    |                |           |
Kira/Kessen | uniprot | pack_uniprot | [branche publish](http://pedago-service.univ-lyon1.fr:2325/kkorelskaia/uniprot/-/tree/publish?ref_type=heads) | 0.1.1
Martin/Matthieu | uniprot | unipack | branche [publish](http://pedago-service.univ-lyon1.fr:2325/projet-poo/uniprot/-/tree/publish) | 0.1.2
Eleonora | uniprot | uniprot_m1_2024 | branche [publish](http://pedago-service.univ-lyon1.fr:2325/egeraci/uniprot/-/tree/publish) | 2.0.0




## Pipeline d'analyses
A vous d'implémenter l'analyse des cinq échantillons dans un
script prenant en arguments les fichiers GTF, uniprot et de comptages.
Soit un fichier `data/countings/countingsX.txt`, proposer à votre superviseur des graphiques 
aidant à caracteriser les échantillons.

> Dépendances 
* Package GTF
* Package Uniprot
* Package matplotlib


### Objectifs
Votre superviseur vient vers vous en courant:

"Je viens de trouver une photo dans l'ancien bureau de mon collaborateur !"

![indice](assets/indice.jpg "Indice")

##### Visualisons les fonctions des protéines abondantes dans les échantillons numérotés et retrouvons ensemble les cinq tissus de notre étude !

