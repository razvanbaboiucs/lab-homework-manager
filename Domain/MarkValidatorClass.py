'''
Created on Nov 22, 2018

@author: Razvan
'''
from Domain.MarkClass import Mark
from Domain.LabProblemClass import LabProblem
from Domain.StudentClass import Student
from Domain.MarkRepositoryClass import MarkInMemoryRepository
from Domain.LabProblemValidatorClass import LabProblemValidator
from Domain.StudentValidatorClass import StudentValidator

class MarkValidator(LabProblemValidator, StudentValidator):
    '''
        Class that validates data for mark and mark repository data
    '''
    
    def validateMark(self, mark):
        error = "Attention: "
        if type(mark.getMark()) is not int or not (mark.getMark() >= 0 and mark.getMark() <= 10):
            error += "- the mark should be a natural number between 0 and 10!\n"
        
        if error != "Attention: ":
            raise ValueError(error)
    
    def validateMarkInRepo(self, mark, mark_repo):
        error = "Attention: "
        if type(mark.getMark()) is not int or not (mark.getMark() >= 0 and mark.getMark() <= 10):
            error += "- the mark should be a natural number between 0 and 10!\n"
            
        for mrk_key in mark_repo.getAllMarks():
            if mark.getStudent().getId() == mark_repo.getMarkById(mrk_key).getStudent().getId() and mark.getProblem().getLabNumber() == mark_repo.getMarkById(mrk_key).getProblem().getLabNumber():
                error += "- the student already has a problem marked for the specified lab!\n"
                break
                
        if error != "Attention: ":
            raise ValueError(error)
    
    def validateMarkId(self, mark_id, mark_repo):
        if mark_id not in mark_repo.getAllMarks() or mark_repo.getMarkById(mark_id).getAvailability() == True:
            raise ValueError("Attention: - the given mark_id is not registered!\n")
        
        
#--------------------------------------------------------- TESTS --------------------------------------------------------------

def test_validateMark():
    val = MarkValidator()
    
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    
    mrk = Mark(st1, pb1, 11)
    try:
        val.validateMark(mrk)
        assert False
    except ValueError:
        assert True
        
    mrk = Mark(st2, pb2, 6.5)
    try:
        val.validateMark(mrk)
        assert False
    except ValueError:
        assert True
        
    mrk = Mark(st2, pb2, "10")
    try:
        val.validateMark(mrk)
        assert False
    except ValueError:
        assert True
        
def test_validateMarkInRepo():
    val = MarkValidator()
    
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    pb3 = LabProblem("06_11", "dada", 2)
    
    mrk_repo = MarkInMemoryRepository()
    
    mrk1 = Mark(st1, pb1, 10)
    mrk_repo.addMark(mrk1)
    mrk2 = Mark(st1, pb2, 6)
    mrk_repo.addMark(mrk2)
    mrk3 = Mark(st2, pb2, 9)
    mrk_repo.addMark(mrk3)
    
    mrk = Mark(st1, pb1, 6)
    try:
        val.validateMarkInRepo(mrk, mrk_repo)
        assert False
    except ValueError:
        assert True
    
    mrk = Mark(st1, pb3, 10)
    try:
        val.validateMarkInRepo(mrk, mrk_repo)
        assert False
    except ValueError:
        assert True
    

def test_validateMarkId():
    val = MarkValidator()
    
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    
    mrk_repo = MarkInMemoryRepository()
    
    mrk1 = Mark(st1, pb1, 10)
    mrk_repo.addMark(mrk1)
    mrk2 = Mark(st1, pb2, 6)
    mrk_repo.addMark(mrk2)
    mrk3 = Mark(st2, pb2, 9)
    mrk_repo.addMark(mrk3)
    
    try:
        val.validateMarkId("2_01_01", mrk_repo)
        assert False
    except ValueError:
        assert True
        
    try:
        val.validateMarkId("0_01_01", mrk_repo)
        assert True
    except ValueError:
        assert False
         

test_validateMark()
test_validateMarkId()
test_validateMarkInRepo() 