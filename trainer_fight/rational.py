from fractions import gcd
import heapq
import itertools
from math import pow

counter = itertools.count()
t_pq = []
s_pq = []

def solution(dimensions, your_position, trainer_position, distance):
    rect = complex(*dimensions)
    sx, sy = your_position
    tx, ty = trainer_position
    t_vec = [object for _ in range(4)]
    s_vec = [object for _ in range(4)]
    dd = pow(distance, 2)

    t_vec[0] = complex(tx - sx, ty - sy)
    t_vec[1] = complex(-tx - sx, ty - sy)
    t_vec[2] = complex(-tx - sx, -ty - sy)
    t_vec[3] = complex(tx - sx, -ty - sy)
    if ddist(t_vec[0]) > dd:
        return 0
    if ddist(t_vec[0]) == dd:
        return 1

    s_vec[0] = complex(0, 0)
    s_vec[1] = complex(-2 * sx, 0)
    s_vec[2] = complex(-2 * sx, -2 * sy)
    s_vec[3] = complex(0, -2 * sy)

    bearings = {}
    for vec in t_vec:
        fill(vec, rect, dd, t_pq)
    while t_pq:
        e = heapq.heappop(t_pq)
        if e[2] not in bearings:
            bearings[e[2]] = e[0]
    for vec in s_vec:
        fill(vec, rect, dd, s_pq)
    while s_pq:
        e = heapq.heappop(s_pq)
        if e[2] in bearings and e[0] < bearings[e[2]]:
            del bearings[e[2]]

    return len(bearings)

def ddist(c):
    return pow(c.real, 2) + pow(c.imag, 2)

def complex_conjugate(c):
    # returns the conjugate of vector c
    return complex(c.real, -c.imag)

def reflect(c):
    yield c
    yield -complex_conjugate(c)
    yield -c
    yield complex_conjugate(c)

def fill(vec, mirrors, max_dd, pq):
    # Finds inv_slope and distance to all same-sense reflections of an object
    # located at displacement vector 'vec' from the source within 'distance'
    # with mirrors on the edges of a rectange from [0, 0] to 'mirrors'
    for mirror in reflect(mirrors):
        image = vec + mirror - mirrors
        image_0 = image
        dd = ddist(image)
        while dd <= max_dd:
            while dd <= max_dd:
                g = abs(gcd(image.real, image.imag))
                if g == 0:
                    add_ray(image, g, pq)
                else:
                    add_ray(image/g, g, pq)
                image += 2* mirror.real
                dd = ddist(image)
            image = image_0.real + (image.imag + 2 * mirror.imag) * 1j
            dd = ddist(image)


def add_ray(slope, distance, pq):
    count = next(counter)
    entry = (distance, count, slope)
    heapq.heappush(pq, entry)

if __name__ == '__main__':
    test = solution([3,2], [1,1], [2,1], 4)
    print(test)