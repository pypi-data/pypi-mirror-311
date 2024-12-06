import .script_annot_visu_final

annotation = script_annot_visu_final.Annotation("Exemple_merge_Human_annotation.gff")

gene_id = input("entrez ici l'ID du gène recherché : ")  # permet de demander à l'utilisateur d'entrer un ID de gène

try:
    gene = annotation.get_gene(gene_id)                  # ici, appelle la fonction pour obtenir le gène
    print("informations sur le gène :")
    print(gene)  
except ValueError as e:
    print(f"aucun gène n'a été trouvé avec l'ID que vous venez d'entrer, revérifiez votre id.")
