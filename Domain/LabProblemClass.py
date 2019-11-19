'''
Created on Nov 9, 2018

@author: Razvan
'''
import unittest

class LabProblem:
    '''
        Defines a lab problem
    '''

    def __init__(self, number, description, deadline = 3):
        '''
            Constructor
            Gives a problem the given description and a deadline
            IN:
                description - string, containing the problem's request
                deadline - integer, representing the number of weeks in which the student
                    is allowed to finish the problem
                         - if not given, it will be automatically set to 3 weeks
                number - string, composed of two parts: lab number _ problem number
        '''
        self.__number = number
        self.__description = description
        self.__deadline = deadline
        self.__notAvailable = False
    
    def __str__(self):
        return "Problem no." + self.__number + "\nDescription: " + self.__description + "\nDeadline: " + str(self.__deadline) + " weeks"
    
    def getNumber(self):
        return str(self.__number)
    
    def getLabNumber(self):
        lab_num, problem_num = self.__number.split("_")
        return int(lab_num)
    
    def getProblemNumber(self):
        lab_num, problem_num = self.__number.split("_")
        return int(problem_num)
    
    def getDescription(self):
        return str(self.__description)
    
    def getDeadline(self):
        return int(self.__deadline)
    
    def __eq__(self, other):
        return self.__description == other.__description
    
    def getAvailability(self):
        return self.__notAvailable
    
    def setNotAvailable(self):
        self.__notAvailable = True
    

#----------------------------------------------------- TESTS --------------------------------------------------------



def test_getNumber():
    pb1 = LabProblem("02_21", "ceva", 4)
    pb2 = LabProblem("14_02", "altceva")
    
    assert pb1.getNumber() == "02_21"
    assert pb2.getNumber() == "14_02"
    
def test_getDeadline():
    pb1 = LabProblem("02_21", "ceva", 4)
    pb2 = LabProblem("14_02", "altceva")
    
    assert pb1.getDeadline() == 4
    assert pb2.getDeadline() == 3

def test_getDescription():
    pb1 = LabProblem("02_21", "ceva", 4)
    pb2 = LabProblem("14_02", "altceva")
    
    assert pb1.getDescription() == "ceva"
    assert pb2.getDescription() == "altceva"
    
def test_getLabNumber():
    pb1 = LabProblem("02_21", "ceva", 4)
    pb2 = LabProblem("14_02", "altceva")
    
    assert pb1.getLabNumber() == 2
    assert pb2.getLabNumber() == 14
    
def test_getProblemNumber():
    pb1 = LabProblem("02_21", "ceva", 4)
    pb2 = LabProblem("14_02", "altceva")
    
    assert pb1.getProblemNumber() == 21
    assert pb2.getProblemNumber() == 2

test_getNumber()
test_getDeadline()
test_getDescription()   
test_getLabNumber()
test_getProblemNumber()