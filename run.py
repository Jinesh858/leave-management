import sqlite3
from easygui import *
import tkinter.messagebox as tm
import random
import datetime as dt
from time import strftime
from tkinter import *



conn = sqlite3.connect('bvcoenm7.db')
cur=conn.cursor()
# conn.execute("CREATE TABLE balance (Emp_ID text,SL int,CL int,ML int)")
# conn.execute("CREATE TABLE status (leave_id int,Emp_ID text,leave text,Date1 text,Date2 text,days int,status text)")
# conn.execute('''CREATE TABLE employee (Emp_ID text,Name text,Contact_no text,Password text)''')

def manlogin():
    msg = "Enter Username and Password"
    title = "Login"
    fieldnames = ["Username","Password"]
    field = []
    field = multpasswordbox(msg,title,fieldnames)
    if(field[0]=='admin' and field[1]=='admin'):
        adminwindow()
    else:
        tm.showerror("Error info","Incorrect username or password")

    
def login():
    msg = "Enter Emp_ID and Password"
    title = "Login"
    fieldnames = ["Emp_ID","Password"]
    field = []
    field = multpasswordbox(msg,title,fieldnames)

    for row in conn.execute('SELECT * FROM employee'):
            if(field[0] == row[0] and field[1] == row[3]):
                global lgn
                lgn = field[0]
                f = 1
                print("Success")
                loginwindow()
                break
    if(not f):
            print("Invalid")
def logout():
    global lgn
    lgn = -1
    lwin.destroy()
def lstatus():
    global ls
    ls=[]
    for i in conn.execute('SELECT * FROM status where Emp_ID=?',lgn):
        ls=i

    statuswindow()
def allstatus():
    allwin=Toplevel(height=500,width=500,borderwidth=20)
    t = Text(allwin,font=36,fg='blue')
    for i in conn.execute('SELECT * FROM status where Emp_ID=?',lgn):
        t.insert(INSERT, i)
        t.insert(INSERT,'\n')

    t.pack()

def empinfowin():
    empinwin=Toplevel(height=500,width=500,borderwidth=20)
    t=Text(empinwin,font=36,fg='blue')
    for i in conn.execute('SELECT Emp_ID,Name,Contact_no FROM employee where Emp_ID=?',lgn):
        t.insert(INSERT,i)
        t.insert(INSERT,'\n')

    t.pack()

def allempinfowin():
    allempinwin=Toplevel(height=500,width=500,borderwidth=20)
    t=Text(allempinwin,font=36,fg='blue')
    for i in conn.execute('SELECT Emp_ID,Name,Contact_no FROM employee'):
        t.insert(INSERT,i)
        t.insert(INSERT,'\n')

    t.pack()
def statuswindow():
    stwin=Toplevel(height=500,width=500,borderwidth=20)
    label_1=Label(stwin,text="Employee ID=",fg="blue",justify=LEFT,font=("Helvetica", 16))
    label_2=Label(stwin,text=ls[1],font=("Helvetica", 16))
    label_3=Label(stwin,text="Type=",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_4=Label(stwin,text=ls[2],font=("Helvetica", 16))
    label_5=Label(stwin,text="start=",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_6=Label(stwin,text=ls[3],font=("Helvetica", 16))
    label_7=Label(stwin,text="end=",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_8=Label(stwin,text=ls[4],font=("Helvetica", 16))
    label_9=Label(stwin,text="Status:",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_10=Label(stwin,text=ls[6],font=("Helvetica", 16))
    label_11=Label(stwin,text="leave_id:",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_12=Label(stwin,text=ls[0],font=("Helvetica", 16))
    label_11.grid(row=0,column=0)
    label_12.grid(row=0,column=1)
    label_1.grid(row=1,column=0)
    label_2.grid(row=1,column=1)
    label_3.grid(row=2,column=0)
    label_4.grid(row=2,column=1)
    label_5.grid(row=3,column=0)
    label_6.grid(row=3,column=1)
    label_7.grid(row=4,column=0)
    label_8.grid(row=4,column=1)
    label_9.grid(row=5,column=0)
    label_10.grid(row=5,column=1)

        
def balance():
    global lgn
    check = (lgn,)
    global bl
    bl=[]
    for i in conn.execute('SELECT * FROM balance WHERE Emp_ID = ?',check):
        bl=i
    conn.commit()

    balancewindow()


def balancewindow():
    blwin=Toplevel(height=500,width=500,borderwidth=20)
    label_1=Label(blwin,text="Employee ID=",fg="blue",justify=LEFT,font=("Helvetica", 16))
    label_2=Label(blwin,text=bl[0],font=("Helvetica", 16))
    label_3=Label(blwin,text="Sick Leave=",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_4=Label(blwin,text=bl[1],font=("Helvetica", 16))
    label_5=Label(blwin,text="Casual Leave=",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_6=Label(blwin,text=bl[2],font=("Helvetica", 16))
    label_7=Label(blwin,text="Maternity Leave=",fg="blue",font=("Helvetica", 16),justify=LEFT)
    label_8=Label(blwin,text=bl[3],font=("Helvetica", 16))
    label_1.grid(row=0,column=0)
    label_2.grid(row=0,column=1)
    label_3.grid(row=1,column=0)
    label_4.grid(row=1,column=1)
    label_5.grid(row=2,column=0)
    label_6.grid(row=2,column=1)
    label_7.grid(row=3,column=0)
    label_8.grid(row=3,column=1)
    
        
def apply():
    msg = "Enter the following details "
    title = "Leave Apply"
    fieldNames = ["Emp_ID","From","To","Days"]
    fieldValues = []  
    fieldValues = multenterbox(msg,title, fieldNames)
    msg1 ="Select type of leave"
    title1 = "Type of leave"
    choices = ["CL","SL","ML"]
    choice = choicebox(msg1, title1, choices)
    leaveid=random.randint(1, 1000)


    
    conn.execute("INSERT INTO status(leave_id,Emp_ID,leave,Date1,Date2,days,status) VALUES (?,?,?,?,?,?,?)",(leaveid,fieldValues[0],choice,fieldValues[1],fieldValues[2],fieldValues[3],"Pending"))
    conn.commit()
    #for row in conn.execute("SELECT * FROM status"):
    #      print(row)

def approveleave():
    msg = "Enter leave_id"
    title = "leave approval"
    fieldNames = ["Leave_id"]
    fieldValues = []  
    fieldValues = multenterbox(msg,title, fieldNames)
    msg1 ="Approve/Deny"
    title1 = "leave approval"
    choices = ["approve","deny"]
    choice = choicebox(msg1, title1, choices)

    conn.execute("UPDATE status SET status = ? WHERE leave_id= ?",(choice,fieldValues[0]))
    conn.commit()
   # for row in conn.execute("SELECT * FROM status"):
   #       print(row)
    if(choice=='approve'):
        print(0)
        cur.execute("SELECT leave FROM status WHERE leave_id=?",(fieldValues[0],))
        row=cur.fetchall()
        col=row
            
        for row in conn.execute("SELECT Emp_ID FROM status WHERE leave_id=?",(fieldValues[0],)):
            print(2)
            tempid=row[0]

        for row in conn.execute("SELECT days FROM status WHERE leave_id=?",(fieldValues[0],)):
            print(2)
            tempdays=row[0]

        

        for row in conn.execute("SELECT SL from balance where Emp_ID=?",(tempid,)):
            bal=row[0]
            print(bal)

        for row in conn.execute("SELECT CL from balance where Emp_ID=?",(tempid,)):
            bal1=row[0]
            print(bal1)

        for row in conn.execute("SELECT ML from balance where Emp_ID=?",(tempid,)):
            bal2=row[0]
            print(bal2)

        if(col[0]==('SL',)):
            print(3)
            conn.execute("UPDATE balance SET SL =? WHERE Emp_ID= ?",((bal-tempdays),(tempid)))

        if(col[0]==('CL',)):
            print(3)
            conn.execute("UPDATE balance SET CL =? WHERE Emp_ID= ?",((bal1-tempdays),(tempid)))

        if(col[0]==('ML',)):
            print(3)
            conn.execute("UPDATE balance SET ML =? WHERE Emp_ID= ?",((bal2-tempdays),(tempid)))

        #cur.execute("DELETE FROM status WHERE leave_id=?",(fieldValues[0],))


                         
            #conn.commit()
            #print(4)
            #for row in conn.execute("SELECT SL FROM balance WHERE Emp_ID=?",(u'tempid',)):
             #   print(row)
            
       # if(temptype=='CL'):
        #    conn.execute("UPDATE balance SET CL = CL-1 WHERE Emp_ID= ?",(u'tempid',))
         #   conn.commit()
        #if(temptype=='ML'):
         #   conn.execute("UPDATE balance SET ML = ML-1 WHERE Emp_ID= ?",(u'tempid',))
          #  conn.commit()
            
def leavelist():
    lvlwin=Toplevel(height=500,width=500,borderwidth=20)
    t = Text(lvlwin,font=36,fg='blue')
    for i in conn.execute('SELECT * FROM status'):

        t.insert(INSERT, i)
        t.insert(INSERT,'\n')

    t.pack()

   
def registration():
    msg = "Enter Details of Employee"
    title = "Registration"
    fieldNames = ["Emp_ID", "Name", "Contact_no","Password"]
    fieldValues = []  
    fieldValues = multpasswordbox(msg,title, fieldNames)
    while 1:
      if fieldValues == None: break
      errmsg = ""
      for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
          errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
      if errmsg == "": break 
      fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
    conn.execute("INSERT INTO employee(Emp_ID,Name,Contact_no,Password) VALUES (?,?,?,?)",(fieldValues[0],fieldValues[1],fieldValues[2],fieldValues[3]))
    conn.execute("INSERT INTO balance(Emp_ID,SL,CL,ML) VALUES (?,?,?,?)",(fieldValues[0],12,12,50))
    conn.commit()
def loginwindow():
    #employee login window after successful login
    global lwin
    lwin=Toplevel()
    lwin.wm_attributes('-fullscreen','1')
    background_label=Label(lwin,image=filename)
    background_label.place(x=0,y=0,relwidth=1,relheight=1)
    empinfo=Button(lwin,text='MY INFORMATION',command=empinfowin,bd=10, relief=RAISED, fg="DARK ORANGE",bg="#ffffb3",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
    empinfo.pack(fill=X,expand=0.2)
    submit=Button(lwin,text='SUBMIT LEAVE',command=apply,bd=10, relief=RAISED, fg="DARK ORANGE",bg="#ffffb3",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
    submit.pack(fill=X,expand=0.2)
    leavebalance=Button(lwin,text='LEAVE BALANCE',command=balance,bd=10, relief=RAISED, fg="DARK ORANGE",bg="#ffffb3",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
    leavebalance.pack(fill=X,expand=0.2)
    leaveappstatus=Button(lwin,text='LAST LEAVE STATUS',command=lstatus,bd=10, relief=RAISED, fg="DARK ORANGE",bg="#ffffb3",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)

    leaveappstatus.pack(fill=X,expand=0.2)
    allleavestatus=Button(lwin,text='ALL LEAVE STATUS',command=allstatus,bd=10, relief=RAISED, fg="DARK ORANGE",bg="#ffffb3",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
    allleavestatus.pack(fill=X,expand=0.2)
    logoutbutton=Button(lwin,text='LOGOUT',command=logout,bd=10, relief=RAISED, fg="DARK ORANGE",bg="#ffffb3",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
    logoutbutton.pack(fill=X,expand=0.2)

def adminwindow():
    # Manager login window after successful login
    awin = Toplevel()
    awin.wm_attributes('-fullscreen', '1')
    background_label = Label(awin, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    empinfo = Button(awin, text='STAFF INFORMATION', command=allempinfowin, bd=25, relief=RAISED, fg="GREEN",
                     bg="#98fb98",
                     font=("ARIAL BLACK", 40, "bold"), pady=3)
    empinfo.pack(fill=X, expand=0.2)

    leavelistbtn = Button(awin, text='LEAVE APPROVAL LIST', command=leavelist, bd=25, relief=RAISED, fg="GREEN",
                          bg="#98fb98",
                          font=("ARIAL BLACK", 40, "bold"), pady=3)
    leavelistbtn.pack(fill=X, expand=0.2)

    approvebtn = Button(awin, text='APPROVE LEAVE', command=approveleave, bd=25, relief=RAISED, fg="GREEN",
                        bg="#98fb98",
                        font=("ARIAL BLACK", 40, "bold"), pady=3)
    approvebtn.pack(fill=X, expand=0.2)
    exitbutton = Button(awin, text='EXIT', command=awin.destroy, bd=25,
                        relief=RAISED, fg="GREEN", bg="#98fb98",
                        font=("ARIAL BLACK", 40, "bold"), pady=3)
    exitbutton.pack(fill=X, expand=0.2)
        
root=Tk()
root.wm_attributes('-fullscreen','1')
root.title("STAFF MANAGEMENT SYSTEM")
root.iconbitmap(default='logo.ico')
filename=PhotoImage(file="e6ffff.png")
background_label=Label(root,image=filename)
background_label.place(x=0,y=0,relwidth=1,relheight=1)
mainlabel=Label(root,text="STAFF MANAGEMENT SYSTEM", bd=20, relief=RAISED, fg="#710193", bg="#FFB6C1",
                  font=("ARIAL BLACK", 42, "bold"), pady=3)
mainlabel.pack(fill=X, expand=0.2)
def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text=string)
    lbl.after(1000, time)


# Styling the label widget so that clock
# will look more attractive
lbl = Label(root, font=('arial black', 40, 'bold'),
            background='#e6ffff',
            foreground='black')
date = dt.datetime.now()
label = Label(root, text=f"{date:%A, %B %d, %Y}", font="Calibri, 20",background='#e6ffff',
            foreground='black' )
label.pack(pady=15)

# Placing clock at the centre
# of the tkinter window
lbl.pack(anchor='center')
time()


manloginbutton=Button(root,text='ADMIN LOGIN',command=manlogin,bd=15, relief=RAISED, fg="#00008B",bg="#00FFFF",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
manloginbutton.pack(fill=X,expand=0.2)
loginbutton=Button(root,text='STAFF LOGIN',command=login,bd=15, relief=RAISED, fg="#00008B",bg="#00FFFF",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
loginbutton.pack(fill=X,expand=0.2)
empreg=Button(root,text='STAFF REGISTRATION',command=registration,bd=15, relief=RAISED, fg="#00008B",bg="#00FFFF",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
empreg.pack(fill=X,expand=0.2)
exitbutton=Button(root,text='EXIT',command=root.destroy,bd=15, relief=RAISED, fg="#00008B",bg="#00FFFF",
                           font=("ARIAL BLACK", 38, "bold"), pady=3)
exitbutton.pack(fill=X,expand=0.2)

root.mainloop()
