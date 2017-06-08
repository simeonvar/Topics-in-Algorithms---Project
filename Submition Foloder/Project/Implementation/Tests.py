#!/usr/bin/env python3
'''Unit tests for dynamic-perfect-hashing'''

import pprint
import unittest
import random

# use weird import because of invalid module name (my bad)
DynPerf = __import__('Dynamic-Perfect-Hashing').DynamicPerfectHashing
HashFunction = __import__('Dynamic-Perfect-Hashing').HashFunction

class PredictableHash:
    def __init__(self, hasher):
        self.hasher = hasher
    def hash(self, element):
        return self.hasher(element)

class TestDynamicPerfectHashing(unittest.TestCase):
    def test_calculate_prime(self):
        dynperf = DynPerf(0)
        self.assertEqual(dynperf.prime, 1)

        dynperf = DynPerf(2)
        self.assertEqual(dynperf.prime, 3)

        dynperf = DynPerf(500)
        self.assertEqual(dynperf.prime, 503)

    def test_is_injective(self):
        '''Force collision with predictable hash''' 
        dynperf = DynPerf(2)
        self.assertFalse(dynperf.is_injective([1, 1], PredictableHash(lambda _: 0)))
        self.assertTrue(dynperf.is_injective([0, 1], PredictableHash(lambda x: x)))

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
    
    def test_insert_multiple(self):
        dynperf = DynPerf(2)

        dynperf.Insert(1)
        self.assertEqual(dynperf.count, 1)
        self.assertTrue(dynperf.Locate(1))

        dynperf.Insert(2)
        self.assertEqual(dynperf.count, 2)
        self.assertTrue(dynperf.Locate(1))
        self.assertTrue(dynperf.Locate(2))

        dynperf.Delete(1)
        self.assertEqual(dynperf.count, 1)
        self.assertFalse(dynperf.Locate(1))

        dynperf.Delete(2)
        self.assertEqual(dynperf.count, 0)
        self.assertFalse(dynperf.Locate(2))


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

    def test_insert_sub_table_no_size_increase_rehash(self):
        '''Create collision by forcing the elements into the same subtable and the same location''' 
        dynperf = DynPerf(30)

        dynperf.global_hash_function = PredictableHash(lambda _: 0)
        dynperf.Insert(0)

        dynperf.table_list[0].hash_function = PredictableHash(lambda _: 0)
        dynperf.Insert(1)

        self.assertEqual(dynperf.count, 2)
        self.assertTrue(dynperf.Locate(0))
        self.assertTrue(dynperf.Locate(1))

    def test_insert_sub_table_size_increase_rehash(self):
        '''Create collision by forcing the elements into the same subtable and the same location''' 
        dynperf = DynPerf(30)

        dynperf.global_hash_function = PredictableHash(lambda _: 0)
        dynperf.Insert(0)

        dynperf.table_list[0].hash_function = PredictableHash(lambda _: 0)

        dynperf.Insert(1)
        # max element count is 2, will force a rehash on subtable
        dynperf.Insert(2)

        self.assertEqual(dynperf.count, 3)
        self.assertTrue(dynperf.Locate(0))
        self.assertTrue(dynperf.Locate(1))
        self.assertTrue(dynperf.Locate(2))
    
    def test_create_another_subtable(self):
        dynperf = DynPerf(100)

        for i in range(4):
            dynperf.Insert(i)

        self.assertTrue(dynperf.count, 4)
        self.assertEqual(len(dynperf.table_list), 1)

        # 4 elements are allowed until the (**) no longer holds
        dynperf.Insert(4)

        self.assertTrue(dynperf.count, 5)
        # s = 2(n - 1) => 2 * 4 = 8
        self.assertEqual(len(dynperf.table_list), 8)

        # make sure another element can be added after the next sublist was created
        dynperf.Insert(5)
        self.assertTrue(dynperf.count, 6)
        self.assertTrue(len(dynperf.table_list), 10)

        for i in range(6):
            self.assertTrue(dynperf.Locate(i))

        for i in range(6):
            dynperf.Delete(i)

        for i in range(6):
            self.assertFalse(dynperf.Locate(i))

    def test_full(self):
        '''Full integration test by randoming 1 million values'''
        count = int(1E6)
        # Our prime calculation method is really naive, so can't have a very
        # large universe size
        universe_size = 5000
        elements = [random.randrange(0, universe_size) for _ in range(count)]

        dynperf = DynPerf(universe_size)

        for ele in elements:
            dynperf.Insert(ele)
            self.assertTrue(dynperf.Locate(ele))

        for ele in elements:
            self.assertTrue(dynperf.Locate(ele))

        previously_deleted = set()
        for ele in elements:
            if ele in previously_deleted:
                self.assertRaises(ValueError, dynperf.Delete, ele)
            else:
                dynperf.Delete(ele)
            previously_deleted.add(ele)

        for ele in elements:
            self.assertFalse(dynperf.Locate(ele))



if __name__ == '__main__':
    unittest.main()
