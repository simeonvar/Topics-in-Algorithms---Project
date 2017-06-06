#!/usr/bin/env python3
'''Unit tests for dynamic-perfect-hashing'''

import unittest

# use weird import because of invalid module name (my bad)
DynPerf = __import__('dynamic-perfect-hashing').DynamicPerfectHashing

class TestDynamicPerfectHashing(unittest.TestCase):
    def test_calculate_prime(self):
        dynperf = DynPerf(0)
        self.assertEqual(dynperf.prime, 1)

        dynperf = DynPerf(2)
        self.assertEqual(dynperf.prime, 3)

        dynperf = DynPerf(500)
        self.assertEqual(dynperf.prime, 503)

    def test_simple(self):
        dynperf = DynPerf(2)

        dynperf.Insert(1)
        self.assertEqual(dynperf.count, 1)
        self.assertEqual(len(dynperf.table_list), 1)
        self.assertTrue(dynperf.Locate(1))

        dynperf.Delete(1)
        self.assertEqual(dynperf.count, 0)
        self.assertEqual(len(dynperf.table_list), 1)
        self.assertFalse(dynperf.Locate(1))

    def test_outside_universe(self):
        dynperf = DynPerf(300)

        dynperf.Insert(0)
        self.assertEqual(dynperf.count, 1)
        self.assertRaises(ValueError, dynperf.Insert, -1)
        self.assertRaises(ValueError, dynperf.Insert, 301)

        self.assertRaises(ValueError, dynperf.Delete, -1)
        self.assertRaises(ValueError, dynperf.Delete, 301)

        self.assertRaises(ValueError, dynperf.Locate, -1)
        self.assertRaises(ValueError, dynperf.Locate, 301)

    def test_insert_duplicate(self):
        '''There's no documentation about how to handle duplicates, but IMO no change should occur'''
        dynperf = DynPerf(50)

        dynperf.Insert(37)
        self.assertEqual(dynperf.count, 1)
        self.assertTrue(dynperf.Locate(37))

        dynperf.Insert(37)
        self.assertEqual(dynperf.count, 1)
        self.assertTrue(dynperf.Locate(37))

        dynperf.Delete(37)
        self.assertEqual(dynperf.count, 0)
        self.assertFalse(dynperf.Locate(37))



if __name__ == '__main__':
    unittest.main()
