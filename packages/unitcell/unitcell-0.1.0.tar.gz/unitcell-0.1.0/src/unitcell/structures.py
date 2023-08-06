from math import sin, cos, tan, pi, sqrt
from .unitcell import UnitCell


c30 = cos(30*pi/180.)
s30 = sin(30*pi/180.)
t30 = tan(30*pi/180.)

def wurtzite_ortho(a):
    """Return a lattice for the wurzite structure with the following
    orthogonal axes

        - x: [1 0 -1 0]
        - y: [1 1 -2 0]
        - z: [0 0 0 1]
    """
    a1 = 2*a*c30
    a2 = a
    bp = a*c30-0.5*a*t30
    h = sqrt(a*a-bp*bp)
    ht = h/2 - bp*bp/(2*h)
    b = h - ht 
    a3 = 2*b + 2*ht
    h1 = ht/a3
    h2 = h1 + b/a3
    h3 = h2 + ht/a3
    bnorm = 0.25*t30/c30

    sites = [('A', 0, 0, 0), ('A', 0.5, 0.5, 0),
              ('B', bnorm, 0.5, h1), ('B', 0.5+bnorm, 0, h1),
              ('A', bnorm, 0.5, h2), ('A', 0.5+bnorm, 0, h2),
              ('B', 0, 0, h3), ('B', 0.5, 0.5, h3)]
    ndict = {
        0: [(0, 0, 0, 2), (-1, 0, 0, 3), (0, -1, 0, 2), (0, 0, -1, 6)],
        1: [(0, 0, 0, 2), (0, 0, 0, 3), (0, 1, 0, 3), (0, 0, -1, 7)],
        2: [(0, 0, 0, 0), (0, 0, 0, 1), (0, 1, 0, 0), (0, 0, 0, 4)],
        3: [(0, 0, 0, 1), (0, -1, 0, 1), (1, 0, 0, 0), (0, 0, 0, 5)],
        4: [(0, 0, 0, 2), (0, 0, 0, 6), (0, 0, 0, 7), (0, 1, 0, 6)],
        5: [(0, 0, 0, 3), (0, 0, 0, 7), (1, 0, 0, 6), (0, -1, 0, 7)],
        6: [(0, 0, 0, 4), (-1, 0, 0, 5), (0, -1, 0, 4), (0, 0, 1, 0)],
        7: [(0, 0, 0, 4), (0, 0, 0, 5), (0, 1, 0, 5), (0, 0, 1, 1)]
        }
    return UnitCell(a=a1, b=a2, c=a3, sites=sites, ndict=ndict)


def SiC4H_ortho(a, orient=None):
    """ SiC-4H structure with the following orthogonal cell:
        - x: [1 0 -1 0]
        - y: [1 1 -2 0]
        - z: [0 0 0 1]
    """
    
    a1 = 2*a*c30
    a2 = a
    bp = a*c30-0.5*a*t30
    h = sqrt(a*a-bp*bp)
    ht = h/2 - bp*bp/(2*h)
    b = h - ht 
    a3 = 4*b + 4*ht
    h1 = ht/a3
    h2 = h1 + b/a3
    h3 = h2 + ht/a3
    h4 = h3 + b/a3
    h5 = h4 + ht/a3
    h6 = h5 + b/a3
    h7 = h6 + ht/a3

    bnorm = 0.25*t30/c30

    sites = [('A', 0, 0, 0), ('A', 0.5, 0.5, 0),
              ('B', bnorm, 0.5, h1), ('B', 0.5+bnorm, 0, h1),
              ('A', bnorm, 0.5, h2), ('A', 0.5+bnorm, 0, h2),
              ('B', 0, 0, h3), ('B', 0.5, 0.5, h3),
              ('A', 0, 0, h4), ('A', 0.5, 0.5, h4),
              ('B', 0.5*bnorm + 0.25, 0, h5), ('B',0.75+0.5*bnorm, 0.5, h5),
              ('A', 0.5*bnorm + 0.25, 0, h6), ('A',0.75+0.5*bnorm, 0.5, h6),
              ('B', 0, 0, h7), ('B', 0.5, 0.5, h7)]
    ndict = {
        0: [(0, 0, 0, 2), (-1, 0, 0, 3), (0, -1, 0, 2), (0, 0, -1, 14)],
        1: [(0, 0, 0, 2), (0, 0, 0, 3), (0, 1, 0, 3), (0, 0, -1, 15)],
        2: [(0, 0, 0, 0), (0, 0, 0, 1), (0, 1, 0, 0), (0, 0, 0, 4)],
        3: [(0, 0, 0, 1), (0, -1, 0, 1), (1, 0, 0, 0), (0, 0, 0, 5)],
        4: [(0, 0, 0, 2), (0, 0, 0, 6), (0, 0, 0, 7), (0, 1, 0, 6)],
        5: [(0, 0, 0, 3), (0, 0, 0, 7), (1, 0, 0, 6), (0, -1, 0, 7)],
        6: [(0, 0, 0, 4), (-1, 0, 0, 5), (0, -1, 0, 4), (0, 0, 0, 8)],
        7: [(0, 0, 0, 4), (0, 0, 0, 5), (0, 1, 0, 5), (0, 0, 0, 9)],
        8: [(0, 0, 0, 6), (0, 0, 0, 10), (-1, 0, 0, 11), (-1, -1, 0, 11)],
        9: [(0, 0, 0, 7), (0, 0, 0, 10), (0, 0, 0, 11), (0, 1, 0, 10)],
        10:[(0, 0, 0, 8), (0, 0, 0, 9), (0, -1, 0, 9), (0, 0, 0, 12)],
        11:[(0, 0, 0, 13), (0, 0, 0, 9), (1, 0, 0, 8), (1, 1, 0, 8)],
        12:[(0, 0, 0, 10), (0, 0, 0, 14), (0, 0, 0, 15), (0, -1, 0, 15)],
        13:[(0, 0, 0, 11), (1, 0, 0, 14), (0, 0, 0, 15), (1, 1, 0, 14)],
        14:[(0, 0, 1, 0), (0, 0, 0, 12), (-1, 0, 0, 13), (-1, -1, 0, 13)],
        15:[(0, 0, 1, 1), (0, 0, 0, 12), (0, 0, 0, 13), (0, 1, 0, 12)]
        }
    if orient == 'x':
        newsites = [(a, d, c, b) for a, b, c, d in site]
        for k, v in ndict.items():
            ndict[k] = [(c, b, a, d) for a, b, c, d in v]
        return UnitCell(a=a3, b=a2, c=a1, sites=newsites, ndict=ndict)

    if orient == 'y':
        newsites = [(a, b, d, c) for a, b, c, d in site]
        for k, v in ndict.items():
            ndict[k] = [(a, c, b, d) for a, b, c, d in v]
        return UnitCell(a=a1, b=a3, c=a2, sites=newsites, ndict=ndict)

    return UnitCell(a=a1, b=a2, c=a3, sites=newsites, ndict=ndict)


def hcp(a=1, orient=None):
    """Hexagonal compact packing structure

    """

    a1 = a
    a2 = a
    a3 = sqrt(8./3.)*a1
    gamma = 120.

    sites = [('X', 0, 0, 0), ('X', 2./3., 1./3., 0.5)]
    ndict = {
      0:[(1, 0, 0, 0), (0, 1, 0, 0), (1, 1, 0, 0),
         (-1, 0, 0, 0), (0, -1, 0, 0), (-1, -1, 0, 0),
         (0, 0, 0, 1), (-1, 0, 0, 1), (-1, -1, 0, 1),
         (0, 0, -1, 1), (-1, 0, -1, 1), (-1, -1, -1, 1)],
      1:[(1, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1),
         (-1, 0, 0, 1), (0, -1, 0, 1), (-1, -1, 0, 1),
         (0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0),
         (0, 0, 0, 1), (1, 0, 0, 1), (1, 1, 0, 1)]}

    return UnitCell(a=a1, b=a2, c=a3, gamma=gamma, sites=sites, ndict=ndict)


def hcp_ortho(a):
    """HCP lattice with the following orthogonal axes:

        - x: [1 0 -1 0]
        - y: [1 1 -2 0]
        - z: [0 0 0 1]
    """
    a1 = 2*a*c30
    a2 = 1.*a
    bp = a/(2.*c30)
    h = sqrt(a*a-bp*bp)
    a3 = 2*h

    sites = [('A', 0, 0, 0), ('A', 0.5, 0.5, 0),
              ('A', 1./6., 0.5, 0.5), ('A', 2./3., 0, 0.5)]

    return UnitCell(a=a1, b=a2, c=a3, sites=sites)


def fcc111_ortho(a):
    """FCC 111 lattice with the following
    orthogonal axes

        - x: [1 0 -1 0]
        - y: [1 1 -2 0]
        - z: [0 0 0 1]
    """
    a1 = 2*a*c30
    a2 = 1.*a
    bp = a/(2.*c30)
    h = sqrt(a*a-bp*bp)
    a3 = 3*h

    sites = [('A', 0, 0, 0), ('A', 0.5, 0.5, 0),
              ('A', 1./6., 0.5, 1./3), ('A', 2./3., 0, 1./3),
              ('A', 5./6., 0.5, 2./3), ('A', 1./3., 0, 2./3)]

    return UnitCell(a=a1, b=a2, c=a3, sites=sites)

