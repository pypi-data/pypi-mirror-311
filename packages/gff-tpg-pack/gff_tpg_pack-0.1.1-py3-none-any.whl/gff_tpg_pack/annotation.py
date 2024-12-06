'Import de librairie'
import matplotlib.pyplot as plt
import argparse

'Définitions des Classes'
class Gene:
    def __init__(self, gene_id, gene_name, seqid, start, end, strand, ligne):
        self.gene_id = gene_id
        self.gene_name = gene_name
        self.seqid = seqid
        self.start = start
        self.end = end
        self.strand = strand
        self.transcrits = []  # Liste des transcrits associés à ce gène
        self.ligne = ligne

    def ajouter_transcrit(self, transcrit):
        """
        Ajoute un transcrit au gène.
        """
        self.transcrits.append(transcrit)

    def obtenir_transcrits(self):
        """
        Retourne les transcrits associés au gène.
        """
        return self.transcrits

    def __repr__(self):
        """
        Retourne certaines informations d'un gène.
        """
        return f"Gene({self.gene_name}, {self.gene_id}, {self.seqid}:{self.start}-{self.end})"
    
    def __add__(self, other):
        """
        Fusionne deux gènes ayant le même 'gene_id'.
        """
        if not isinstance(other, Gene):
            raise TypeError("L'objet à fusionner doit être de type 'Gene'.")
        
        if self.gene_id != other.gene_id:
            raise ValueError(f"Impossible de fusionner les gènes avec des IDs différents: {self.gene_id} et {other.gene_id}.")
        
        # Fusionner les transcrits (sans doublons grâce à set{} et __eq__ sur les deux listes de transcrit éclatées par *)
        nouveaux_transcrits = list({*self.transcrits, *other.transcrits})

        # Créer un nouveau gène fusionné
        gene_fusionne = Gene(
            self.gene_id,
            self.gene_name,
            self.seqid,
            min(self.start, other.start),
            max(self.end, other.end),
            self.strand,
            self.ligne,
        )

        for transcrit in nouveaux_transcrits:
            gene_fusionne.ajouter_transcrit(transcrit)

        return gene_fusionne

class Transcrit:
    def __init__(self, transcrit_id, gene, seqid, start, end, strand,ligne):
        self.transcrit_id = transcrit_id
        self.gene = gene  # Le gène auquel appartient ce transcrit
        self.seqid = seqid
        self.start = start
        self.end = end
        self.strand = strand
        self.exons = []  # Liste des exons associés à ce transcrit
        gene.ajouter_transcrit(self)  # Ajoute ce transcrit au gène
        self.ligne = ligne

    def ajouter_exon(self, exon):
        """
        Ajoute un exon au transcrit.
        """
        self.exons.append(exon)

    def obtenir_exons(self):
        """
        Retourne les exons associés au transcrit.
        """
        return self.exons

    def __repr__(self):
        """
        Retourne certaines informations d'un trascrit.
        """
        return f"Transcrit({self.transcrit_id}, {self.gene.gene_name}, {self.seqid}:{self.start}-{self.end})"
    
    def __hash__(self):
        return hash(self.seqid)
    
    def __eq__(self, other):
        """
        Vérifie l'égalité entre deux transcrits.
        """
        if not isinstance(other, Transcrit):
            return NotImplemented
        return self.transcrit_id == other.transcrit_id and self.gene.gene_id == other.gene.gene_id


class Exon:
    def __init__(self, start, end, transcrit, seqid, strand, ligne):
        self.start = start
        self.end = end
        self.transcript = transcrit  # Le transcrit auquel appartient cet exon
        self.gene = transcrit.gene  # Le gène auquel appartient ce transcrit
        self.seqid = seqid
        self.strand = strand
        transcrit.ajouter_exon(self)  # Ajoute cet exon au transcrit
        self.ligne = ligne

    def __repr__(self):
        """
        Retourne certaines informations d'un exon.
        """
        return f"Exon({self.seqid}:{self.start}-{self.end}, {self.transcript.transcrit_id})"


class Annotation:
    def __init__(self):
        self.genes = {}  # Dictionnaire pour stocker les gènes par leur ID

    def ajouter_gene(self, gene):
        """
        Ajoute un gène à l'annotation.
        """
        self.genes[gene.gene_id] = gene

    def obtenir_gene(self, gene_id):
        """
        Retourne un gène par son ID.
        """
        return self.genes.get(gene_id)
    
    def get_gene(self, gene_id):
        """
        Retourne un gène par son ID et retourne un message d'erreur si l'ID n'est pas une clée d'annotation.
        """
        gene_id_list = list(self.genes.keys())
        if gene_id in gene_id_list:
            return self.genes[gene_id]
        raise ValueError(f"Aucun gène avec l'identifiant '{gene_id}' trouvé dans l'annotation.")

    def __repr__(self):
        """
        Retourne un nombre correspondant au nombre de gènes contenu dans cette annotation.
        """
        return f"Annotation({len(self.genes)} genes)"
    
    def __add__(self,other):
        """
        Fusionne deux annotations en fusionnant les gènes ayant le même 'gene_id' dans une nouvelle annotation et en ajoutant également les autres gènes.
        """
        if not isinstance(other, Annotation):
            raise TypeError("L'objet à fusionner doit être de type 'Annotation'.")
        
        # Nouvelle annotation résultante
        annotation_resultante = Annotation()
        
        # Recuperer toutes les clés gene_id de self.genes et other.genes, en fusionant les clés similaires
        gene_id_list = list({*self.genes.keys(), *other.genes.keys()})

        # Utiliser les clés gene_id pour ajouter les genes dans annotation_resultante
        for gene_ID in gene_id_list:
            if gene_ID in self.genes and gene_ID in other.genes :
                gene = self.obtenir_gene(gene_ID) + other.obtenir_gene(gene_ID)
                annotation_resultante.ajouter_gene(gene)
            elif gene_ID in self.genes:
                gene = self.obtenir_gene(gene_ID)
                annotation_resultante.ajouter_gene(gene)
            else:
                gene = other.obtenir_gene(gene_ID)
                annotation_resultante.ajouter_gene(gene)
        
        return annotation_resultante
    
    def rna_lens(self,chemin): 
        """
        Créer un Boxplot ayant une boite par gène, la boite étant définie par les longueurs des différents transcrits de ce gène, et l'enregistre au format .pnj 
        """
        # Création de la figure et des axes
        fig, ax = plt.subplots(1, 1, figsize=(15, 8))  # Taille de la figure (largeur x hauteur)

        # Collection des données, en commençant par récupérer les gene_id dans self
        gene_id_list = list(self.genes.keys())

        ## le nom des genes
        nom_des_genes = []
        for gene_id in gene_id_list:
            nom_des_genes.append(self.obtenir_gene(gene_id).gene_name)

        ## la tailles des exons et les nom des fichiers qui ont servit à générer les 
        RNAlens = []
        for gene_id in gene_id_list:
            ListLenExon=[]
            for transcrit in self.obtenir_gene(gene_id).transcrits:
                LenExon=0
                for exon in transcrit.exons:
                    LenExon = LenExon + exon.end - exon.start
                ListLenExon.append(LenExon)
            RNAlens.append(ListLenExon)

        # Création du boxplot
        ax.boxplot(RNAlens)

        # Personnalisation des labels de l'axe des abscisses
        ax.set_xticklabels(nom_des_genes, rotation=45, ha='right')

        # Titres et labels des axes
        ax.set_title(f"Distribution des longueurs d'ARN par gène du fichier {chemin}")
        ax.set_ylabel("Longueur totale des exons (pb)")
        ax.set_xlabel("Nom des gènes")

        # Ajustement automatique des marges pour éviter le chevauchement
        plt.tight_layout()

        # Sauvegarde de la figure
        fig.savefig(f"Box_Plot_{self}.png")

    def to_gff(self,chemin):
        """
        Ecrit un nouveau fichier .gff avec les informations de self
        """
        with open(chemin,'w') as f:
            gene_id_list = list(self.genes.keys())
            for gene_id in gene_id_list:
                f.write (self.obtenir_gene(gene_id).ligne)
                for transcrit in self.obtenir_gene(gene_id).transcrits: # self.obtenir_gene(gene_id).transcrits la liste des trascrits du gène d'ID "gene_id"
                    f.write (transcrit.ligne)
                    for exon in transcrit.exons:
                        f.write (exon.ligne)
    
    def stat(self,chemin):
        """
        Ecrit dans un fichier .txt les gene_id de self avec leur nombre de transcrits, et pour chaque transcrit le nombre d'exons
        """
        with open(chemin,'w') as f:
            gene_id_list = list(self.genes.keys())
            for gene_id in gene_id_list:
                f.write (f'Le gene {self.obtenir_gene(gene_id).gene_id} possède {len(self.obtenir_gene(gene_id).transcrits)} trascrits:\n')
                for transcrit in self.obtenir_gene(gene_id).transcrits: # self.obtenir_gene(gene_id).transcrits la liste des trascrits du gène d'ID "gene_id"
                    f.write (f"Le transcrit d'identifiant {transcrit.transcrit_id} est costitué de {len(transcrit.exons)} exons:\n")
           

####################################################################################################################################################

'Fonction de parsing du fichier GFF'
def parser_gff(fichier_gff):
    """
    Parcour un fichier .gff et initialise les classes Gene, Transcrit, Exon puis Annotation. 
    """
    annotation = Annotation()
    current_gene = None
    current_transcrit = None

    with open(fichier_gff, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue  # Ignorer les lignes de commentaire

            # Découper la ligne en colonnes
            columns = line.strip().split("\t")
            seqid, source, feature_type, start, end, score, strand, phase, attributes = columns

            start = int(start)
            end = int(end)

            # Parsing des attributs
            attributes_dict = {attr.split()[0]: attr.split()[1] for attr in attributes.split(";")}

            if feature_type == "gene":
                # Création du gène
                gene_id = attributes_dict.get("ID")
                gene_name = attributes_dict.get("Name", gene_id)
                current_gene = Gene(gene_id, gene_name, seqid, start, end, strand,line)
                annotation.ajouter_gene(current_gene)

            elif feature_type == "mRNA":
                # Création du transcrit
                transcript_id = attributes_dict.get("ID")
                parent_id = attributes_dict.get("Parent")
                if current_gene and parent_id == current_gene.gene_id:
                    current_transcrit = Transcrit(transcript_id, current_gene, seqid, start, end, strand,line)

            elif feature_type == "exon":
                # Création de l'exon
                parent_id = attributes_dict.get("Parent")
                if current_transcrit and parent_id == current_transcrit.transcrit_id:
                    Exon(start, end, current_transcrit, seqid, strand,line)
    return annotation

def main():
    """
    Permet d'utiliser les différentes méthodes de la classe Annotation dirrectement depuis un terminal Bash avec : python3 annotation.py chemin_du_fichier_gff --méthode
    """
    # Création du parser pour les arguments
    parser = argparse.ArgumentParser(description="Analyse des annotations biologiques.")
    
    # Argument pour le fichier d'annotation (obligatoire)
    parser.add_argument("file", type=str, help="Chemin du fichier d'annotation GFF.")
    
    # Argument pour afficher les statistiques des annotations
    parser.add_argument("--stats", "-s", type=str, help="Afficher les statistiques des annotations.")
    
    # Argument pour spécifier qu'il faut fusionner le fichier d'entrer avec ce fichier
    parser.add_argument("--fusion", "-f", type=str, help="Le chemin du fichier où sauvegarder le boxplot et necessite l'utilisation de --output pour définir le nom du fichier de sortie.")

    # Argument pour spécifier le fichier de sortie au format .gff
    parser.add_argument("--output", "-o", type=str, help="Le chemin du fichier de sortie sauvegarder.")

    # Argument pour spécifier le fichier de sortie du boxplot au format .png
    parser.add_argument("--image", "-i", action="store_true" , help="Le chemin du fichier où sauvegarder le boxplot (si 'rna_lens' est appelé).")

    # Argument pour spécifier le gene_id correspondant au gene dont on veux écrire ses informations dans un fichier texte au format .txt
    parser.add_argument("--geneid", "-g", type=str, help="Ecrirt dans un fichier .txt du nom de gene_id les informations qui correspondent au gene s'il est présent dans le fichier .gff.")
    
    # Analyse des arguments
    args = parser.parse_args()

    # Vérifier que le fichier d'entrée existe avant de continuer
    try:
        # Charger les annotations depuis le fichier
        annotation = parser_gff(args.file)
        #annotation.parse(args.file)  # Méthode pour charger les données du fichier
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return
    
    # Si l'option --fusion ou -f est utilisée, uttilise la méthode __add__ de la classe Annotation
    fusion = 0
    if args.fusion and args.output:
        try:
            annotation2 = parser_gff(args.fusion)  # Appel de la méthode fonction parser_gff pour le fichier à fusionner 
            annotation = annotation + annotation2
            print(f"les fichiers {args.file} et {args.fusion} ont été fusionnés and le fichier {args.output}")
            fusion = 1
        except Exception as e:
            print(f"Erreur lors de la fusion des fichier : {args.file} et {args.fusion}")

    # Si l'option --geneid ou -g est utilisée, uttilise la méthode get_gene de la classe Annotation
    if args.geneid:
        try:
            gene = annotation.get_gene(args.geneid)
            with open(f'{args.geneid}.txt','w') as fgeneid:
                fgeneid.write(f"Le gène d'identifiant {gene.gene_id} à pour nom : {gene.gene_name}\n")
                fgeneid.write(f"Les positions génomique du gène sont {gene.start} et {gene.end}, et est sur le br'in d'AND {gene.strand}\n")
                fgeneid.write(f"Son identifiant de séquence est le : {gene.seqid}\n")
                fgeneid.write(f"Ce gène possède {len(gene.transcrits)} transcrit(s), et leurs identifiant sont :\n")
                for transcrit in gene.transcrits:
                    fgeneid.write (f"{transcrit.transcrit_id}\n")
            print(f"Les informations du gene {args.geneid} ont bien été écrites dans le fichier {args.geneid}.txt")
        except Exception as e:
            print(e)

    # Si l'option --image ou -i est utilisée, uttilise la méthode rna_lens de la classe Annotation
    if args.image:
        if fusion == 0:
            try:
                annotation.rna_lens(args.file)
                print(f"Le Boxplot du fichier {args.file} a été créé")
            except Exception as e:
                print(f"Erreur lors de la creation du Boxplot")
        else:
            try:
                annotation.rna_lens(args.output) 
                print(f"Le Boxplot du fichier {args.output} a été créé")
            except Exception as e:
                print(f"Erreur lors de la creation du Boxplot")
    
    # Si l'option --stats est utilisée, appeler la méthode stats de la classe Annotation
    if args.stats:
        try:
            annotation.stat(args.stats)
            print(f"le fichier créer est : {args.stats}")
        except Exception as e:
            print(f"Erreur lors de l'affichage des statistiques : {e}")

    # Si l'option --output ou -o est utilisée, appel de la méthode to_gff de la classe Annotation
    if args.output:
        try:
            annotation.to_gff(args.output)
            print(f"le fichier créer est : {args.output}")
        except Exception as e:
            print(f"Erreur lors de la création du fichier de sortie : {e}")

if __name__ == "__main__":
    main()

