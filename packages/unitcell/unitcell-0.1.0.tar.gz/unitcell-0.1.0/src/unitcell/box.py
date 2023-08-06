"""
A box
"""

from geometry import *

class Lattice:

    def __init__(self, unit_cell, n1, n2, n3, default_value=0, bc=None):
        self.uc = unit_cell
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.bc = bc
    
        self.cell_id = []
        self.cell_dict = {}
        ncell = 0
        self.cell_value = []
        for site_id in self.uc.iter_sites(self.n1, self.n2, self.n3):
            self.cell_id.append(site_id)
            self.cell_dict[site_id] = ncell
            ncell += 1
            self.cell_value = default_value
        self.ncells = ncell

    def set(self, site_id, value):
        self.cell_value[self.cell_dict[site_id]] = value

    def get_points(self):
        pl = []
        for i in range(self.ncells):
            value = self.cell_value[i]
            if value == 0:
                continue
            else:
                site_id = self.cell_id[i]
                row = [value].extend(self.uc.get_point(*site_id))
                pl.append(row)
        return pl
    

