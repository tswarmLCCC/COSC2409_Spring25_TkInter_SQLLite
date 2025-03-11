from sqlalchemy import create_engine,text
my_conn = create_engine("sqlite:///my_db.db") # fixed connection path
my_conn=my_conn.connect()

###### end of connection ####
r_set=my_conn.execute(text("SELECT count(*) as no from STUDENT"))
data_row=r_set.fetchone()
no_rec=data_row[0] # Total number of rows in table
limit = 8; # No of records to be shown per page.

##### tkinter window ######
import tkinter  as tk 
from tkinter import * 
my_w = tk.Tk()
my_w.geometry("350x200") 
def my_display(offset):    

    q="SELECT * from student LIMIT "+ str(offset) +","+str(limit)
    r_set=my_conn.execute(text(q));
    i=0 # row value inside the loop 
    for student in r_set: 
        for j in range(len(student)):
            e = Entry(my_w, width=10, fg='blue') 
            e.grid(row=i, column=j) 
            e.insert(END, student[j])
        i=i+1
    while (i==0):
        b2["state"]="active"  # enable Prev button
    else:
        b2["state"]="disabled"# disable Prev button      
my_display(0)        
my_w.mainloop()