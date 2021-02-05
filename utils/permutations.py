"""Module defining permutations.

Version 0.2.0
Derived from module permutation0.py, v0.1.0. That module uses a "dummy index 0".
In this module, index 0 is not dummy.

A permutation is represented by a list, e.g. (0,2,1) is represented by [0,2,1].
Note: other than in most mathematical texts, the number 0 is also used.
That is, permutations operate on the integers 0,1,2,... and not 1,2,3...

Here, we use 'N0' to denote the set of non negative integers 0,1,2,...

The permutations (2,0,1) and (2,0,1,3,4) are considered equal. More generally:
A permutation is considered as a function f:N0-->N0 with the following 2 properties:
  (1) one-to-one
  (2) only a finite number of elements of N0 are changed by f
  
Thus, the above 2 permutations both represent the function f with
  f(0)=2,f(1)=0,f(2)=1 and f(n)=n for all n>2
  
The identity is represented by (0) -- maybe () would be more consistent and more practical.

The lexicographic order ist defined for permutations, e.g. (1,3,2) < (2,1,3).
Therefore, a list containing permutations can be sorted.
"""

from __future__ import annotations  # for type annotations with forward references
from typing import List, Tuple  # for type annotations

import copy 
import functools


PList = List[int]
# List of integers representing a permutation.


@functools.total_ordering  # generates from == and < the other comparison operators
class Permutation:
    """Models a permutation and its operations

    Attributes:
        p: PList
            A list of integers representing a permutation.
            Note that this list must satisfy special conditions, see check_list.

    Example:
        Permutation([1, 2, 0]) creates the permutation (1,2,0)
    """
    
    @staticmethod
    def check_list(plist: PList) -> None:
        """ Check with assertions that plist is a list representing a permutation."""
        assert isinstance(plist, list)
        n = len(plist)
        assert n >= 1  # at least 1 element, also for identity (0)
        occupied = [False for _ in range(n)]
        for k in range(n):
            assert isinstance(plist[k], int)
            assert 0 <= plist[k] <= n-1
            assert not occupied[plist[k]]
            occupied[plist[k]] = True
    
    def __init__(self, plist: PList):
        self.check_list(plist)
        self.p = copy.deepcopy(plist)
        self._normalize()
        
    def __repr__(self):
        return repr(self.p)
        
    def __str__(self):
        s = f"({self.p[0]}"
        for k in range(1, len(self.p)):
            s += f", {self.p[k]}"
        s += ")"
        return s
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.p == other.p
        else:
            return NotImplemented
        
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.p < other.p
        else:
            return NotImplemented

    def _normalize(self) -> None:
        """Reduce the length of the list as much as possible, e.g. (2,0,1,3,4) to (2,0,1)."""
        n = len(self.p)-1
        while (n > 0) and (self.p[n] == n):
            n -= 1
        if n < len(self. p)-1:
            self.p = self.p[:n+1]
            
    def __call__(self, n: int) -> int:
        """Return the value of the permutation at index n.
        Note: if n is >= "length" of the permutation, then returns n.
        """
        assert isinstance(n, int)
        assert n >= 0
        if n < len(self.p):
            return self.p[n]
        else:
            return n

    def length(self) -> int:
        """Return the length of the internal list representing the permutation.
        The identity permutation Permutation.one() has length 1.
        """
        return len(self.p)

    def lengthen(self, n) -> PList:
        """Return a possibly longer list that represents the same permutation.
        Example: if p is the permutation (1,2,0) then
            p.lengthen(6) returns the list [1,2,0,3,4]
            p.lengthen(n) returns the list [1,2,0] for n <= 3
        """
        if n > len(self.p):
            p_new = self.p + [k for k in range(len(self.p), n)]
            return p_new
        else:
            return copy.deepcopy(self.p)
    
    def mul(self, other) -> Permutation:
        """Return the "multiplication" of 2 permutations in the sense of composition of functions.
        The expression p.mul(q) means: first apply q then p  (-- note the reversed order!)
        """
        assert isinstance(other, self.__class__)
        n = max(len(self.p), len(other.p))
        p = self.lengthen(n)
        q = other.lengthen(n)
        assert len(p) == len(q)
        r = [p[q[k]] for k in range(0, n)]
        return Permutation(r)
        
    def inv(self) -> Permutation:
        """Return the inverse permutation."""
        n = len(self.p)
        p = [0 for _ in range(n)]
        for k in range(n):
            p[self.p[k]] = k
        return Permutation(p)

    def apply(self, a_list: list) -> list:
        """Apply the permutation to a_list and return the new list.
        The length of the permutation must be <= len(a_list).
        Example: Permutation([2, 0, 1]).apply([1, 'a', 5.0, 8, "xxx"]) returns ['a', 5.0, 1, 8, "xxx"]
        """
        n = len(a_list)
        assert self.length() <= n
        p = self.inv()  # !!!
        new_list = [a_list[p(k)] for k in range(n)]
        return new_list

    @classmethod
    def sorted(cls, a_list, key=None, reverse=False) -> Tuple[list, Permutation]:
        """Return a sorted copy of a_list and the permutation that when applied to a_list returns this copy.
        The parameters are as for the builtin function sorted, except that a_list must be a list,
        other iterables are not (yet) allowed.
        Example: Permutation.sorted([3,5,4,2]) returns [2,3,4,5],(1,3,2,0)
                 Permutation.sorted([3,5,4,2], reverse=True) returns [5,4,3,2],(2,0,1,3)
        """
        # sort the list, single out empty case
        assert isinstance(a_list, list)
        n = len(a_list)
        if n == 0:
            return [], cls.one()
        new_list = sorted(a_list, key=key, reverse=reverse)
        # generate the permutation
        p_list = []
        occupied = [False for _ in new_list]
        for item in a_list:
            indices = [k for k in range(n) if item == new_list[k] and not occupied[k]]
            assert len(indices) > 0
            index = indices[0]
            occupied[index] = True
            p_list.append(index)
        p = Permutation(p_list)
        # check
        assert len(p_list) == n
        for k in range(n):
            assert a_list[k] == new_list[p(k)]
        assert p.apply(a_list) == new_list
        assert a_list == p.inv().apply(new_list)
        # result
        return new_list, p
        
    @classmethod
    def one(cls) -> Permutation:
        return cls([0])
