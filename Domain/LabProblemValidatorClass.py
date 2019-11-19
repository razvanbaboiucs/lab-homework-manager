'''
Created on Nov 16, 2018

@author: Razvan
'''
from Domain.LabProblemClass import LabProblem
from Domain.LabProblemRepositoryClass import LabProblemInMemoryRepository

class LabProblemValidator:
    '''
        Validates the data for labProblems
    '''
    
    def validateProblem(self, pb):
        error = "Attention:"
        if type(pb.getDeadline()) is not int:
            error += "- the deadline should be a natural number!\n"
        if type(pb.getDeadline()) is int and pb.getDeadline() <= 0:
            error += "- the deadline should be at least one week!\n"
        if type(pb.getDescription()) is not str:
            error += "- the problem's description should be a string!\n"
        if type(pb.getDescription()) is str and pb.getDescription() == "":
            error += "- the problem's description should not be empty!\n"
        if type(pb.getNumber()) is not str or pb.getNumber() == "" or len(pb.getNumber()) != 5:
            error += "- the problem number should be a string (lab number_Problem number)!\n"
        else:
            new_number = str(pb.getNumber())
            new_number = new_number.split("_")
            if len(new_number) != 2:
                error += "- give only the lab_number and the problem_number!\n"
            if new_number[0].isdigit() == False or len(new_number[0]) != 2:
                error += "- the lab_number should be formed from 2 digits (example: 02)!\n"
            if new_number[1].isdigit() == False or len(new_number[1]) != 2:
                error += "- the problem number should be formed from 2 digits (example: 03)!\n"
                
        if error != "Attention:":
            raise ValueError(error)
            
        
    def validateProblemNumber(self, pb_number, pb_repo):
        error = "Attention:"
        if type(pb_number) is not str or pb_number == "" or len(pb_number) != 5:
            error += "- the problem's number should be a string (labNo_problemNo)\n"
        else:
            new_number = str(pb_number)
            new_number = new_number.split("_")
            if len(new_number) != 2:
                error += "- give only the lab_number and the problem_number!\n"
            if new_number[0].isdigit() == False or len(new_number[0]) != 2:
                error += "- the lab_number should be formed from 2 digits (example: 02)!\n"
            if new_number[1].isdigit() == False or len(new_number[1]) != 2:
                error += "- the problem number should be formed from 2 digits (example: 03)!\n"
        
        if pb_number not in pb_repo.getAllProblems() or pb_repo.getProblemByNumber(pb_number).getAvailability() == True:
            error += "- the problem with the given number doesn't exist!\n"
        
        if error != "Attention:":
            raise ValueError(error)

#-------------------------------------------------- TESTS -------------------------------------------------

def test_validateProblem():
    val = LabProblemValidator()
    
    try:
        pb1 = LabProblem("02_21", "ceva", 2)
        pb2 = LabProblem("14_05","", 5)
        val.validateProblem(pb1)
        assert True
        val.validateProblem(pb2)
        assert False
    except ValueError:
        assert True
        
    try:
        pb1 = LabProblem("22_01","ceva", "one")
        val.validateProblem(pb1)
        assert False
    except ValueError:
        assert True
        
    try:
        pb1 = LabProblem("22_02", "altceva", -2)
        val.validateProblem(pb1)
        assert False
    except ValueError:
        assert True
    
    try:
        pb1 = LabProblem("03_03", "dada")
        val.validateProblem(pb1)
        assert True
    except ValueError:
        assert False
    
    try:
        pb2 = LabProblem("0a_05", "daa", 2)
        val.validateProblem(pb2)
        assert False
    except ValueError:
        assert True
    
    try:
        pb2 = LabProblem("1_22", "nun")
        val.validateProblem(pb2)
        assert False
    except ValueError:
        assert True
    
    try:
        pb1 = LabProblem("22_3", "dada", 10)
        val.validateProblem(pb1)
        assert False
    except ValueError:
        assert True
    
    try:
        pb2 = LabProblem(22, "nun", 2)
        val.validateProblem(pb1)
        assert False
    except ValueError:
        assert True
        
    
def test_validateProblemNumber():
    pb1 = LabProblem("01_02", "ceva", 2)
    pb2 = LabProblem("00_33", "ceva2", 4)
    pb3 = LabProblem("22_04", "ceva3")
    pb_repo = LabProblemInMemoryRepository()
    
    pb_repo.addProblem(pb1)
    pb_repo.addProblem(pb2)
    pb_repo.addProblem(pb3)
    
    val = LabProblemValidator()
    
    try:
        pb_num = "01_15"
        val.validateProblemNumber(pb_num, pb_repo)
        assert False
    except ValueError:
        assert True
    
    try:
        pb_num = ""
        val.validateProblemNumber(pb_num, pb_repo)
        assert False
    except ValueError:
        assert True
        
    try:
        pb_num = 12
        val.validateProblemNumber(pb_num, pb_repo)
        assert False
    except ValueError:
        assert True
    
    
test_validateProblemNumber()        
test_validateProblem()