import math as m
from .geometry import Vec3, triple, vprod

def calc_ucvectors(a=1., b=1., c=1., alpha=90., beta=90., gamma=90.,
        deg=True):
    """ Calculate the lattice vectors assuming that the the 1 0 0
    is oriented along the x axis and that the a, b vectors are contained
    in the xy plane"""

    if deg:
        al = alpha*m.pi/180.
        bet= beta*m.pi/180.
        gam = gamma*m.pi/180.
    else:
        al, bet, gam = alpha, beta, gamma

    a_v = Vec3(a, 0., 0.)
    b_v = Vec3(b*m.cos(gam), b*m.sin(gam), 0.)

    cx = m.cos(bet)
    cy = (m.cos(al)-cx*m.cos(gam))/m.sin(gam)
    cz = m.sqrt(1-cx*cx-cy*cy)
    c_v = c*Vec3(cx,cy,cz)
    return a_v, b_v, c_v


def calc_reciprocals(a1, a2, a3):
    """ Calculate and return the reciprocal vectors given three
    basis vectors a1, a2, a3
    """

    volume = triple(a1, a2, a3)
    ar = vprod(a2, a3)/volume
    br = vprod(a3, a1)/volume
    cr = vprod(a1, a2)/volume
    return ar, br, cr


def new_site(p, site_id='X'):
    """Defines a new site at a position given by a Vec3 p"""
    return (site_id, p.x, p.y, p.z)       


def get_neigh_dist(uc, dx, dmax, nmax=3):

    nbins = m.ceil(dmax/dx)
    neigh_dist = {}

    for si in range(uc.nsites):

        dist_list = [[] for _ in range(nbins)]

        p0 = uc.get_vector(0,0,0,si)
        for u in range(-nmax, nmax):
            for v in range(-nmax, nmax):
                for w in range(-nmax, nmax):
                    for s in range(uc.nsites):
                        if u == 0 and v == 0 and w == 0 and s == si:
                            continue
                        p1 = uc.get_vector(u, v, w, s)
                        d = abs(p1-p0)
                        n = m.floor(d/dx)
                        if n >= nbins:
                            continue
                        else:
                            dist_list[n].append((u, v, w, s))
        neigh_dist[si] = dist_list
    return neigh_dist

