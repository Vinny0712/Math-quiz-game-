import random 
import threading 
from time import *
import tkinter as tk
from tkinter import ttk
import re







#---------------------------------MATH----------------------------------------#


#this function generate 6 random numbers(single digit) and returns a list 
def generate_number():
    six_num=[]
    for n in range(6):
#ensures that no same numbers are generated, jic
        element= random.randrange(1,10)
        bool1= element in six_num
        while bool1:
            element= random.randrange(1,10) 
            bool1= element in six_num
        six_num.append(element)
    return six_num



def generate_target_number(six_num):
    var_num=[]
    for n in range(4):
    #ensures that no same numbers are generated, jic
            element1= random.choice(six_num)
            bool2= element1 in var_num
            while bool2:
                element1= random.choice(six_num)
                bool2= element1 in var_num
            var_num.append(element1)
            
    #did not include divide as divide may easily generate a float which is harder to calculate mentally 
    operators= ["+","-","*"]
    #this shall be the default eqn (a[+/-/*]b)[+/-/*]c[/ or +/-/* ]d
    #if front part is divisible by d then we can only add / as int will be generated 

    a=random.choice(operators)
    b=random.choice(operators)
    c="/"


    expression="({}{}{}){}{}".format(var_num[0],a,var_num[1],b,var_num[2])

    if eval(expression)% var_num[3]==0:
        expression+=c+str(var_num[3])
    else:
        c=random.choice(operators)
        expression+=c+str(var_num[3])
    print(expression)
    target_number= int(eval(expression))
    correct_operators=[a,b,c] #needed in hint
    return target_number,correct_operators

    
def check_expression(user_expression,six_num,target_number,correct_operators):
    #checks if the element inputted is valid characters

    regex =  r"([^0-9\+\-\/\*\(\)])|^[\+\-\)\*\/]|[\+\-\(\*\/]$|[\+\-\*\/]+[\+\-\*\/]"
    matches = re.search(regex,user_expression)
    
    #([^0-9\+\-\/\*\(\)]) : Checks for any char in the string that is not a numeral or a operator
    #^[\+\-\)\*\/] : Checks whether the start of a string contains a operator
    #[\+\-\(\*\/]$ : Checks whether the end of a string contains a operator
    #[\+\-\\/]+[\+\-\\/] : Checks whether any operators are stacked with one another i.e '+-'
    
    #Remove blank lists elements
    format= re.sub('[\(\)]','', user_expression)
    numbers = re.split("[\+\-\*\/]",format)
    print(numbers)
    for i in range(len(numbers)):
        if numbers[i]=='':
            numbers.remove(numbers[i])
            i=i-1
    print(numbers)
    
    #Check if any of the numbers are not from the sub list
    for i in numbers:
        isnum = False
        for j in six_num:
            if int(i) == int(j):
                isnum= True
        if isnum is False:
            return "A number you entered is not part of the 6 numbers given"
        # if i==target_number:
        #         return "Invalid2"
    
    #Check if the input contains invalid characters or symbols
    if matches:
        return "You entered an invalid character"
    
    #Checks if there is a proper pair of parenthesis
    paren_checker=[char for char in user_expression]
    paren_state1=False
    paren_state2=False
    #print(paren_checker)
    
    for i in range(len(paren_checker)):
        if paren_checker[i]=='(':
            paren_state1=True
        elif paren_state1 == True and paren_checker[i]==')':
            paren_state2=True
            break
        elif paren_state1 == False and paren_checker[i]==')':
            return "The parenthesis is not closed"
    print (paren_state1,paren_state2)
    if paren_state2 == False and paren_state1 == True:
        return "The parenthesis is not closed"
            

    #print(eval(user_expression))
    print(eval(user_expression))
    if eval(user_expression)==target_number:
            return "Correct"
    else:
        return "Try again! \n a possible solution:({}{}{}){}{}{}{}".format('number',correct_operators[0],'number',correct_operators[1],'number',correct_operators[2],'number')