import argparse
from .annotation import Annotation, Exon, Transcrit, Gene

"""
Ce script permet d'analyser les annotations biologiques à partir d'un fichier au format GFF depuis le terminal. 
Il offre deux fonctionnalités principales :
1. Générer et sauvegarder un boxplot des longueurs des transcrits (option `--output` ou `-o`).
2. Afficher des statistiques détaillées sur les gènes, transcrits et exons (option `--stats`).

Utilisation :
- Fournir en argument le chemin du fichier d'annotation GFF.
- Ajouter l'option `--stats` pour afficher les statistiques des annotations.
- Ajouter l'option `--output <chemin>` pour générer un boxplot et le sauvegarder dans le fichier spécifié.
- Ajouter l'option `--help` pour afficher un message d'aide .


Exemples de commandes bash :
1. Afficher les statistiques des annotations :
   > python3 script_annotation.py fichier.gff --stats

2. Générer un boxplot des longueurs des transcrits et le sauvegarder :
   > python3 script_annotation.py fichier.gff --output monplot.png
"""
def main():
    # Création du parser pour les arguments
    parser = argparse.ArgumentParser(description="Analyse des annotations biologiques.")
    
    # Argument pour le fichier d'annotation (obligatoire)
    parser.add_argument("file", type=str, help="Chemin du fichier d'annotation GFF.")
    
    # Argument pour afficher les statistiques des annotations
    parser.add_argument("--stats", action="store_true", help="Afficher les statistiques des annotations.")
    
    # Argument pour spécifier le fichier de sortie du boxplot
    parser.add_argument("--output", "-o", type=str, help="Le chemin du fichier où sauvegarder le boxplot (si 'rna_lens' est appelé).")
    
    # Analyse des arguments
    args = parser.parse_args()

    # Vérifier que le fichier d'entrée existe avant de continuer
    try:
        # Charger les annotations depuis le fichier
        annotation = Annotation(args.file)
        annotation._parse_gff(args.file)  # Méthode pour charger les données du fichier
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return

    # Si l'option --output ou -o est utilisée, appel de la méthode rna_lens
    if args.output:
        try:
            annotation.rna_lens(args.output)  # Appel de la méthode rna_lens avec le chemin du fichier de sortie 
            print(f"Boxplot sauvegardé sous : {args.output}")
        except Exception as e:
            print(f"Erreur lors de la création du boxplot : {e}")
    
    # Si l'option --stats est utilisée, appeler la méthode stats
    if args.stats:
        try:
            annotation.stats()  # Appeler la méthode stats pour afficher les statistiques
        except Exception as e:
            print(f"Erreur lors de l'affichage des statistiques : {e}")

if __name__ == "__main__":
    main()

