'''
Created on Dec 3, 2018

@author: Razvan
'''
import unittest
from Domain.StudentClass import Student
from Domain.StudentRepositoryClass import StudentInMemoryRepository
from Domain.LabProblemClass import LabProblem
from Domain.MarkClass import Mark
from Domain.MarkRepositoryClass import MarkInMemoryRepository
from BussinesLogic.LabProblemServiceClass import LabProblemService
from Domain.LabProblemValidatorClass import LabProblemValidator
from Domain.LabProblemRepositoryClass import LabProblemInMemoryRepository


class TestCaseStudentClass(unittest.TestCase):
    
    
    def setUp(self):
        self.st1 = Student("Ion Popescu", 211, 4)
        self.st2 = Student("Ana", 415, 5)
        
    def testGetName(self):
        self.assertTrue(self.st1.getName() == "Ion Popescu")
        self.assertTrue(self.st2.getName() == "An")
        
    def testGetGroup(self):
        self.assertTrue(self.st1.getGroup() == 211)
        self.assertTrue(self.st2.getGroup() == 415)
        
    def testGetId(self):
        self.assertTrue(self.st1.getId() == 4)
        self.assertTrue(self.st2.getId() == 5)
        
    def testGetInitial(self):
        self.assertTrue(self.st1.getInitial() == "I")
        self.assertTrue(self.st2.getInitial() == "A")

class TestCaseStudentRepositoryClass(unittest.TestCase):
    
    
    def setUp(self):
        self.st1 = Student("Ion", 21, 1)
        self.st2 = Student("Ana", 32, 2)
        self.st3 = Student("Mircea", 14, 3)
        self.st_repo = StudentInMemoryRepository()
        self.st_repo.addStudent(self.st1)
        self.st_repo.addStudent(self.st2)
        self.st_repo.addStudent(self.st3)
        
    def testAddStudent(self):
        self.st_repo.addStudent(Student("Danut", 22, 6))
        self.assertEqual(self.st_repo.getNumberOfStudents(), 4)
        self.st_repo.addStudent(Student("Mircea", 56, 9))
        self.assertEqual(self.st_repo.getNumberOfStudents(), 5)
        
    def testRemoveStudent(self):
        self.st_repo.removeStudent(self.st1.getId())
        self.assertEqual(self.st_repo.getNumberOfStudents(), 2)
        self.st_repo.removeStudent(self.st2.getId())
        self.assertEqual(self.st_repo.getNumberOfStudents(), 1)
        
    def testGetStudentById(self):
        self.assertEqual(self.st_repo.getStudentById(self.st1.getId()), self.st1)
        self.assertEqual(self.st_repo.getStudentById(self.st3.getId()), self.st3)

    def testUpdateStudent(self):
        new_st = Student("Marin", 3, 2)
        self.st_repo.updateStudent(new_st)
        self.assertEqual(self.st_repo.getStudentById(2).getName(), "Marin")
        new_st = Student("Ana", 32, 0)
        self.st_repo.updateStudent(new_st)
        self.assertEqual(self.st_repo.getStudentById(0).getGroup(), 32)
        

class TestCaseMarkClass(unittest.TestCase):
    
    def setUp(self):
        self.st1 = Student("ana", 211, 1)
        self.st2 = Student("mircea", 212, 2)
        self.pb1 = LabProblem("21_01", "ceva", 3)
        self.pb2 = LabProblem("01_02", "altceva", 2)
        
        self.mark1 = Mark(self.st1, self.pb1, 10)
        self.mark2 = Mark(self.st2, self.pb1, 5)
        self.mark3 = Mark(self.st2, self.pb2, 8)
        
    def testGetStudent(self):
        self.assertTrue(self.mark1.getStudent() == self.st1)
        self.assertTrue(self.mark2.getStudent() == self.st2)
        self.assertTrue(self.mark3.getStudent() == self.st2)
        
    def testGetProblem(self):
        self.assertTrue(self.mark1.getProblem() == self.pb1)
        self.assertTrue(self.mark2.getProblem() == self.pb1)
        self.assertTrue(self.mark3.getProblem() == self.pb2)
        
    def testGetMark(self):
        self.assertTrue(self.mark1.getMark() == 10)
        self.assertTrue(self.mark2.getMark() == 5)
        self.assertTrue(self.mark3.getMark() == 8)
        
    def testGetId(self):
        self.assertTrue(self.mark1.getId() == "1_21_01")
        self.assertTrue(self.mark2.getId() == "2_21_01")
        self.assertTrue(self.mark3.getId() == "2_01_02")

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
        
class TestCaseLabProblemService(unittest.TestCase):
    
    def setUp(self):
        self.pbs = LabProblemInMemoryRepository()
        self.val = LabProblemValidator()
        self.pb_service = LabProblemService(self.pbs, self.val)
        
        self.pb_service.addProblem(21, "fa ceva", 2)
        self.pb_service.addProblem(1, "nu aia", 2)
        self.pb_service.addProblem(21, "dada", 5)
        
    def testUpdateProblem(self):
        '''
            Example of BlackBox testing
        '''
        self.pb_service.updateProblem("21_01", "fa altceva", 6)
        self.assertTrue(self.pbs.getProblemByNumber("21_01").getDeadline() == 6)
        
        self.assertRaises(ValueError, self.pb_service.updateProblem, "1_2", "altceva", 5)
        self.assertRaises(ValueError, self.pb_service.updateProblem, 12, "altceva", 5)
        self.assertRaises(ValueError, self.pb_service.updateProblem, "21_01", "", 5)
        self.assertRaises(ValueError, self.pb_service.updateProblem, "21_01", "altceva", "")
        self.assertRaises(ValueError, self.pb_service.updateProblem, "123_02", "altceva", 5)
        self.assertRaises(ValueError, self.pb_service.updateProblem, "21_04", "altceva", 5)
        self.assertRaises(ValueError, self.pb_service.updateProblem, "21_02", "altceva", -5)
        
        
class TestCaseLabProblemClass(unittest.TestCase):
    
    def setUp(self):
        self.pb1 = LabProblem("02_21", "ceva", 4)
        self.pb2 = LabProblem("14_02", "altceva")
        
    def testGetNumber(self):
        self.assertTrue(self.pb1.getNumber() == "02_21")
        self.assertTrue(self.pb2.getNumber() == "14_02")
        
    def testGetDeadline(self):
        self.assertEqual(self.pb1.getDeadline(), 4)
        self.assertEqual(self.pb2.getDeadline(), 3)
        
    def testGetDescription(self):
        self.assertEqual(self.pb1.getDescription(), "ceva")
        self.assertEqual(self.pb2.getDescription(), "altceva")
        
    def testGetAvailability(self):
        self.assertEqual(self.pb1.getAvailability(), False)
        self.assertEqual(self.pb2.getAvailability(), False)
        self.pb2.setNotAvailable()
        self.assertEqual(self.pb2.getAvailability(), True)
    
    def testGetProblemNumber(self):
        self.assertEqual(self.pb1.getProblemNumber(), 21)
        self.assertEqual(self.pb2.getProblemNumber(), 2)
        
    def testGetLabNumber(self):
        self.assertEqual(self.pb1.getLabNumber(), 2)
        self.assertEqual(self.pb2.getLabNumber(), 14)

unittest.main()
