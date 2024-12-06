from . import uniprot
import math
from matplotlib import figure
import os 


def collection_from_file(file_path):
    """
    Crée une instance de la classe Collection à partir d'un fichier contenant des entrées Uniprot.
    file_path: chemin vers le fichier d'entrée
    """
    # Lire le contenu du fichier
    with open(file_path, "r") as file:
        file_content = file.read()
    
    # Diviser le contenu en entrées Uniprot basées sur le séparateur "//\n"
    splitted_entries = file_content.split("//\n")
    
    # Créer des objets Uniprot à partir de chaque entrée
    uniprot_objects = [uniprot.Uniprot(entry) for entry in splitted_entries if entry.strip()]
    
    # Retourner une instance de Collection contenant tous les objets Uniprot
    return Collection(uniprot_objects)

def create_plot(x, y, uniprot_id):
    """
    Crée un en fonction des données x et y.
    x: Liste des valeurs de l'axe des abscisses.
    y: Liste des valeurs de l'axe des ordonnées.
    uniprot_id: str, identifiant de l'objet Uniprot.
    """
    fig = figure.Figure()
    ax = fig.subplots(1,1)
    ax.bar(x, y)
    if not os.path.exists("figures"):
        os.makedirs("figures")
    fig.savefig(f"figures/{uniprot_id}.png")


class Collection:
    """
    Cette classe a pour but d'organiser et d'opérer sur plusieurs objets Uniprot.
    """

    def __init__(self, list_Uniprot):
        """
        Crée une instance de la classe Collection a partir de list_Uniprot.
        list_Uniprot : Liste contenant des objets Uniprot
        """
        self.uniprot_objects = []

        for uniprot in list_Uniprot:
            self.uniprot_objects.append(uniprot)


    def __repr__(self):
        """
        Affiche les informations de chaque objet Uniprot.
        """
        return f"Collection({self.uniprot_objects})"
    
    def __iter__(self):
        """
        Makes the collection iterable.
        """
        for element in self.uniprot_objects:
            yield element
    

    def __add__(self, collection2):
        """
        Combine deux collections en une seule.
        collection2: Collection a combiner avec la collection self.
        """
        # Crée une nouvelle liste pour stocker les objets uniques
        combined_objects = self.uniprot_objects[:]
        
        for uniprot in collection2.uniprot_objects:
            # Vérifie si l'objet Uniprot n'est pas déjà dans combined_objects
            if not any(existing_uniprot.id == uniprot.id for existing_uniprot in combined_objects):
                combined_objects.append(uniprot)
        return Collection(combined_objects)

    def __getitem__(self, search_id):
        """
        Retourne l'objet Uniprot correspondant à l'identifiant donné.
        id: str, identifiant de l'objet Uniprot.
        """
        for uniprot in self.uniprot_objects:
            if uniprot.id == search_id:
                return uniprot
        raise Exception("Aucun objet Uniprot ne correspond à cet identifiant dans la collection.")

    def add(self, contenu_uniprot:str):
        """
        Ajoute un objet Uniprot à la collection.
        contenu_uniprot: str, contenu du fichier Uniprot.
        """
        new_uniprot = uniprot.Uniprot(contenu_uniprot)
        id_list = [uniprot.id for uniprot in self.uniprot_objects]
        if new_uniprot.id in id_list:
            raise Exception("Un objet Uniprot identique est déjà dans la collection.")
        self.uniprot_objects.append(new_uniprot)


    def del_(self, uniprot_id:str): # NB : del ne peut pas être utilisé comme nom de méthode
        """
        Supprime un objet Uniprot de la collection.
        uniprot_id: str, identifiant de l'objet Uniprot.
        """
        for uniprot in self.uniprot_objects:
            if uniprot.id == None:
                continue
            if uniprot_id in uniprot.id:
                self.uniprot_objects.remove(uniprot)
                return
        raise Exception("Aucun objet Uniprot ne correspond à cet identifiant.")


    def sort_by_length(self):
        """
        Trie dans l'ordre croissant les objets Uniprot par la longueur de leur séquence peptidique
        """
        self.uniprot_objects.sort(key=lambda uniprot: len(uniprot.sequence_pept))
        return self.uniprot_objects
    

    def filter_for_hydrophobic(self, min_hydro:int):
        """
        Filtre les objets Uniprot par hydrophobicité.
        min_hydro: int, valeur minimale d'hydrophobicité.
        """
        #Comment améliorer et pourquoi les list sont limité?
        #Limite l'accés contrairement au dico? qui nous mermettrait de tout avoir pas que l'hydrophobicité
        filtered_objects = list(filter(lambda uniprot: uniprot.average_hydrophobicity() > min_hydro, self.uniprot_objects))
        
        # Retourner les objets filtré 
        return filtered_objects
    

    def go_view(self):
        '''
        Méthode qui retourne le dictionnaire des nombres 
        d'occurrences des mots-clés GO portés par toutes 
        les membres de la  Collection (self).
        '''
        dico_GO={}
        for uniprot in self.uniprot_objects:
            for GO_id in  uniprot.GO_id:
                if GO_id in dico_GO.keys():
                    dico_GO[GO_id] += 1
                else:
                    dico_GO[GO_id] = 1
        
        return dico_GO

    def draw_ABRL(self, uniprot_id: str):
        """
        Dessine un graphique ABRL pour une protéine spécifique identifiée par son ID.
        """
        dico_nb_AA_prot = uniprot.amino_acids_empty_count(retour="int")
        dico_nb_AA_coll = uniprot.amino_acids_empty_count(retour="int")
        dico_log_AA = uniprot.amino_acids_empty_count(retour="int")
        nb_prot = 0

        for uniprot_obj in self.uniprot_objects:
            nb_prot += 1
            if uniprot_obj.id == uniprot_id:
                for AA in uniprot_obj.sequence_pept:
                    dico_nb_AA_prot[AA] += 1
                    dico_nb_AA_coll[AA] += 1
            else:
                for AA in uniprot_obj.sequence_pept:
                    dico_nb_AA_coll[AA] += 1

        for AA in dico_nb_AA_prot:
            if dico_nb_AA_coll[AA] != 0 and dico_nb_AA_prot[AA] != 0:
                dico_log_AA[AA] = (math.log(
                    (dico_nb_AA_prot[AA]/sum(dico_nb_AA_prot.values()))
                    /
                    (dico_nb_AA_coll[AA]/sum(dico_nb_AA_coll.values()))
                    ))
                # Calcul : log((nb_AA_prot / nb_total_prot) / (nb_AA_coll / nb_total_coll))
            else:
                print(f"Division par 0 évitée ou ln(0) évité")
                dico_log_AA[AA] = 0
        create_plot(dico_log_AA.keys(), dico_log_AA.values(), uniprot_id)
        print(f"Graphique sauvegardé sous le nom {uniprot_id}.png.")

    def filter(self, predicate_fn:callable)->list:
        """
        Retourne la liste des objets Uniprot pour lesquels predicate_fn retourne True.
        """
        return list(filter(predicate_fn, self.uniprot_objects))
    
def filtre_longueur(entry:uniprot, n=500)->bool:
    """
    Retourne True si la longueur de la séquence peptidique est supérieure à n.
    ATTENTION : nécessité d'utiliser functools.partial pour passer n en argument, sinon n=500 par défaut.
    """
    return len(entry.sequence_pept) > n
