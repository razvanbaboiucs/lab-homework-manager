'''
Created on Nov 16, 2018

@author: Razvan
'''
from Domain.StudentClass import Student
from Domain.StudentRepositoryClass import StudentInMemoryRepository

class StudentValidator:
    '''
        Validates data for the student class
    '''
    
    def validateStudent(self, st):
        error = "Attention:"
        if type(st.getName()) is not str:
            error += " - the name cannot to be a number\n"
        if type(st.getName()) is str and st.getName() == "":
            error += " - the name is missing\n"
        if not st.getInitial().isupper():
            error += "- the name should start with a capital letter!\n"
        if all(x.isalpha() or x.isspace() for x in st.getName()) == False :
            error += " - the name can only contain letters!\n"
        if type(st.getGroup()) is not int or type(st.getGroup()) is int and st.getGroup() < 0:
            error += "- the number of the group has to be a natural number!\n"
        if type(st.getId()) is not int or st.getId() < 0:
            error += "- the id entered should be a natural number!\n"
            
        if error != "Attention:":
            raise ValueError(error)
    
    def validateIdInRepo(self, st_id, st_repo):
        error = "Attention: "
        if type(st_id) is not int or st_id < 0:
            error += "- the id should be a natural number! \n"
        elif st_id not in st_repo.getAllStudents() or st_repo.getStudentById(st_id).getAvailability() == True:
            error += "- the specified id is not registered! \n"
        
        if error != "Attention: ":
            raise ValueError(error)
        

#--------------------------------------------- TESTS ----------------------------------------------------
    
def test_valdidateStudent():
    val = StudentValidator()
    try:
        st1 = Student("Ion Popescu", 211, 12)
        st2 = Student("Maricica24POpescu", "2", 9)
        val.validateStudent(st1)
        assert True
        val.validateStudent(st2)
        assert False
    except ValueError:
        assert True
    
    try:
        st1 = Student("Marin", "45", 4)
        val.validateStudent(st1)
        assert False
    except ValueError:
        assert True
    
    try:
        st2 = Student("Marin Preda", False, 5)
        val.validateStudent(st2)
        assert False
    except ValueError:
        assert True
    
    try:
        st2 = Student("Ion", 2, 4)
        st1 = Student("Ana", 5, 6)
        val.validateStudent(st2)
        assert True
        val.validateStudent(st1)
        assert True
    except ValueError:
        assert False
        
    try:
        st1 = Student("ion", 21, 3)
        val.validateStudent(st1)
        assert False
    except ValueError:
        assert True
    
    
def test_validateIdInRepo():
    st_repo = StudentInMemoryRepository()
    st1 = Student("ana", 12, 1)
    st_repo.addStudent(st1)
    st2 = Student("ion", 131, 0)
    st_repo.addStudent(st2)
    st3 = Student("gigi", 14, 5)
    st_repo.addStudent(st3)
    val = StudentValidator()
    
    st_id = -1
    try:
        val.validateIdInRepo(st_id, st_repo)
        assert False
    except ValueError:
        assert True
        
    st_id = "unu"
    try: 
        val.validateIdInRepo(st_id, st_repo)
        assert False
    except ValueError:
        assert True
    
    st_id = 2
    try:
        val.validateIdInRepo(st_id, st_repo)
        assert False
    except ValueError:
        assert True
        
    st_id = 1
    try:
        val.validateIdInRepo(st_id, st_repo)
        assert True
    except ValueError:
        assert False

test_validateIdInRepo()
test_valdidateStudent()