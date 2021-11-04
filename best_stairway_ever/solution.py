#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt
from collections import defaultdict

CACHE = defaultdict(int) # len(CACHE) == n to solution <= 201

def solution(n):
    '''
    Solution to Greatest Staircase EVER! problem in Google foo.bar
    '''
    CACHE[0] = 1
    '''
    Subtracts 1 from the sum of distinct partitions p_d(n). Problem statement
    calls for identity case, i.e. "5 ⊂ p(5)" to be discarded from the answer:
    "stairs must have at least 2 steps"
    '''
    return partition(n) - 1

def partition(n):
    '''
    Applies Euler's Pentagonal Theorem: 
    sum of distinct partitions p_d(n) == sum of odd partitions p_0(n)
    p_d(n) = SUM(A_k + p(n-1**2) - p(n-2**2) - p(n-3**2) + p(n - 4**2) ...
        for all n-k**2 >= 0
    values of p(n-k**2) when n-k**2 < 0 are 0 and can be ignored

    The A_k term is +/- 1 when n is a pentagonal number, 0 for others

    Solution resolves to member of integer sequence OEIS A000009
    Time complexity is O(2**n) before cacheing, closer to O(n**2) with cache
    '''
    if CACHE[n] != 0:
        return CACHE[n]
    r = int(sqrt(n) + 1)
    s = 0
    
    for k in range(1, r):
        s += (-1) ** (k + 1) * partition(n - k**2)
    CACHE[n] = s * 2 + A_k(n)
    return CACHE[n]

def A_k(k):
    '''
    Efficiently tests whether an integer 'k' is a pentagonal number
    Further determines the coefficient of the 'k'th element in
    the A_k + SUM.. form of Euler's Pentagonal Theorem:

    A_k(k) == 0 while k is not pentagonal
    A_k(k) == 1 while k is pentagonal and A_k is +1
    A_k(k) == -1 while k is pentagonal and A_k is -1

    With 0 <= k to INF the sequence produced is OEIS A010815
    By inspection, time complexity is O(1) (not regarding built-ins)
    '''
    m = int(sqrt(24 * k + 1)) # inelegant, sufficient for small k
    if m**2 != 24 * k + 1: # non-pentagonal case
        return 0
    # coeff determined by parity of div 6
    elif m % 6 == 1:
        return (-1)**((m - 1) // 6) 
    else:
        return (-1)**((m + 1) // 6)

if __name__ == '__main__':
    s = [None for _ in range(20)]
    for i in range(20):
        s[i] = A_k(i)
    print(s)
