'''
Created on Nov 25, 2018

@author: Razvan
'''

class StudentMarkDTO:


    def __init__(self, mark):
        self.__student_name = mark.getStudent().getName()
        self.__mark = mark.getMark()
    
    def __str__(self):
        return self.__student_name + ", mark: " + str(self.__mark)
    
    def __eq__(self, other):
        return self.__student_name == other.__student_name and self.__mark == other.__mark
    
    def __lt__(self, other):
        if self.__student_name < other.__student_name:
            return True
        elif self.__student_name == other.__student_name and self.__mark < other.__mark:
            return True
        else:
            return False
    
    def __le__(self, other):
        return self == other or self < other
    
    def __gt__(self, other):
        return not (self <= other)
    
    def __ge__(self, other):
        return self == other or self > other
    