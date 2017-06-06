#!/usr/bin/env python3
'''Unit tests for dynamic-perfect-hashing'''

import unittest

# use weird import because of invalid module name (my bad)
dynamicperfecthashing = __import__('dynamic-perfect-hashing')

class TestDynamicPerfectHashing(unittest.TestCase):
    def test_calculate_prime(self):
        dynperf = dynamicperfecthashing.DynamicPerfectHashing(0)
        self.assertEqual(dynperf.prime, 1)

        dynperf = dynamicperfecthashing.DynamicPerfectHashing(2)
        self.assertEqual(dynperf.prime, 3)

        dynperf = dynamicperfecthashing.DynamicPerfectHashing(500)
        self.assertEqual(dynperf.prime, 503)

    def test_insert(self):
        dynperf = dynamicperfecthashing.DynamicPerfectHashing(2)

        dynperf.Insert(1)
        self.assertTrue(dynperf.Locate(1))

    def test_delete(self):
        dynperf = dynamicperfecthashing.DynamicPerfectHashing(2)

        dynperf.Insert(1)
        self.assertTrue(dynperf.Locate(1))

        dynperf.Delete(1)
        self.assertFalse(dynperf.Locate(1))

if __name__ == '__main__':
    unittest.main()
