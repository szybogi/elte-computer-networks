end = False
coding = 0


def nrz_l(input_code):
    result = ""
    for code_element in str(input_code):
        if(code_element == "1"):
            result += "(11),"
        elif(code_element == "0"):
            result += ("(00),")
    print(result)


def rz(input_code):
    result = ""
    for code_element in str(input_code):
        if(code_element == "1"):
            result += "(10),"
        elif(code_element == "0"):
            result += ("(00),")
    print(result)


def man(input_code):
    result = ""
    for code_element in str(input_code):
        if(code_element == "1"):
            result += "(10),"
        elif(code_element == "0"):
            result += ("(01),")
    print(result)


def dman(input_code):
    result = ""
    last_element = 1
    for code_element in str(input_code):
        if(code_element == "1" and last_element == 1):
            result += "(10),"
            last_element = 0
        elif(code_element == "1" and last_element == 0):
            result += "(01),"
            last_element = 1
        elif(code_element == "0" and last_element == 1):
            result += "(01),"
        elif(code_element == "0" and last_element == 0):
            result += "(10),"
    print(result)


while(not end):
    coding = input(
        "Choose a coding (0-NRZ-L, 1-RZ, 2-Manchester, 3-DiffManchester, 4-exit): ")

    if(coding == 0):
        input_code = raw_input("Input: ")
        nrz_l(input_code)
    elif(coding == 1):
        input_code = raw_input("Input: ")
        rz(input_code)
    elif(coding == 2):
        input_code = raw_input("Input: ")
        man(input_code)
    elif(coding == 3):
        input_code = raw_input("Input: ")
        dman(input_code)
    elif(coding == 4):
        end = True
    else:
        print("Wrong value! Try again!")
