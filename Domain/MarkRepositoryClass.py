'''
Created on Nov 18, 2018

@author: Razvan
'''
from Domain.MarkClass import Mark
from builtins import str
from Domain.StudentClass import Student
from Domain.LabProblemClass import LabProblem
import unittest

class MarkInMemoryRepository:
    '''
        It defines the repository for marks (a catalog)
    '''

    def __init__(self):
        self.__catalog = {}
        
        
    def addMark(self, mrk):
        '''
            Adds a mark to the repository
            Creates a unique key for the mark and stores the value in the catalog
            IN:
                mrk - mark
        '''
        self.__catalog[mrk.getId()] = mrk
    
    def removeMark(self, mrk_id):
        '''
            Removes the mark from a given student and from a specific problem 
            IN:
               mrk_id - string
        '''
        self.__catalog[mrk_id].setNotAvailable()
        
    def updateMark(self, new_mark):
        '''
            Updates the mark for a given student for a specific problem
            IN:
                new_mark - markClass
                
        '''
        self.__catalog[new_mark.getId()] = new_mark
        
        
    def getMarkById(self, mrk_id):
        '''
            Returns the mark for a specific student and a specific problem
            IN:
                mrk_id - string
        '''
        return self.__catalog[mrk_id]
    
    def getAllMarks(self):
        '''
            Returns all the marks from all students and all problems
        '''
        return dict(self.__catalog)
    
    def __str__(self):
        not_registered = True
        for mark_key in self.__catalog:
            if self.__catalog[mark_key].getAvailability() == False:
                not_registered = False
        if not self.__catalog or not_registered:
            return "No marks added!\n"
        mrk_str = ""
        for mrk_key in self.__catalog:
            if self.__catalog[mrk_key].getAvailability() == False:
                mrk_str += str(self.__catalog[mrk_key]) + "-" * 15 + "\n"
        return mrk_str
    
    def getNumberOfMarks(self):
        '''
            Returns the number of marks available in the catalog (repository)
        '''
        number_of_marks = 0
        for mrk_key in self.__catalog:
            if self.__catalog[mrk_key].getAvailability() == False:
                number_of_marks += 1
        return number_of_marks
    
class MarkFileRepository(MarkInMemoryRepository):
    
    def __init__(self, file_name, student_repo, problem_repo):
        MarkInMemoryRepository.__init__(self)
        self.__f_name = file_name
        self.__students = student_repo
        self.__problems = problem_repo
        self.__loadFromFile()
        
    def __loadFromFile(self):
        '''
            Loads the file information in the repo
        '''
        with open(self.__f_name) as file:
            for line in file:
                try:
                    st_id, pb_num, grade = line.split(";")
                    st_id = int(st_id)
                    grade = int(grade)
                    student = self.__students.getStudentById(st_id)
                    problem = self.__problems.getProblemByNumber(pb_num)
                    mark = Mark(student, problem, grade)
                    MarkInMemoryRepository.addMark(self, mark)
                except ValueError:
                    pass
                except KeyError:
                    pass
        with open(self.__f_name, "a") as file:
            file.write("\n")
    
    def addMark(self, mark):
        '''
            Adds the mark in the repository
            IN:
                mark - Mark Class
        '''
        MarkInMemoryRepository.addMark(self, mark)
        self.__appendToFile(mark)
        
    def removeMark(self, mrk_id):
        MarkInMemoryRepository.removeMark(self, mrk_id)
        mark = self.getMarkById(mrk_id)
        self.__removeFromFile(mark)
    
    def updateMark(self, new_mark):
        mark_to_remove = self.getMarkById(new_mark.getId())
        MarkInMemoryRepository.updateMark(self, new_mark)
        self.__removeFromFile(mark_to_remove)
        self.__appendToFile(new_mark)
        
    
    def __appendToFile(self, mark):
        with open(self.__f_name, "a") as file:
            line = str(mark.getStudent().getId()) + ";" + str(mark.getProblem().getNumber()) + ";" + str(mark.getMark()) + "\n"
            file.write(line)
        
    def __removeFromFile(self, mark):
        line_to_remove = str(mark.getStudent().getId()) + ";" + str(mark.getProblem().getNumber()) + ";" + str(mark.getMark()) + "\n"
        with open(self.__f_name) as file:
            lines_list = file.readlines()
        lines_list.remove(line_to_remove)
        with open(self.__f_name, "w") as file:
            file.writelines(lines_list)
        
    
#----------------------------------------------------- TESTS -----------------------------------------------------------


class TestCaseMarkRepositoryClass(unittest.TestCase):
    
    def setUp(self):
        st1 = Student("Ana", 21, 0)
        st2 = Student("Ion", 14, 1)
        
        pb1 = LabProblem("01_01", "fa ceva", 3)
        pb2 = LabProblem("06_10", "altceva", 5)
        
        self.mrk_repo = MarkInMemoryRepository()
        
        self. mrk1 = Mark(st1, pb1, 10)
        self.mrk_repo.addMark(self.mrk1)
        self.mrk2 = Mark(st1, pb2, 6)
        self.mrk_repo.addMark(self.mrk2)
        self.mrk3 = Mark(st2, pb2, 9)
        self.mrk_repo.addMark(self.mrk3)
        
    def testAddMark(self):
        self.mrk_repo.addMark(Mark(Student("Ceva", 22, 9), LabProblem("05_07", "dada", 6), 2))
        self.assertTrue(self.mrk_repo.getNumberOfMarks() == 4)
        self.mrk_repo.addMark(Mark(Student("Ceva", 22, 7), LabProblem("08_07", "dada", 6), 6))
        self.assertTrue(self.mrk_repo.getNumberOfMarks() == 5)
        
    def testRemoveMark(self):
        self.mrk_repo.removeMark(self.mrk1.getId())
        self.assertTrue(self.mrk_repo.getNumberOfMarks() == 2)
        self.mrk_repo.removeMark(self.mrk2.getId())
        self.assertTrue(self.mrk_repo.getNumberOfMarks() == 1)
        
    def testGetMarkById(self):
        self.assertTrue(self.mrk_repo.getMarkById(self.mrk1.getId()).getMark() == 10)
        self.assertTrue(self.mrk_repo.getMarkById(self.mrk2.getId()).getStudent() == Student("Ana", 21, 0))

    
    def testUpdateMark(self):
        mrk_new = Mark(Student("Ana", 21, 0), LabProblem("01_01", "fa ceva", 3), 7)
        self.mrk_repo.updateMark(mrk_new)
        self.assertTrue(self.mrk_repo.getMarkById(mrk_new.getId()).getMark() == 7)
        mrk_new = Mark(Student("Ion", 14, 1), LabProblem("06_10", "altceva", 5), 9)
        self.mrk_repo.updateMark(mrk_new)
        self.assertTrue(self.mrk_repo.getMarkById(mrk_new.getId()).getMark() == 9)
        
    
def test_addMark():
    st1 = Student("Ana", 21, 0)
    st2 = Student("Ion", 14, 1)
    
    pb1 = LabProblem("01_01", "fa ceva", 3)
    pb2 = LabProblem("06_10", "altceva", 5)
    
    mrk_repo = MarkInMemoryRepository()
    
    mrk = Mark(st1, pb1, 10)
    mrk_repo.addMark(mrk)
    assert mrk_repo.getNumberOfMarks() == 1
    
    mrk = Mark(st1, pb2, 6)
    mrk_repo.addMark(mrk)
    assert mrk_repo.getNumberOfMarks() == 2
    
    mrk = Mark(st2, pb2, 9)
    mrk_repo.addMark(mrk)
    assert mrk_repo.getNumberOfMarks() == 3

def test_removeMark():
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
    
    mrk_repo.removeMark(mrk1.getId())
    assert mrk_repo.getNumberOfMarks() == 2
    
    mrk_repo.removeMark(mrk2.getId())
    assert mrk_repo.getNumberOfMarks() == 1
    
    mrk_repo.removeMark(mrk2.getId())
    assert mrk_repo.getNumberOfMarks() == 1
    

def test_updateMark():
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
    
    mrk_new = Mark(st1, pb1, 7)
    mrk_repo.updateMark(mrk_new)
    assert mrk_repo.getMarkById(mrk_new.getId()).getMark() == 7
    
    mrk_new = Mark(st2, pb2, 9)
    mrk_repo.updateMark(mrk_new)
    assert mrk_repo.getMarkById(mrk_new.getId()).getMark() == 9
    
    mrk_new = Mark(st1, pb2, 8)
    mrk_repo.updateMark(mrk_new)
    assert mrk_repo.getMarkById(mrk_new.getId()).getMark() == 8
    
    mrk_new = Mark(st1, pb1, 5)
    mrk_repo.updateMark(mrk_new)
    assert mrk_repo.getMarkById(mrk_new.getId()).getMark() == 5
    

def test_getMarkById():
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
    
    assert mrk_repo.getMarkById(mrk1.getId()).getMark() == 10
    assert mrk_repo.getMarkById(mrk2.getId()).getStudent() == st1


test_addMark()
test_getMarkById()
test_removeMark()
test_updateMark()