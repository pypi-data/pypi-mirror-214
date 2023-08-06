
from .geometry import *
import math as m
from .primitive import PrimitiveCell


class UnitCell(PrimitiveCell):
    """Class UnitCell contains the properties and methods to define the unit
    cell of a 3D crystal"""
    
    def __init__(self, a=1., b=1., c=1., alpha=90.,
            beta=90., gamma=90.,
            sites=[('X', 0, 0, 0)], name=''):
        PrimitiveCell.__init__(self, a, b, c, alpha, beta, gamma, name)

        self.sites = [toVec3(si[1:]) for si in sites]
        self._nsites = len(self.sites)

        self._ids = [si[0] for si in sites]
        self._uniqueids = set(self._ids)


    def get_vector(self, u, v, w, n=0):
        """Return the coordinates of a lattice site (u, v, x, n)
        as a Vector
        
        """
        v1 = (self.sites[n].x + u)*self.a1
        v2 = (self.sites[n].y + v)*self.a2
        v3 = (self.sites[n].z + w)*self.a3
        return v1 + v2 + v3
    
    def get_point(self, u, v, w, n=0):
        """Return the coordinates of lattice site (u, v, w, n)
        as a tuple
        
        """
        v = self.get_vector(u, v, w, n)
        return v.x, v.y, v.z

    def get_site(self, u, v, w, n=0):
        """Return the coordinates and the id of the lattice site u, v, w, n
        """
        x, y, z = self.get_point(u, v, w, n)
        return self._ids[n], x, y, z
          

    @property
    def siteids(self):
        """Return the unique ids of the sites defined in the base of the 
        unit cell

        Return a set with the unique values
        """
        return self._uniqueids
    
    @property
    def nsites(self):
        """Return the number of sites defined in the base of the unit
        cell

        """
        return self._nsites

    def get_siteid(self, s):
        return self._ids[s]


    def iter_points(self, n1, n2, n3):
        """Iterate through the list of sites contained in a
        n1xn2xn3 volume"""
        for i in range(n1):
            for j in range(n2):
                for k in range(n3):
                    for ns in range(self.nsites):
                        yield self.get_point(i, j, k, ns)

    def iter_sites(self, n1, n2, n3):
        """Iterate through the list of sites contained in a
        n1xn2xn3 volume"""
        for i in range(n1):
            for j in range(n2):
                for k in range(n3):
                    for ns in range(self.nsites):
                        yield self.get_site(i, j, k, ns)



class Cubic(UnitCell):

    def __init__(self, a, sites=None):
        if sites is None:
            UnitCell.__init__(self, a, a, a, 90, 90, 90)
        else:
            UnitCell.__init__(self, a, a, a, 90, 90, 90, sites=sites)


class Tetragona(UnitCell):

    def __init__(self, a, c, sites=None):
        if sites is None:
            UnitCell.__init__(self, a, a, c, 90, 90, 90)
        else:
            UnitCell.__init__(self, a, a, c, 90, 90, 90, sites=sites)


class Orthorhombic(UnitCell):

    def __init__(self, a, b, c, sites=None):
        if sites is None:
            UnitCell.__init__(self, a, b, c, 90, 90, 90)
        else:
            UnitCell.__init__(self, a, b, c, 90, 90, 90, sites=sites)


class Hexagonal(UnitCell):

    def __init__(self, a, c, sites=None):
        if sites is None:
            UnitCell.__init__(self, a, a, c, 90, 90, 120)
        else:
            UnitCell.__init__(self, a, a, c, 90, 90, 120, sites=sites)


class Rhombohedral(UnitCell):

    def __init__(self, a, alpha, sites=None):
        if sites is None:
            UnitCell.__init__(self, a, a, a, alpha, alpha, alpha)
        else:
            UnitCell.__init__(self, a, a, a, alpha, alpha, alpha, sites=sites)


