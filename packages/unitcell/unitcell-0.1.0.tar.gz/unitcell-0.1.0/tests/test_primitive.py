import unittest as ut
from unitcell import PrimitiveCell
from unitcell.geometry import Vec3

class TestPrimitive(ut.TestCase):

    def setUp(self) -> None:
        self.pc = PrimitiveCell(1.0, 1.0, 1.0, 90, 90, 90)
        return super().setUp()
    
    def assertSamePoint(self, p1, p2):
        self.assertAlmostEqual(p1[0], p2[0])
        self.assertAlmostEqual(p1[1], p2[1])
        self.assertAlmostEqual(p1[2], p2[2])
    
    def assertSameVector(self, v1, v2):
        self.assertAlmostEqual(abs(v1-v2),0)

    def test_basevector(self):
        self.assertSameVector(self.pc.a1, Vec3(1,0,0))
        self.assertSameVector(self.pc.a2, Vec3(0,1,0))
        self.assertSameVector(self.pc.a3, Vec3(0,0,1))

    def test_getpoint(self):
        pt = self.pc.get_point(0,0,0)
        self.assertSamePoint(pt, [0,0,0])
        pt2 = self.pc.get_point(-1,0,0)
        self.assertSamePoint(pt2, [-1,0,0])
        pt3 = self.pc.get_point(0,2,0)
        self.assertSamePoint(pt3, [0,2,0])
        pt4 = self.pc.get_point(-1,0,3)
        self.assertSamePoint(pt4, [-1,0,3])