'''
Created on Nov 26, 2018

@author: Razvan
'''

class StudentProblemsDTO:
    '''
        A DTO for a student and the number of problems of that student
    '''


    def __init__(self, st_id, name, number_of_problems):
        '''
            IN:
                st_id - integer
                name - string
                number_of_problems - integer
        '''
        self.__id = st_id
        self.__name = name
        self.__number_of_problems = number_of_problems
    
    def __str__(self):
        return "ID: " + str(self.__id) + ", " + self.__name + ", number of problems:" + str(self.__number_of_problems) + "\n"
    
    def __eq__(self, other):
        return self.__id == other.__id and self.__name == other.__name and self.__number_of_problems == other.__number_of_problems
    
