"""
Script to confirm that changes to nbody scripts have not impacted its output

Testing Instructions:
    #Run both versions of the program, piping results into txt files
    #Enter numerical values associated with each txt file into is_identical
    #Function will return true if output matches & false if it does not

"""

def is_identical(iteration_num_1, iteration_num_2):

    filename_dict = {
        0: "output_00_original.txt",
        1: "output_01_functions.txt",
        2: "output_02_variables.txt",
        3: "output_03_looping.txt",
        4: "output_04_built_in.txt",
        "opt_03": "nbody_opt_03.txt"}

    filename_01, filename_02 = filename_dict[iteration_num_1], filename_dict[iteration_num_2]
    list_01, list_02 = open(filename_01).readlines(  ), open(filename_02).readlines(  )
    return list_01 == list_02

print(is_identical(0, 2))
