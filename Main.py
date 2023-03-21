
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from arc_theme_ttk import themed_style  #module we got online to make all GUI the same theme
import logic  # a module we created that is used to generate the numbers and validate user input
import threading #requires threading so that timer can run concurrently in the "background" 
#referenced: https://youtu.be/Mp6YMt8MSAU- for threading 
from time import *
from scoreboard import make_score_frame #scoreboard is a module we created to make the leaderboard GUI and also store past scores

#making the window
root = tk.Tk()
root.title('Mystery Six')
root.geometry('600x400')
root.resizable(0,0)
style = themed_style()



score=0 
hinted=False #needed for score system


#switch from start to main frame
def start_to_main():

    #remove previous frame which is start frame
    start_frame.pack_forget()

    #---------------creating scaffold(aka frames) to put the GUI elements------------------#


    #makes the main parent frame to contain all child frames
    global main_frame
    main_frame = ttk.Frame(root, padding=25)
    main_frame.pack(fill='both', expand='yes') 

    #making 4 child frames: each rep a row in the window ( width and height in pixels)
    #chose to create frame so that multiple related elements can be grouped together and displayed if needed

    global time_frame # to contain label for timer countdown
    time_frame = ttk.Frame(main_frame,width=500,height=300)
    time_frame.pack()

    global target_frame #to contain label for target number
    target_frame=ttk.Frame(main_frame,width=500,height=300)
    target_frame.pack()

    global numbers_frame # to contain a series of 6 number boxes 
    numbers_frame = ttk.Frame(main_frame,width=500,height=300)
    numbers_frame.pack()

    global input_frame  # to contain a label and input box for answer as well as submit button
    input_frame = ttk.Frame(main_frame,width=500,height=300)
    input_frame.pack()

    #----------------------------------end of scaffolding--------------------------------#

    #----------------------------------adding in GUI elements----------------------------#

    #create timer countdown label first so it can be updated in begin_timer function
    global time_label
    time_label = ttk.Label(time_frame, text="time",font=('Helvetica', 35))
    time_label.grid(row=0, sticky=tk.E, padx=5, pady=5,)


    begin_timer() #starts timer in background,updates the countdown timer label accordingly and switches screen to leaderboard when time runs out
    set_question_UI() #initializes and adds other GUI elements specific to the question (target number,number boxes,input box and submit button)
    

    
#creating numbers to be placed in UI for that specific qn    
def set_parameters():

    
    global six_num
    global target_num
    global correct_operators  #needed to be displayed in hint
    
    six_num=logic.generate_number()
    target_num,correct_operators=logic.generate_target_number(six_num)
    
#--------------------------functions to create individual UI elements-------------------------------#

#creates label to display target number
def target_UI():

    global target_label
    target_label = ttk.Label(target_frame, text=str(target_num),font=('Helvetica', 35))
    target_label.grid(row=0, sticky=tk.S, padx=5, pady=5,)

#dynalically creates 6 boxes, each containing a number, in a row                            
def numbers_6_UI(frame,num_list):
    frame.columnconfigure(0,weight=1)  #empty column at the left side 

    global number_label_list  #needed to update UI later on
    number_label_list=[] 

    #creating the 6 boxes             
    for i in range(1,len(num_list)+1):
                    
        frame.columnconfigure(i,weight=3)
            
        number_label = ttk.Label(frame, text=num_list[i-1],font=('Helvetica', 35),background="orange",foreground="white")
        number_label.grid(column=i, row=3, sticky=tk.W, padx=5, pady=5,)
        number_label_list.append(number_label)
                
    



#creates UI for input box and hint label            
def input_UI():
        
    #answer input
    global answer_label
    answer_label=tk.Label(input_frame, text="input your equation:")
    answer_label.grid(row=0,column=0, sticky=tk.W, padx=5, pady=5,)
    global answer_input
    answer_input = ttk.Entry(input_frame)
    answer_input.grid(row=0,column=1, sticky=tk.S, padx=5, pady=5,)
    global hint_label
    hint_label=ttk.Label(input_frame,text="")
    hint_label.grid(row=1, sticky=tk.S, padx=5, pady=5,)

#to be called when user press submit button and decides what to do based on the result
def update():
    global hinted
    global score
    print("user input:",answer_input.get())
    user_expression=answer_input.get()
    
    print(six_num)
    if (logic.check_expression(user_expression,six_num,target_num,correct_operators)=="Correct"):
        if(hinted):
            score+=50 
        else:
            score+=100
        new_question_set_UI()  #updates the UI for next question

    elif(logic.check_expression(user_expression,six_num,target_num,correct_operators)=="invalid"):
        hint_label.config(text="invalid")
                
    else:
        result=logic.check_expression(user_expression,six_num,target_num,correct_operators)
        hint_label.config(text=result)
        hinted=True 
                
        

def answer_UI():       #submit button
    global answer_button
    answer_button = ttk.Button(input_frame, text="Submit",command=lambda:update())
    answer_button.grid( row=0,column=2,sticky=tk.EW, padx=5, pady=5)
    



def skip_UI():  #skip button
    global skip_button
    skip_button=ttk.Button(input_frame, text="Skip",command=lambda:new_question_set_UI())
    skip_button.grid( row=5,sticky=tk.EW, padx=5, pady=5)        

def set_question_UI(): #initializes and adds other GUI elements specific to the question (target number,number boxes,input box and submit button)
    set_parameters()
    print("-------------first qn--------------")
    print(six_num,target_num,correct_operators)
    #create UIs for 6 number boxes, target number and input box
    numbers_6_UI(numbers_frame,six_num)
    target_UI()
    input_UI() 
    answer_UI() 
    skip_UI()  

def new_question_set_UI():  #called for subsequent qn (other than first qn) to update the existing UI elements
    print("current score:",score)
    print('---------new qn---------------')

    #generate new set of parameters for new qn
    set_parameters() 
    hinted=False

    #update respective UIs
    target_label.config(text=str(target_num))
    hint_label.config(text="")
    
    print("to check elements displayed correctly:",six_num,target_num,correct_operators)
    
    #update 6 numbers box UI
    for i in range(len(six_num)):
        number_label_list[i].config(text=str(six_num[i]))
    answer_input.delete(0, 'end')




    



    

#------------TIME functions(also updates frame when timer runs out)-------------------#


#creating this variable so that we can modify time limit easily, else we can always set it directly in the function
time_limit=40
def timer():
#introduce "global" keyword so that variable can be accessed out of the timer() function:
    global timing
    timing = time_limit 
#using for loop to constant revise timing 
    for i in range(timing):
        sleep(1) #sleep introduced to ensure 1 loop= 1s
        timing+=-1
 
        
#this statement updates time on UI, btw 0-10s, time text will turn red to warn user 
        if timing>0 and timing<11:
            time_label.config(text="Time remaining: {}s".format(timing),foreground= "red")
        elif timing>=11:
            time_label.config(text="Time remaining: {}s".format(timing),foreground= "green")
        elif timing==0:
            #swap to leaderboard frame when time's up
            main_frame.pack_forget()
            make_score_frame(root,score) 
            
#start running thread- this will run once button clicks aka command function for start button 
def begin_timer():
    timer_thread= threading.Thread(target= timer)
    timer_thread.start()

#-------------------------------DRIVER function----------------------------------------#


#makes start frame and upon clicking the start button, everything else continues from there based on user interaction with GUI


start_frame = ttk.Frame(root, padding=25)
start_frame.pack(fill='both', expand='yes')



start_label = ttk.Label(start_frame,text="""GAME INSTRUCTIONS:
1. 6 numbers will be generated.
2. Use these numbers to formulate an expressions consisting of the numbers, 
    brackets ( only '(' and ')' ) and operands ( +, - , * , / ) given.
    You do not have to use all the operands and numbers. 
3. You should only use the numbers once and operands can be repeated. 
4. Do not use numbers out of the six numbers displayed.
5. Do not put spacing between the numbers and operands.
You do not need to put the '=' sign after you have typed your expression, simply press 'enter'.

SCORING SYSTEM:
100 points if you get the expression correct without hints
50 points if you get the expression correct with the hints
0 points if you get it wrong
You have unlimited attempts for each question. 
You may choose to skip the question if you get stuck and no points be deducted.
You only have three minutes to solve the questions. Good luck and have fun!""")
start_label.grid(row=0, sticky=tk.W, padx=5, pady=5,)

start_button = ttk.Button(start_frame,text= "START", command=lambda:start_to_main())
start_button.grid(row=1, sticky=tk.NS, padx=5, pady=5,)

root.mainloop()
