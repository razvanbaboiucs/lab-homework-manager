'''
Created on Nov 11, 2018

@author: Razvan
'''
def printUpdateMenu():
    menu = """1. Manage students.
2. Manage lab problems.
3. Manage marks.
4. Manage statistics.
x. Exit application.\n
"""
    menu += "-" * 15
    print(menu)
    
def printStudentsMenu():
    menu = """1. Show all students.
2. Add student.
3. Remove student.
4. Update student information.
5. Find a student.
6. Generate random students.
x. Return to main menu. \n
"""
    menu += "-" * 15
    print(menu)
    
def printProblemsMenu():
    menu = """1. Show all problems.
2. Add problem.
3. Remove problem.
4. Update problem information.
5. Find problem.
6. Generate random problems.
x. Return to main menu.\n
"""
    menu += "-" * 15
    print(menu)
    
def printMarksMenu():
    menu = """1. Show all marks.
2. Add mark.
3. Remove mark.
4. Update mark.
5. Find mark.
x. Return to main menu.\n
"""
    menu += "-" * 15
    print(menu)
    
def printStatisticsMenu():
    menu = """1. Get all marks and students for a given problem.
2. Get all students with marks lower than 5.
3. Get student with most problems which have the mark over a given number (between 0 and 10).
x. Return to main menu. \n
"""
    menu += "-" * 15
    print(menu)
    
def printExitMessage():
    message = "Bella ciao,\nBella ciao,\nBella ciao, ciao, ciao!\n* the italian version of 'Goodbye world!' *"
    print(message)
    exit