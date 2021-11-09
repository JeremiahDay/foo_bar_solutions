'''
Growth Series Compared                                                           
    Fibonacci:  1   1   2   3   5   8   13   21
    Exp of 2:   1   2   4   8   16  32

         │                                                                     
         │ │ │   │     │         │               │        Fib              │   
         ├─▼─▼─▲─▼─────▼─────────▼─────▲─────────▼─────────────────────▲───▼──▶
         │ │   │       │               │                  Exp_2        │       
         │                                                                     
         0                                                                     

'''

def fib(n):
    '''
    Maximum membership growth is by comparison of funds 'n' to the
    sums of the ordered fibonacci series. A list 'f' holds the two
    most recent sequence numbers beginning with n = 3, f_s holds
    the sum of sequence, and the number of members is returned when
    f_s exceeds funds 'n'
    '''
    BIG_NUM = 1000 # arbitrarily large number to drive range generator

    if n < 3:
        return n
    f = [1, 1]
    f_s = 2
    for i in range(2, BIG_NUM):
        f_n = sum(f)
        f_s += f_n
        if f_s > n:
            return i
        f[i % 2] = f_n

def exp_2(n):
    '''
    Bitwise operators to quickly find exponents to 2. By inspection
    of the sequence we see that each new member is afforded at
    2^n - 1, where the new member is the 'n'th addition. This is
    equivalent to log-base-2 growth rate in membership over funds
    available.

    Bitwise method finds the position of the leading 1 bit in the
    integer representation by replacing all rightward '0's with '1's,
    then applying the bin.count() function to count total 1 bits
    '''
    n += 1
    n = n >> 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16

    return bin(n).count('1')

def solution(n):
    return fib(n) - exp_2(n)