LEFT = False
RIGHT = True

def solution(h, q):
    '''
    h: height of tree
    q: list of integers to consider'''
    q_rev = [x for x in reversed(q)]
    s = []
    while q_rev:
        n = q_rev.pop()
        node = n
        height = h
        while True:
            rank = int.bit_length(node)

            if rank >= height:
                hand = RIGHT
            else:
                hand = LEFT
                height = rank
            if node == 2 ** height - 1:
                if hand == LEFT:
                    offset = node + 1
                else:
                    offset = 1
                break
            if hand == RIGHT:
                height -= 1
                node -= 2 ** height - 1

        label = n + offset
        if label >= 2 ** h:
            s.append(-1)
        else:
            s.append(label)
    return s

if __name__ == '__main__':
    print(solution(3, [7, 3, 5, 1]))
    print(solution(5, [19, 14, 28]))
    print(solution(5, [i for i in range(1, 31)]))