'''
Created on Dec 3, 2018

@author: Razvan
'''

class CleanUpFile:
    '''
        Cleans txt files
    '''

    def __init__(self, st_f_name, pb_f_name, mrk_f_name):
        self.__st_f_name = st_f_name
        self.__pb_f_name = pb_f_name
        self.__mrk_f_name = mrk_f_name
        
    def clean(self):
        self.__cleanFile(self.__st_f_name)
        self.__cleanFile(self.__pb_f_name)
        self.__cleanFile(self.__mrk_f_name)
    
    def __cleanFile(self, file_name):
        with open(file_name) as file:
            lines_list = file.readlines()
        while "\n" in lines_list:
            lines_list.remove("\n")
        with open(file_name, "w") as file:
            file.writelines(lines_list)
        