from .geometry import *
from .utils import calc_ucvectors, calc_reciprocals
import math as m

class PrimitiveCell:
    """Implement a primitive cell"""
    
    def __init__(self, a=1., b=1., c=1., alpha=90.,
            beta=90., gamma=90., name=''):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.al_deg = alpha
        self.bet_deg = beta
        self.gam_deg = gamma

        self.al = m.pi*alpha/180.
        self.bet = m.pi*beta/180.
        self.gam = m.pi*gamma/180.

        # reference vectors of 001 orientation:
        self.a01, self.a02, self.a03 = calc_ucvectors(self.a,
                self.b, self.c, self.al, self.bet, self.gam, deg=False)

        self.a1, self.a2, self.a3 = self.a01, self.a02, self.a03
        self.update_reciprocals()

    def update_reciprocals(self):
        self.b1, self.b2, self.b3 = calc_reciprocals(self.a1, 
                self.a2, self.a3)
 

    def get_pos(self, u, v, w):
        return self.get_vector(u, v, w)


    def get_vector(self, u, v, w):
        """Return the coordinates of a lattice site (u, v, x, n)
        as a Vector
        
        """
        return u*self.a1 + v*self.a2 + w*self.a3


    def get_point(self, u, v, w):
        """Return the coordinates of lattice site (u, v, w)
        as a tuple
        
        """
        p = self.get_vector(u, v, w)
        return p.x, p.y, p.z
        
    def iter_vectors(self, xr, yr, zr):
        """Iterate through the lattice points in the range given by xr, yr, zr,
        returning a vector
        
        if the range is a scalar, it assumes that the minimum value is zero
        """
    
        if hasattr(xr, '__iter__'):
            xmin, xmax = xr
        else:
            xmin = 0
            xmax = xr
        if hasattr(yr, '__iter__'):
            ymin, ymax = yr
        else:
            ymin = 0
            ymax = yr
        if hasattr(zr, '__iter__'):
            zmin, zmax = zr
        else:
            zmin = 0
            zmax = zr
        for u in range(xmin, xmax):
            for v in range(ymin, ymax):
                for w in range(zmin, zmax):
                    yield self.get_vector(u, v, w)


    def iter_points(self, xr, yr, zr):
        """Iterate through the lattice points in the range given by xr, yr, zr,
        returning the coordinates as a tuple
        
        if the range is a scalar, it assumes that the minimum value is zero
        """

        if hasattr(xr, '__iter__'):
            xmin, xmax = xr
        else:
            xmin = 0
            xmax = xr
        if hasattr(yr, '__iter__'):
            ymin, ymax = yr
        else:
            ymin = 0
            ymax = yr
        if hasattr(zr, '__iter__'):
            zmin, zmax = zr
        else:
            zmin = 0
            zmax = zr
        for u in range(xmin, xmax):
            for v in range(ymin, ymax):
                for w in range(zmin, zmax):
                    p = self.get_vector(u, v, w)
                    yield (p.x, p.y, p.z)
   

    def get_basis(self):
        """ Returns the current lattice vectors """
        return self.a1, self.a2, self.a3
    
    def get_reciprocals(self):
        """ Return the reciprocal vectors """
        return self.b1, self.b2, self.b3
    
    def get_normal(self, h, k, l):
        """ Return the normal vector to the i j k plane """
        return unit_vector(h*self.b1 + k*self.b2 + l*self.b3)
    
    def get_planedist(self, h, k, l):
        """ Return the distance between i j k planes """
        return 1./abs(h*self.b1 + k*self.b2 + l*self.b3)

    def xrotate(self, theta):
        self.a1.xrotate(theta)
        self.a2.xrotate(theta)
        self.a3.xrotate(theta)
        self.update_reciprocals()

    def yrotate(self, theta):
        self.a1.yrotate(theta)
        self.a2.yrotate(theta)
        self.a3.yrotate(theta)
        self.update_reciprocals()

    def zrotate(self, theta):
        self.a1.zrotate(theta)
        self.a2.zrotate(theta)
        self.a3.zrotate(theta)
        self.update_reciprocals()



