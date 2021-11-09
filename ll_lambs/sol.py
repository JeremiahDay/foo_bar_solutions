def solution(total_lambs):
    '''
    Maximum membership growth is by comparison of funds 'n' to the
    sums of the ordered fibonacci series. A list 'f' holds the two
    most recent sequence numbers beginning with n = 3, f_s holds
    the sum of sequence, and the number of members is returned when
    f_s exceeds funds 'n'
    '''
    BIG_NUM = 1000 # arbitrarily large number to drive range generator
    
    fib = total_lambs
    if fib < 3:
        maximum = fib
    else:
        f = [1, 1]
        f_s = 2
        for i in range(2, BIG_NUM):
            f_n = sum(f)
            f_s += f_n
            if f_s > fib:
                maximum = i
                break
            f[i % 2] = f_n

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
    exp_2 = total_lambs
    exp_2 += 1
    exp_2 = exp_2 >> 1
    exp_2 |= exp_2 >> 1
    exp_2 |= exp_2 >> 2
    exp_2 |= exp_2 >> 4
    exp_2 |= exp_2 >> 8
    exp_2 |= exp_2 >> 16
    
    minimum = bin(exp_2).count('1')
    
    return maximum - minimum
