'''
Created on Nov 8, 2018

@author: Razvan
'''
import unittest


class Student:
    '''
        Defines a student object 
    '''
    
    def __init__(self, name, group, st_id):
        '''
            Constructor
            Gives the student a given name and group and creates an id, which is set to -1
            IN:
                name - string, representing the name of the student
                group - integer, representing the number of the student's group
                st_id - integer, representing the student's id
        '''
        self.__name = name
        self.__group = group
        self.__id = st_id
        self.__notAvailable = False
    
    def __str__(self):
        return "Id: " + str(self.__id) + ", " + str(self.__name) + ", gr. " + str(self.__group)
    
    def getName(self):
        return self.__name
    
    def getInitial(self):
        return self.__name[0]
    
    def getGroup(self):
        return self.__group
    
    def getId(self):
        return self.__id
    
    def __eq__(self, other):
        return self.__id == other.__id   
    
    def getAvailability(self):
        return self.__notAvailable 
    
    def setNotAvailable(self):
        self.__notAvailable = True
    
    
#------------------------------------- TESTS --------------------------------------------------


class TestCaseStudentClass(unittest.TestCase):
    
    
    def setUp(self):
        self.st1 = Student("Ion Popescu", 211, 4)
        self.st2 = Student("Ana", 415, 5)
        
    def testGetName(self):
        self.assertTrue(self.st1.getName() == "Ion Popescu")
        self.assertTrue(self.st2.getName() == "Ana")
        
    def testGetGroup(self):
        self.assertTrue(self.st1.getGroup() == 211)
        self.assertTrue(self.st2.getGroup() == 415)
        
    def testGetId(self):
        self.assertTrue(self.st1.getId() == 4)
        self.assertTrue(self.st2.getId() == 5)
        
    def testGetInitial(self):
        self.assertTrue(self.st1.getInitial() == "I")
        self.assertTrue(self.st2.getInitial() == "A")