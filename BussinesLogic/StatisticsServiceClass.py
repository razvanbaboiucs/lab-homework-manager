'''
Created on Nov 25, 2018

@author: Razvan
'''
from Domain.StudentMarkDTOClass import StudentMarkDTO
from Domain.MarkClass import Mark
from Domain.LabProblemClass import LabProblem
from Domain.StudentRepositoryClass import StudentInMemoryRepository
from Domain.LabProblemRepositoryClass import LabProblemInMemoryRepository
from Domain.MarkRepositoryClass import MarkInMemoryRepository
from Domain.LabProblemValidatorClass import LabProblemValidator
from Domain.StudentClass import Student
from Domain.StudentProblemsDTOClass import StudentProblemsDTO
from BussinesLogic.SortAlgorithmsClass import SortingAlgorithms

class StatisticsService:
    '''
        Works and does statistics for the marks, problems and students added
    '''

    def __init__(self, st_repo, pb_repo, mark_repo, problem_val):
        self.__students = st_repo
        self.__problems = pb_repo
        self.__marks = mark_repo
        self.__problem_val = problem_val
        
    def __getListOfStudentsForProblem(self, given_lab_num, given_problem_num, marks_dict):
        '''
            Recursive function that returns a list of studentMarkDTOs with students that have assigned a given problem
            IN:
                given_lab_num - string, example: "02"
                given_problem_num - string, example: "19"
                marks_dict - dictionary of marks
        '''
        auxiliary_list = []
        mark_key = list(marks_dict.keys())[0]
        pb = marks_dict[mark_key].getProblem()
        lab_num, problem_num = pb.getNumber().split("_")
        if lab_num == given_lab_num and problem_num == given_problem_num:
            stmrk = StudentMarkDTO(marks_dict[mark_key])
            auxiliary_list.append(stmrk)
        if len(marks_dict) > 1:
            marks_dict.pop(marks_dict[mark_key].getId())
            auxiliary_list += self.__getListOfStudentsForProblem(given_lab_num, given_problem_num, marks_dict)
        return auxiliary_list
    
    def getStudentsForProblemRecursive(self, problem_number):
        '''
           Returns the students and their marks for a specific problem
            IN:
                problem_number - string, labNo_problemNo 
        '''
        self.__problem_val.validateProblemNumber(problem_number, self.__problems)
        given_lab_num, given_problem_num = problem_number.split("_")
        marks_dict = dict(self.__marks.getAllMarks())
        students_with_problem = self.__getListOfStudentsForProblem(given_lab_num, given_problem_num, marks_dict)
        sortAlg = SortingAlgorithms()
        sortAlg.bubbleSort(students_with_problem)
        return students_with_problem
    
    def getStudentsForProblemIterative(self, problem_number):
        '''
            Returns the students and their marks for a specific problem
            IN:
                problem_number - string, labNo_problemNo
                
            COMPLEXITY:
            - BEST CASE: - O(n)
                         - description: if the students with the given problem are already sorted alphabetically
                                        and in an ascending order by their marks in the marks_repository
            - WORST CASE: - O(n * log(n))
                          - description: if the students with the given problem are sorted in a descending order
                                         (alphabetically and by their marks) in the marks_repository
            - AVERAGE CASE: - O(n * log(n))
            - WORST-CASE SPACE COMPLEXITY: O(n)
            - Where n - the number of marks given (assigned problems)                  
                                
        '''
        self.__problem_val.validateProblemNumber(problem_number, self.__problems)
        students_with_problem = []
        given_lab_num, given_problem_num = problem_number.split("_")
        for mark_key in self.__marks.getAllMarks():
            pb = self.__marks.getMarkById(mark_key).getProblem()
            lab_num, problem_num = pb.getNumber().split("_")
            if lab_num == given_lab_num and problem_num == given_problem_num:
                stmrk = StudentMarkDTO(self.__marks.getMarkById(mark_key))
                students_with_problem.append(stmrk)
        
        sortAlg = SortingAlgorithms()
        sortAlg.bubbleSort(students_with_problem)
        return students_with_problem
    
    def __getAverageForStudent(self, student_key, marks_dict, average_mark, num_of_marks):
        '''
            Returns the average_mark and num_of_marks for student_key
        '''
        mark_key = list(marks_dict.keys())[0]
        new_st_id, lab_num, pb_num = marks_dict[mark_key].getId().split("_")
        if int(new_st_id) == student_key:
            average_mark += marks_dict[mark_key].getMark()
            num_of_marks += 1
        if len(marks_dict) > 1:
            marks_dict.pop(mark_key)
            average_mark, num_of_marks = self.__getAverageForStudent(student_key, marks_dict, average_mark, num_of_marks)
        return average_mark, num_of_marks
            
        
    def __getListOfStudentsNotPassing(self, students_dict, marks_dict):
        '''
            Recursive method that returns a list of studentMarksDTOs with all the students that have an average bellow 5
            IN:
                students_dict - dictionary with students
                marks_dict - dictionary with marks
        '''
        auxiliary_list = []
        student_key = list(students_dict.keys())[0]
        average_mark, num_of_marks = self.__getAverageForStudent(student_key, dict(marks_dict), 0, 0)
        if num_of_marks > 0 and average_mark / num_of_marks < 5:
            mrk = Mark(students_dict[student_key], LabProblem("", "", 0), average_mark/num_of_marks)
            auxiliary_list.append(StudentMarkDTO(mrk))
        if len(students_dict) > 1:
            students_dict.pop(student_key)
            auxiliary_list += self.__getListOfStudentsNotPassing(students_dict, marks_dict)
        return auxiliary_list
    
    def getStudentsWithMarksUnder5Recursive(self):
        '''
            Returns all the students and their marks with the average of the marks lower than 5
        '''
        students_dict = dict(self.__students.getAllStudents())
        marks_dict = dict(self.__marks.getAllMarks())
        students_not_passing = self.__getListOfStudentsNotPassing(students_dict, marks_dict)
        sortAlg = SortingAlgorithms()
        sortAlg.shellSort(students_not_passing)
        return students_not_passing
    
    def getStudentsWithMarksUnder5Iterative(self):
        '''
            Returns all the students and their marks with the average of the marks lower than 5
        '''
        students_not_passing = []
        for st_id in self.__students.getAllStudents():
            average_mark = 0
            num_of_marks = 0
            for mark_key in self.__marks.getAllMarks():
                new_st_id, lab_num, pb_num = self.__marks.getMarkById(mark_key).getId().split("_")
                if int(new_st_id) == st_id:
                    average_mark += self.__marks.getMarkById(mark_key).getMark()
                    num_of_marks += 1
            if num_of_marks > 0 and average_mark / num_of_marks < 5:
                mrk = Mark(self.__students.getStudentById(st_id), LabProblem("", "", 0), average_mark/num_of_marks)
                students_not_passing.append(StudentMarkDTO(mrk))
        sortAlg = SortingAlgorithms()
        sortAlg.shellSort(students_not_passing)
        return students_not_passing
    
    def getStudentWithMostProblemsMarkOver(self, minimum_mark):
        '''
            Returns the id, name and number of problems for the student with the most marks over the given minimum 
            IN:
                minimum_mark - integer
        '''
        big_student = StudentProblemsDTO(0, "", 0)
        most_problems = 0
        for st_id in self.__students.getAllStudents():
            num_of_problems = 0
            for mark_key in self.__marks.getAllMarks():
                new_st_id, lab_num, pb_num = self.__marks.getMarkById(mark_key).getId().split("_")
                if int(new_st_id) == st_id and self.__marks.getMarkById(mark_key).getMark() >= minimum_mark:
                    num_of_problems += 1
            if num_of_problems > most_problems:
                big_student = StudentProblemsDTO(st_id, self.__students.getStudentById(st_id).getName(), num_of_problems)
                most_problems = num_of_problems
        
        if most_problems > 0:
            return big_student
        else:
            return None
    
        
#--------------------------------------------------- TESTS -----------------------------------------------------------------
            

def test_getStudentsForProblem():
    st_repo = StudentInMemoryRepository()
    pb_repo = LabProblemInMemoryRepository()
    mrk_repo = MarkInMemoryRepository()
    pb_val = LabProblemValidator()
    statistics_service = StatisticsService(st_repo, pb_repo, mrk_repo, pb_val)
    
    st_repo.addStudent(Student("Ana", 21, 0))
    st_repo.addStudent(Student("Ion", 22, 1))
    st_repo.addStudent(Student("Mircea", 21, 2))
    st_repo.addStudent(Student("Pas", 56, 3))
    
    pb_repo.addProblem(LabProblem("01_01", "ceva", 3))
    pb_repo.addProblem(LabProblem("03_01", "altceva", 6))
    pb_repo.addProblem(LabProblem("03_05", "mama", 2))
    pb_repo.addProblem(LabProblem("16_01", "dada", 10))
    
    mrk_repo.addMark(Mark(Student("Ana", 21, 0), LabProblem("01_01", "ceva", 3), 8))
    mrk_repo.addMark(Mark(Student("Ion", 22, 1), LabProblem("01_01", "ceva", 3), 5))
    mrk_repo.addMark(Mark(Student("Ana", 21, 0), LabProblem("16_01", "dada", 10), 9))
    mrk_repo.addMark(Mark(Student("Ion", 22, 1), LabProblem("16_01", "dada", 10), 3))
    mrk_repo.addMark(Mark(Student("Mircea", 21, 2), LabProblem("01_01", "ceva", 3), 4))
    mrk_repo.addMark(Mark(Student("Ionel", 56, 3), LabProblem("03_01", "altceva", 6), 5))
    
    assert statistics_service.getStudentsForProblemRecursive("01_01") == [StudentMarkDTO(mrk_repo.getMarkById("0_01_01")), StudentMarkDTO(mrk_repo.getMarkById("1_01_01")), StudentMarkDTO(mrk_repo.getMarkById("2_01_01"))]
    try:
        statistics_service.getStudentsForProblemRecursive("02_04")
        assert False
    except ValueError:
        assert True
    

def test_getStudentsWithMarksUnder5():
    st_repo = StudentInMemoryRepository()
    pb_repo = LabProblemInMemoryRepository()
    mrk_repo = MarkInMemoryRepository()
    pb_val = LabProblemValidator()
    statistics_service = StatisticsService(st_repo, pb_repo, mrk_repo, pb_val)
    
    st_repo.addStudent(Student("Ana", 21, 0))
    st_repo.addStudent(Student("Ion", 22, 1))
    st_repo.addStudent(Student("Mircea", 21, 2))
    st_repo.addStudent(Student("Pas", 56, 3))
    
    pb_repo.addProblem(LabProblem("01_01", "ceva", 3))
    pb_repo.addProblem(LabProblem("03_01", "altceva", 6))
    pb_repo.addProblem(LabProblem("03_05", "mama", 2))
    pb_repo.addProblem(LabProblem("16_01", "dada", 10))
    
    mrk_repo.addMark(Mark(Student("Ana", 21, 0), LabProblem("01_01", "ceva", 3), 8))
    mrk_repo.addMark(Mark(Student("Ion", 22, 1), LabProblem("01_01", "ceva", 3), 5))
    mrk_repo.addMark(Mark(Student("Ana", 21, 0), LabProblem("16_01", "dada", 10), 9))
    mrk_repo.addMark(Mark(Student("Ion", 22, 1), LabProblem("16_01", "dada", 10), 3))
    mrk_repo.addMark(Mark(Student("Mircea", 21, 2), LabProblem("01_01", "ceva", 3), 4))
    mrk_repo.addMark(Mark(Student("Ionel", 56, 3), LabProblem("03_01", "altceva", 6), 5))
    
    
    assert statistics_service.getStudentsWithMarksUnder5Recursive() == [StudentMarkDTO(Mark(st_repo.getStudentById(1), LabProblem("", "", 0), 4.0)), StudentMarkDTO(Mark(st_repo.getStudentById(2), LabProblem("", "", 0), 4.0))]
    

def test_getStudentWithMostProblemsMarkOver():
    st_repo = StudentInMemoryRepository()
    pb_repo = LabProblemInMemoryRepository()
    mrk_repo = MarkInMemoryRepository()
    pb_val = LabProblemValidator()
    statistics_service = StatisticsService(st_repo, pb_repo, mrk_repo, pb_val)
    
    st_repo.addStudent(Student("Ana", 21, 0))
    st_repo.addStudent(Student("Ion", 22, 1))
    st_repo.addStudent(Student("Mircea", 21, 2))
    st_repo.addStudent(Student("Ionel", 56, 3))
    
    pb_repo.addProblem(LabProblem("01_01", "ceva", 3))
    pb_repo.addProblem(LabProblem("03_01", "altceva", 6))
    pb_repo.addProblem(LabProblem("03_05", "mama", 2))
    pb_repo.addProblem(LabProblem("16_01", "dada", 10))
    
    mrk_repo.addMark(Mark(Student("Ana", 21, 0), LabProblem("01_01", "ceva", 3), 8))
    mrk_repo.addMark(Mark(Student("Ion", 22, 1), LabProblem("01_01", "ceva", 3), 5))
    mrk_repo.addMark(Mark(Student("Ana", 21, 0), LabProblem("16_01", "dada", 10), 8))
    mrk_repo.addMark(Mark(Student("Ion", 22, 1), LabProblem("16_01", "dada", 10), 3))
    mrk_repo.addMark(Mark(Student("Mircea", 21, 2), LabProblem("01_01", "ceva", 3), 4))
    mrk_repo.addMark(Mark(Student("Ionel", 56, 3), LabProblem("03_01", "altceva", 6), 5))
    
    expected = StudentProblemsDTO(0, "Ana", 2)
    assert statistics_service.getStudentWithMostProblemsMarkOver(5) == expected
    
    expected = None
    assert statistics_service.getStudentWithMostProblemsMarkOver(9) == expected


test_getStudentWithMostProblemsMarkOver()
test_getStudentsForProblem()
test_getStudentsWithMarksUnder5()   