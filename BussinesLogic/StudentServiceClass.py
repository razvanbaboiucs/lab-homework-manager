'''
Created on Nov 16, 2018

@author: Razvan
'''
from Domain.StudentClass import Student
from Domain.StudentRepositoryClass import StudentInMemoryRepository
from Domain.StudentValidatorClass import StudentValidator
import random, string
from Domain.LabProblemClass import LabProblem
from Domain.MarkClass import Mark
from Domain.MarkRepositoryClass import MarkInMemoryRepository


class StudentService:
    '''
        Deals with the operations on student's repository
    '''


    def __init__(self, st_repository, validator, mark_repo = MarkInMemoryRepository()):
        self.__students = st_repository
        self.__val = validator
        self.__catalog = mark_repo
        
    def getAvailableId(self):
        '''
            Returns the first available id (not already in use)
        '''
        new_id = 0
        while new_id in self.__students.getAllStudents():
            new_id += 1
        return new_id
    
    def addStudent(self, name, group):
        '''
            Creates a student and adds it to the students (student repository)
            IN:
                name - string
                group - integer 
        '''
        st_id = self.getAvailableId()
        st = Student(name, group, st_id)
        self.__val.validateStudent(st)
        self.__students.addStudent(st)
        return "The student was added...\n"
    

    def __removeMarksForStudent(self, st_id):
        '''
            Removes all the marks for the student with st_id
            IN:
                st_id - integer
        '''
        for mark_key in self.__catalog.getAllMarks():
            stud_id, lab_id, pb_id = mark_key.split("_")
            if int(stud_id) == st_id:
                problem_number = lab_id + "_" + pb_id
                st = self.getStudentById(st_id)
                pb = LabProblem(problem_number, "", 0)
                mrk = Mark(st, pb, 0)
                self.__catalog.removeMark(mrk.getId())
    
    
    def removeStudent(self, st_id):
        '''
            Removes the student with the specified id, name and group
            IN:
                st_id - integer
        '''
        self.__val.validateIdInRepo(st_id, self.__students)
        self.__removeMarksForStudent(st_id)    
        self.__students.removeStudent(st_id)
        return "The students was removed...\n"
        
    def getStudentById(self, st_id):
        '''
            Returns a student with the st_id
            IN:
                student_id - integer, student's id
        '''
        self.__val.validateIdInRepo(st_id, self.__students)
        return self.__students.getStudentById(st_id)
    

    def __updateMarksForStudent(self, st, st_id):
        for mark_key in self.__catalog.getAllMarks():
            stud_id, lab_id, pb_id = mark_key.split("_")
            if int(stud_id) == st_id:
                new_mark = Mark(st, self.__catalog.getMarkById(mark_key).getProblem(), self.__catalog.getMarkById(mark_key).getMark())
                self.__catalog.updateMark(new_mark)
    
    
    def updateStudent(self, st_id, name, group):
        '''
            Updates the information of a specific student from students
            Returns all the students in students
            IN:
                st_id - integer
                name - string
                group - integer
        '''
        self.__val.validateIdInRepo(st_id, self.__students)
        st = Student(name, group, st_id)
        self.__val.validateStudent(st)
        self.__updateMarksForStudent(st, st_id)
        self.__students.updateStudent(st)
        return "The student was updated...\n"
    
    def getAllStudents(self):
        '''
            Returns all the students as a string to print
        '''
        return str(self.__students)
    
    def generateRandomStudents(self, number_of_students):
        '''
            Generates a given number of students and adds them to the repository
            IN:
                number_of_students - a natural number
        '''
        while number_of_students:
            lenght_of_name = random.randint(1, 25)
            letters = string.ascii_letters
            name = "".join(random.choice(letters) for i in range(lenght_of_name))
            group = random.randint(-1001, 1001)
            try:
                self.addStudent(name, group)
                number_of_students -= 1
            except ValueError:
                pass
            
        return "Random students were generated...\n"
            
#--------------------------------------- TESTS -----------------------------------------------------


def test_addStudent():
    sts = StudentInMemoryRepository()
    val = StudentValidator()
    st_service = StudentService(sts, val)
    
    st_service.addStudent("Ana", 211)
    assert len(sts.getAllStudents()) == 1
    
    st_service.addStudent("Cami", 2)
    assert len(sts.getAllStudents()) == 2
    
    
def test_removeStudent():
    sts = StudentInMemoryRepository()
    val = StudentValidator()
    st_service = StudentService(sts, val)
    
    st_service.addStudent("Cami", 2)
    st_service.addStudent("Ana", 211)
    st_service.addStudent("Ioana", 214)
    
    st_service.removeStudent(0)
    assert sts.getNumberOfStudents() == 2
    
    st_service.removeStudent(2)
    assert sts.getNumberOfStudents() == 1
    
    try:
        st_service.removeStudent(0)
        assert False
    except ValueError:
        assert True
    

def test_updateStudent():
    sts = StudentInMemoryRepository()
    val = StudentValidator()
    st_service = StudentService(sts, val)
    
    st_service.addStudent("Cami", 2)
    st_service.addStudent("Ana", 211)
    st_service.addStudent("Ioana", 214)
    
    st_service.updateStudent(0, "Ciocarlia", 44)
    assert sts.getStudentById(0).getName() == "Ciocarlia"
    
    st_service.updateStudent(2, "Madona", 0)
    assert sts.getStudentById(2).getGroup() == 0
    
    try:
        st_service.updateStudent(1, "12", "56")
        assert False
    except ValueError:
        assert True
        
    try:
        st_service.updateStudent(3, "mn", 55)
        assert False
    except ValueError:
        assert True
        

def test_getStudentById():
    sts = StudentInMemoryRepository()
    val = StudentValidator()
    st_service = StudentService(sts, val)
    
    st_service.addStudent("Cami", 2)
    st_service.addStudent("Ana", 211)
    st_service.addStudent("Ioana", 214)
    
    st = st_service.getStudentById(1)
    assert st.getName() == "Ana"
    assert st.getGroup() == 211
    
    st = st_service.getStudentById(0)
    assert st.getGroup() == 2
    
def test_generateRandomStudents():
    sts = StudentInMemoryRepository()
    val = StudentValidator()
    st_service = StudentService(sts, val)
    st_service.generateRandomStudents(10)
    assert len(sts.getAllStudents()) == 10
    
    st_service.generateRandomStudents(4)
    assert len(sts.getAllStudents()) == 14
    
test_addStudent()
test_getStudentById()
test_removeStudent()
test_updateStudent()
test_generateRandomStudents()