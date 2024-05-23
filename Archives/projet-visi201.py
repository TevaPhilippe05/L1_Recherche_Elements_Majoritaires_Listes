import random
from random import shuffle as mel
import timeit as tps
import time as t

### Espace déclaration des listes de test ###

lst_test = ["a","a","a","a","a","a","b","c","d","c","e","a","c","d","f","g"]


lst_1 = []
for i in range(3000000):
    lst_1.append(random.randint(0,5))
    
    
time_s = t.perf_counter()
lst_2 = []
for i in range(3000000):
    lst_2.append(random.randint(0,10))
    lst_2.append(3)
time_e = t.perf_counter() ; exe_time = time_e - time_s
print("Test Temps lst3 :", f"Programme exécuté en : {exe_time: .5f} secondes") ; print()


time_s = t.perf_counter()
lst_3 = []
compteur = 6000
while compteur != 0:
    for i in range(compteur):
        lst_3.append(compteur)
    compteur -= 1
time_e = t.perf_counter() ; exe_time1 = time_e - time_s


time_s = t.perf_counter()
mel(lst_3)
time_e = t.perf_counter() ; exe_time2 = time_e - time_s
print("Test Temps lst4 :", f"Programme exécuté en : {exe_time1: .5f} secondes", "|", f"Mélange fait en : {exe_time2: .5f} secondes") ; print()


### -------------------------------------- ###

### Espace fonctions ###

# Algo 1

def space_saving(lst:list):
    """Algorithme space_saving"""
    elem_e = lst[0] ; elem_e_compteur = 0
    
    elem_em = "" ; elem_em_compteur = 0
   
    for e in lst:
        if e == elem_e:
            elem_e_compteur += 1
        
        elif e == elem_em:
            elem_em_compteur += 1
            
        else:
            if elem_e_compteur < elem_em_compteur:
                elem_e = e ; elem_e_compteur += 1
                
            else:
                elem_em = e ; elem_em_compteur += 1  
                
    return elem_e, elem_em

# Algo 2

def elem_maj1(lst:list):
    """Algorithme qui renvoi l'élément majoritaire avec 100% de réussite. Peu efficace"""
    if len(lst) == 0:
        return("La liste est vide")  
    
    max_nb_occurence = 0 #le nombre d'occurrence de l'élément le plus fréquent
    compteur_global = 0 # permet de savoir lorsque l'on a atteint le dernier element
        
    while compteur_global != len(lst):
        compteur = 0 # compte le nombre 
        for i in range (0, len(lst)):
            if lst[i] == lst[compteur_global]:
                compteur += 1
                
        if compteur > max_nb_occurence:
            res = lst[compteur_global] ; max_nb_occurence = compteur
            
        compteur_global += 1
            
    return res

# Algo 3

def elem_maj2(lst:list):
    """Algorithme qui renvoi l'élément majoritaire avec 100% de réussite. On utilise ici les dictionnaires pour le rendre plus efficace."""
    if len(lst) == 0:
        return("La liste est vide") 
    
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

# Algo 4

def space_saving_n_elements1(lst:list, n:int):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des listes."""
    
    compt = [[lst[0],0]]
    
    for i in range(1,n):
        compt.append(["",0])
    
    for e in lst:
        trouve = False
        for f in compt:
            if e == f[0]:
                f[1]+=1 
                trouve = True
        
        if not trouve:
            mini = compt[0][1]
            for g in range(len(compt)):
                if compt[g][1] < mini:
                    mini = compt[g][1]
                    minim = g
            
            compt[minim][0] = e
            compt[minim][1] += 1
            
    return compt, n

# Algo 5

def space_saving_n_elements2(lst:list, n:int):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des dictionnaires."""
    
    compt = {}
    i = 0
    while len(compt) < n:
        compt[lst[i]] = compt.get(lst[i], 0)
        i += 1
    
    for j in range(len(lst)):
        trouve = False
        for elem in compt:
            if elem == lst[j]:
                compt[elem] += 1
                trouve = True
        
        if not trouve:
            prem_elem = False
            for elem in compt:
                if not prem_elem:
                    mini = compt[elem] ; minim = elem
                    prem_elem = True
                if compt[elem] < mini:
                    mini = compt[elem] ; minim = elem
                    
            compt[lst[j]] = compt[minim] + 1
            del compt[minim]
            
    return compt, n

### -------------------------------------- ###

# ### Tests d'executions ###

# # Test 1.1

# e, em = space_saving(lst_1)
# print("Test 1.1 : - Space Saving :", "Element maj 1:", e, "|", "Element maj 2:", em) ; print()

# # Test 1.2

# # e = elem_maj1(lst_1)
# # print("Test 1.2 : - Element_maj1 :", "Element maj:", e) ; print()

# # Test 1.3

# e = elem_maj2(lst_1)
# print("Test 1.3 : - Element_maj2 :", "Element maj:", e) ; print()

# # Test 1.4

# e, n = space_saving_n_elements1(lst_1, 3)
# print("Test 1.4 : - Space Saving n elements_listes :", n, "Elements maj:", e) ; print()

# # Test 1.5

# e, n = space_saving_n_elements2(lst_1, 3)
# print("Test 1.5 : - Space Saving n elements_dico :", n, "Elements maj:", e) ; print()


# # Test 2.1

# e, em = space_saving(lst_2)
# print("Test 2.1 : - Space Saving :", "Element maj 1:", e, "|", "Element maj 2:", em) ; print()

# # # Test 2.2

# # e = elem_maj1(lst_2)
# # print("Test 2.2 : - Element_maj1 :", "Element maj:", e) ; print()

# # Test 2.3

# e = elem_maj2(lst_2)
# print("Test 2.3 : - Element_maj2 :", "Element maj:", e) ; print()

# # Test 2.4

# e, n = space_saving_n_elements1(lst_2, 3)
# print("Test 2.4 : - Space Saving n elements_listes :", n, "Elements maj:", e) ; print()

# # Test 2.5

# e, n = space_saving_n_elements2(lst_2, 3)
# print("Test 2.5 : - Space Saving n elements_dico :", n, "Elements maj:", e) ; print()

# # Test 3.1

# e, em = space_saving(lst_3)
# print("Test 3.1 : - Space Saving :", "Element maj 1:", e, "|", "Element maj 2:", em) ; print()

# # # Test 3.2

# # e = elem_maj1(lst_3)
# # print("Test 3.2 : - Element_maj1 :", "Element maj:", e) ; print()

# # Test 3.3

# e = elem_maj2(lst_3)
# print("Test 3.3 : - Element_maj2 :", "Element maj:", e) ; print()

# # Test 3.4

# e, n = space_saving_n_elements1(lst_3, 3)
# print("Test 3.4 : - Space Saving n elements_listes :", n, "Elements maj:", e) ; print()

# # Test 3.5

# e, n = space_saving_n_elements2(lst_3, 3)
# print("Test 3.5 : - Space Saving n elements_dico :", n, "Elements maj:", e) ; print()

### Tests de temps ###

def test(instruction, num):
    var = instruction
    print(f"{num} effectué en : {var: .5f} secondes")
    
# Test 1

test(tps.timeit(stmt="space_saving(lst_1)", setup="", number = 1, globals = globals()), "Test 1.1")
# test(tps.timeit(stmt="elem_maj1(lst_1)", setup="", number = 1, globals = globals()), "Test 1.2")
test(tps.timeit(stmt="elem_maj2(lst_1)", setup="", number = 1, globals = globals()), "Test 1.3")
test(tps.timeit(stmt="space_saving_n_elements1(lst_1, 3)", setup="", number = 1, globals = globals()), "Test 1.4")
test(tps.timeit(stmt="space_saving_n_elements2(lst_1, 3)", setup="", number = 1, globals = globals()), "Test 1.5") ; print()

# Test 2

test(tps.timeit(stmt="space_saving(lst_2)", setup="", number = 1, globals = globals()), "Test 2.1")
# test(tps.timeit(stmt="elem_maj1(lst_2)", setup="", number = 1, globals = globals()), "Test 2.2")
test(tps.timeit(stmt="elem_maj2(lst_2)", setup="", number = 1, globals = globals()), "Test 2.3")
test(tps.timeit(stmt="space_saving_n_elements1(lst_2, 3)", setup="", number = 1, globals = globals()), "Test 2.4")
test(tps.timeit(stmt="space_saving_n_elements2(lst_2, 3)", setup="", number = 1, globals = globals()), "Test 2.5") ; print()

# Test 3

test(tps.timeit(stmt="space_saving(lst_3)", setup="", number = 1, globals = globals()), "Test 3.1")
# test(tps.timeit(stmt="elem_maj1(lst_3)", setup="", number = 1, globals = globals()), "Test 3.2")
test(tps.timeit(stmt="elem_maj2(lst_3)", setup="", number = 1, globals = globals()), "Test 3.3")
test(tps.timeit(stmt="space_saving_n_elements1(lst_3, 3)", setup="", number = 1, globals = globals()), "Test 3.4")
test(tps.timeit(stmt="space_saving_n_elements2(lst_3, 3)", setup="", number = 1, globals = globals()), "Test 3.5") ; print()