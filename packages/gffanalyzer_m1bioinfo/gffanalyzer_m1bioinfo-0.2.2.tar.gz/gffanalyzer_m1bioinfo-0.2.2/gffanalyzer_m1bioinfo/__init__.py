from .annotation import Annotation, Gene, Transcrit, Exon

def plot_and_stats(gff_file : str, stats : bool = False, plot_out :str = None):
    '''
    Retourne statistiques et un boxplot à partir d'un fichier GFF, 
    '''
    try:
        # Charger les annotations depuis le fichier
        annotation = Annotation(gff_file)
        annotation._parse_gff(gff_file)  # Méthode pour charger les données du fichier
    except Exception as e:
        raise IOError(f"Erreur lors du chargement du fichier : {e}")
    if stats:
        annotation.stats()
    elif plot_out:
        try:
            annotation.rna_lens(plot_out)  # Appel de la méthode rna_lens avec le chemin du fichier de sortie 
            print(f"Boxplot sauvegardé sous : {plot_out}")
        except Exception as e:
            print(f"Erreur lors de la création du boxplot : {e}")
    else: 
        raise ValueError("Aucun argument appelé, ni stats, ni output")

def test_install():
    print("Le package gffanalyzer est bien installé !")
    
