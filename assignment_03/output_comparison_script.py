def is_identical(file_01, file_02):
    list_01, list_02 = open(file_01).readlines(  ), open(file_02).readlines(  )

    return list_01 == list_02

#"output_00_original.txt"
#"output_01_functions.txt"

print(is_identical("output_00_original.txt", "output_01_functions.txt"))
