from gffanalyzer_m1bioinfo import Annotation, Gene, Transcrit, Exon 

'''TEST DE LA CLASSE EXON ET TRANSCRIT


transcrit = Transcrit("transcrit1", "gene1", 100, 200, "+")
exon1 = Exon("exon1", "transcrit1", "gene1", 100, 150, "+")
exon2 = Exon("exon2", "transcrit1", "gene1", 160, 200, "+")
transcrit.add_exon(exon1)
transcrit.add_exon(exon2)

print(transcrit)
'''

'''
//TEST DE LA CLASSE TRANSCRITS ET GENE
gene = Gene("gene1", "gene_name1", 100, 1000, "+")
print(gene)  # Vérifie l'affichage

# Ajout de transcrits
transcrit1 = Transcrit("transcrit1", "gene1", 100, 500, "+")
transcrit2 = Transcrit("transcrit2", "gene1", 600, 1000, "+")
gene.add_transcrit(transcrit1)
gene.add_transcrit(transcrit2)
print(gene)  # Vérifie que les transcrits sont ajoutés
'''

'''
TEST DE LA FUSION DE GENES
# Création de deux gènes identiques pour tester la fusion
gene1 = Gene("gene1", "gene_name1", 100, 1000, "+")
gene2 = Gene("gene1", "gene_name1", 50, 1100, "+")
transcrit1 = Transcrit("transcrit1", "gene1", 100, 500, "+")
transcrit2 = Transcrit("transcrit2", "gene1", 600, 1000, "+")
gene1.add_transcrit(transcrit1)
gene2.add_transcrit(transcrit2)

# Fusion des gènes
merged_gene = gene1 + gene2
print(merged_gene)  # Vérifie que les transcrits et les positions sont correctement fusionnés
for tran in merged_gene.transcrits:
    print(tran)
'''
'''
annotation = Annotation("data/Human_sample1.gff")
print(annotation)  # Vérifie que les gènes sont correctement parsés

# Accès à un gène
try:
    gene = annotation.get_gene("GPR157")
    print(gene)
except ValueError as e:
    print(e)  # Vérifie le cas où un gène n'est pas trouvé
'''

# Charger l'annotation à partir du fichier GFF
annotation1 = Annotation("data/Human_sample1.gff")
annotation2 = Annotation("data/Human_sample2.gff")
annotation3 = Annotation("data/ADGRB2.gff")

gene_ids = list(iter(annotation1))

# Création des exons pour le premier gène
exon1_gene1 = Exon(
    exon_id="Exon1_Gene1",
    parent_transcript_id="Transcript1_Gene1",
    parent_gene_id="Gene2",
    start=100,
    end=200,
    strand="+",
    gff_line="..."
)

exon2_gene1 = Exon(
    exon_id="Exon2_Gene1",
    parent_transcript_id="Transcript1_Gene1",
    parent_gene_id="Gene2",
    start=250,
    end=350,
    strand="+",
    gff_line="..."
)

# Création des transcrits pour le premier gène
transcrit1_gene1 = Transcrit(
    transcript_id="Transcript1_Gene1",
    parent_gene_id="Gene2",
    start=100,
    end=350,
    strand="+",
    gff_line="..."
)
transcrit1_gene1.add_exon(exon1_gene1)
transcrit1_gene1.add_exon(exon2_gene1)

transcrit2_gene1 = Transcrit(
    transcript_id="Transcript2_Gene1",
    parent_gene_id="Gene2",
    start=150,
    end=300,
    strand="+",
    gff_line="..."
)
transcrit2_gene1.add_exon(exon1_gene1)

# Création du premier gène
gene1 = Gene(
    gene_id="Gene2",
    name="GeneName1",
    start=100,
    end=400,
    strand="+",
    gff_line="..."
)
gene1.transcrits.append(transcrit1_gene1)
gene1.transcrits.append(transcrit2_gene1)


# Création des exons pour le deuxième gène
exon1_gene2 = Exon(
    exon_id="Exon1_Gene2",
    parent_transcript_id="Transcript1_Gene2",
    parent_gene_id="Gene2",
    start=500,
    end=600,
    strand="-",
    gff_line="..."
)

exon2_gene2 = Exon(
    exon_id="Exon2_Gene2",
    parent_transcript_id="Transcript1_Gene2",
    parent_gene_id="Gene2",
    start=650,
    end=750,
    strand="-",
    gff_line="..."
)

# Création des transcrits pour le deuxième gène
transcrit1_gene2 = Transcrit(
    transcript_id="Transcript1_Gene2",
    parent_gene_id="Gene2",
    start=500,
    end=750,
    strand="-",
    gff_line="..."
)
transcrit1_gene2.add_exon(exon1_gene2)
transcrit1_gene2.add_exon(exon2_gene2)

# Création du deuxième gène
gene2 = Gene(
    gene_id="Gene2",
    name="GeneName2",
    start=500,
    end=800,
    strand="-",
    gff_line="..."
)
gene2.transcrits.append(transcrit1_gene2)
gene1.transcrits.append(transcrit1_gene2)

annotf = annotation1 + annotation2

print(annotf.get_gene("GPR157"))

