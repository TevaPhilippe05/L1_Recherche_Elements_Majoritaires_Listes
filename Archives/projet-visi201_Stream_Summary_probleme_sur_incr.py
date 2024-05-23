"""
Au total, mon code fait environ 200 lignes.
J'ai utilisé des listes doublement chainées **circulaires**.


   - Les méthodes de la classe Cell ne sont pas très difficile. Essaie de
     les faire tout seul, on en discutera la prochaine fois.

   - La classe StreamSummary est un peu plus complexe. Essaie de
     comprendre comment je la définis et de réfléchir à comment
     implémenter la méthode __init__.
     Pour ne pas m'embêter dans la suite, je l'initialise avec des
     valeurs "factices" (j'ai pris les entiers négatifs -1, -2, ... , -k,
     mais tu peux mettre ce que tu veux) avec un compteur égal à 0.

"""

def space_saving(L, k):
     """returns the `k` elements saved by the space saving algorithm
     Note: this usually doesn't return the same elements as the
     `exact_majority` function, but it uses much less memory.
     This version uses the ad hoc data structure, implemented in pure Python.
     It is slower than the `exact_majority` function, but that shouldn't be the
     case in a compiled language."""
     S = StreamSummary(k)
     for e in L:
         S.update(e)
     return S.list()


class Cell:
     """non-empty doubly linked circular lists, identified by a single starting
     cell"""
     def __init__(self, v):
         """create a doubly linked circular list with a single value"""
         self.prev = self
         self.next = self
         self.value = v

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

     def add(self, c):
         """add a new cell, **after** self"""       
         c.next = self.next
         self.next.prev = c
         self.next = c
         self.next.prev = self
               
     def pop(self):
         """remove `self` from its list
         NOTE: if the list only contained `self`, the next and prev
         pointers for `self` are set to None"""
         if self.next != self:  # S'il n'y a qu'une seule cellule dans la liste
             self.prev.next = self.next
             self.next.prev = self.prev
         else:
             self.prev = None
             self.next = None
         

class Counter(Cell):
     def __init__(self, c, E=None):
         self.prev = self
         self.next = self
         self.value = c          # actual value of the counter (int)
         self.E = E              # reference to list of elements sharing this counter


class Element(Cell):
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
        self.lst_compteurs = Counter(0) # juste un compteur qu'on va parcourir
        self.elements = {0: Element(0, self.lst_compteurs)}
        self.lst_compteurs.E = self.elements[0]
        
        var = self.lst_compteurs.E
        for elem in range(k-1):     
            self.elements[elem+1] = Element(elem+1, self.lst_compteurs)
            var.add(self.elements[elem+1])
            var = var.next

    def show(self):
        print(self.elements)
        print()
        print(self.lst_compteurs.value,self.lst_compteurs.E.value, self.lst_compteurs.E.next.value, self.lst_compteurs.E.next.next.value, self.lst_compteurs.E.next.next.next.value)
        print()
        print(self.lst_compteurs.next.value, self.lst_compteurs.next.E.value, self.lst_compteurs.next.E.next.value, self.lst_compteurs.next.E.next.next.value, self.lst_compteurs.next.E.next.next.next.value)
        print()
        print(self.lst_compteurs.next.next.value, self.lst_compteurs.next.next.E.value, self.lst_compteurs.next.next.E.next.value, self.lst_compteurs.next.next.E.next.next.value, self.lst_compteurs.next.next.E.next.next.next.value)
        
         
         #... pour afficher le contenu du "stream summary", pratique pour déboguer ...
         #... une quinzaine de lignes de Python ...

    def list(self):
         liste = []
         for i, j in self.elements.items():
             liste.append([i,j.C.value])
         return liste
         # A LA FIN
         #... pour transformer le "stream summary" en liste d'élépments avec leurs compteurs ...
         #... une quinzaine de lignes de Python ...

    def update(self, k):
         """update the stream summary by increasing counter for `k`
         if `k` wasn't in the stream summary, we first replace a minimal symbol
         by `k`"""
         e = self.elements.get(k)
         if e is None:
             self.replace_min(k)
         self.incr(k)

    def replace_min(self, k):
        """replace the first symbol with minimal counter by `k`"""
        v = self.lst_compteurs.E.value
        self.lst_compteurs.E.value = k
        self.elements[k] = self.lst_compteurs.E
        del self.elements[v]
        
        

    def incr(self, k):
        """increase counter for symbol `k`"""
        E = self.elements[k]
        C = E.C
        
        if C.value + 1 == C.next.value:
            C.next.E.add(Element(k, C.next))
            E.C = C.next

        else:
            C.add(Counter(C.value + 1))
            C.next.E = Element(k, C.next)
            E.C = C.next

        E.pop()
        
        if E.next != None :
            C.E = E.next
        
        if C.E.next == None:
            C.pop()
                
            if self.lst_compteurs == C:
                self.lst_compteurs = C.next
                
        self.show()
