import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class Exon:
    # Initialisation des attributs de l'exon
    def __init__(self, exon_id :str, parent_transcript_id :str, parent_gene_id :str, start :int, end :int, strand :str, gff_line :str = ""):
        """
        Initialise un objet Exon en prenant en paramètres son ID, les IDs de son transcrit et gène parents, ses coordonnées génomiques (start, end), son brin (+ ou -), et, optionnellement, la ligne GFF associée. 
        Ces informations sont utilisées pour structurer les données d'annotation. 
        Le constructeur ne retourne rien mais crée une instance d'Exon avec les attributs spécifiés, prête à être intégrée dans une annotation génomique.
        """
        self.exon_id = exon_id
        self.parent_transcript_id = parent_transcript_id
        self.parent_gene_id = parent_gene_id
        self.start = start
        self.end = end
        self.strand = strand 
        self.gff_line = gff_line # Ligne au format GFF associée à l'exon

    def __repr__(self):
        """
        Retourne une représentation textuelle de l'objet Exon. Cette méthode affiche de manière concise et lisible 
        les informations clés : ID de l'exon, IDs de ses parents (transcrit et gène), ses coordonnées génomiques 
        (start, end) et son brin. Appelé lors de l'utilisation de `print()` sur un objet de la classe.
        """
        return f"Exon(id={self.exon_id}, parent_transcript={self.parent_transcript_id}, parent_gene={self.parent_gene_id}, start={self.start}, end={self.end}, strand={self.strand})"

class Transcrit:
    # Initialisation des attributs du transcrit (mRNA)
    def __init__(self, transcript_id :str, parent_gene_id :str, start :int, end :int, strand :str, gff_line :str = ""):
        """
        Initialise un objet Transcrit en prenant en paramètres son ID, l'ID de son gène parent, ses coordonnées génomiques (start, end), son brin (+ ou -), et, optionnellement, la ligne GFF associée. 
        Ces informations sont utilisées pour structurer les données d'annotation. 
        Le constructeur ne retourne rien mais crée une instance de Transcrit avec les attributs spécifiés, prête à être intégrée dans une annotation génomique.
        """
        self.transcript_id = transcript_id
        self.parent_gene_id = parent_gene_id
        self.start = start
        self.end = end
        self.strand = strand
        self.exons = [] # Liste des exons associés au transcrit
        self.gff_line = gff_line # Ligne au format GFF associée au transcrit
    
    def __eq__(self, other):
        """
        Compare deux objets Transcrit pour vérifier leur égalité. La méthode vérifie que l'objet comparé est une 
        instance de la classe Transcrit, puis compare les IDs du transcrit et du gène parent. Renvoie True si 
        les deux objets représentent le même transcrit, sinon False.
        Paramètre : un objet de la classe Transcrit.
        """
        if not isinstance(other, Transcrit):
            return NotImplemented
        return (
            self.transcript_id == other.transcript_id
            and self.parent_gene_id == other.parent_gene_id
        )

    def add_exon(self, exon :Exon):
        """
        Ajoute un exon à la liste des exons du transcrit. La méthode prend un objet Exon en paramètre et l'ajoute 
        à l'attribut `exons` du transcrit, qui est une liste. Cela permet d'enrichir le transcrit avec un nouvel exon.
        """
        self.exons.append(exon)

    def __repr__(self):
        """
        Retourne une représentation textuelle de l'objet Transcrit. Cette méthode affiche de manière concise et lisible 
        les informations clés : ID du transcrit, ID du gène parent, ses coordonnées génomiques 
        (start, end) et son brin. Appelé lors de l'utilisation de `print()` sur un objet de la classe.
        """
        return f"Transcrit(id={self.transcript_id}, parent_gene={self.parent_gene_id}, exons={len(self.exons)}, start={self.start}, end={self.end}, strand={self.strand}, Number of exons = {len(self.exons)} )"

class Gene:
    # Initialisation des attributs du gène
    def __init__(self, gene_id :str, name :str, start :int, end :int, strand :str, gff_line :str = ""):
        """
        Initialise un objet Gene en prenant en paramètres son ID, son nom, ses coordonnées génomiques (start, end), son brin (+ ou -), et, optionnellement, la ligne GFF associée. 
        Ces informations sont utilisées pour structurer les données d'annotation. 
        Le constructeur ne retourne rien mais crée une instance de Gene avec les attributs spécifiés, prête à être intégrée dans une annotation génomique.
        """
        self.gene_id = gene_id
        self.name = name
        self.start = start
        self.end = end
        self.strand = strand
        self.transcrits = [] # Liste des transcrits associés au gène
        self.gff_line = gff_line # Ligne au format GFF associée au gène


    def add_transcrit(self, transcrit :Transcrit):
        """
        Ajoute un transcrit à la liste des transcrits du gène. La méthode prend un objet Transcrit en paramètre et 
        l'ajoute à l'attribut `transcrits` du gène, permettant ainsi d'associer un transcrit supplémentaire au gène.
        Paramètre : un objet de la classe Transcrit.
        """
        self.transcrits.append(transcrit)

    def __add__(self, other):
        """
        Fusionne deux gènes en combinant leurs transcrits, en éliminant les doublons. La méthode vérifie d'abord que les objets
        sont de la même classe `Gene` et que leurs `gene_id` sont identiques. Si ce n'est pas le cas, une erreur est levée.
        Si les gènes sont compatibles, les transcrits des deux gènes sont fusionnés.
        Paramètre : un objet de la classe Transcrit.
        Retourne un objet de la classe Gene.
        """
        if not isinstance(other, Gene): # Vérification que les deux objets soit de la même nature 
            return NotImplemented
        if self.gene_id != other.gene_id:
            raise ValueError(
                f"Cannot merge genes with different GeneIDs: {self.gene_id} != {other.gene_id}"
            )

        # Fusionner les transcrits en éliminant les doublons
        transcrits_fusionnes = self.transcrits.copy()
        for transcrit in other.transcrits:
            if transcrit not in transcrits_fusionnes:
                transcrits_fusionnes.append(transcrit)

        # Créer un nouvel objet Gene fusionné
        new_gene = Gene(
            gene_id=self.gene_id,
            name=self.name,  # On conserve le nom de self (ou other si besoin)
            start=min(self.start, other.start),
            end=max(self.end, other.end),
            strand=self.strand,  # On suppose que le brin est identique
            gff_line=self.gff_line # On suppose que la ligne est identique 
        )
        new_gene.transcrits = transcrits_fusionnes
        return new_gene

    def __repr__(self):
        """
        Représentation textuelle d'un gène, affichant ses informations principales telles que l'ID, le nom, le nombre de transcrits,
        les coordonnées de début et de fin, ainsi que le brin. Appelé lors de l'utilisation de `print()` sur un objet de la classe.
        """
        return f"Gene(id={self.gene_id}, name={self.name}, transcrits={len(self.transcrits)}, start={self.start}, end={self.end}, strand={self.strand}, Number of transcripts = {len(self.transcrits)})"

  
class Annotation:
    # Classe pour gérer l'annotation depuis un fichier GFF  
    def __init__(self, gff_file :str):
        """
        Initialise l'annotation en parsant le fichier GFF. Crée des objets Gene, Transcrit et Exon à partir des lignes du fichier GFF.
        Les objets sont stockés dans un dictionnaire où les clés sont les GeneIDs et les valeurs sont les objets Gene correspondants.
        Paramètre : chemin du fichier GFF (str).        
        """
        self.genes = {}  # Dictionnaire avec GeneID comme clé et Gene comme valeur
        self._parse_gff(gff_file)

    def __iter__(self):
        """
        Permet d'itérer sur les gènes de l'annotation, en renvoyant chaque identifiant de gène (GeneID) un par un.
        Cette méthode rend l'objet itérable, permettant une boucle sur les gènes de l'annotation.
        """
        for elt in self.genes:
            yield elt

    def __getitem__(self, val :str):
        """
        Permet d'accéder à un gène par son GeneID en appelant la méthode `get_gene`.
        Cette méthode permet d'utiliser la syntaxe d'indexation pour récupérer un gène par son ID.
        Paramètere : une chaîne de caractères correspondant à un ID de gène.
        """
        return self.get_gene(val)


    def _parse_gff(self, gff_file :str):
        """
        Parse le fichier GFF, crée des objets Gene, Transcrit et Exon, et remplit le dictionnaire des gènes.
        La méthode ne retourne rien mais modifie l'attribut `genes` de la classe en ajoutant des objets Gene,
        Transcrit et Exon extraits du fichier GFF. Elle utilise la méthode `_parse_attributes' sur la 9ème colonne du fichier.
        Elle gère également les lignes malformées et ignore les commentaires ou les lignes vides.
        Paramètre : chemin du fichier GFF (str).
        """
        current_gene = None
        current_transcrit = None

        with open(gff_file, "r") as file:
            for line in file:
                if line.startswith("#") or not line.strip():
                    continue  # Ignorer les commentaires et lignes vides

                # Découpe les colonnes du fichier GFF
                columns = line.strip().split("\t")
                if len(columns) < 9:
                    print(f"Ligne non-conforme ignorée : {line.strip()}")
                    continue  # Passer à la ligne suivante si la ligne est malformée
                feature_type = columns[2]  # "gene", "mRNA", "exon"
                attributes = self._parse_attributes(columns[8])

                if feature_type == "gene":
                    # Création d'un nouvel objet Gene
                    gene_id = attributes.get("ID", "").replace("gene-", "")
                    gene_name = attributes.get("Name", "")
                    current_gene = Gene(
                        gene_id=gene_id,
                        name=gene_name,
                        start=int(columns[3]),
                        end=int(columns[4]),
                        strand=columns[6],
                        gff_line= line
                    )

                    self.genes[gene_id] = current_gene

                elif feature_type == "mRNA" and current_gene:
                    # Création d'un nouvel objet Transcrit
                    transcript_id = attributes.get("ID", "")
                    current_transcrit = Transcrit(
                        transcript_id, 
                        parent_gene_id=current_gene.gene_id, 
                        start = int(columns[3]), 
                        end = int(columns[4]), 
                        strand = columns[6],
                        gff_line= line)
                    current_gene.add_transcrit(current_transcrit)

                elif feature_type == "exon" and current_transcrit:
                    # Création d'un nouvel objet Exon
                    exon_id = attributes.get("ID", "")
                    exon = Exon(
                        exon_id=exon_id,
                        parent_transcript_id=current_transcrit.transcript_id,
                        parent_gene_id=current_gene.gene_id,
                        start=int(columns[3]),
                        end=int(columns[4]),
                        strand=columns[6],
                        gff_line= line)
                    current_transcrit.add_exon(exon)

    def __add__(self, other):
        """
        Fusionne deux objets Annotation. Si un gène est présent dans les deux annotations,
        fusionne les gènes en utilisant l'opérateur + défini pour les gènes. La méthode vérifie d'abord que les objets
        sont de la même classe `Annotation`.
        Paramètre : un objet de la classe Annotation.
        Retourne une nouvelle instance d'Annotation contenant la fusion des gènes des deux annotations.
        """
        if not isinstance(other, Annotation):
            return NotImplemented

        merged_annotation = Annotation.__new__(Annotation)  # Crée une instance vide
        merged_annotation.genes = self.genes.copy()  # Copie des gènes de l'annotation actuelle

        for gene_id, other_gene in other.genes.items():
            if gene_id in merged_annotation.genes:
                # Fusionne les gènes existants
                merged_annotation.genes[gene_id] = (
                    merged_annotation.genes[gene_id] + other_gene
                )
            else:
                # Ajoute les nouveaux gènes
                merged_annotation.genes[gene_id] = other_gene

        return merged_annotation

    def _parse_attributes(self, attributes_str :str):
        """
        Parse les attributs d'une colonne d'attributs du fichier GFF et retourne un dictionnaire.
        Chaque attribut est séparé par un point-virgule et contient une clé et une valeur.
        Utilisée dans la méthode `_parse_gff`.
        Paramètre : chaîne de caractères correspondant à une colonne du fichier GFF.
        Retourne un dictionnaire avec les paires clé-valeur extraites des attributs.
        """
        attributes = {}
        for attribute in attributes_str.split(";"):
            # Nettoyage des espaces
            key_value = attribute.strip().split(" ", 1)
            if len(key_value) == 2:
                key, value = key_value
                attributes[key] = value.strip()
        return attributes

    def get_gene(self, gene_id :str):
        """
        Retourne l'objet Gene correspondant au GeneID donné.
        Lève une exception si le GeneID n'existe pas dans l'annotation.
        Paramètre : Identifiant du gène à rechercher (str)
        Retourne : un objet Gene correspondant au GeneID
        Erreur : Si aucun gène ne correspond au GeneID
        """
        if gene_id in self: # Utilisation de la méthode __iter__, on parcours directement self au lieu de self.genes
            return self.genes[gene_id]
        raise ValueError(f"Aucun gène avec l'identifiant '{gene_id}' trouvé dans l'annotation.")

    def __repr__(self):
        # Représentation textuelle d'une annotation
        """
        Calcul du nombre de gènes, de transcrits et d'exons présents dans l'annotation.
        Retourne un résumé sous forme de chaîne de caractères avec
        le nombre de gènes, de transcrits et d'exons.
        """
        gene_count = len(self.genes)
        transcript_count = sum(len(gene.transcrits) for gene in self.genes.values())
        exon_count = sum(len(transcrit.exons) for gene in self.genes.values() for transcrit in gene.transcrits)
        
        return f"Annotation: {gene_count} gène(s), {transcript_count} transcrit(s), {exon_count} exon(s)"
    
    def to_gff(self, filepath :str):
        """
        Écrit le contenu de l'objet Annotation dans un fichier au format GFF.
        Le fichier généré contient les lignes GFF des gènes, transcrits et exons associés.
        Paramètre : Chemin du fichier dans lequel écrire les données GFF (str)
        Retourne : Aucun retour (écriture dans le fichier)
        """
        with open(filepath, 'w') as f:
            for gene_id, gene in self.genes.items():
                # Écriture de la ligne GFF du gène
                f.write(gene.gff_line + '\n')
            
                for transcript in gene.transcrits:
                    # Écriture des lignes GFF de transcrit pour chaque gène
                    f.write(transcript.gff_line + '\n')
                
                    for exon in transcript.exons:
                        # Écriture des lignes GFF des exons de chaque transcrit
                        f.write(exon.gff_line + '\n')
        
    def _calculate_transcript_lengths(self):
        """
        Calcule les longueurs des transcrits en somme des longueurs des exons pour chaque gène.
        Cette méthode est appelée dans `rna_lens`, fournit les valeurs pour la construction du graphique.
        Retourne : 
            - Une liste de longueurs de transcrits (chaque entrée étant une liste des longueurs des transcrits d'un gène)
            - Une liste des noms des gènes correspondants
        """
        RNAlens = []
        gene_names = []

        for gene_id, gene in self.genes.items():
            transcript_lengths = []
            for transcrit in gene.transcrits:
                # Calcul des longueurs des exons pour chaque transcrit
                exon_lengths = [exon.end - exon.start + 1 for exon in transcrit.exons]
                transcript_lengths.append(sum(exon_lengths))  # Longueur totale du transcrit

            if transcript_lengths:  # Ajouter uniquement si des transcrits existent
                RNAlens.append(transcript_lengths)
                gene_names.append(gene_id)

        return RNAlens, gene_names

    def rna_lens(self, output_filepath: str):
        """
        Calcule les longueurs des transcrits pour chaque gène à l'aide de `calculate_transcripts_lengths` et génère un boxplot.
        Sauvegarde le boxplot dans le fichier spécifié par `output_filepath`. La personnalisation du graphique est réalisée grâce 
        à la bibliothèque Matplotlib, permettant de modifier l'apparence du boxplot en ajustant la couleur des boîtes, des moustaches,
        des limites extrêmes et de la médiane, ainsi qu'en ajoutant une légende, une grille, des titres, et des étiquettes claires pour
        améliorer la lisibilité du graphique.
        En paramètre :
            - output_filepath (str) : Le chemin où sauvegarder le boxplot.
        Retourne :
            Aucun retour explicite, mais notification de réussite de la sauvegarde d'un fichier image du boxplot à l'emplacement spécifié.
        """
        # Récupérer les longueurs des transcrits et les noms des gènes en appelant la méthode
        RNAlens, gene_names = self._calculate_transcript_lengths()

        # Création du graphique de distribution des longueurs des transcrits
        fig = Figure(figsize=(20, 8))  # Taille de la figure
        ax = fig.add_subplot(1, 1, 1)

        # Génération du boxplot
        box = ax.boxplot(RNAlens, labels=gene_names, patch_artist=True)

        # Personnalisation du boxplot
        for patch in box['boxes']:
            patch.set_facecolor('#A9C9FF')  # Couleur de fond pour les boîtes
            patch.set_edgecolor('#1F77B4')  # Bordure bleue
            patch.set_linewidth(1.5)

        # Personnalisation de l'étendue des données 
        for whisker in box['whiskers']:
            whisker.set(color='orange', linewidth=1.5)

        # Personnalisation des limites extrêmes 
        for cap in box['caps']:
            cap.set(color='green', linewidth=2)

        # Personnalisation de la médiane
        for median in box['medians']:
            median.set(color='red', linewidth=2)

        # Ajout des titres et des labels
        ax.set_title("Distribution des longueurs des transcrits par gène", fontsize=14)
        ax.set_xlabel("Gènes", fontsize=14)
        ax.set_ylabel("Longueur des transcrits (en bp)", fontsize=14)

        # Écriture verticale des noms de gènes pour une meilleure lisibilité 
        ax.set_xticklabels(gene_names, rotation=90, fontsize=12)

        # Ajout d'une grille horizontale pour faciliter la lecture des données sur l'axe des ordonnées 
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Ajout d'un fond clair
        ax.set_facecolor('#f9f9f9')

        # Création de la légende
        handles = [
            plt.Line2D([0], [0], color='#A9C9FF', lw=4, label='Interquartile'),
            plt.Line2D([0], [0], color='orange', lw=4, label='Étendue des données'),
            plt.Line2D([0], [0], color='green', lw=4, label='Limites extrêmes'),
            plt.Line2D([0], [0], color='red', lw=4, label='Médiane')
        ]
        ax.legend(handles=handles, loc='upper right', fontsize=12, frameon=True)

        # Ajuster l'espacement du graphique
        fig.tight_layout()

        # Sauvegarder le graphique dans le fichier spécifié
        fig.savefig(output_filepath)

        # Afficher un message de réussite de la sauvegarde
        print(f"Le graphique a été sauvegardé sous : {output_filepath}")

    def stats(self):
        """
        Calcul et affiche des statistiques détaillées sur les gènes, transcrits et exons.
        Les statistiques incluent :
        - Nombre total de gènes
        - Nombre total de transcrits
        - Nombre total d'exons
        - Moyenne d'exons par transcrit
        - Moyenne de transcrits par gène
        - Proportion des gènes ayant plus d'un transcrit
        - Les trois gènes avec le plus de transcrits
        """
        # Calcul du nombre total de gènes, transcrits et exons dans l'annotation
        num_genes = len(self.genes)
        num_transcripts = sum(len(g.transcrits) for g in self.genes.values())
        num_exons = sum(sum(len(t.exons) for t in g.transcrits) for g in self.genes.values())

        # Calcul des moyennes de trancrits par gène et d'exons par transcrit
        avg_transcripts_per_gene = num_transcripts / num_genes if num_genes > 0 else 0
        avg_exons_per_transcript = num_exons / num_transcripts if num_transcripts > 0 else 0

        # Proportion de gènes avec plus d'un transcrit
        genes_with_multiple_transcripts = sum(1 for g in self.genes.values() if len(g.transcrits) > 1)
        prop_genes_with_multiple_transcripts = (
           genes_with_multiple_transcripts / num_genes * 100 if num_genes > 0 else 0
        )

        # Trouver les cinq gènes avec le plus de transcrits
        top_genes = sorted(
            self.genes.items(),
            key=lambda item: len(item[1].transcrits),
            reverse=True
        )[:5]

        # Préparer les données des 5 gènes pour affichage
        top_genes_info = [
            (gene_id, len(gene.transcrits)) for gene_id, gene in top_genes
        ]

        # Affichage des résultats
        print("=== Statistiques d'Annotation ===")
        print(f"Nombre total de gènes : {num_genes}")
        print(f"Nombre total de transcrits : {num_transcripts}")
        print(f"Nombre total d'exons : {num_exons}")
        print(f"Moyenne de transcrits par gène : {avg_transcripts_per_gene:.2f}")
        print(f"Moyenne d'exons par transcrit : {avg_exons_per_transcript:.2f}")
        print(f"Proportion de gènes avec plus d'un transcrit : {prop_genes_with_multiple_transcripts:.2f}%")
        print("Top 5 des gènes avec le plus de transcrits :")
        for i, (gene_id, num_transcripts) in enumerate(top_genes_info, start=1):
            print(f"  {i}. {gene_id} ({num_transcripts} transcrits)")
        print("==================================")

    





