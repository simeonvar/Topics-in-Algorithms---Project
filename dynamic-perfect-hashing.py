#!/usr/bin/env python3
'''Implementation of dynamic perfect hashing'''

import random

class DynamicPerfectHashing:
    def __init__(self, universe_size):
        self.count = 0
        self.tables = []
        self.entry = []
        self.M = 0
        self.j = 0
        # nice number
        self.c = 0.5
        self.universe_size = universe_size
        self.prime = self.calculate_prime(universe_size)
        # some bogus start value
        self.universal_hash_function = HashFunction(1, 0)
        #Flag telling whether this entry has been deleted and should be removed or not
        self.isDeleted = false

    def calculate_prime(self, universe_size):
        '''Calculates prime larger than the universe_size'''
        primes = []
        value = 3
        while True:
            # check if it's divisible by prime
            for prime in primes:
                if value % prime == 0:
                    # can skip twice because never divisible by 2
                    value += 2
                    continue

            # return if bigger than universe size
            if value > universe_size:
                return value

            # add to prime list because not divisible by prime
            primes.append(value)
            value += 2


    def RehashAll(self, element):
        '''x is the new value that will be inserted'''
        L = []

        for table in self.tables:
            for entry in table:
                L.append(entry)
                entry.deleted = True

        self.element_count = sum([len(sub_table) for sub_table in L])
        self.M = self.calculate_m(self.element_count)

        W = [set() for _ in range(len(L))]
        while not self.star_star_condition(W, self.element_count):
            universal_hash_function = HashFunction(
                self.prime, self.element_count)

    def Delete(self, element):
        '''Deletion of x simply flags x as deleted without removal and increments count.'''
        self.count+=1
        j=self.universal_hash_function.hash(element)

        if(self.tables[j] != null):
            self.location = self.tables[j].self.universal_hash_function.hash(element)

            if(self.tables[j].L[location] != null):
                self.tables[j].L[location].setDeleted(true)

        if(self.count>=self.M):
            self.RehashAll(-1)
    '''Sets whether this entry should be marked for deletion or not. If true this element is set for deletion.'''
    def setDeleted(boolean, isDeleted):
        self.isDeleted=isDeletde

    def calculate_m(self, element_count):
        '''Calculate M'''
        M = (1 + self.c) * element_count
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
        self.prime = prime
        self.M = M
        self.k = random.randrange(1, prime - 1)

    def hash(self, element):
        '''Hash the element'''
        return (self.k * element % self.prime) % self.M
