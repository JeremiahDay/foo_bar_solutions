from fractions import *
import copy
from collections import defaultdict, namedtuple

Point = namedtuple('Point', ['x', 'y'])
Vector = namedtuple('Vector', ['dx', 'dy', 'm'])
Rectangle = namedtuple('Rectangle', ['p0', 'p1'])
Tile = namedtuple('Tile', ['tx', 'ty', 'r'])

ORIGIN = Point(0, 0)

def solution(dimensions, your_position, trainer_position, distance):
    reference = Rectangle(ORIGIN, Point(*dimensions))
    player = Point(*your_position)
    target = Point(*trainer_position)
    dd = distance**2
    pieces = {'miss': player, 'hit': target}

    room = Frame(reference=reference, contents=pieces)
    tiles = room.tiles_within_circle(player, distance)
    count = 0
    # 'line_of_sight' has objects sorted by beam line slope and filtered
    # by shortest distance from player -> object; slope: (distance, type)
    line_of_sight = defaultdict(lambda: (float('inf'), 'miss'))
    for tile in tiles:
        for e in room.contents.keys():
            if e == 'hit':
                step = 1
            else:
                step = -1
            e_r = room.get_reflected_item(tile, e)
            s = slope(player, e_r)
            if s == 'IDENTITY':
                continue
            e_r_dd = dist_square(player, e_r)
            if e_r_dd > dd:
                continue
            if e_r_dd <= line_of_sight[s][0]:
                if line_of_sight[s][1] == e:
                    pass
                else:
                    count += step
                line_of_sight[s] = (e_r_dd, e)
    for e in line_of_sight.items():
        if e[1][1] == 'hit':
            print(e)
    return count

def dist_square(a, b):
    # Returns the square of the distance of two Point objects
    return (b.x - a.x)**2 + (b.y - a.y)**2

def translate(item, dist):
    '''
    Returns a new item a given Vector 'dist' from the given 'item'
    '''
    x = item.x + dist.dx * dist.m
    y = item.y + dist.dy * dist.m
    return Point(x, y)

def reflect(item, r):
    '''
    Returns a new item a given rotation 'r' from the given 'item'.
    'r' uses the reflection/rotation notation from Tile objects;
    see the Frame class docs
    '''
    x, y = item
    if 2 <= r:
        y *= -1
    if 0 < r and r < 3:
        x *= -1
    return Point(x, y)

def slope(a, b):
    '''
    Returns the fractional slope of a path from Point a to Point b
    To preserve sense slope is expressed using the convention (sn, sd)
    where sn, sd are all integers EXCLUDING sd == 0; for all slope
    values with sn > 0 when sd would be 0, 'VERTICAL_UP' is returned
    For sn < 0 and sd would be 0, 'VERTICAL_DN' is returned
    For sn == 0 and sd would be 0, 'IDENTITY' is returned
    '''
    if a == b:
        return 'IDENTITY'
    sd = b.x - a.x
    sn = b.y - a.y
    if sd == 0:
        if sn > 1:
            return 'VERTICAL_UP'
        else:
            return 'VERTICAL_DN'
    f = Fraction(sn, abs(sd)) # automatically reduces with gcd
    rn, rd = (f.numerator, f.denominator)
    if sd < 1:
        rd *= -1
    return (rn, rd)

class Frame(object):
    def __init__(self, reference, contents):
        '''
        Creates a Frame of reference object representing a reference rectange
        and its three mirrored states: up/down symmetry, left/right symmetry,
        and pi radial symmetry.

        Arguments:
        reference: A Rectangle namedtuple defining the dimensions of a
          mirrored space.
        contents: A dictionary of form tag: Point

        Frames define _tiles_, which are images of the reference space and its
        contents. Tiles are translated, reflected, and/or rotated; the
        condition of any tile is described by its properties:
          t: translation of the tile origin point (i.e. reference rectange
          point 'p0'). The displacement values are expressed as tx and ty
          r: reflection/rotation value. This is a value between 0 and 3
            r = 0: no reflection/rotation,
                   equiv to reference * [[1, 0], [0, 1]]
            r = 1: reflected left/right along the vertical axis through 'p0',
                   equiv to reference * [[-1, 0], [0, 1]]
            r = 2: rotated by pi radians around 'p0', equiv to 
                   reference * [[-1, 0], [0, -1]]
            r = 3: reflected up/down along the horizontal axis through 'p0',
                   equiv to reference * [[1, 0], [0, -1]]

        The reference tile matches Tag(tx=0, ty=0, r=0). The left/right mirror
        for the reference tile matches Tag(tx=0, ty=0, r=1). The tile located 3
        Frames below the origin Frame and 2 Frames right and rotated by pi
        would match Tag(tx=-3, ty=2, r=2).
        '''
        self._ref = reference
        self._contents = copy.deepcopy(contents)  # no clobbering

    @property
    def contents(self):
        return self._contents
    
    def get_reflected_item(self, tile, tag):
        item = copy.deepcopy(self._contents[tag])
        item = reflect(item, tile.r)
        dx = tile.tx * 2 * self._ref.p1.x
        dy = tile.ty * 2 * self._ref.p1.y
        item = translate(item, Vector(dx, dy, 1))
        return item
        
    def tiles_within_circle(self, pos, distance):
        dd = distance**2
        hx, hy = self._ref.p1
        for ix in range(0, distance + pos.x, hx):
            for iy in range(0, distance + pos.y, hy):
                if ix**2 + iy**2 < dd:
                    tx = (ix + hx) / (2 * hx)
                    ty = (iy + hy) / (2 * hy)
                    r = (tx % 2 + (-1)**(1 + tx % 2) * (ty % 2)) % 4
                    yield Tile(tx, ty, r)
        if pos.x**2 < dd:  # second quadrant; x < 0, y >= 0
            for ix in range(-distance - pos.x, 1, hx):
                for iy in range(0, distance + pos.y, hy):
                    if ix**2 + iy**2 < dd:
                        tx = (ix + hx) / (2 * hx)
                        ty = (iy + hy) / (2 * hy)
                        r = ((tx + 1) % 2 + \
                            (-1)**(1 + (tx + 1) % 2) * (ty % 2)) % 4
                        yield Tile(tx, ty, r)
        if pos.x**2 + pos.y**2 < dd:  # third quadrant; x < 0, y < 0
            for ix in range(-distance - pos.x, 1, hx):
                for iy in range(-distance - pos.y, 1, hy):
                    if ix** 2 + iy**2 < dd:
                        tx = (ix + hx) / (2 * hx)
                        ty = (iy + hy) / (2 * hx)
                        r = ((tx + 1) % 2 + \
                            (-1)**(1 + (tx + 1) % 2) * ((ty + 1) % 2)) % 4
                        yield Tile(tx, ty, r)
        if pos.y**2 < dd:  # fourth quadrant; x >= 0, y < 0
            for ix in range(0, distance + pos.y, hx):
                for iy in range(-distance - pos.y, 1, hy):
                    if ix**2 + iy**2 < dd:
                        tx = (ix + hx) / (2 * hx)
                        ty = (iy + hy) / (2 * hy)
                        r = (tx % 2 + (-1)**(1 + tx % 2) * ((ty + 1) % 2)) % 4
                        yield Tile(tx, ty, r)

if __name__ == '__main__':
    test = solution([3,2], [1,1], [2,1], 4)
    print(test)