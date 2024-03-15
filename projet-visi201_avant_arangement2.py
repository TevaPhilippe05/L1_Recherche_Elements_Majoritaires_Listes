from random import shuffle as mel, randint as ran
import timeit as tps
import time as t
import numpy as np
import copy as c # Copier un itérateur
import types as ty
import matplotlib.pyplot as plt
# from typing import Union # Indiquer plusieurs types

##### ----------------------------------------------------------------------------- #####

### Fonctions éléments fréquents ####

# Algo 1

def elem_maj_lst(lst:list):
    """Algorithme qui renvoi l'élément majoritaire avec 100% de réussite. Peu efficace"""
    if len(lst) > 15000:
        lst = lst[0:15000]
       
    max_nb_occurence = 0 #le nombre d'occurrence de l'élément le plus fréquent
    compteur_global = 0 # permet de savoir lorsque l'on a atteint le dernier element
        
    while compteur_global != len(lst):
        compteur = 0
        for i in range (0, len(lst)):
            if lst[i] == lst[compteur_global]:
                compteur += 1
                
        if compteur > max_nb_occurence:
            res = lst[compteur_global] ; max_nb_occurence = compteur
            
        compteur_global += 1
    return res, len(lst)


# Algo 2

def elem_maj_dict(lst:list):
    """Algorithme qui renvoi l'élément majoritaire avec 100% de réussite. On utilise ici les dictionnaires pour le rendre plus efficace."""
    if len(lst) == 0:
        return("La liste est vide") 
    
    D = {}
    for k in lst:
        D[k] = D.get(k,0) + 1
        
    print(D)
        
    maxi = 0
    indice = 0
    
    for el in D:
        if D[el] > maxi:
            maxi = D[el]
            indice = el
            
    return indice


# Algo 3

def ss_lst(lst:iter, n:int=2):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des listes. Adapté aux itérateurs"""
    if type(lst) == list:
        lst = iter(lst)
        
    compt = [[next(lst, None),1]]
    
    while len(compt)!=2:
        for i in range(len(compt)):
            lm = next(lst, None)
            if compt[i] == lm:
                compt[i] +=1
            else:
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


# Algo 4

def ss_dict(lst:iter, n:int=2):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des dictionnaires. Adapté aux itérateurs"""
    if type(lst) == list:
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

def test_exe_lst(elem:list, nom:str):
    """Test de résultats sur une liste ou un générateur"""
    print() ; print("Test sur", nom, ":","\n")
    e, n = elem_maj_lst(elem) ; print("Element majoritaire avec des listes nous renvoi :", e, "|", "avec une taille pour la liste de", n, "\n")
    e = elem_maj_dict(elem) ; print("Element majoritaire avec des dictionnaires nous renvoi :", e, "|\n")
    e, em = ss_lst(elem) ; print("Space_Saving avec des listes :", e, "| Soit les", em, "elements les plus fréquents\n")
    e, em = ss_dict(elem) ; print("Space Saving avec des dictionnaires  :", e, "| Soit les", em, "elements les plus fréquents\n") ; print()

def test_exe_it_gen(elem, nom:str, elem_copie=None):
    """Test de résultats sur un itérateur ou un générateur"""
    if type(elem) != ty.GeneratorType:
        elem_copie = c.copy(elem)
    print() ; print("Test sur", nom, ":","\n")
    e, em = ss_lst(elem) ; print("Space_Saving avec des listes :", e, "| Soit les", em, "elements les plus fréquents\n") ; print()
    e, em = ss_dict(elem_copie) ; print("Space Saving avec des dictionnaires  :", e, "| Soit les", em, "elements les plus fréquents\n") ; print()     


### Fonctions de tests de temps d'execution ###

def test(instruction, nom:str, algo:str):
    var = instruction
    print(f"Test sur {nom} effectué en : {var: .5f} secondes avec {algo}")
    
def test_tps(nom:str, n:int, typ:str):
    """Test de temps d'execution pour les listes"""
    if typ == "list":
        test(tps.timeit(stmt="elem_maj_lst(" + nom + ")", setup="", number = n, globals = globals()), nom, "elem_maj_lst")
        test(tps.timeit(stmt="elem_maj_dict(" + nom + ")", setup="", number = n, globals = globals()), nom, "elem_maj_dict")
    test(tps.timeit(stmt="ss_lst(" + nom + ")", setup="", number = n, globals = globals()), nom, "ss_lst")
    nom_copie = nom
    if typ == "ite" or typ == "gene":
        nom_copie += "_c"
    test(tps.timeit(stmt="ss_dict(" + nom_copie + ")", setup="", number = n, globals = globals()), nom, "ss_dict")   

##### ----------------------------------------------------------------------------- #####

### Elements de tests de résultats ###

# Listes de test
lst1_res = liste_random(2001000) ; lst2_res = liste_random(2001000, True) ; lst3_res = liste_arrange(2000)

# Iterateur et Générateurs de test
ite1_res = iter(range(0,2001000, 2))
gene1_res = iterateur_zipf(2001000, False, 2) ; gene1_res_c = iterateur_zipf(2001000, False, 2)
gene2_res = iterateur_zipf(2001000, True, 3) ; gene2_res_c = iterateur_zipf(2001000, True, 3)

### Elements de tests de temps d'execution ###

# Listes de test
lst1_tps = liste_random(2001000) ; lst2_tps = liste_random(2001000, True) ; lst3_tps = liste_arrange(2000)

# Iterateur et Générateurs de test
ite1_tps = iter(range(0,2001000, 2)) ; ite1_tps_c = iter(range(0,2001000, 2))
gene1_tps = iterateur_zipf(2001000, False, 2) ; gene1_tps_c = iterateur_zipf(2001000, False, 2)
gene2_tps = iterateur_zipf(2001000, True, 3) ; gene2_tps_c = iterateur_zipf(2001000, True, 3)


# ##### ----------------------------------------------------------------------------- #####

# ### Tests de résultats ###

# # Test liste et Itérateurs / Générateurs
# test_exe_lst(lst1_res, "lst1_res") ; test_exe_lst(lst2_res, "lst2_res") ; test_exe_lst(lst3_res, "lst3_res")
# test_exe_it_gen(ite1_res, "ite1_res") ; test_exe_it_gen(gene1_res, "gene1_res", gene1_res_c) ; test_exe_it_gen(gene2_res, "gene2_res", gene2_res_c)

# ### Tests de temps d'execution ###

# Test liste et Itérateurs / Générateurs
# test_tps("lst1_tps", 1, "list") ; test_tps("lst2_tps", 1, "list") ; test_tps("lst3_tps", 1, "list")
# test_tps("ite1_tps", 1, "ite") ; test_tps("gene1_tps", 1, "gene") ; test_tps("gene2_tps", 1, "gene")

##### ----------------------------------------------------------------------------- #####
""" EN COURS """



def test_tps_list_graphe(nom:str, n:int, typ:str):
    """Test de temps d'execution pour les listes"""
    if typ == "list":
        maj_lst = tps.timeit(stmt="elem_maj_lst(" + nom + ")", setup="", number = n, globals = globals())
        maj_dict = tps.timeit(stmt="elem_maj_dict(" + nom + ")", setup="", number = n, globals = globals())
    ss_lst = tps.timeit(stmt="ss_lst(" + nom + ")", setup="", number = n, globals = globals())
    nom_copie = nom
    if typ == "ite" or typ == "gene":
        nom_copie += "_c"
    ss_dict = tps.timeit(stmt="ss_dict(" + nom_copie + ")", setup="", number = n, globals = globals())
    return maj_lst, maj_dict, ss_lst, ss_dict

maj_lst_g, maj_dict_g, ss_lst_g, ss_dict_g = test_tps_list_graphe("lst1_tps", 1, "list")
         
### Graphes ###

labels = ["elem_maj_lst","elem_maj_dict","ss_lst","ss_dict"]
sizes = [f"{maj_lst_g: .5f}", f"{maj_dict_g: .5f}", f"{ss_lst_g: .5f}", f"{ss_dict_g: .5f}"]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels)
plt.show()

data = np.array([maj_lst_g, maj_dict_g, ss_lst_g, ss_dict_g])

# Tracé du graphique à barres
plt.bar(labels, data)

# Affichage du graphique
plt.show()

""" A FAIRE """
# Graphe ( photo) + maj_dict avec ite + del maj_list
# Fonctions uniquement avec un for e in ...
# globals = globals()


""" REMARQUE"""

# isinstance(gene1, ty.GeneratorType) est mieux