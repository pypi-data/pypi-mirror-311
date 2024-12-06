import os 

class Uniprot:
    """
    Classe Uniprot qui permet de lire un fichier Uniprot et d'en extraire les informations.
    Les différentes méthodes permettent d'afficher les informations, de créer un fichier fasta,
    de calculer le poids moléculaire et l'hydrophobicité moyenne de la séquence peptidique.
    """
    def __init__(self, file_content:str):
        """
        Crée une instance de la classe Uniprot à partir de 
        file_content qui est  une chaine de caractères contenant
        toutes les information d'un fichier uniprot
        """
        # Variables pour la lecture du fichier.
        nb_AC = 0
        seq = False

        # Informations de l'entrée Uniprot.
        self.id = None
        self.first_accession_number = None
        self.organism = None
        self.first_gene_name = None
        self.sequence_pept = ""
        self.GO_id = []

        f = file_content.split("\n")
        for line in f:
            if line.startswith("ID "):
                self.id = line.split("  ")[1].strip()
                continue

            if line.startswith("DR") and line.split("  ")[1].strip().startswith("GO"):
                GO_id = line.split("  ")[1].strip().split(";")[1].split(":")[1].strip()
                self.GO_id.append(GO_id)
                continue
            

            if line.startswith("AC") and nb_AC == 0:
                nb_AC = 1
                self.first_accession_number = line.split("  ")[1].split(";")[0].strip()
                continue

            if line.startswith("OS"):
                self.organism = line.split("  ",)[1].strip()
                continue

            if line.startswith("GN") and line.split("  ")[1].strip().startswith("Name"):
                self.first_gene_name = line.split("  ")[1].strip().split(" ")[0].split("=")[1]
                continue

            if line.startswith("//"):
                seq = False

            if seq:
                self.sequence_pept += line.replace(" ", "").strip()

            if line.startswith("SQ") or seq:
                if seq:
                    continue
                seq = True 


    def __repr__(self):
        """
        Méthode qui affiche les informations de d'une objet Uniprot 
        """
        return f"""ID: {self.id}
        First Accession Number: {self.first_accession_number}
        Organism: {self.organism}
        First Gene Name:{self.first_gene_name}
        Sequence Pept: {self.sequence_pept}
        GO IDs: {', '.join(self.GO_id)}


"""


    def fasta_dump(self):
        """
        Crée un fichier fasta contenant une ligne de commentaire contenant
         l'identifiant, l'organisme et le nom du gène de l'objet Uniprot en entrée.
         Le fichier est nommé avec le nom du premier accession number et l'extension .fasta
        """
        file_name = f"fasta_outputs/{self.first_accession_number}.fasta"

        if not os.path.exists("fasta_outputs"):
            os.makedirs("fasta_outputs")

        with open(file_name, "w") as f:
            f.write(f">{self.id}\t{self.organism}\t{self.first_gene_name}\n")
            f.write(f"{self.sequence_pept}\n")
        print("le fichier ",f"{self.first_accession_number}.fasta","a bien été créé.")


    def molecular_weight(self)->float:
        """
        Retourne le poids moléculaire de l'objet Uniprot en entrée.
        """
        amino_acids = get_amino_acids()
        weight = 0.0

        for aa in self.sequence_pept:
            weight += amino_acids[aa].mol_weight
        
        return weight


    def average_hydrophobicity(self, ph=7.0)->float:
        """
        Retourne l'hydrophobicité moyenne de la séquence peptidique.
        Si default_hydrophobicity est True, on prend la première valeur de l'hydrophobicité,
        sinon on prend la deuxième valeur. (Pour l'hystidine)
        """
        amino_acids = get_amino_acids()
        hydrophobicity = 0.0
        default_hydrophobicity = True

        if ph > 6.0:
            default_hydrophobicity = False

        for aa in self.sequence_pept:
            current_hydrophobicity = amino_acids[aa].hydrophobicity
            
            if current_hydrophobicity == "n/a":
                continue

            if "or" in str(current_hydrophobicity):
                if default_hydrophobicity:
                    current_hydrophobicity = float(current_hydrophobicity.split(" or ")[0])
                else:
                    current_hydrophobicity = float(current_hydrophobicity.split(" or ")[1])
             
            hydrophobicity += current_hydrophobicity
        
        return hydrophobicity / len(self.sequence_pept)


class AminoAcid:
    """
    Class AminoAcid qui permet de créer une instance d'un acide aminé.
    """
    def __init__(self, name, code3, code1, mol_weight, aa_class, hydrophobicity):
        self.name = name
        self.code3 = code3
        self.code1 = code1
        self.mol_weight = mol_weight
        self.aa_class = aa_class
        self.hydrophobicity = hydrophobicity
    
    def __str__(self):
        return (f"Name: {self.name}\n"
                f"3-letter code: {self.code3}\n"
                f"1-letter code: {self.code1}\n"
                f"Molecular weight: {self.mol_weight} Da\n"
                f"Class: {self.aa_class}\n"
                f"Hydrophobicity scale: {self.hydrophobicity}")


def get_amino_acids()->dict:
    """
    Retourne un dictionnaire contenant les acides aminés.
    """
    return {
        "A": AminoAcid("Alanine", "Ala", "A", 89, "Aliphatic", 0.33),
        "R": AminoAcid("Arginine", "Arg", "R", 174, "Charged (+)", 1.00),
        "N": AminoAcid("Asparagine", "Asn", "N", 132, "Polar", 0.43),
        "D": AminoAcid("Aspartic acid", "Asp", "D", 133, "Charged (-)", 2.41),
        "C": AminoAcid("Cysteine", "Cys", "C", 121, "Polar or Aliphatic", 0.22),
        "Q": AminoAcid("Glutamine", "Gln", "Q", 146, "Polar", 0.19),
        "E": AminoAcid("Glutamic acid", "Glu", "E", 147, "Charged (-)", 1.61),
        "G": AminoAcid("Glycine", "Gly", "G", 75, "Polar", 1.14),
        "H": AminoAcid("Histidine", "His", "H", 155, "Polar or Charged (+)", "0.06 or 1.37"),
        "I": AminoAcid("Isoleucine", "Ile", "I", 131, "Aliphatic", -0.81),
        "L": AminoAcid("Leucine", "Leu", "L", 131, "Aliphatic", -0.69),
        "K": AminoAcid("Lysine", "Lys", "K", 146, "Charged (+)", 1.81),
        "M": AminoAcid("Methionine", "Met", "M", 149, "Aliphatic", -0.44),
        "F": AminoAcid("Phenylalanine", "Phe", "F", 165, "Aliphatic", -0.58),
        "P": AminoAcid("Proline", "Pro", "P", 115, "Aliphatic", -0.31),
        "S": AminoAcid("Serine", "Ser", "S", 105, "Polar", 0.33),
        "T": AminoAcid("Threonine", "Thr", "T", 119, "Polar", 0.11),
        "W": AminoAcid("Tryptophan", "Trp", "W", 204, "Aliphatic", -0.24),
        "Y": AminoAcid("Tyrosine", "Tyr", "Y", 181, "Polar", 0.23),
        "V": AminoAcid("Valine", "Val", "V", 117, "Aliphatic", -0.53)
    }

def amino_acids_empty_count(retour = "")->dict:
    """
    Retourne un dictionnaire avec tous les acides aminés et un compte de 0 associé.
    """
    amino_acids = get_amino_acids()
    if retour == "int":
        return {aa: 0 for aa in amino_acids.keys()}
    elif retour == "float":
        return {aa: 0.0 for aa in amino_acids.keys()}
    else:
        raise ValueError("le paramètre retourné doit-être un 'int' ou un 'float'")



def uniprot_from_file(file_path:str)->Uniprot:
    """
    Retourne une instance de la classe Uniprot à partir d'un fichier Uniprot.
    file_path: str, chemin du fichier Uniprot.
    """
    with open(file_path, "r") as f:
        file_content = f.read()
    
    return Uniprot(file_content)


