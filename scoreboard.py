import tkinter as tk
import csv
from pathlib import Path
from tkinter import StringVar, ttk
from tkinter import messagebox
from tkinter.constants import NO
from tkinter.scrolledtext import ScrolledText
from arc_theme_ttk import themed_style

def sb_write(score):
    name=name_entry.get()
    # print(name_entry.get())
    # print(score)
    if name == "":
        return None
        
    ## Reading the previous records and inserting the new one inside
    ls=sb_read()
    ls.append([name,score])
    #print(("Initial: " + str(ls)))
    
    #Sorts the list from highest score to lowest
    ls.sort(key=lambda x:int(x[1]) ,reverse=True)
    #print(("Sorted: " +str(ls)))        

    #Updating the CSV file with the new score
    p = Path(__file__).with_name('leaderboard.csv')
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        for i in ls:
            #print(i)
            writer.writerow([i[0],i[1]])
            sb_update(ls)
            
#Function to read the CSV File
def sb_read():
    ls =  []
    p = Path(__file__).with_name('leaderboard.csv')
    with p.open('r',newline='',encoding='utf-8-sig') as f:
        reader= csv.reader(f)
        ls=list(reader)
        print(ls)
        return(ls)

#Function to update Scoreboard
def sb_update(ls):
    for record in scoreboard.get_children():
        scoreboard.delete(record)
    for i in range(len(ls)):
        scoreboard.insert('','end',values=[i+1, ls[i][0], ls[i][1] ])



def make_score_frame(root,score):
    #Variables
    global playerscore 
    playerscore= score
    global scoretext
    scoretext= "Your Score: " + str(playerscore)
    #Frame Setup
    frame = ttk.Frame(root)#padding="3 3 12 12"
    frame.pack(fill='both', expand='yes')

    #Scoreboard Label
    
    sblabel= ttk.Label(frame, text='Scoreboard', font='-size 20')
    sblabel.grid(column=0, row=0, columnspan=3, sticky=tk.NS,padx=130)

    #Scoreboard Treeview
    global scoreboard
    scoreboard = ttk.Treeview(frame, selectmode='none',columns=[1, 2, 3],displaycolumns=[1,2,3])
    scoreboard.heading(1, text='Rank')
    scoreboard.heading(2, text='Name')
    scoreboard.heading(3, text='Score')
    scoreboard.column('#0',width=0,stretch=NO,anchor='center')
    scoreboard.column(1,width=50,stretch=NO,anchor='center')
    scoreboard.column(2,width=100,anchor='center')
    scoreboard.column(3,width=50,stretch=NO,anchor='center')
    sb_update(sb_read())
    scoreboard.grid(column=0, row=1, columnspan=3,rowspan=3, sticky=(tk.NS))

    #Player Score Label
    
    scorelabel= ttk.Label(frame, text=scoretext, font='-size 10')
    scorelabel.grid(column=0, row=4,columnspan=3, sticky=(tk.NS),padx=20)

    #Player Name Label
    
    namelabel= ttk.Label(frame, text='Name:', font='-size 10')
    namelabel.grid(column=0, row=5, sticky=(tk.E))

    #Name input
    global name_entry
    name_entry = ttk.Entry(frame,width=7)
    name_entry.grid(column=1, row=5, sticky=(tk.EW))

    #Score Submit Button
    
    scorebutton = ttk.Button(frame, text="Submit", command=lambda arg1=playerscore: sb_write(arg1))
    scorebutton.grid(column=2, row=5, sticky=tk.W, padx=5, pady=5)

    




