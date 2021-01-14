'''
Permutations
Version 0.1.0

A permutation is represented by a list, e.g. (1,3,2) is represented by [*,1,3,2].
The element at index 0 is not used resp. can be used as a "scratch field".

The permutation (3,1,2) and (3,1,2,4,5) are considered equal. More generally:
A permutation is considered as a function f:N-->N with the following 2 properties:
  (1) injective
  (2) only a finite number of elements of N are changed by f
  
Thus, the above 2 permutations both represent the function f with
  f(1)=3,f(2)=1,f(3)=2 and f(n)=n for all n>3
  
The identity is represented by (1)
'''

import copy 
import functools

@functools.total_ordering #generates from == and < the other comparison operators
#lexikographic ordering is used
class Permutation:
    
    @staticmethod
    def checkList(plist):
        '''
        Check with assertions that p is a list representing a permutation
        '''
        assert isinstance(plist,list)
        n = len(plist)
        assert n >= 2 #scratch and at least 1 element
        occupied = [False for k in range(n)]
        for k in range(1,n):
            assert isinstance(plist[k],int)
            assert 1 <= plist[k] <= n-1
            assert not occupied[plist[k]]
            occupied[plist[k]] = True
        
    
    def __init__(self, plist):
        '''
        plist must be a list of integers, representing a permutation
        Note that plist[0] is not part of the permutation and may have any value.
        '''
        self.checkList(plist)
        self.p = copy.deepcopy(plist)
        self._normalize()
        
    def __repr__(self):
        return repr(self.p[1:])
        
    def __str__(self):
        s=f"({self.p[1]}"
        for k in range(2,len(self.p)):
            s+=f",{self.p[k]}"
        s+=")"
        return s
    
    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return self.p[1:] == other.p[1:]
        else:
            return NotImplemented
        
    def __lt__(self,other):
        if isinstance(other,self.__class__):
            return self.p[1:] < other.p[1:]
        else:
            return NotImplemented
    

    def _normalize(self):
        '''
        reduce the length of the list as much as possible,
        e.g. (3,1,2,4,5) is reduced to (3,1,2)
        '''
        n = len(self.p)-1
        while n>1 and self.p[n]==n:
            n-=1
        if n < len(self.p)-1:
            self.p=self.p[:n+1]
            
    def __call__(self,n):
        '''
        Returns the value of the permutation at place n.
        n : int, >0
        Note: if n is > "length" of the permutation, then returns n.
        '''
        assert isinstance(n, int)
        assert n > 0
        if n < len(self.p):
            return self.p[n]
        else:
            return n
            
            
    def lengthen(self,n):
        '''
        Returns a possibly longer list that represents the same permutation.
        Example: if p is the permutation (2,3,1) then
            p.lengthen(6) returns the list [*,2,3,1,4,5]
            p.lengthen(n) returns the list [*,2,3,1] for n <= 4
        '''
        if n > len(self.p):
            pnew = self.p + [k for k in range(len(self.p),n)]
            return pnew
        else:
            return copy.deepcopy(self.p)
    
    def mul(self,other):
        '''
        Returns the "multiplication" of 2 permutations in the sense of composition of functions.
        The expression p.mul(q) means: first apply q then p
        '''
        assert isinstance(other,self.__class__)
        n = max(len(self.p),len(other.p))
        p = self.lengthen(n)
        q = other.lengthen(n)
        assert len(p) == len(q)
        r = [0] + [p[q[k]] for k in range(1,n)]
        return Permutation(r)
        
    def inv(self):
        '''
        Returns the inverse permutation
        '''
        n = len(self.p)
        p = [0 for k in range(n)]
        for k in range(1,n):
            p[self.p[k]] = k
        return Permutation(p)
        
    @classmethod
    def ONE(cls):
        return cls([0,1])
    
        
