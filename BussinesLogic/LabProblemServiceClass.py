'''
Created on Nov 16, 2018

@author: Razvan
'''
from Domain.LabProblemClass import LabProblem
from Domain.LabProblemRepositoryClass import LabProblemInMemoryRepository
from Domain.LabProblemValidatorClass import LabProblemValidator
from Domain.MarkRepositoryClass import MarkInMemoryRepository
from Domain.MarkClass import Mark
from Domain.StudentClass import Student
import random
import string



class LabProblemService:
    '''
        Deals with the lab problems' operations
    '''


    def __init__(self, pb_repository, validator, mark_repo = MarkInMemoryRepository()):
        self.__problems = pb_repository
        self.__val = validator
        self.__catalog = mark_repo
        
    def availableProblemNumber(self, lab_number):
        '''
            Returns a string with the format 'labNumber_problemNumber'
            Problem number will be generated as the next available problem number for the specified lab
            IN:
                lab_number - natural number
        '''
        if lab_number < 1 or lab_number > 99:
            raise ValueError("Attention: - the lab number should be a natural number between 1 and 99!")
        
        problem_number = ""
        if lab_number < 10:
            problem_number += "0"
        problem_number += str(lab_number) + "_01"
        
        while problem_number in self.__problems.getAllProblems():
            problem_number = list(problem_number)
            new_number = int(problem_number[3]) * 10 + int(problem_number[4]) + 1
            new_bigger = new_number // 10
            new_smaller = new_number % 10
            problem_number[3] = str(new_bigger)
            problem_number[4] = str(new_smaller)
            problem_number = "".join(problem_number)
        
        return problem_number
        
    def addProblem(self, lab_number, description, deadline):
        '''
            Adds a problem to the repository
            IN:
                lab_number - 2 digit max natural number
                description - string
                deadline - natural number, number of weeks
        '''
        problem_number = self.availableProblemNumber(lab_number)
        pb = LabProblem(problem_number, description, deadline)
        self.__val.validateProblem(pb)
        self.__problems.addProblem(pb)
        return "The problem was added...\n"
        

    def __removeMarksForProblem(self, problem_number):
        '''
            Removes all the marks with the problem problem_number
        '''
        for mark_key in self.__catalog.getAllMarks():
            stud_id, lab_id, pb_id = mark_key.split("_")
            pb_num = lab_id + "_" + pb_id
            if pb_num == problem_number:
                st = Student("", 0, stud_id)
                pb = self.getProblemByNumber(problem_number)
                mrk = Mark(st, pb, 0)
                self.__catalog.removeMark(mrk.getId())
    
    
    def removeProblem(self, problem_number):
        '''
            Removes a problem (specified by it's number) from the repository
            IN:
                problem_number - string
        '''
        self.__val.validateProblemNumber(problem_number, self.__problems)
        self.__removeMarksForProblem(problem_number)
        self.__problems.removeProblem(problem_number)
        return "The problem was removed...\n"
    

    def __updateMarkForProblem(self, pb, problem_number):
        for mark_key in self.__catalog.getAllMarks():
            stud_id, lab_id, pb_id = mark_key.split("_")
            new_problem_num = lab_id + "_" + pb_id
            if new_problem_num == problem_number:
                new_mark = Mark(self.__catalog.getMarkById(mark_key).getStudent(), pb, self.__catalog.getMarkById(mark_key).getMark())
                self.__catalog.updateMark(new_mark)
    
    
    def updateProblem(self, problem_number, description, deadline):
        '''
            Updates the information of a specified problem in the repository
            IN:
                problem_number - string, with the format labNo_problemNo
                description - string
                deadline - natural number
        '''
        self.__val.validateProblemNumber(problem_number, self.__problems)
        pb = LabProblem(problem_number, description, deadline)
        self.__val.validateProblem(pb)
        self.__updateMarkForProblem(pb, problem_number)
        self.__problems.updateProblem(pb)
        return "The problem was updated...\n"
    
    def getProblemByNumber(self, problem_number):
        '''
            Returns the problem with the specified problem_number
            IN:
                problem_number - string
        '''
        self.__val.validateProblemNumber(problem_number, self.__problems)
        return self.__problems.getProblemByNumber(problem_number)
        
    def getAllProblems(self):
        '''
            Returns all the problems as a string
        '''
        return str(self.__problems)
        
    def generateRandomProblems(self, number_of_problems):
        '''
            Generates random problems
            IN:
                number_of_problems - integer
        '''
        while number_of_problems:
            lenght_of_word = random.randint(1, 15)
            number_of_words = random.randint(1, 6)
            letters = string.ascii_letters
            description = ""
            while number_of_words:
                description += "".join(random.choice(letters) for i in range(lenght_of_word)) + " "
                number_of_words -= 1
            lab_number = random.randint(1, 99)
            deadline = random.randint(1, 10)
            try:
                self.addProblem(lab_number, description, deadline)
                number_of_problems -= 1
            except ValueError:
                pass
            
        return "Random students were generated...\n"

#--------------------------------------------------- TESTS --------------------------------------------------------------

def test_addProblem():
    pb_repo = LabProblemInMemoryRepository()
    val = LabProblemValidator()
    pb_service = LabProblemService(pb_repo, val)
    
    pb_service.addProblem(1, "ceva", 2)
    assert pb_repo.getProblemByNumber("01_01").getDescription() == "ceva"
    
    pb_service.addProblem(1, "altceva", 5)
    assert pb_repo.getProblemByNumber("01_02").getDeadline() == 5
    
    pb_service.addProblem(4, "ceva1", 2)
    assert pb_repo.getProblemByNumber("04_01").getDescription() == "ceva1"

def test_removeProblem():
    pbs = LabProblemInMemoryRepository()
    val = LabProblemValidator()
    pb_service = LabProblemService(pbs, val)
    
    pb_service.addProblem(21, "fa ceva", 2)
    pb_service.addProblem(1, "nu aia", 2)
    pb_service.addProblem(21, "dada", 5)
    
    pb_service.removeProblem("21_01")
    assert pbs.getNumberOfProblems() == 2
    
    pb_service.removeProblem("21_02")
    assert pbs.getNumberOfProblems() == 1
    
    try:
        pb_service.removeProblem("02_02")
        assert False
    except ValueError:
        assert True
    
    try:
        pb_service.removeProblem("1_22")
        assert False
    except ValueError:
        assert True
        
def test_updateProblem():
    pbs = LabProblemInMemoryRepository()
    val = LabProblemValidator()
    pb_service = LabProblemService(pbs, val)
    
    pb_service.addProblem(21, "fa ceva", 2)
    pb_service.addProblem(1, "nu aia", 2)
    pb_service.addProblem(21, "dada", 5)
    
    pb_service.updateProblem("21_01", "fa altceva", 4)
    assert pbs.getProblemByNumber("21_01").getDescription() == "fa altceva"
    assert pbs.getProblemByNumber("21_01").getDeadline() == 4
    
    pb_service.updateProblem("01_01", "da aia", 2)
    assert pbs.getProblemByNumber("01_01").getDescription() == "da aia"
    
    try:
        pb_service.updateProblem("01_02", "daa", 2)
        assert False
    except ValueError:
        assert True
    
    try:
        pb_service.updateProblem("1", "neah", 7)
        assert False
    except ValueError:
        assert True
    
def test_getProblem():
    pbs = LabProblemInMemoryRepository()
    val = LabProblemValidator()
    pb_service = LabProblemService(pbs, val)
    
    pb_service.addProblem(21, "fa ceva", 2)
    pb_service.addProblem(1, "nu aia", 2)
    pb_service.addProblem(21, "dada", 5)
    
    
    pb = pb_service.getProblemByNumber("01_01")
    assert pb.getDescription() == "nu aia"
    assert pb.getDeadline() == 2
    
    pb = pb_service.getProblemByNumber("21_01")
    assert pb.getDeadline() == 2
    
    try:
        pb = pb_service.getProblemByNumber("_2101")
        assert False
    except ValueError:
        assert True
    

def test_generateRandomProblems():
    pbs = LabProblemInMemoryRepository()
    val = LabProblemValidator()
    pb_service = LabProblemService(pbs, val)
    
    pb_service.generateRandomProblems(6)
    assert pbs.getNumberOfProblems() == 6
    
    pb_service.generateRandomProblems(5)
    assert pbs.getNumberOfProblems() == 11

test_generateRandomProblems()
test_addProblem()
test_removeProblem()
test_updateProblem()
test_getProblem()