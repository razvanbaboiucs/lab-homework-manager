'''
Created on Nov 16, 2018

@author: Razvan
'''

import UI.text

class Console:
    '''
        It defines a console 
    '''


    def __init__(self, student_service, problem_service, marks_service, statistics_service):
        '''
            It defines the services
            IN:
                student_service - StudentServiceClass
                problem_service - ProblemServiceClass
        '''
        self.__students = student_service
        self.__problems = problem_service
        self.__marks = marks_service
        self.__statistics = statistics_service
        
    def getString(self, message):
        '''
            Returns a string
            IN:
                message - input message displayed in console

        '''
        user_input = input(message)
        print()
        return user_input
    
    def getInt(self, message):
        '''
            Returns an integer
            IN:
                message - input message displayed in console
        '''
        while True:
            try:
                user_input = int(input(message))
                print()
                return user_input
            except ValueError:
                print("Attention: - the input should be a number!\n")
        
    def getCommand(self, message):
        '''
            Returns a command 
            IN:
                message - input message displayed in console

        '''
        command = self.getString(message)
        command.strip()
        return command 
    
    def printList(self, lst):
        string_of_elements = ""
        for el in lst:
            string_of_elements += str(el) + "\n"
        print (string_of_elements)
        
    def manageStudents(self):
        menu = {
            "1" : self.__students.getAllStudents,
            "2" : self.__students.addStudent, 
            "3" : self.__students.removeStudent, 
            "4" : self.__students.updateStudent, 
            "5" : self.__students.getStudentById,
            "6" : self.__students.generateRandomStudents, 
            "x" : None, 
            }
        while True:
            UI.text.printStudentsMenu()
            command = self.getCommand("Select an operation: ")
            try: 
                if command in menu:   
                    if command == "1":
                        print(menu[command]())
                    elif command == "2":
                        name = self.getString("Give the name of the student: ")
                        group = self.getInt("Give the group number of the student: ")
                        print(menu[command](name, group))
                    elif command in ["3", "5"]:
                        student_id = self.getInt("Give the student's id: ")
                        print(menu[command](student_id))
                    elif command == "4":
                        student_id = self.getInt("Give the student's id: ")
                        name = self.getString("Give the student's new name: ")
                        group = self.getInt("Give the student's new group: ")
                        print(menu[command](student_id, name, group))
                    elif command == "6":
                        number_of_students = self.getInt("Give the number of students you want to generate: ")
                        print(menu[command](number_of_students))
                    else:
                        break
                else:
                    print("Attention: - the command given is not available!\n")
            except ValueError as error:
                print("-" * 10, "\n", error,  "\n", "-" * 10)
            
    def manageLabProblems(self):
        menu = {
            "1" : self.__problems.getAllProblems,
            "2" : self.__problems.addProblem, 
            "3" : self.__problems.removeProblem, 
            "4" : self.__problems.updateProblem, 
            "5" : self.__problems.getProblemByNumber, 
            "6" : self.__problems.generateRandomProblems,
            "x" : None, 
            }
        while True:
            UI.text.printProblemsMenu()
            command = self.getCommand("Select an operation: ")
            try:
                if command in menu:
                    if command == "1":
                        print(menu[command]())
                    elif command == "2":
                        lab_number = self.getInt("Give the lab number: ")
                        description = self.getString("Give problem description: ")
                        deadline = self.getInt("Give deadline (number of weeks): ")
                        print(menu[command](lab_number, description, deadline))
                    elif command in ["3", "5"]:
                        problem_number = self.getCommand("Give problem number (labNo_problemNo): ")
                        print(menu[command](problem_number))
                    elif command == "4":
                        problem_number = self.getCommand("Give problem number (labNo_problemNo): ")
                        description = self.getString("Give problem description: ")
                        deadline = self.getInt("Give deadline (number of weeks): ")
                        print(menu[command](problem_number, description, deadline))
                    elif command == "6":
                        number_of_problems = self.getInt("Give number of problems to generate: ")
                        print(menu[command](number_of_problems))
                    else:
                        break
                else:
                    print("Attention: - the command given is not available!\n")
            except ValueError as error:
                print("-" * 10, "\n", error, "\n", "-" * 10)
                
    def manageMarks(self):
        menu = {
            "1" : self.__marks.getAllMarks,
            "2" : self.__marks.addMark, 
            "3" : self.__marks.removeMark,
            "4" : self.__marks.updateMark, 
            "5" : self.__marks.getMark,
            "x" : None,
            
            }
        while True:
            UI.text.printMarksMenu()
            command = self.getCommand("Select an operation: ")
            try:
                if command in menu:
                    if command in ["2", "4"]:
                        st_id = self.getInt("Give the student id: ")
                        problem_number = self.getCommand("Give problem number (labNo_problemNo): ")
                        mark = self.getInt("Give a mark (between 0 and 10): ")
                        print(menu[command](st_id, problem_number, mark))
                    elif command in ["3", "5"]:
                        st_id = self.getInt("Give the student id: ")
                        problem_number = self.getCommand("Give problem number (labNo_problemNo): ")
                        print(menu[command](st_id, problem_number))
                    elif command == "1":
                        print(menu[command]())
                    else:
                        break
                else:
                    print("Attention: - the command given is not available!\n")
            except ValueError as error:
                print("-" * 10, "\n", error, "\n", "-" * 10)
    

    def manageStatistics(self):
        menu = {
            "1" : self.__statistics.getStudentsForProblemRecursive, 
            "2" : self.__statistics.getStudentsWithMarksUnder5Recursive, 
            "3" : self.__statistics.getStudentWithMostProblemsMarkOver, 
            "x" : None, 
            
            }
        while True:
            UI.text.printStatisticsMenu()
            command = self.getCommand("Select an operation: ")
            try:
                if command in menu:
                    if command == "1":
                        problem_number = self.getString("Give problem number (labNo_problemNo): ")
                        print("The students that have the given problem are: \n")
                        self.printList(menu[command](problem_number))
                    elif command == "2":
                        print("The students with the average mark under 5 are: \n")
                        self.printList(menu[command]())
                    elif command == "3":
                        minimum_mark = self.getInt("Give minimum mark: ")
                        to_print = menu[command](minimum_mark)
                        print(to_print)
                    else:
                        break
                else:
                    print("Attention: - the given command is not available!\n")
            except ValueError as error:
                print("-" * 10, "\n", error, "\n", "-" * 10)
                        
    
    def run(self):
        menu = {
            "1" : self.manageStudents,
            "2" : self.manageLabProblems,
            "3" : self.manageMarks,
            "4" : self.manageStatistics,
            "x" : UI.text.printExitMessage,
            }
        while True:
            UI.text.printUpdateMenu()
            command = self.getCommand("Select what do you want to manage: ")
            if command in menu:
                menu[command]()
                if command == "x" or command == "X":
                    break
            else:
                print("Attention: - the chosen command is not available!\n")  