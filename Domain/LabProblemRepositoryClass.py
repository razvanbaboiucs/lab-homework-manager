'''
Created on Nov 10, 2018

@author: Razvan
'''
from Domain.LabProblemClass import LabProblem
        
class LabProblemInMemoryRepository:
    '''
        A repository for LabProblem objects
    '''
    
    def __init__(self):
        '''
            Constructor
            Creates a dictionary for lab problems
        '''
        self.__problems = {}
        
    def __str__(self):
        not_registered = True
        for problem_key in self.__problems:
            if self.__problems[problem_key].getAvailability() == False:
                not_registered = False
                
        if not self.__problems or not_registered:
            return "No problems added!\n"
        
        all_problems = "Problems added: \n\n"
        for pb in self.getAllProblems():
            if self.__problems[pb].getAvailability() == False:
                all_problems += str(self.__problems[pb]) + "\n" + "-" * 10 + "\n"
        return all_problems
    
    def addProblem(self, pb):
        '''
            Adds a problem pb to the repository
            IN:
                pb - LabProblem object
        '''
        self.__problems[pb.getNumber()] = pb
    
    def removeProblem(self, pb_number):
        '''
            Removes a problem (specified by it's number) from the repository
            IN:
                pb_number - string
        '''
        self.__problems[pb_number].setNotAvailable()
        
    def getAllProblems(self):
        return dict(self.__problems)
    
    def getProblemByNumber(self, pb_number):
        '''
            Returns the problem with pb_number
            IN:
                pb_number - string
        '''
        return self.__problems[pb_number]
    
    def updateProblem(self, pb):
        '''
            Updates the information of a specific problem in the repository (identified by pb_number)
            IN:
                pb_number - string
                pb_description - string
                pb_deadline - integer
        '''
        self.__problems[pb.getNumber()] = pb
        
    def getNumberOfProblems(self):
        '''
            Returns the number of problems still available in the repository
        '''
        number_of_problems = 0
        for pb in self.__problems:
            if self.__problems[pb].getAvailability() == False:
                number_of_problems += 1
        return number_of_problems
    
    
class LabProblemFileRepository(LabProblemInMemoryRepository):
    
    def __init__(self, file_name):
        LabProblemInMemoryRepository.__init__(self)
        self.__f_name = file_name
        self.__loadFromFile()
        #self.__prepareFile()
        
    def __loadFromFile(self):
        with open(self.__f_name) as file:
            for line in file:
                try:
                    num_problem, description, deadline = line.split(";")
                    deadline = int(deadline)
                    problem = LabProblem(num_problem, description, deadline)
                    LabProblemInMemoryRepository.addProblem(self, problem)
                except ValueError:
                    pass
        with open(self.__f_name, "a") as file:
            file.write("\n")
            
    def __prepareFile(self):
        with open(self.__f_name, "a") as file:
            file.write("\n")
                   
    def removeProblem(self, pb_number):
        LabProblemInMemoryRepository.removeProblem(self, pb_number)
        problem = self.getProblemByNumber(pb_number)
        self.__removeFromFile(problem)
        
    def __removeFromFile(self, problem):
        line_to_remove = problem.getNumber() + ";" + problem.getDescription() + ";" + str(problem.getDeadline()) + "\n"
        with open(self.__f_name) as file:
            lines_list = file.readlines()
        lines_list.remove(line_to_remove)
        with open(self.__f_name, "w") as file:
            file.writelines(lines_list)
                
    def updateProblem(self, problem):
        pb_to_remove = self.getProblemByNumber(problem.getNumber())
        LabProblemInMemoryRepository.updateProblem(self, problem)
        self.__removeFromFile(pb_to_remove)
        self.__appendToFile(problem)
        
        
    def addProblem(self, pb):
        LabProblemInMemoryRepository.addProblem(self, pb)
        self.__appendToFile(pb)
        
                
    def __appendToFile(self, problem):
        with open(self.__f_name, "a") as file:
            line = problem.getNumber() + ";" + problem.getDescription() + ";" + str(problem.getDeadline()) + "\n"
            file.write(line)
        
    
        
#-------------------------------------------- TESTS ------------------------------------------------------- 

        
def test_addProblem():
    pb1 = LabProblem("01_02", "ceva", 2)
    pb2 = LabProblem("00_33", "ceva2", 4)
    pb3 = LabProblem("22_04", "ceva3")
    pb_repo = LabProblemInMemoryRepository()
    
    pb_repo.addProblem(pb1)
    assert pb_repo.getNumberOfProblems() == 1
    
    pb_repo.addProblem(pb2)
    assert pb_repo.getNumberOfProblems() == 2
    
    pb_repo.addProblem(pb3)
    assert pb_repo.getNumberOfProblems() == 3
    

def test_removeProblem():
    pb1 = LabProblem("01_02", "ceva", 2)
    pb2 = LabProblem("00_33", "ceva2", 4)
    pb3 = LabProblem("22_04", "ceva3")
    pb_repo = LabProblemInMemoryRepository()
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    pb_repo.removeProblem("01_02")
    assert pb_repo.getNumberOfProblems() == 2
    
    pb_repo.removeProblem(pb3.getNumber())
    assert pb_repo.getNumberOfProblems() == 1
    

def test_getProblemByNumber():
    pb1 = LabProblem("01_02", "ceva", 2)
    pb2 = LabProblem("00_33", "ceva2", 4)
    pb3 = LabProblem("22_04", "ceva3")
    pb_repo = LabProblemInMemoryRepository()
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    pb4 = pb_repo.getProblemByNumber("01_02")
    assert pb4 == pb1
    
    pb4 = pb_repo.getProblemByNumber(pb2.getNumber())
    assert pb4 == pb2

def test_updateProblem():
    pb1 = LabProblem("01_02", "ceva", 2)
    pb2 = LabProblem("00_33", "ceva2", 4)
    pb3 = LabProblem("22_04", "ceva3")
    pb_repo = LabProblemInMemoryRepository()
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    new_pb = LabProblem("01_02", "altceva", 1)
    pb_repo.updateProblem(new_pb)
    assert pb_repo.getProblemByNumber("01_02").getDescription() == "altceva"
    assert pb_repo.getProblemByNumber("01_02").getDeadline() == 1
    
    new_pb = LabProblem(pb2.getNumber(), pb3.getDescription())
    pb_repo.updateProblem(new_pb)
    assert pb_repo.getProblemByNumber("00_33").getDescription() == "ceva3"
    assert pb_repo.getProblemByNumber("00_33").getDeadline() == 3
    

test_getProblemByNumber()
test_addProblem()        
test_removeProblem()
test_updateProblem()