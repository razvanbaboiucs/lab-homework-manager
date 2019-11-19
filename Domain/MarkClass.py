'''
Created on Nov 18, 2018

@author: Razvan
'''
from Domain.StudentClass import Student
from Domain.LabProblemClass import LabProblem


class Mark:
    '''
        Defines a mark for a specific student, for a specific problem 
    '''

    def __init__(self, st, pb, mark):
        '''
            IN:
                st - Student
                pb - LabProblem
                mark - integer
        '''
        self.__student = st
        self.__problem = pb
        self.__mark = mark
        self.__notAvailable = False
    
    def getStudent(self):
        return self.__student
    
    def getProblem(self):
        return self.__problem
    
    def getMark(self):
        return self.__mark
    
    def getId(self):
        return str(self.__student.getId()) + "_" + str(self.__problem.getNumber())
    
    def __str__(self):
        return "Student: " + str(self.__student) + "\n" + "Problem: " + str(self.__problem) + "\n" + "Mark: " + str(self.__mark) + "\n"
    
    def getAvailability(self):
        return self.__notAvailable
    
    def setNotAvailable(self):
        self.__notAvailable = True
    
#------------------------------------------------ TESTS --------------------------------------------------------------------
        
        
def test_getStudent():
    st1 = Student("ana", 211, 1)
    st2 = Student("mircea", 212, 2)
    pb1 = LabProblem("21_01", "ceva", 3)
    pb2 = LabProblem("01_02", "altceva", 2)
    
    mark1 = Mark(st1, pb1, 10)
    mark2 = Mark(st2, pb1, 5)
    mark3 = Mark(st2, pb2, 8)
    
    assert mark1.getStudent() == st1
    assert mark2.getStudent() == st2
    assert mark3.getStudent() == st2
    

def test_getProblem():
    st1 = Student("ana", 211, 1)
    st2 = Student("mircea", 212, 2)
    pb1 = LabProblem("21_01", "ceva", 3)
    pb2 = LabProblem("01_02", "altceva", 2)
    
    mark1 = Mark(st1, pb1, 10)
    mark2 = Mark(st2, pb1, 5)
    mark3 = Mark(st2, pb2, 8)
    
    assert mark1.getProblem() == pb1
    assert mark2.getProblem() == pb1
    assert mark3.getProblem() == pb2
    

def test_getMark():
    st1 = Student("ana", 211, 1)
    st2 = Student("mircea", 212, 2)
    pb1 = LabProblem("21_01", "ceva", 3)
    pb2 = LabProblem("01_02", "altceva", 2)
    
    mark1 = Mark(st1, pb1, 10)
    mark2 = Mark(st2, pb1, 5)
    mark3 = Mark(st2, pb2, 8)
    
    assert mark1.getMark() == 10
    assert mark2.getMark() == 5
    assert mark3.getMark() == 8
    
    
def test_getId():
    st1 = Student("ana", 211, 1)
    st2 = Student("mircea", 212, 2)
    pb1 = LabProblem("21_01", "ceva", 3)
    pb2 = LabProblem("01_02", "altceva", 2)
    
    mark1 = Mark(st1, pb1, 10)
    mark2 = Mark(st2, pb1, 5)
    mark3 = Mark(st2, pb2, 8)

    assert mark1.getId() == "1_21_01"
    assert mark2.getId() == "2_21_01"
    assert mark3.getId() == "2_01_02"
    

test_getMark()
test_getProblem()
test_getStudent()
test_getId()