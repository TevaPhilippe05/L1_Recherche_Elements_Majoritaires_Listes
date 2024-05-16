from random import shuffle as mel, randint as ran
import timeit as tps
import numpy as np
import copy as c # Copier un itérateur
import types as ty
import matplotlib.pyplot as plt
import math
from StreamSummary import space_saving 
# from typing import Union # Indiquer plusieurs types

##### ----------------------------------------------------------------------------- #####

### Fonctions éléments fréquents ####

# Algo 1

def elem_maj_dict(lst:iter):
    """Algorithme qui renvoi l'élément majoritaire avec 100% de réussite. On utilise ici les dictionnaires pour le rendre plus efficace."""
    D = {}
    for k in lst:
        D[k] = D.get(k,0) + 1
            
    maxi = 0
    indice = 0
    
    for el in D:
        if D[el] > maxi:
            maxi = D[el]
            indice = el
            
    return indice


# Algo 2

def ss_lst(lst:iter, n):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des listes. Adapté aux itérateurs"""
    lst = iter(lst)
        
    compt = [[next(lst, None),1]]
    
    while len(compt)!= n:
        lm = next(lst, None)
        i=0
        while compt[i] == lm and i != len(compt):
            if compt[i] == lm:
                compt[i] += 1
            i += 1
                
        if compt[i-1] != lm:
            compt.append([lm, 1])
                    
    for e in lst:
        trouve = False
        for f in compt:
            if e == f[0]:
                f[1]+=1
                trouve = True
        
        if not trouve:
            mini = compt[0][1]
            minim = 0
            for g in range(1, len(compt)):
                if compt[g][1] < mini:
                    mini = compt[g][1]
                    minim = g


            compt[minim][0] = e
            compt[minim][1] += 1
    return compt, n


# Algo 3

def ss_dict(lst:iter, n):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des dictionnaires. Adapté aux itérateurs"""
    lst = iter(lst)
    compt = {}
    compteur = 0
    while len(compt) < n:
        lm = next(lst) ; compteur += 1
        compt[lm] = compt.get(lm, 0) + 1

    for lm in lst:
        compteur += 1
        if lm in compt:
            compt[lm] += 1
            
        else:
            for elem in compt:
                
                
                if compt[elem] < compteur:

                    compteur = compt[elem] + 1
                    minim = elem
            
            del compt[minim]
            compt[lm] = compteur
        
    return compt, n


### Fonctions créations listes / itérateurs ###

VALEUR_BIAISE = 3

def liste_arrange(n):
    lst = []
    while n != 0:
        lst.extend([n]*n)
        n -= 1
    mel(lst)
    return lst


def liste_random(n, biaise=False):
    lst = []
    if biaise:
        n = n//2
    for i in range(n):
        lst.append(ran(0,10000))
        if biaise:
            lst.append(VALEUR_BIAISE)
    return lst

def iterateur_zipf(n, biaise=False, seed=None, a=2):
    if biaise:
        n = n//2
    if seed is not None:
        g = np.random.default_rng(seed)
    else:
        g = np.random.default_rng()
        
    for i in range(n):
        yield g.zipf(a)
        if biaise:
            yield VALEUR_BIAISE
           

### Fonctions de tests de résultats ###

def test(instruction, nom:str, algo:str):
    var = instruction
    print(f"Test sur {nom} effectué en : {var: .5f} secondes avec {algo}")

def test_exe(el1:iter, el2:iter, el3:iter, nom:str, nb_var:int):
    """Test de résultats"""        
    print() ; print("Test sur", nom, ":","\n")
    el1 = iterateur_zipf(2001000, False, 2)
    e = elem_maj_dict(el1) ; print("Element majoritaire avec des dictionnaires nous renvoi :", e, "|\n")    
    el2 = iterateur_zipf(2001000, False, 2)
    e, em = ss_lst(el2, nb_var) ; print("Space_Saving avec des listes :", e, "| Soit les", em, "elements les plus fréquents\n")    
    el3 = iterateur_zipf(2001000, False, 2)
    e, em = ss_dict(el3, nb_var) ; print("Space Saving avec des dictionnaires  :", e, "| Soit les", em, "elements les plus fréquents\n") ; print()

### Fonctions de tests de temps d'execution ###

def test_tps(nom:str, n:int, nb_var:int, elem):
    """Test de temps d'execution pour les listes"""
        
    un = test(tps.timeit(stmt="elem_maj_dict(" + str(elem) + ")", setup="", number = n, globals = globals()), nom, "elem_maj_dict")
    deux = test(tps.timeit(stmt="ss_lst(" + str(elem) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_lst")
    trois = test(tps.timeit(stmt="ss_dict(" + str(elem) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_dict")
    return un, deux, trois
    
def test_tps_gene1(nom:str, n:int, nb_var:int):
    """Test de temps d'execution pour les listes"""
    elem1 = "iterateur_zipf(2001000, False, 2)"
    un = test(tps.timeit(stmt="elem_maj_dict(" + str(elem1) + ")", setup="", number = n, globals = globals()), nom, "elem_maj_dict")
    elem2 = "iterateur_zipf(2001000, False, 2)"
    deux = test(tps.timeit(stmt="ss_lst(" + str(elem2) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_lst")
    elem3 = "iterateur_zipf(2001000, False, 2)"
    trois = test(tps.timeit(stmt="ss_dict(" + str(elem3) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_dict")
    return un, deux, trois
    
def test_tps_gene2(nom:str, n:int, nb_var:int):
    """Test de temps d'execution pour les listes"""
    un = elem1 = "iterateur_zipf(2001000, True, 3)"
    test(tps.timeit(stmt="elem_maj_dict(" + str(elem1) + ")", setup="", number = n, globals = globals()), nom, "elem_maj_dict")
    deux = elem2 = "iterateur_zipf(2001000, True, 3)"
    test(tps.timeit(stmt="ss_lst(" + str(elem2) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_lst")
    trois = elem3 = "iterateur_zipf(2001000, True, 3)"
    test(tps.timeit(stmt="ss_dict(" + str(elem3) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_dict") 
    return un, deux, trois

##### ----------------------------------------------------------------------------- #####

### Tests de résultats ###

# # Test liste et Itérateurs / Générateurs
# test_exe(liste_random(2001000), liste_random(2001000), liste_random(2001000), "lst1", 5) ; test_exe(liste_random(2001000, True), liste_random(2001000, True), liste_random(2001000, True), "lst2", 5) ; test_exe(liste_arrange(2000), liste_arrange(2000), liste_arrange(2000), "lst3", 5)
# test_exe(iterateur_zipf(2001000, False, 2), iterateur_zipf(2001000, False, 2), iterateur_zipf(2001000, False, 2), "gene1", 5) ; test_exe(iterateur_zipf(2001000, True, 3), iterateur_zipf(2001000, True, 3), iterateur_zipf(2001000, True, 3), "gene2", 5)

# test_tps("lst1", 1, 10, liste_random(2001000)) ; test_tps("lst2", 1, 10, liste_random(2001000, True)); test_tps("lst3", 1, 10, liste_arrange(2000))
# test_tps_gene1("gene1", 1, 10) ; test_tps_gene2("gene2", 1, 10)

##### ----------------------------------------------------------------------------- #####

def test_(instruction, nom:str, algo:str):
    return(f"{instruction: .5f}")

def test_tps_(nom:str, n:int, nb_var:int, elem):
    """Test de temps d'execution pour les listes"""
    un = test_(tps.timeit(stmt="elem_maj_dict(" + str(elem) + ")", setup="", number = n, globals = globals()), nom, "elem_maj_dict")
    deux = test_(tps.timeit(stmt="ss_lst(" + str(elem) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_lst")
    trois = test_(tps.timeit(stmt="ss_dict(" + str(elem) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_dict")
    quatre = test_(tps.timeit(stmt="space_saving(" + str(elem) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "space_saving")
    return un, deux, trois, quatre
    
def test_tps_gene1_(nom:str, n:int, nb_var:int, nb_elem:str):
    """Test de temps d'execution pour les listes"""
    elem1 = "iterateur_zipf("+nb_elem+", False, 2)"
    un = test_(tps.timeit(stmt="elem_maj_dict(" + str(elem1) + ")", setup="", number = n, globals = globals()), nom, "elem_maj_dict")
    elem2 = "iterateur_zipf("+nb_elem+", False, 2)"
    deux = test_(tps.timeit(stmt="ss_lst(" + str(elem2) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_lst")
    elem3 = "iterateur_zipf("+nb_elem+", False, 2)"
    trois = test_(tps.timeit(stmt="ss_dict(" + str(elem3) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_dict")
    elem4 = "iterateur_zipf("+nb_elem+", False, 2)"
    quatre = test_(tps.timeit(stmt="space_saving(" + str(elem4) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "space_saving")
    return un, deux, trois, quatre
    
def test_tps_gene2_(nom:str, n:int, nb_var:int, nb_elem:str):
    """Test de temps d'execution pour les listes"""
    elem1 = "iterateur_zipf("+nb_elem+", True, 3)"
    un = test_(tps.timeit(stmt="elem_maj_dict(" + str(elem1) + ")", setup="", number = n, globals = globals()), nom, "elem_maj_dict")
    elem2 = "iterateur_zipf("+nb_elem+", True, 3)"
    deux = test_(tps.timeit(stmt="ss_lst(" + str(elem2) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_lst")
    elem3 = "iterateur_zipf("+nb_elem+", True, 3)"
    trois = test_(tps.timeit(stmt="ss_dict(" + str(elem3) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "ss_dict")
    elem4 = "iterateur_zipf("+nb_elem+", True, 3)"
    quatre = test_(tps.timeit(stmt="space_saving(" + str(elem4) + "," + str(nb_var) + ")", setup="", number = n, globals = globals()), nom, "space_saving") 
    return un, deux, trois, quatre

""" ============================================================================================ """
"""GRAPHE LISTE 1"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst1", 1, 10, liste_random(100))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst1", 1, 10, liste_random(1000))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst1", 1, 10, liste_random(10000))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst1", 1, 10, liste_random(50000))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst1", 1, 10, liste_random(100000))


# tailles_listes = ["100", "1000", "10000", "50000", "100000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille de la liste 1 avec les 10 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE LISTE 2"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst2", 1, 10, liste_random(100, True))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst2", 1, 10, liste_random(1000, True))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst2", 1, 10, liste_random(10000, True))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst2", 1, 10, liste_random(50000, True))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst2", 1, 10, liste_random(100000, True))


# tailles_listes = ["100", "1000", "10000", "50000", "100000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste


# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille de la liste 2 avec les 10 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE LISTE 3"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst3", 1, 10, liste_arrange(45))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst3", 1, 10, liste_arrange(141))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst3", 1, 10, liste_arrange(446))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst3", 1, 10, liste_arrange(1425))

# tailles_listes = ["1035", "10011", "101025", "1016025"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4]         # Exemple de temps pour ss_dict pour chaque taille de liste

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille de la liste 3 avec les 10 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE GENE 1"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_gene1_("gene1", 1, 10, "1000")
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst1 = test_tps_gene1_("gene1", 1, 10, "10000")
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst1 = test_tps_gene1_("gene1", 1, 10, "100000")
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_gene1_("gene1", 1, 10, "500000")
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_gene1_("gene1", 1, 10, "1000000")


# tailles_listes = ["1000", "10000", "100000", "500000", "1000000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille du generateur 1 avec les 10 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE GENE 2"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_gene2_("gene2", 1, 10, "1000")
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_gene2_("gene2", 1, 10, "10000")
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_gene2_("gene2", 1, 10, "100000")
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_gene2_("gene2", 1, 10, "500000")
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_gene2_("gene2", 1, 10, "1000000")


# tailles_listes = ["1000", "10000", "100000", "500000", "1000000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille du generateur 2 avec les 10 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

""" ============================================================================================ """
"""GRAPHE LISTE 1"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst1", 1000, 1, liste_random(100))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst1", 1000, 1, liste_random(1000))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst1", 1000, 1, liste_random(10000))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst1", 1000, 1, liste_random(20000))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst1", 1000, 1, liste_random(30000))


# tailles_listes = ["100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille de la liste 1 avec les 1000 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE LISTE 2"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst2", 1000, 1, liste_random(100, True))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst2", 1000, 1, liste_random(1000, True))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst2", 1000, 1, liste_random(10000, True))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst2", 1000, 1, liste_random(20000, True))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst2", 1000, 1, liste_random(30000, True))


# tailles_listes = ["100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille de la liste 2 avec les 1000 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE LISTE 3"""

maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst3", 1000, 1, liste_arrange(15)) # 15 : 120, 45: 1035, 141: 10011, 201: 20301, 245: 30135, 446: 101025, 635: 201930
maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst3", 1000, 1, liste_arrange(45))
maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst3", 1000, 1, liste_arrange(141))
maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst3", 1000, 1, liste_arrange(201))
maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst3", 1000, 1, liste_arrange(245))


tailles_listes = ["120", "1035", "10011", "20301", "30135"]
temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
temps_ss_lst_int = [float(x) for x in temps_ss_lst]
temps_ss_dict_int = [float(x) for x in temps_ss_dict]
temps_space_saving_int = [float(x) for x in temps_space_saving]

# Tracé du graphique

plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# Ajout de titres et d'étiquettes
plt.title('Temps d\'exécution en fonction de la taille de la liste 3 avec les 1000 plus grand éléments')
plt.xlabel('Taille de la liste')
plt.ylabel('Temps d\'exécution (secondes)')
plt.legend()

# Affichage du graphique
plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
plt.show()

"""GRAPHE GENE 1"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_gene1_("gene1", 1000, 1, "100")
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_gene1_("gene1", 1000, 1, "1000")
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_gene1_("gene1", 1000, 1, "10000")
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_gene1_("gene1", 1000, 1, "20000")
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_gene1_("gene1", 1000, 1, "30000")


# tailles_listes = ["100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille du generateur 1 avec les 1000 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE GENE 2"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_gene2_("gene2", 1000, 1, "100")
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_gene2_("gene2", 1000, 1, "1000")
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_gene2_("gene2", 1000, 1, "10000")
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_gene2_("gene2", 1000, 1, "20000")
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_gene2_("gene2", 1000, 1, "30000")


# tailles_listes = ["100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction de la taille du generateur 2 avec les 1000 plus grand éléments')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

""" ============================================================================================ """
# """GRAPHE LISTE 1"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst1", 10, 1, liste_random(100))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst1", 100, 1, liste_random(100))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst1", 1000, 1, liste_random(100))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst1", 10000, 1, liste_random(100))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst1", 20000, 1, liste_random(100))
# maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_("lst1", 30000, 1, liste_random(100))


# tailles_listes = ["10", "100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')


# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 100 elements (liste1)')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE LISTE 2"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst2", 10, 1, liste_random(100, True))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst2", 100, 1, liste_random(100, True))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst2", 1000, 1, liste_random(100, True))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst2", 10000, 1, liste_random(100, True))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst2", 20000, 1, liste_random(100, True))
# maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_("lst2", 30000, 1, liste_random(100, True))


# tailles_listes = ["10", "100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')


# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 100 elements (liste2)')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE LISTE 3"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst3", 10, 1, liste_arrange(15))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst3", 100, 1, liste_arrange(15))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst3", 1000, 1, liste_arrange(15))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst3", 10000, 1, liste_arrange(15))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst3", 20000, 1, liste_arrange(15))
# maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_("lst3", 30000, 1, liste_arrange(15))


# tailles_listes = ["10", "100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 120 elements (liste3)')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE GENE 1"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst6 = test_tps_gene1_("gene1", 10, 10, "100")
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst6 = test_tps_gene1_("gene1", 100, 10, "1000")
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst6 = test_tps_gene1_("gene1", 1000, 10, "100")
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst6 = test_tps_gene1_("gene1", 10000, 10, "100")
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst6 = test_tps_gene1_("gene1", 20000, 10, "100")
# maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_gene1_("gene1", 30000, 10, "100")


# tailles_listes = ["10", "100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 100 elements (gene1)')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE GENE 2"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_gene2_("gene2", 10, 10, "100")
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_gene2_("gene2", 100, 10, "100")
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_gene2_("gene2", 1000, 10, "100")
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_gene2_("gene2", 10000, 10, "100")
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_gene2_("gene2", 20000, 10, "100")
# maj_dict_g_ls65, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_gene2_("gene2", 30000, 10, "100")


# tailles_listes = ["10", "100", "1000", "10000", "20000", "30000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 100 elements (gene2)')
# plt.xlabel('Taille de la liste')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

""" ============================================================================================ """
"""GRAPHE LISTE 1"""

maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst1", 1, 10, liste_random(100000))
maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst1", 1, 100, liste_random(100000))
maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst1", 1, 1000, liste_random(100000))
maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst1", 1, 2000, liste_random(100000))
maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst1", 1, 3000, liste_random(100000))
maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_("lst1", 1, 4000, liste_random(100000))


tailles_listes = ["10", "100", "1000", "2000", "3000", "4000"]
temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
temps_ss_lst_int = [float(x) for x in temps_ss_lst]
temps_ss_dict_int = [float(x) for x in temps_ss_dict]
temps_space_saving_int = [float(x) for x in temps_space_saving]

# Tracé du graphique

plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# Ajout de titres et d'étiquettes
plt.title('Temps d\'exécution en fonction des n plus grands elements avec 100000 elements (liste1)')
plt.xlabel('Nombres de plus grands elements')
plt.ylabel('Temps d\'exécution (secondes)')
plt.legend()

# Affichage du graphique
plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
plt.show()

"""GRAPHE LISTE 2"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst2", 1, 10, liste_random(100000, True))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst2", 1, 100, liste_random(100000, True))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst2", 1, 1000, liste_random(100000, True))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst2", 1, 2000, liste_random(100000, True))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst2", 1, 3000, liste_random(100000, True))
# maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_("lst2", 1, 4000, liste_random(100000, True))


# tailles_listes = ["10", "100", "1000", "2000", "3000", "4000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 100000 elements (liste2)')
# plt.xlabel('Nombres de plus grands elements')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE LISTE 3"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_("lst3", 1, 10, liste_arrange(44))
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_("lst3", 1, 100, liste_arrange(446))
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_("lst3", 1, 200, liste_arrange(446))
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_("lst3", 1, 300, liste_arrange(446))
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_("lst3", 1, 400, liste_arrange(446))


# tailles_listes = ["10", "100", "200", "300", "400", "500"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 101025 elements (liste3)')
# plt.xlabel('Nombres de plus grands elements')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE GENE 1"""

# maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_gene1_("gene1", 10, 10, "10000")
# maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_gene1_("gene1", 100, 10, "10000")
# maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_gene1_("gene1", 1000, 10, "10000")
# maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_gene1_("gene1", 2000, 10, "10000")
# maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_gene1_("gene1", 3000, 10, "10000")
# maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_gene1_("gene1", 4000, 10, "10000")


# tailles_listes = ["10", "100", "1000", "2000", "3000", "4000"]
# temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
# temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
# temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
# temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

# temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
# temps_ss_lst_int = [float(x) for x in temps_ss_lst]
# temps_ss_dict_int = [float(x) for x in temps_ss_dict]
# temps_space_saving_int = [float(x) for x in temps_space_saving]

# # Tracé du graphique

# plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
# plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
# plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
# plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# # Ajout de titres et d'étiquettes
# plt.title('Temps d\'exécution en fonction des n plus grands elements avec 10000 elements (gene1)')
# plt.xlabel('Nombres de plus grands elements')
# plt.ylabel('Temps d\'exécution (secondes)')
# plt.legend()

# # Affichage du graphique
# plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
# plt.show()

"""GRAPHE GENE 2"""

maj_dict_g_lst1, ss_lst_g_lst1, ss_dict_g_lst1, space_saving_lst1 = test_tps_gene2_("gene2", 10, 10, "10000")
maj_dict_g_lst2, ss_lst_g_lst2, ss_dict_g_lst2, space_saving_lst2 = test_tps_gene2_("gene2", 100, 10, "10000")
maj_dict_g_lst3, ss_lst_g_lst3, ss_dict_g_lst3, space_saving_lst3 = test_tps_gene2_("gene2", 1000, 10, "10000")
maj_dict_g_lst4, ss_lst_g_lst4, ss_dict_g_lst4, space_saving_lst4 = test_tps_gene2_("gene2", 2000, 10, "10000")
maj_dict_g_lst5, ss_lst_g_lst5, ss_dict_g_lst5, space_saving_lst5 = test_tps_gene2_("gene2", 3000, 10, "10000")
maj_dict_g_lst6, ss_lst_g_lst6, ss_dict_g_lst6, space_saving_lst6 = test_tps_gene2_("gene2", 4000, 10, "10000")


tailles_listes = ["10", "100", "1000", "2000", "3000", "4000"]
temps_elem_maj_dict = [maj_dict_g_lst1, maj_dict_g_lst2, maj_dict_g_lst3, maj_dict_g_lst4, maj_dict_g_lst5, maj_dict_g_lst6]  # Exemple de temps pour elem_maj_dict pour chaque taille de liste
temps_ss_lst = [ss_lst_g_lst1, ss_lst_g_lst2, ss_lst_g_lst3, ss_lst_g_lst4, ss_lst_g_lst5, ss_lst_g_lst6]         # Exemple de temps pour ss_lst pour chaque taille de liste
temps_ss_dict = [ss_dict_g_lst1, ss_dict_g_lst2, ss_dict_g_lst3, ss_dict_g_lst4, ss_dict_g_lst5, ss_dict_g_lst6]         # Exemple de temps pour ss_dict pour chaque taille de liste
temps_space_saving = [space_saving_lst1, space_saving_lst2, space_saving_lst3, space_saving_lst4, space_saving_lst5, space_saving_lst6]

temps_elem_maj_dict_int = [float(x) for x in temps_elem_maj_dict]
temps_ss_lst_int = [float(x) for x in temps_ss_lst]
temps_ss_dict_int = [float(x) for x in temps_ss_dict]
temps_space_saving_int = [float(x) for x in temps_space_saving]

# Tracé du graphique

plt.plot(tailles_listes, temps_elem_maj_dict_int, marker='o', label='elem_maj_dict')
plt.plot(tailles_listes, temps_ss_lst_int, marker='s', label='ss_lst')
plt.plot(tailles_listes, temps_ss_dict_int, marker='^', label='ss_dict')
plt.plot(tailles_listes, temps_space_saving_int, marker='d', label='space_saving')

# Ajout de titres et d'étiquettes
plt.title('Temps d\'exécution en fonction des n plus grands elements avec 10000 elements (gene2)')
plt.xlabel('Nombres de plus grands elements')
plt.ylabel('Temps d\'exécution (secondes)')
plt.legend()

# Affichage du graphique
plt.grid(True)  # Ajout d'une grille pour une meilleure lisibilité
plt.show()
