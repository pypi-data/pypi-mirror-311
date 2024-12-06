import Xomics_Clara_Mariam.script_annot_visu_final as sf

def main():
   path_gff1 = "data/exemple_sample1.gff"          #ici, remplacez par le chemin de vos fichiers gff
   path_gff2 = "data/exemple_sample2.gff"
 

   annotation1 = sf.Annotation(path_gff1)
   annotation2 = sf.Annotation(path_gff2)

   print("\nAnnotation 1 :")
   print(annotation1)

   print("\nAnnotation 2 :")
   print(annotation2)

   annotations_merge = annotation1 + annotation2

   print("\nAnnotation fusionnée :")
   print(annotations_merge)

   output_path = "Exemple/Exemple_merge_annotation.gff"                  #là, vous pouvez remplacer le nom du fichier fusionné gff de sortie par le chemin que vous souhaitez.
   print(f"\n l'annotation est exportée dans le fichier {output_path}")
   annotations_merge.to_gff(output_path)

   print("génération du graphique des longueurs des transcrits...")
   annotations_merge.rna_lens("Exemple/Exemple_output_graph.png")        #ici, vous pouvez remplacer le nom du fichier de visualisation de sortie par le chemin que vous souhaitez.

if __name__ == "__main__":

   print(sf)
   main()

