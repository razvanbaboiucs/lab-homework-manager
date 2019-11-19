'''
Created on Dec 12, 2018

@author: Razvan
'''
import unittest
from random import randint
from copy import deepcopy

class SortingAlgorithms:
        
    def bubbleSort(self, my_list, *, key = lambda x : x, cmp = lambda x, y: x - y, reverse = False):
        '''
            Sorts to_sort using bubble sort algorithm
            IN:
                to_sort - list
        '''
        to_sort = deepcopy(my_list)
        sorted = False
        while not sorted:
            sorted = True
            for i in range(1, len(to_sort)):
                if cmp(key(to_sort[i - 1]), key(to_sort[i])) > 0:
                    to_sort[i - 1], to_sort[i] = to_sort[i], to_sort[i - 1]
                    sorted = False
        if reverse == True:
            to_sort = to_sort[::-1]
        return list(to_sort)
    
    def shellSort(self, my_list, *, key = lambda x : x, cmp = lambda x, y: x - y, reverse = False):
        '''
            Sorts to_sort using shell sort algorithm
            IN:
                to_sort - list
        '''
        to_sort = deepcopy(my_list)
        gap = len(to_sort) // 2
        while gap > 0:
            for i in range(gap, len(to_sort)):
                auxiliary= to_sort[i]
                j = i
                while j >= gap and cmp(key(to_sort[j - gap]), key(auxiliary)) > 0:
                    to_sort[j] = to_sort[j - gap]
                    j -= gap
                to_sort[j] = auxiliary
            gap //= 2
        if reverse == True:
            to_sort = to_sort[::-1]
        return list(to_sort)
    
class TestCaseSortingAlgorithms(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.list1 = [12, 2, 15, 16, 13, 14, 89, 100, 67]
        self.list2 = [0, 1, 2, 3, 4]
        self.list3 = [9, 8, 7, 6, 5]
        self.list4 = []
        self.list5 = [1]
        self.alg = SortingAlgorithms()
        
    def __getRandomList(self):
        new_list = []
        for index in range(500):
            new_list.append(randint(-100000, 100000))
        return new_list
        
    def testBubbleSort(self):
        self.assertSequenceEqual(self.alg.bubbleSort(self.list1), sorted(self.list1))
        self.assertSequenceEqual(self.alg.bubbleSort(self.list2), sorted(self.list2))
        self.assertSequenceEqual(self.alg.bubbleSort(self.list3), sorted(self.list3))
        self.assertSequenceEqual(self.alg.bubbleSort(self.list4), sorted(self.list4))
        self.assertSequenceEqual(self.alg.bubbleSort(self.list5), sorted(self.list5))
    
    def __myKey(self, x):
        return x * x * x - 1
    
    def testBigData(self):
        for index in range(100):
            new_list = self.__getRandomList()
            self.assertSequenceEqual(self.alg.bubbleSort(new_list), sorted(new_list))
            self.assertSequenceEqual(self.alg.shellSort(new_list), sorted(new_list))
            self.assertSequenceEqual(self.alg.bubbleSort(new_list, reverse = True), sorted(new_list, reverse = True))
            self.assertSequenceEqual(self.alg.shellSort(new_list, reverse = True), sorted(new_list, reverse = True))
            self.assertEqual(self.alg.bubbleSort(new_list, key = self.__myKey), sorted(new_list, key = self.__myKey))
            self.assertEqual(self.alg.shellSort(new_list, key = self.__myKey), sorted(new_list, key = self.__myKey))
        
    def testShellSort(self):
        self.assertSequenceEqual(self.alg.shellSort(self.list1), sorted(self.list1))
        self.assertSequenceEqual(self.alg.shellSort(self.list2), sorted(self.list2))
        self.assertSequenceEqual(self.alg.shellSort(self.list3), sorted(self.list3))
        self.assertSequenceEqual(self.alg.shellSort(self.list4), sorted(self.list4))
        self.assertSequenceEqual(self.alg.shellSort(self.list5), sorted(self.list5))
    
if __name__ == "__main__":
    unittest.main()
        