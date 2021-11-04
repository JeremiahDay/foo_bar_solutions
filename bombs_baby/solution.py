from itertools import count

def solution(M, F):
    sol = [int(M), int(F)]
    k = lambda i: sol[i]
    c = [0, 1]
    i = 0
    while True:
        if sol == [1, 1]:
            return str(i)
        sol_sort = sorted(c, key=k)
        diff = sol[sol_sort[1]] - sol[sol_sort[0]]
        if diff == 0:
            return 'impossible'

        n = max(diff / sol[sol_sort[0]], 1)
        sol[sol_sort[1]] -= sol[sol_sort[0]] * n
        i += n

if __name__ == '__main__':
    print(solution('4', '9'))