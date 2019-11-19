'''
Created on Nov 22, 2018

@author: Razvan
'''
from Domain.MarkClass import Mark
from Domain.MarkValidatorClass import MarkValidator
from Domain.StudentClass import Student
from Domain.LabProblemClass import LabProblem
from Domain.MarkRepositoryClass import MarkInMemoryRepository
from Domain.StudentRepositoryClass import StudentInMemoryRepository
from Domain.LabProblemRepositoryClass import LabProblemInMemoryRepository

class MarkService:
    '''
        It deals with the operations regarding marks
    '''


    def __init__(self, mark_repo, st_repo, pb_repo, validator):
        self.__catalog = mark_repo
        self.__students = st_repo
        self.__problems = pb_repo
        self.__val = validator
        
    def addMark(self, st_id, problem_num, mark):
        '''
            It adds a mark for the student with st_id and the problem with problem_num
            IN:
                st_id - integer
                problem_num - string, labNo_ProblemNo
                mark - integer
        '''
        self.__val.validateIdInRepo(st_id, self.__students)
        st = self.__students.getStudentById(st_id)
        self.__val.validateProblemNumber(problem_num, self.__problems)
        pb = self.__problems.getProblemByNumber(problem_num)
        mrk = Mark(st, pb, mark)
        self.__val.validateMarkInRepo(mrk, self.__catalog)
        self.__catalog.addMark(mrk)
        return "The mark has been added... \n"
    
    def removeMark(self, st_id, pb_no):
        '''
            It removes a mark from the repository
            IN:
               st_id - integer
               pb_no - string, labNo_problemNo
        '''
        self.__val.validateIdInRepo(st_id, self.__students)
        self.__val.validateProblemNumber(pb_no, self.__problems)
        st = self.__students.getStudentById(st_id)
        pb = self.__problems.getProblemByNumber(pb_no)
        mark = Mark(st, pb, 1)
        self.__val.validateMarkId(mark.getId(), self.__catalog)
        self.__catalog.removeMark(mark.getId())
        return "The mark has been removed...\n"
    
    def updateMark(self, st_id, pb_num, mark):
        '''
            Updates the mark for a specific student 
            IN:
               st_id - integer
               pb_num - string, labNo_problemNo
               mark - integer, between 0 and 10 
        '''
        self.__val.validateIdInRepo(st_id, self.__students)
        self.__val.validateProblemNumber(pb_num, self.__problems)
        st = self.__students.getStudentById(st_id)
        pb = self.__problems.getProblemByNumber(pb_num)
        mrk = Mark(st, pb, mark)
        self.__val.validateMark(mrk)
        self.__val.validateMarkId(mrk.getId(), self.__catalog)
        self.__catalog.updateMark(mrk)
        return "The mark has been updated... \n"
    
    def getAllMarks(self):
        '''
            Returns all marks as a formated and ready_to_print state
        '''
        return str(self.__catalog)
    
    def getMark(self, st_id, pb_num):
        '''
            Returns a mark
            IN:
                st_id - integer
                pb_num - string, labNo_problemNo
        '''
        self.__val.validateIdInRepo(st_id, self.__students)
        self.__val.validateProblemNumber(pb_num, self.__problems)
        st = self.__students.getStudentById(st_id)
        pb = self.__problems.getProblemByNumber(pb_num)
        mrk = Mark(st, pb, 1)
        self.__val.validateMarkId(mrk.getId(), self.__catalog)
        return self.__catalog.getMarkById(mrk.getId())
        
        
#---------------------------------------- TESTS --------------------------------------------------------


def test_addMark():
    val = MarkValidator()
    mrk_repo = MarkInMemoryRepository()
    st_repo = StudentInMemoryRepository()
    pb_repo = LabProblemInMemoryRepository()
    
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    st_repo.addStudent(st1)
    st_repo.addStudent(st2)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    pb3 = LabProblem("01_02", "ma rog", 2)
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    mark_service = MarkService(mrk_repo, st_repo, pb_repo, val)
    
    mark_service.addMark(0, "01_01", 10)
    assert mrk_repo.getNumberOfMarks() == 1
    
    mark_service.addMark(0, "06_10", 6)
    assert mrk_repo.getNumberOfMarks() == 2
    
    mark_service.addMark(1, "01_01", 8)
    assert mrk_repo.getNumberOfMarks() == 3
    
    try:
        mark_service.addMark(0, "01_06", 10)
        assert False
    except ValueError:
        assert True
        
    try:
        mark_service.addMark(0, "01_02", 5)
        assert False
    except ValueError:
        assert True
        
    
def test_removeMark():
    val = MarkValidator()
    mrk_repo = MarkInMemoryRepository()
    st_repo = StudentInMemoryRepository()
    pb_repo = LabProblemInMemoryRepository()
    
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    st_repo.addStudent(st1)
    st_repo.addStudent(st2)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    pb3 = LabProblem("01_02", "ma rog", 2)
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    mark_service = MarkService(mrk_repo, st_repo, pb_repo, val)
    
    mark_service.addMark(0, "01_01", 10)
    mark_service.addMark(0, "06_10", 6)
    mark_service.addMark(1, "01_01", 8)
    
    mark_service.removeMark(0, "01_01")
    assert mrk_repo.getNumberOfMarks() == 2
    
    mark_service.removeMark(1, "01_01")
    assert mrk_repo.getNumberOfMarks() == 1
    
    try:
        mark_service.removeMark(0, "01_01")
        assert False
    except ValueError:
        assert True
        
def test_updateMark():
    val = MarkValidator()
    mrk_repo = MarkInMemoryRepository()
    st_repo = StudentInMemoryRepository()
    pb_repo = LabProblemInMemoryRepository()
    
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    st_repo.addStudent(st1)
    st_repo.addStudent(st2)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    pb3 = LabProblem("01_02", "ma rog", 2)
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    mark_service = MarkService(mrk_repo, st_repo, pb_repo, val)
    
    mark_service.addMark(0, "01_01", 10)
    mark_service.addMark(0, "06_10", 6)
    mark_service.addMark(1, "01_01", 8)
    
    mark_service.updateMark(0, "01_01", 9)
    assert mrk_repo.getMarkById("0_01_01").getMark() == 9
    
    mark_service.updateMark(1, "01_01", 5)
    assert mrk_repo.getMarkById("1_01_01").getMark() == 5
    
    try:
        mark_service.updateMark(1, "06_10", 8)
        assert False
    except ValueError:
        assert True
        
    try:
        mark_service.updateMark(0, "01_01", 9.5)
        assert False
    except ValueError:
        assert True
        
        
def test_getMark():
    val = MarkValidator()
    mrk_repo = MarkInMemoryRepository()
    st_repo = StudentInMemoryRepository()
    pb_repo = LabProblemInMemoryRepository()
    
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    st_repo.addStudent(st1)
    st_repo.addStudent(st2)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    pb3 = LabProblem("01_02", "ma rog", 2)
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    mark_service = MarkService(mrk_repo, st_repo, pb_repo, val)
    
    mark_service.addMark(0, "01_01", 10)
    mark_service.addMark(0, "06_10", 6)
    mark_service.addMark(1, "01_01", 8)
    
    assert mark_service.getMark(0, "01_01").getMark() == 10
    assert mark_service.getMark(1, "01_01").getStudent() == st2
    
    try:
        mark_service.getMark(1, "06_10")
        assert False
    except ValueError:
        assert True
    

test_getMark()
test_updateMark()
test_addMark()
test_removeMark()