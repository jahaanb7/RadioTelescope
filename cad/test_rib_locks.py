"""Run with python -m unittest discover -s cad -p 'test_rib_locks.py'."""
import unittest
from rib_lock_prototype import LockDesign, check_coupon, joint_plan
from rib_lock_assembly import modify_support, placed
import build as baseline


class RibLockChecks(unittest.TestCase):
    def test_fit_variants_insert_rotate_and_retain(self):
        for wood in (2.8, 3.175, 3.4):
            for clearance in (0.3, 0.5, 0.7):
                with self.subTest(wood=wood,clearance=clearance):
                    design=LockDesign(wood,clearance)
                    checks=check_coupon(design,design.coupon())
                    self.assertGreater(checks["locked_withdrawal_interference_mm3"],1)

    def test_load_transfer_connections_remain_bolted(self):
        plan=joint_plan()
        protected={60,80,100,180,260,280,300}
        self.assertEqual({r["angle_deg"] for r in plan if r["rim"]=="M4 retained"},protected)
        self.assertTrue(all(r["hub"]=="M4 retained" for r in plan))
        self.assertEqual(sum(1+(2 if r["rim"].startswith("2") else 0) for r in plan),40)

    def test_outside_reviewed_range_is_rejected(self):
        for wood,clearance in ((1,0.5),(8,0.5),(3.175,0.01),(3.175,2)):
            with self.assertRaises(ValueError):
                LockDesign(wood,clearance)

    def check_support_pair(self, shape, sites):
        design=LockDesign()
        supports=[]
        for angle in (-10,10):
            part=baseline.rz(shape,angle)
            for site in sites:
                part,changed=modify_support(part,design,site)
                self.assertTrue(changed)
            self.assertTrue(part.isValid())
            self.assertEqual(len(part.Solids()),1)
            supports.append(part)
        self.assertLess(supports[0].intersect(supports[1]).Volume(),1e-5)
        for site in sites:
            lock=placed(design.lock(),site)
            for part in supports:
                self.assertLess(lock.intersect(part).Volume(),1e-5)

    def test_actual_middle_spacers(self):
        self.check_support_pair(baseline.spacer(),[(0,baseline.MID_HOLE_R,baseline.MID_HOLE_Z)])

    def test_actual_plain_rim_bays(self):
        self.check_support_pair(baseline.rim_panel()[0],[(0,baseline.RIM_HOLE_R,z) for z in baseline.RIM_HOLE_Z])


if __name__=="__main__":
    unittest.main()
