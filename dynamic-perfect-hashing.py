#!/usr/bin/env python3
'''Implementation of dynamic perfect hashing'''

import random

class DynamicPerfectHashing:
    def __init__(self, universe_size):
        self.count = 0
        self.table_list = []
        self.entry = []
        self.M = 0
        # nice number
        self.c = 0.5
        self.universe_size = universe_size
        self.prime = self.calculate_prime(universe_size)
        # some bogus start value
        self.universal_hash_function = HashFunction(self.prime, 0)

    def calculate_prime(self, universe_size):
        '''Calculates prime larger than the universe_size'''
        # base cases
        if universe_size == 0:
            return 1
        elif universe_size == 1:
            return 2

        primes = []
        value = 3
        is_prime = True
        while True:
            # check if it's divisible by prime
            for prime in primes:
                if value % prime == 0:
                    is_prime = False
                    break

            # return if bigger than universe size
            if value > universe_size and is_prime:
                return value

            # add to prime list because not divisible by prime
            primes.append(value)
            value += 2
            is_prime = True


    def RehashAll(self, element):
        '''x is the new value that will be inserted'''
        L = []

        for table in self.table_list:
            for entry in table.elements:
                if not entry.deleted:
                    L.append(entry)
                    entry.deleted = True

        self.count = sum([len(sub_table) for sub_table in L])
        self.M = self.calculate_m(self.count)

        W = [set() for _ in range(self.M * 2)]

        while not self.star_star_condition(W, self.count):
            self.universal_hash_function = HashFunction(
                self.prime, self.count)

            for element in L:
                W[self.universal_hash_function.hash(element)].add(element)

        self.table_list = [Table(self.prime) for _ in range(self.M * 2)]
        for index, table in enumerate(self.table_list):
            element_count = len(W[index])
            table.max_element_count = 2 * element_count
            table.allocated_space = 2 * element_count * (element_count - 1)

        for element in L:
            self.Insert(element.value)

    def Delete(self, element):
        '''Deletion of x simply flags x as deleted without removal and increments count.'''
        self.count -= 1
        j = self.universal_hash_function.hash(element)

        if self.table_list[j] != None:

            table = self.table_list[j]

            location = table.hash_function.hash(element)

            if table.elements[location] != None:
                table.elements[location].deleted = True

        if self.count >= self.M:
            self.RehashAll(-1)

    def Insert(self, element):
        exit(1)


    def Locate(self,element):
        j = self.universal_hash_function.hash(element)
        if self.table_list[j] != None:
            table= self.table_list[j]
            location = table.hash_function.hash(element)

            if table.elements[location] != None:
                return true
        else :
            return false

    def calculate_m(self, element_count):
        '''Calculate M'''
        M = (1 + self.c) * max(element_count, 4)
        if M == 0:
            M = 1
        return M

    def star_star_condition(self, W, element_count):
        '''Returns True if the condition holds'''
        lhs = sum([2*(len(w) ** 2) for w in W])
        rhs = (8 * (element_count ** 2) /
               (self.calculate_m(element_count))) + 2 * element_count

        return lhs < rhs

class Entry:
    def __init__(self, value):
        self.value = value
        self.deleted = False

class HashFunction:
    def __init__(self, prime, M):
        # it's okay to increase the size of the prime
        # do it to have a bigger random range
        if prime == 1:
            prime = 3
        self.prime = prime
        self.M = M
        self.k = random.randrange(1, prime - 1)

    def hash(self, element):
        '''Hash the element'''
        return (self.k * element % self.prime) % self.M

class Table:
    def __init__(self, prime):
        self.elements = []
        self.element_count = 0
        self.max_element_count = 0 # M
        self.allocated_space = 0
        self.hash_function = HashFunction(prime, self.max_element_count)
