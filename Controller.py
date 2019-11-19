'''
Created on Nov 16, 2018

@author: Razvan
'''

from Domain.LabProblemRepositoryClass import LabProblemInMemoryRepository, LabProblemFileRepository
from Domain.StudentRepositoryClass import StudentInMemoryRepository, StudentFileRepository
from Domain.StudentValidatorClass import StudentValidator
from Domain.LabProblemValidatorClass import LabProblemValidator
from BussinesLogic.StudentServiceClass import StudentService
from BussinesLogic.LabProblemServiceClass import LabProblemService
from UI.ConsoleClass import Console
from Domain.MarkRepositoryClass import MarkInMemoryRepository, MarkFileRepository
from Domain.MarkValidatorClass import MarkValidator
from BussinesLogic.MarkServiceClass import MarkService
from BussinesLogic.StatisticsServiceClass import StatisticsService
from CleanUpFileClass import CleanUpFile


def __main__():
    #student_repo = StudentInMemoryRepository()
    student_repo = StudentFileRepository("students.txt")
    student_val = StudentValidator()
    
    
    #problem_repo = LabProblemInMemoryRepository()
    problem_repo = LabProblemFileRepository("problems.txt")
    problem_val = LabProblemValidator()
    
    
    #mark_repo = MarkInMemoryRepository()
    mark_repo = MarkFileRepository("marks.txt", student_repo, problem_repo)
    mark_val = MarkValidator()
    
    statistics_service = StatisticsService(student_repo, problem_repo, mark_repo, problem_val)
    mark_service = MarkService(mark_repo, student_repo, problem_repo, mark_val)
    student_service = StudentService(student_repo, student_val, mark_repo)
    problem_service = LabProblemService(problem_repo, problem_val, mark_repo)
    
    console = Console(student_service, problem_service, mark_service, statistics_service)
    console.run()
    
    cleanup = CleanUpFile("students.txt", "problems.txt", "marks.txt")
    cleanup.clean()
    
__main__()
