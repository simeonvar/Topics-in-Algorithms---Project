#!/usr/bin/env python3
'''Implementation of dynamic perfect hashing'''

import math
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
                    L.append(entry.value)
                    entry.deleted = True

        L.append(element)

        self.count = len(L)
        self.M = self.calculate_m(self.count)

        s = max(1, 2 * (self.count - 1))

        W = [set() for _ in range(s)]

        while True:
            self.universal_hash_function = HashFunction(
                self.prime, s)

            for element in L:
                W[self.universal_hash_function.hash(element)].add(element)

            sub_table_space_list = [self.calculate_required_space(sub_table) for sub_table in W]

            # continue until the condition is true
            if self.star_star_condition(sub_table_space_list, self.M):
                break

            # reset W
            W = [set() for _ in range(s)]


        self.table_list = [Table(self.prime) for _ in range(s)]
        for index, table in enumerate(self.table_list):
            element_count = len(W[index])
            table.update(element_count)

        for idx, table_set in enumerate(W):
            sub_table = self.table_list[idx]
            while not self.is_injective(table_set, sub_table.hash_function):
                sub_table.hash_function = HashFunction(self.prime, sub_table.allocated_space)

        for element in L:
            j = self.universal_hash_function.hash(element)
            table = self.table_list[j]
            location = table.hash_function.hash(element)
            table.elements[location].value = element
            table.elements[location].deleted = False


    def calculate_required_space(self, elements):
        b = len(elements)
        m = 2 * b
        s = 2 * m * (m - 1)
        return s

    def Delete(self, element):
        '''Deletion of x simply flags x as deleted without removal and increments count.'''

        if element < 0 or element > self.universe_size:
            raise ValueError('Element is outside of universe')

        self.count -= 1
        j = self.universal_hash_function.hash(element)

        table = self.table_list[j]

        location = table.hash_function.hash(element)

        if table.elements[location].deleted:
            raise ValueError('Element does not exist')
        else:
            table.elements[location].deleted = True

        if self.count >= self.M:
            self.RehashAll(-1)

    def Insert(self, element):
        if element < 0 or element > self.universe_size:
            raise ValueError('Element is outside of universe')

        self.count += 1

        if self.count > self.M:
            self.RehashAll(element)
        else:
            j = self.universal_hash_function.hash(element)

            table = self.table_list[j]
            location = table.hash_function.hash(element)



            # if a duplicate element is inserted, do nothing
            if not table.elements[location].deleted and table.elements[location].value == element:
                self.count -= 1
                return

            table.element_count += 1
            # Is there enough space for the element
            if table.element_count <= table.max_element_count:
                if table.elements[location].deleted:
                    table.elements[location].value = element
                    table.elements[location].deleted = False

                else:
                    self.update_sub_table_same_size(table, element)
            # We have to increase the size of the subtable
            else:
                self.update_sub_table_increase_size(table, element)


    def update_sub_table_same_size(self, table, new_element):
        '''Returns an injective hash function for the given table'''
        sub_table_elements = list(map(lambda x: x.value, filter(
            lambda element: not element.deleted, table.elements)))

        for element in table.elements:
            element.deleted = True

        sub_table_elements.append(new_element)
        table.element_count = len(sub_table_elements)

        hash_function = HashFunction(table.prime, table.allocated_space)

        while not self.is_injective(sub_table_elements, hash_function):
            hash_function = HashFunction(table.prime, table.allocated_space)

        table.hash_function = hash_function

        for element in sub_table_elements:
            location = table.hash_function.hash(element)

            table.elements[location].value = element
            table.elements[location].deleted = False


        return hash_function

    def update_sub_table_increase_size(self, table, new_element):
        previous_allocated_space = table.allocated_space

        table.max_element_count = 2 * max(1, table.max_element_count)
        table.allocated_space = 2 * table.max_element_count * (table.max_element_count - 1)

        # add the amount of new elements
        table.elements.extend([Entry() for _ in range(
            table.allocated_space - previous_allocated_space)])

        sub_table_space_list = [table.allocated_space for table in self.table_list]

        if self.star_star_condition(sub_table_space_list, self.M):
            self.update_sub_table_same_size(table, new_element)
        else:
            self.RehashAll(new_element)

    def is_injective(self, element_list, hash_function):
        '''Check if a hash on a list is injective'''
        location_list = set()

        for element in element_list:
            location = hash_function.hash(element)
            if location in location_list:
                return False
            location_list.add(location)

        return True

    def Locate(self,element):
        '''Return true if the element exists'''
        if element < 0 or element > self.universe_size:
            raise ValueError('Element is outside of universe')

        j = self.universal_hash_function.hash(element)
        table = self.table_list[j]
        location = table.hash_function.hash(element)

        prev_element = table.elements[location]

        if not table.elements[location].deleted and table.elements[location].value == element:
            return True

        return False

    def calculate_m(self, element_count):
        '''Calculate M'''
        M = math.ceil((1 + self.c) * max(element_count, 4))
        return M

    def star_star_condition(self, sub_table_space_list, M):
        '''Returns True if the condition holds'''
        lhs = sum(sub_table_space_list)
        rhs = (32 * (M ** 2) /
               (len(sub_table_space_list) + 4 * M))

        return lhs <= rhs

class Entry:
    def __init__(self):
        self.value = None
        self.deleted = True
    
    def __repr__(self):
        return (str(self.value), str(self.deleted))

class HashFunction:
    def __init__(self, prime, allocated_space):
        # it's okay to increase the size of the prime
        # do it to have a bigger random range
        if prime == 1:
            prime = 3
        self.prime = prime
        self.allocated_space = allocated_space
        self.k = random.randrange(1, prime - 1)

    def hash(self, element):
        '''Hash the element'''
        return (self.k * element % self.prime) % self.allocated_space
    
    def __repr__(self):
        return "s: {}, k: {}".format(self.allocated_space, self.k)


class Table:
    def __init__(self, prime):
        self.elements = []
        self.element_count = 0
        self.max_element_count = 0 # M
        self.allocated_space = 0
        self.prime = prime
        self.hash_function = None

    def update(self, element_count):
        self.element_count = element_count

        # make space for at least two elements
        element_count = max(1, element_count)

        self.max_element_count = 2 * element_count
        self.allocated_space = 2 * self.max_element_count * (self.max_element_count - 1)
        self.elements = [Entry() for _ in range(self.allocated_space)]
        self.hash_function = HashFunction(self.prime, self.allocated_space)

    def __repr__(self):
        return 'count: {}, max: {}, allocated: {}, hash: {}'.format(
            self.element_count, self.max_element_count,
            self.allocated_space, self.hash_function)
