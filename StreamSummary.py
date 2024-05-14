def space_saving(L, k):
     """returns the `k` elements saved by the space saving algorithm
     Note: this usually doesn't return the same elements as the
     `exact_majority` function, but it uses much less memory.
     This version uses the ad hoc data structure, implemented in pure Python.
     It is slower than the `exact_majority` function, but that shouldn't be the
     case in a compiled language."""
     S = StreamSummary(k) # On initialise un objet S de Stream Summary
     for e in L:     # Nous allons prendre un à un les éléments de L 
         S.update(e) # Et les ajouté avec une méthode de Stream Summary
     return S.list() # On renvoie la listes des éléments majoritaires avec la méthode 


class Cell:
     """non-empty doubly linked circular lists, identified by a single starting
     cell"""
     def __init__(self, v): # On définit une cellule comme ayant
         """create a doubly linked circular list with a single value"""
         self.prev = self   # Un pointeur vers l'élément précédent (qui au début est lui-même)
         self.next = self   # Un pointeur vers l'élément suivant (qui au début est lui-même)
         self.value = v     # Une valeur v

     def __str__(self): 
         s = ""
         c = self
         while True:
             s = s + str(c.value)
             c = c.next
             if c == self:
                 break

     def check(self):
         """check sanity of a doubly linked list"""
         elem = str(self.value)

         if str((self.prev).next) == elem and str((self.next).prev) == elem:
             return True
         return False

     def add(self, c): # rédéfinit les pointeurs qui partent vers l'éléments et ceux qui pointent vers celui-ci
         """add a new cell, **after** self"""       
         c.next = self.next
         self.next.prev = c
         self.next = c
         self.next.prev = self
               
     def pop(self): # redéfinit les pointeurs qui pointaient vers l'élément
         """remove `self` from its list
         NOTE: if the list only contained `self`, the next and prev
         pointers for `self` are set to None"""
         if self.next != self:  # S'il n'y a qu'une seule cellule dans la liste
             self.prev.next = self.next
             self.next.prev = self.prev
         else: # si on supprime un élément et qu'il ne pointaient vers aucune autre éléments, on définit ses pointeurs comme nulles
             print("ha")
             self.prev = None
             self.next = None
         

class Counter(Cell): # Un compteur est une cellule qui pointe vers une "liste" d'éléments (Attention, il ne s'agit pas de la structure de donnée "liste" mais d'un chaine d'éléments liés entre eux par des pointeurs)
     def __init__(self, c, E=None):
         self.prev = self
         self.next = self
         self.value = c          # actual value of the counter (int)
         self.E = E              # reference to list of elements sharing this counter


class Element(Cell): # Un élément est une cellule qui pointe vers un compteur
     def __init__(self, e, C):
         self.prev = self
         self.next = self
         self.value = e          # actual value of the element
         self.C = C              # reference to counter for this element


class StreamSummary:
    """
     A StreamSummary S contains the following data:

       - a (doubly linked) list of Counter: S.counters
         Each counter contains a positive integer (the actual counter), and a
         reference to the list of elements sharing that counter.
         This list is sorted, and S.counters references the smallest counter.

       - several (doubly linked) lists of Element
         Each such list contains elements consisting of an actual value and a
         reference to the corresponding counter.
         Those lists are only indirectly accessible, from the counters, or the
         dictionary of elements.
         All those lists contains exactly k elements in total.

       - a dictionary of containing k Element: S.elements
         The keys are the elements themselves, and the values are references to
         the corresponding Element
    """
    def __init__(self, k): 
        """
            On initialise la liste des compteurs, le dictionnaires d'éléments et 
            une première liste E qui contient des elements inéxistants mais qui 
            pointent vers le compteur 0
        """
        self.lst_compteurs = Counter(0)
        self.elements = {0: Element(0, self.lst_compteurs)}
        self.lst_compteurs.E = self.elements[0]
        
        var = self.lst_compteurs.E
        for elem in range(k-1):     
            self.elements[elem+1] = Element(elem+1, self.lst_compteurs)
            var.add(self.elements[elem+1])
            var = var.next

    def show(self):
        """ 
            Fonction utilisé pour le débugage pour visualiser les connexion et
            trouver les problèmes plus facilement. Il est difficile de les voirs 
            avec une telle structure de donnée.
        """
        
        print(self.elements)
        print()
        print(self.lst_compteurs.value,self.lst_compteurs.E.value, self.lst_compteurs.E.next.value, self.lst_compteurs.E.next.next.value, self.lst_compteurs.E.next.next.next.value)
        print()
        print(self.lst_compteurs.next.value, self.lst_compteurs.next.E.value, self.lst_compteurs.next.E.next.value, self.lst_compteurs.next.E.next.next.value, self.lst_compteurs.next.E.next.next.next.value)
        print()
        print(self.lst_compteurs.next.next.value, self.lst_compteurs.next.next.E.value, self.lst_compteurs.next.next.E.next.value, self.lst_compteurs.next.next.E.next.next.value, self.lst_compteurs.next.next.E.next.next.next.value)


    def list(self):
         """ Renvoi la liste des éléments majoritaires à partir du dictionnaire """
         liste = []
         for i, j in self.elements.items():
             liste.append([i,j.C.value])
         return liste

    def update(self, k):
         """Ici, si l'élément k n'existe pas, on remplace un element de la liste
         par celui ci en conservant le compteur, conformément au code space saving.
         On incrément ensuie son compteur"""
         e = self.elements.get(k)
         if e is None:
             self.replace_min(k)
         self.incr(k)

    def replace_min(self, k):
        """replace the first symbol with minimal counter by `k`"""
        v = self.lst_compteurs.E.value # On séléctionne le premier élément du plus petit compteur
        self.lst_compteurs.E.value = k # On remplace la valeur du premier élément du plus petit compteur
        self.elements[k] = self.lst_compteurs.E # On ajoute ensuite le nouvel element dans le dictionnaire
        del self.elements[v] # On supprime le premier élément

    def incr(self, k):
        """increase counter for symbol `k`"""
        E = self.elements[k] # On prend l'élément k
        C = E.C # On prend aussi le compteur de l'élément k
        
        E.pop() # On supprimer l'élément de sa liste
        
        if C.E == E: # Dans le cas où le premier élément du compteur était l'élément supprimé
            C.E = E.next # On définit la valeur suivante comme valeur du pointeur
                  
        if C.value + 1 == C.next.value: # On distingue deux cas. Dans le cas où le compteur suivant à la valeur du compteur actuel + 1
            C.next.E.add(E) # On ajoute l'élément dans la liste d'éléments du compteur suivant
            E.C = C.next # On définit le pointeur de cet élément sur le compteur suivant
        else:
            nC = Counter(C.value+1, E)
            C.add(nC) # On ajoute un nouveau compteur qui à la valeur +1 dans la liste des compteurs, et on définit sa liste d'éléments avec notre Element
            E.C = nC # On redéfinit ici aussi le pointeur de notre élément sur ce compteur
            
            #Puisque l'élément est dans seul dans une liste et qu'il à conservé ses pointeurs, on les rédinit sur lui même
            E.prev = E 
            E.next = E
        
        if C.E is None: # Si jamais, après avoir enlevé l'élément de sa liste initiale, celle ci est vide
             C.pop() # On supprime le compteur de sa liste
             if self.lst_compteurs == C: # Si le compteur était le premier de la listes des compteurs
                self.lst_compteurs = C.next # On définit le premier élément de la liste des compteurs comme le compteur suivant
            
        self.show()
            
        
        
            
        
        
            
        
                    
            
            
        
        
