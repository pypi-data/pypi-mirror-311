try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib n'est pas installé sur votre python! il est pourtant nécessaire pour la représentation graphique de vos résultat. vous devez donc l'installer avec la commande :")
    print("pip install matplotlib")
    exit(1)

class Gene:
    def __init__(self, gene_id, gene_name, start, end, ligne_base=None):
        """
        permet d'initialiser l'objet "Gene" avec (dans l'ordre) son identifiant, nom, début de position, fin de position, et la ligne de base au format GFF
        """
        self.gene_id = gene_id
        self.gene_name = gene_name
        self.start = int(start)
        self.end = int(end)
        self.transcripts = []
        self.ligne_base = ligne_base

    def add_transcript(self, transcript):
        """
        permet d'ajouter un transcrit à la liste de transcrits associés au gène, si ce n'est pas déjà le cas
        """
        if transcript not in self.transcripts:
            self.transcripts.append(transcript)
            
    def get_length(self):
        """
        calcule la longueur totale des transcrits associés au gène. 
        retourne la longueur totale des transcrits
        """
        total_length = 0
        for transcript in self.transcripts:
            total_length += transcript.get_length()  
        return total_length

    def __add__(self, other):
        """
        fusionne deux gènes, si leur id sont identiques après vérification. 
        retourne une erreur si l'objet à merge n'est pas un gène, ou si l'id est différent. sinon, retourne le nouveau gène fusionné.
        """
        if not isinstance(other, Gene):
            raise TypeError("impossible d'ajouter un objet Gene avec un objet non-Gene.")
        if self.gene_id != other.gene_id:
            raise ValueError(f"impossible de merge deux ID différents: {self.gene_id} et {other.gene_id}.")
        merged_gene = Gene(self.gene_id, self.gene_name, self.start, self.end, self.ligne_base)
        merged_transcripts = self.transcripts + [t for t in other.transcripts if t not in self.transcripts]
        for transcript in merged_transcripts:
            merged_gene.add_transcript(transcript)
        return merged_gene

    def __repr__(self):
        """
        prend le gène et ses informations, et le retourne sous forme de chaine de caractère.
        """
        return (f"Gene(gene_id={self.gene_id}, gene_name={self.gene_name}, "
                f"transcripts_count={len(self.transcripts)}, "
                f"start={self.start}, end={self.end})")
    

class Transcript:
    def __init__(self, transcript_id, transcript_name, gene_id, start, end, ligne_base=None):
        """
        permet d'initialiser l'objet "Transcript" avec (dans l'ordre) son identifiant, nom, son gène parent, début de position, fin de position, ses exons, et la ligne de base au format GFF
        """
        self.transcript_id = transcript_id
        self.transcript_name = transcript_name
        self.gene_id = gene_id
        self.start = int(start)
        self.end = int(end)
        self.exons = []
        self.ligne_base = ligne_base

    def add_exon(self, exon):
        """        
        permet d'ajouter un exon à la liste des exons associés au transcrit
        """
        self.exons.append(exon)
        
    def get_length(self):
        """
        calcule la longueur totale des exons associés au transcrit. 
        retourne la longueur totale des exons
        """
        total_length = 0  
        for exon in self.exons:
            total_length += (exon.end - exon.start + 1) 
        return total_length  

        

    def __repr__(self):
        """
        prend le transcrit et ses informations, puis le retourne sous forme de chaine de caractère.
        """
        return (f"Transcript(transcript_id={self.transcript_id}, "
                f"gene_id={self.gene_id}, exons={len(self.exons)}, "
                f"start={self.start}, end={self.end})")
            
    def __eq__(self, other):
        """
        permet de vérifier si deux transcrits sont les mêmes (en vérifiant l'id du transcrit, et le gène parent)
        retourne True s'ils sont identiques, False si ce n'est pas le cas.
        """
        if isinstance(other, Transcript):
            return self.transcript_id == other.transcript_id and self.gene_id == other.gene_id
        return False

class Exon:
    def __init__(self, exon_id, transcript_id, gene_id, start, end, ligne_base=None):
        """
        permet d'initialiser l'objet "Exon" avec (dans l'ordre) son identifiant, son transcrit parent (id), son gène parent (id), début de position, fin de position, et la ligne de base au format GFF
        """
        self.exon_id = exon_id
        self.transcript_id = transcript_id
        self.gene_id = gene_id
        self.start = int(start)
        self.end = int(end)
        self.ligne_base = ligne_base

    def __repr__(self):
        """
        prend l'exon et ses informations (identifiant, transcrit parent, gène parent, début et fin de position), puis le retourne sous forme de chaine de caractère.
        """
        return (f"Exon(exon_id={self.exon_id}, "
                f"transcript_id={self.transcript_id}, "
                f"gene_id={self.gene_id}, "
                f"start={self.start}, end={self.end})")


def sep_ligne(ligne):
    """
    permet de séparer, à l'intérieur du fichier gff, les différentes informations de chaque ligne sous forme de colonnes. dans chaque colonne se trouve les éléments de feature (gène, transcrit ou exon), de début et fin de position, et l'éléments d'attributs.
    retourne un tuple avec chaque élément : feature, début de position du feature, fin de position du feature, attributs contenant les informations supplémentaires.
    """
    colonne = ligne.strip().split("\t")                     #strip() pour retirer les espaces autour de la ligne, et split(\t) pour marquer la séparation des lignes en colonnes aux endroits des tabulations.
    feature = colonne[2]
    start, end = colonne[3], colonne[4]
    attributs = colonne[8]
    return feature, start, end, attributs


def sep_attributs(chaine_attributs):
    """
    permet d'extraire la partie attributs en dictionnaire.
    retourne un dictionnaire des attributs séparés individuellement
    """
    attributs = {}
    attributs_sep = chaine_attributs.strip().split(";")     #ici cela permet de séparer la ligne d'attributs par leur séparateur ";".
    for objet in attributs_sep:                             
        objet = objet.strip()
        if " " in objet:
            clé, val = objet.split(" ", 1)
            attributs[clé.strip()] = val.strip()
    return attributs


class Annotation : 
    def __init__(self,path_gff):
        """
        initialise la classe Annotation, qui contient le dictionnaire des gènes. elle permet de parcourir le fichier gff, et charge les informations à partir de ce fichier
        """
        self.genes = {}
        if path_gff :      
            self.get_gff(path_gff)  
    

    def get_gff(self,path_gff):
        """
        permet de charger les informations du fihier gff, et construit l'annotation en partant de chaque "feature" (gène, transcrit ou exon)
        """
        with open(path_gff, 'r') as file:                               #ouvre le fichier gff à partir du chemin donné et seulement en mode lecture, "r"
            for ligne in file:
                feature, start, end, attributs = sep_ligne(ligne)
                attributs_dict = sep_attributs(attributs)

                if feature == "gene":
                    gene_id = attributs_dict.get("ID", "inconnu")
                    name = attributs_dict.get("Name", "inconnu")
                    gene_etudie = Gene(gene_id, name, start, end)
                    self.genes[gene_id] = gene_etudie

                elif feature == "mRNA":
                    transcript_id = attributs_dict.get("ID", "inconnu")
                    parent_gene = attributs_dict.get("Parent", "inconnu")
                    transcript_name = attributs_dict.get("Name", "inconnu")
                    transcrit_etudie = Transcript(transcript_id, transcript_name, parent_gene, start, end)
                    self.genes[parent_gene].add_transcript(transcrit_etudie)

                elif feature == "exon":
                    exon_id = attributs_dict.get("ID", "inconnu")
                    parent_transcript = attributs_dict.get("Parent", "inconnu")

                    for gene in self.genes.values():                    #pour vérifier que l'exon appartient au bon gene (ensuite au bon transcrit)
                        for transcript in gene.transcripts:            #pour regarder les transcrits dans le dict genes
                            if transcript.transcript_id == parent_transcript:   #vérifie que l'id transcrit est le même que l'id gene
                                exon = Exon(exon_id, parent_transcript, gene.gene_id, start, end) 
                                transcript.add_exon(exon)                       # 
                                break  
        

    def get_gene(self, gene_id):
        if gene_id not in self.genes:
            raise ValueError(f"pas de gène avec l'ID {gene_id} trouvé dans l'annotation.")
        return self.genes[gene_id]

                   

    def __add__(self, other):
        """
        permet de fusionner des annotations de gènes, lorsque celles-ci sont identiques
        retourne alors un nouvel objet Annotation de gène fusionné
        """
        if not isinstance(other, Annotation):                   #sert à vérifier que l'objet avec lequel on veut merge appartient bien à la classe annotation
            raise TypeError("impossible d'ajouter un objet annotation avec un objet non-annotation") 
        merged_annotation = Annotation("")                      #on part d'une annotation vide qu'on rempli ensuite
        merged_annotation.genes = self.genes.copy()             #.copy() permet de créer une copie du dict. genes, sans risquer de modifier le dictionnaire déjà créé
        for gene_id, other_gene in other.genes.items():         #.items() permet de récupérer les clé + val de l'autre dict.
            if gene_id in merged_annotation.genes:
                merged_annotation.genes[gene_id] = merged_annotation.genes[gene_id] + other_gene
            else:
                merged_annotation.genes[gene_id] = other_gene
        return merged_annotation

    




    def to_gff(self, output_path):
        """
        permet d'exporter l'annotation sous la forme d'un nouveau fichier gff. intervient dans le script d'exécution pour retourner un fichier de sortie. 
        """
        with open(output_path, 'w') as file:
            for gene in self.genes.values():
                if gene.ligne_base is None:
                    gene.ligne_base = f"{gene.gene_id}\t.\tgene\t{gene.start}\t{gene.end}\t.\t.\t.\tID={gene.gene_id};Name={gene.gene_name}"
                file.write(gene.ligne_base + "\n")
                
                for transcript in gene.transcripts:
                    if transcript.ligne_base is None:
                        transcript.ligne_base = f"{transcript.gene_id}\t.\tmRNA\t{transcript.start}\t{transcript.end}\t.\t.\t.\tID={transcript.transcript_id};Parent={transcript.gene_id};Name={transcript.transcript_name}"
                    file.write(transcript.ligne_base + "\n")
                    
                    for exon in transcript.exons:
                        if exon.ligne_base is None:
                            exon.ligne_base = f"{exon.gene_id}\t.\texon\t{exon.start}\t{exon.end}\t.\t.\t.\tID={exon.exon_id};Parent={exon.transcript_id}"
                        file.write(exon.ligne_base + "\n")

    def get_genes_length(self):
        """
        permet de chercher la longueur des gènes calculée par la fonction get_length dans les deux classes Gene et Transcript.
        retourne la taille de chaque gène dans un dictionnaire avec le gène en clé et la taille correspondante en valeur.
        """
        gene_lengths = {}  
        for gene_id, gene in self.genes.items():
            gene_lengths[gene_id] = gene.get_length() 
        return gene_lengths

    

    def __repr__(self):
        """
        permet calculer le nombre de gènes dans l'annotation
        retourne le nombre de gènes dans l'annotation.
        """
        gene_count = len(self.genes)                            #grace à la longueur du dictionnaire de gènes
        return f"Annotation(gene_count={gene_count})"
    
        
    def rna_lens(self, fichier_output):
        """
        permet de construire un boxplot grâce au module matplotlib, à partir de la longueur des transcrits pour chaque gène.
        dans le script d'exécution, la fonction est utilisée pour retourner une figure dans le chemin d'output souhaité.
        """
        RNAlens = []                                                        #stocke la longueur des transcrits
        gene_names = []                                                   

        for gene_id, gene in self.genes.items():                            # boucle for pour faire le tour de chaque gène du fichier gff
            print(f"gène traité : {gene_id}")                               #retourne das le terminal le gène traité dans la boucle 
            transcript_lengths = [
            transcript.get_length() for transcript in gene.transcripts      # récupère pour chaque transcrit du gène, la longueur du transcrit
        ]  
            if transcript_lengths:  
                RNAlens.append(transcript_lengths)                          # permet d'ajouter les longueurs trouvées de chaque transcrit qui sont associés au gène
                gene_names.append(gene.gene_name)

        if not RNAlens: 
            print("pas de transcrit trouvé. il faut revérifier les données d'entrée !")
            return

    
        fig, ax = plt.subplots(figsize=(10, 6))                             # ici, taille de l'image.
        ax.boxplot(RNAlens, labels=gene_names, patch_artist=True)           # création du boxplot.
        ax.set_title("Distribution des longueurs des transcrits par gène")  # titre du plot
        ax.set_xlabel("Gènes (id)")                                              # nom pour l'axe des abscisses (x)
        ax.set_ylabel("Longueur des transcrits (bases)")                    # nom pour l'axe des ordonnées (y)
        ax.set_xticklabels(gene_names, rotation=90)                         # oriente les noms des gènes à 90°C (pour mieux les voir)
        
    
        fig.tight_layout() 
        fig.savefig(fichier_output)                                           # permet de sauvegarder la figure dans le chemin de sortie (définit dans le script d'exécution)
        print(f"votre boxplot est sauvegardé dans le fichier : {fichier_output}")


            



