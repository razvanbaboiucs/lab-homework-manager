'''
Created on Nov 8, 2018

@author: Razvan
'''
from Domain.StudentClass import Student
import unittest

class StudentInMemoryRepository:
    '''
        A repository for student objects
    '''

    def __init__(self):
        '''
            Constructor
            Creates a dictionary to store students in
        '''
        self.__students = {}
    
    def __str__(self):
        
        not_registered = True
        for student_key in self.__students:
            if self.__students[student_key].getAvailability() == False:
                not_registered = False
        
        if not self.__students or not_registered:
            return "No students registered!\n"
        
        all_students = "The registered students are:\n"
        for st in self.__students:
            if self.__students[st].getAvailability() == False:
                all_students += str(self.__students[st]) + "\n"
        return all_students
    
    def addStudent(self, st):
        '''
            Adds student(value) to the repository by their id (key)
            IN:
                st - Student object
        '''
        self.__students[st.getId()] = st
    
    def removeStudent(self, st_id):
        '''
            Removes student(value) from the repository by their id
            IN:
                st_id - integer, student's id
        '''
        self.__students[st_id].setNotAvailable()
    
    def getStudentById(self, st_id):
        '''
            Returns the student with the specified id
            IN:
                st_id - natural number
        '''
        return self.__students[st_id]
    
    def getAllStudents(self):
        return dict(self.__students)
    
    def updateStudent(self, st):
        '''
            Updates the information for a specific student (by id)
            IN:
                st - Student
        '''
        self.__students[st.getId()] = st
        
    def getNumberOfStudents(self):
        '''
            Returns the number of students available in the repo
        '''
        number_of_sts = 0
        for st in self.__students:
            if self.__students[st].getAvailability() == False:
                number_of_sts += 1
        return number_of_sts
    
    
class StudentFileRepository:
    
    def __init__(self, file_name):
        #StudentInMemoryRepository.__init__(self)
        self.__f_name = file_name
        #self.__loadFromFile()
        self.__prepareFile()
        
    def __loadFromFile(self):
        '''
            Loads the file in the repo
        '''
        with open(self.__f_name) as file:
            for line in file:
                try:
                    student = self.__getStudentForLine(line)
                    StudentInMemoryRepository.addStudent(self, student)
                except ValueError:
                    pass
        with open(self.__f_name, "a") as file:
            file.write("\n")
            
    def __prepareFile(self):
        '''
            Prepares the file for working with it
        '''
        with open(self.__f_name, "a") as file:
            file.write("\n")
                
    def addStudent(self, student):
        '''
            Adds a student to the repository
            IN:
                student - Student class
        '''
        #StudentInMemoryRepository.addStudent(self,  student)
        self.__appendToFile(student)
    
    def updateStudent(self, student):
        '''
            Updates a student's information (the student with the id student.getId())
            IN:
                student - Student class
        '''
        student_to_remove = self.getStudentById(student.getId())
        #StudentInMemoryRepository.updateStudent(self, student)
        self.__removeFromFile(student_to_remove)
        self.__appendToFile(student)
    
    def removeStudent(self, st_id):
        '''
            Removes a student from the repository
            IN:
                st_id - integer
        '''
        #StudentInMemoryRepository.removeStudent(self, st_id)
        student = self.getStudentById(st_id)
        self.__removeFromFile(student)
        
    def getAllStudents(self):
        '''
            Returns a dictionary with all the students from the file, where the key is the st_id and the value is the student 
        '''
        students= {}
        with open(self.__f_name) as file:
            for line in file:
                try:
                    student = self.__getStudentForLine(line)
                    students[student.getId()] = student
                except ValueError:
                    pass
        return dict(students)
    
    def getStudentById(self, st_id):
        '''
            Returns a student with the given id
            IN:
                st_id - integer
        '''
        with open(self.__f_name) as file:
            for line in file:
                student = self.__getStudentForLine(line)
                if student.getId() == st_id:
                    return student
                
    def __getStudentForLine(self, line):
        '''
            Returns a student formed with the information from the given line
            IN:
                line - string, got from file, with the format (stId;stName;stGroup)
        '''
        st_id, name, group = line.split(";")
        st_id = int(st_id)
        group = int(group)
        student = Student(name, group, st_id)
        return student
    
    def __removeFromFile(self, student):
        '''
            Removes the line where the student given has the information
            IN:
                student - Student class
        '''
        line_to_remove = str(student.getId()) + ";" + student.getName() + ";" + str(student.getGroup()) + "\n"
        with open(self.__f_name) as file:
            lines_list = file.readlines()
        lines_list.remove(line_to_remove)
        with open(self.__f_name, "w") as file:
            file.writelines(lines_list)
                
    def __appendToFile(self, student):
        '''
            Gets a student and adds it to the file
            IN:
                student - Student class
        '''
        with open(self.__f_name, "a") as file:
            line = str(student.getId()) + ";" + student.getName() + ";" + str(student.getGroup()) + "\n"
            file.write(line)
    
    def __str__(self):
        str_to_print = ""
        with open(self.__f_name) as file:
            for line in file:
                try:
                    student = self.__getStudentForLine(line)
                    str_to_print += str(student) + "\n"
                except ValueError:
                    pass
        return str_to_print

#---------------------------------------------- TESTS -------------------------------------------------

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
        