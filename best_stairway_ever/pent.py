from math import sqrt

def pent(k):
    '''
    Efficiently tests whether an integer 'k' is a pentagonal number
    Further determines the coefficient of the 'k'th element in
    the x^k form of Euler's Pentagonal Theorem:

    pent(k) == 0 while k is not pentagonal
    pent(k) == 1 while k is pentagonal and coeff to x^k is +1
    pent(k) == -1 while k is pentagonal and coeff to x^k is -1

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
        s[i] = pent(i)
    print(s)