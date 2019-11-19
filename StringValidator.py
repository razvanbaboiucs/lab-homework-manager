'''
Created on Nov 12, 2018

@author: Razvan

!!!!!!! NOT IN USE !!!!!!
'''

class StringValidator:
    '''
        Validates a string
        The string should:
            - start with a lower case letter.
            - cannot end with spaces
            - cannot have more than one space
            - after a space it should be a lower case letter
            - can only contain letters, digits or spaces
    '''

    def validate(self, st):
        error = "Attention: \n"
        if not st[0].islower():
            error += "- the string has to start with a lower case letter!\n"
        
        spaces_no = 0
        for ch in st:
            if ch == " ":
                spaces_no += 1
        if spaces_no > 1:
            error += "- the string cannot have more than one space!\n"
        
        for contor in range(len(st)):
            if st[contor] == " " and contor + 1 < len(st) and not st[contor + 1].islower():
                error += "- after a space, the string should start with a lower case letter!\n"
                
        if not st[len(st) - 1].isalpha() and not st[len(st) - 1].isdigit():
            error += "- the string should end with a letter or a digit!\n"
        
        if all(x.isalpha() or x.isdigit() or x.isspace() for x in st) == False:
            error += "- the string should only contain letters, digits or spaces"
        
        if error != "Attention: \n":
            raise ValueError(error)


def test_validator():
    val = StringValidator()
    
    input_st = "ana"
    try:
        val.validate(input_st)
        assert True
    except ValueError:
        assert False
    
    input_st = "aNa7"
    try:
        val.validate(input_st)
        assert True
    except ValueError:
        assert False
    
    input_st = "aNa72 "
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
    
    input_st = "Ana"
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
        
    input_st = "aNa2Tp a"
    try:
        val.validate(input_st)
        assert True
    except ValueError:
        assert False
    
    input_st = "aNa2Tp A"
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
        
    input_st = "a~N"
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
        
    input_st = "aN  7"
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
    
    input_st = "aN  b"
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
    
    input_st = "aNa aN "
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
    
    input_st = "aN aN an"
    try:
        val.validate(input_st)
        assert False
    except ValueError:
        assert True
        
    input_st = "an a3"
    try:
        val.validate(input_st)
        assert True
    except ValueError:
        assert False
        
test_validator()