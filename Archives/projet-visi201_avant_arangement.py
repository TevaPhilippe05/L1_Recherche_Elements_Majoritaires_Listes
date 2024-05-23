from random import shuffle as mel, randint as ran
import timeit as tps
import time as t
import numpy as np

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
            minim = 0
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
        
        if lst[j] in compt:
            compt[lst[j]] += 1
        
        else:  
            mini = len(lst)
            for elem in compt:
                
                if compt[elem] < mini:
                    mini = compt[elem]
                    minim = elem
                    
            compt[lst[j]] = mini + 1
            del compt[minim]
            
    return compt, n


# Algo 6

def space_saving_n_elements1_iterateurs(lst:iter, n:int):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des listes. Adapté aux itérateurs"""
    if type(lst) == list:
        lst = iter(lst)
        
    compt = [[next(lst, None),0]]
    
    for i in range(1,n):
        compt.append([next(lst, None),0])

    for e in lst:
        trouve = False
        for f in compt:
            if e == f[0]:
                f[1]+=1 
                trouve = True
        
        if not trouve:
            mini = compt[0][1]
            minim = 0
            for g in range(len(compt)):
                if compt[g][1] < mini:
                    mini = compt[g][1]
                    minim = g
            
            compt[minim][0] = e
            compt[minim][1] += 1
            
    return compt, n



# Algo 7 # voir mypy

def space_saving_n_elements2_iterateurs(lst:iter, n:int):
    """Algorithme space_saving qui renvoie les n éléments les plus fréquents
    Algorithme réalisé avec des dictionnaires. Adapté aux itérateurs"""

    compt = {}
    compteur = 0
    while len(compt) < n:
        lm = next(lst) ; compteur += 1
        compt[lm] = compt.get(lm, 0) + 1
    lm = next(lst) ; compteur += 1
    
    for lm in lst:
        if lm in compt:
            compt[lm] += 1
        
        else:
            for elem in compt:
                if compt[elem] < compteur:
                    compteur = compt[elem]
                    minim = elem
            compt[lm] = compteur
            del compt[minim]
            
        compteur += 1

    return compt, n





























































### Espace déclaration des listes de test ###

lst_test = ["a","a","a","a","a","a","b","c","d","c","e","a","c","d","f","g"]


time_s = t.perf_counter()
lst_1 = []
for i in range(30000):
    lst_1.append(ran(0,30000))
time_e = t.perf_counter() ; exe_time = time_e - time_s ; print("Test Temps lst1 :", f"Programme exécuté en : {exe_time: .5f} secondes") ; print()
   
 
time_s = t.perf_counter()
lst_2 = []
for i in range(30000):
    lst_2.append(ran(0,10000))
    lst_2.append(3)
time_e = t.perf_counter() ; exe_time = time_e - time_s ; print("Test Temps lst2 :", f"Programme exécuté en : {exe_time: .5f} secondes") ; print()


time_s = t.perf_counter()
lst_3 = []
compteur = 5000
while compteur != 0:
    lst_3.extend([compteur]*compteur)
    compteur -= 1
time_e = t.perf_counter() ; exe_time1 = time_e - time_s


time_s = t.perf_counter()
mel(lst_3)
time_e = t.perf_counter() ; exe_time2 = time_e - time_s ; print("Test Temps lst3 :", f"Programme exécuté en : {exe_time1: .5f} secondes", "|", f"Mélange fait en : {exe_time2: .5f} secondes") ; print()

time_s = t.perf_counter()
ite1 = iter(range(0,10000000, 2))
time_e = t.perf_counter() ; exe_time = time_e - time_s ; print("Test Temps ite1 :", f"Programme exécuté en : {exe_time: .5f} secondes") ; print()

time_s = t.perf_counter()
var = iter(np.random.zipf(a=2, size=(800)))
time_e = t.perf_counter() ; exe_time = time_e - time_s ; print("Test Temps ite1 :", f"Programme exécuté en : {exe_time: .5f} secondes") ; print()



# ite2 = iter(np.random.zipf(a=2, size=(80)))


def creer_iterateur(n, a=3):
    for i in range(n):
        yield np.random.default_rng().zipf(2)


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

# # Test 4.6

# e, n = space_saving_n_elements2_iterateurs(ite1, 3)
# print("Test 4.6 : - Space Saving n elements_iterateurs_dico :", n, "Elements maj:", e) ; print()

# Test 5.6

# e, n = space_saving_n_elements2_iterateurs(creer_iterateur(100000), 3)
# print("Test 6 .6 : - Space Saving n elements_iterateurs_dico :", n, "Elements maj:", e) ; print()



### Tests de temps ###

def test(instruction, num):
    var = instruction
    print(f"{num} effectué en : {var: .5f} secondes")
    
# ite1 = iter(range(0,100000, 2))
    
# Test 1

# test(tps.timeit(stmt="space_saving(lst_1)", setup="", number = 1, globals = globals()), "Test 1.1")
# # test(tps.timeit(stmt="elem_maj1(lst_1)", setup="", number = 1, globals = globals()), "Test 1.2")
# test(tps.timeit(stmt="elem_maj2(lst_1)", setup="", number = 1, globals = globals()), "Test 1.3")
# test(tps.timeit(stmt="space_saving_n_elements1(lst_1, 30)", setup="", number = 1, globals = globals()), "Test 1.4")
# test(tps.timeit(stmt="space_saving_n_elements2(lst_1, 30)", setup="", number = 1, globals = globals()), "Test 1.5") ; print()

# Test 2

# test(tps.timeit(stmt="space_saving(lst_2)", setup="", number = 1, globals = globals()), "Test 2.1")
# # test(tps.timeit(stmt="elem_maj1(lst_2)", setup="", number = 1, globals = globals()), "Test 2.2")
# test(tps.timeit(stmt="elem_maj2(lst_2)", setup="", number = 1, globals = globals()), "Test 2.3")
# test(tps.timeit(stmt="space_saving_n_elements1(lst_2, 300)", setup="", number = 1, globals = globals()), "Test 2.4")
# test(tps.timeit(stmt="space_saving_n_elements2(lst_2, 300)", setup="", number = 1, globals = globals()), "Test 2.5") ; print()

# Test 3

# test(tps.timeit(stmt="space_saving(lst_3)", setup="", number = 1, globals = globals()), "Test 3.1")
# # test(tps.timeit(stmt="elem_maj1(lst_3)", setup="", number = 1, globals = globals()), "Test 3.2")
# test(tps.timeit(stmt="elem_maj2(lst_3)", setup="", number = 1, globals = globals()), "Test 3.3")
# test(tps.timeit(stmt="space_saving_n_elements1(lst_3, 300)", setup="", number = 1, globals = globals()), "Test 3.4")
# test(tps.timeit(stmt="space_saving_n_elements2(lst_3, 300)", setup="", number = 1, globals = globals()), "Test 3.5") ; print()

# test 4

# test(tps.timeit(stmt="space_saving_n_elements2_iterateurs(ite1, 3)", setup="", number = 1, globals = globals()), "Test 4.6") ; print()
