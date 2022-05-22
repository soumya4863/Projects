from sqlite3 import Cursor
from time import strftime
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.anchorlayout import AnchorLayout
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from mail import sendM
from kivy.metrics import dp
from datetime import datetime
from kivy.uix.button import Button
from kivymd.uix.datatables import MDDataTable
from kivy.uix.dropdown import DropDown  
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.snackbar import Snackbar
from attendanceTrial import record
from cam2Working import capture1,capture
import matplotlib.pyplot as plt
from attendanceTrial import get_cur_hr
from attendanceTrial import get_cur_time
import numpy as np
import mysql.connector
from sql_connection import get_sql_connection
from datetime import date
layout=None
graph = None
field = None
class IconListItem(Button):
    pass
#database connection

Clock.max_iteration = 30
Window.size = (350,580)

class LoginPage(MDApp):
    dialog = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attendance_1 = Builder.load_file("attendance_1.kv")
        self.attendance_2 = Builder.load_file("attendance_2.kv")
        self.screen = Builder.load_file("report.kv")
        self.screen2 = Builder.load_file("report2.kv")
        self.view_report_1 = Builder.load_file("view_report_1.kv")
        self.view_report_2 = Builder.load_file("view_report_2.kv")
        
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        classes = ["class1","class2","class3","class4","class5","class6","class7","class8","class9","class10"]
        courses = ["English","Hindi","Marathi","Maths","EVS","Social Studies","Science","Sanskrit","Arts"]


        self.menu = DropDown()  
        for index in range(12):  
    
            btton = Button(text =months[index], size_hint_y = None, height = 40,background_normal="",background_color="#ffffff",color="#000000")  
            
            btton.bind(on_release = lambda btton: self.menu.select(btton.text))  
            
            self.menu.add_widget(btton) 
        self.menu.bind(on_select = lambda instance, x: self.changeText(x)) 

        self.menu2 = DropDown()  
        for index in range(8):  
    
            btton = Button(text =classes[index], size_hint_y = None, height = 40,background_normal="",background_color="#ffffff",color="#000000")  
            
            btton.bind(on_release = lambda btton: self.menu2.select(btton.text))  
            
            self.menu2.add_widget(btton) 
        self.menu2.bind(on_select = lambda instance, x: self.changeText(x)) 

        self.menu3 = DropDown()  
        for index in range(12):  
    
            btton = Button(text =months[index], size_hint_y = None, height = 40,background_normal="",background_color="#ffffff",color="#000000")  
            
            btton.bind(on_release = lambda btton: self.menu3.select(btton.text))  
            
            self.menu3.add_widget(btton) 
        self.menu3.bind(on_select = lambda instance, x: self.changeText(x))

        self.menu4 = DropDown()  
        for index in range(10):  
    
            btton = Button(text =classes[index], size_hint_y = None, height = 40,background_normal="",background_color="#ffffff",color="#000000")  
            
            btton.bind(on_release = lambda btton: self.menu4.select(btton.text))  
            
            self.menu4.add_widget(btton) 
        self.menu4.bind(on_select = lambda instance, x: self.changeText(x)) 

        self.menu5 = DropDown()  
        for index in range(9):  
    
            btton = Button(text =courses[index], size_hint_y = None, height = 40,background_normal="",background_color="#ffffff",color="#000000")  
            
            btton.bind(on_release = lambda btton: self.menu5.select(btton.text))  
            
            self.menu5.add_widget(btton) 
        self.menu5.bind(on_select = lambda instance, x: self.changeText(x)) 

    def addMonth(inst,f,menu):
        global field
        field = f
        menu.open(field) 

    def changeText(self,x):
        field.text =  x   





    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("pre-splash.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("Adlogin.kv"))
        screen_manager.add_widget(Builder.load_file("AdDash.kv"))
        screen_manager.add_widget(Builder.load_file("tDash.kv"))
        screen_manager.add_widget(Builder.load_file("attendance.kv"))
        screen_manager.add_widget(Builder.load_file("addT.kv"))
        screen_manager.add_widget(Builder.load_file("addS.kv"))
        screen_manager.add_widget(self.attendance_1)
        screen_manager.add_widget(self.attendance_2)
        screen_manager.add_widget(self.screen)
        screen_manager.add_widget(self.screen2)
        screen_manager.add_widget(self.view_report_1)
        screen_manager.add_widget(self.view_report_2)
        return screen_manager

    #teacher login verification
    def verify_tdata(self,username,password):

        #Get Data
        connection=get_sql_connection()
        cursor=connection.cursor()
        cursor.execute("select * from tlogin")
        user_list = []

        #Get Specific column like email or password
        for i in cursor.fetchall():
            user_list.append(i[0])

        #Verify username And Password
        if username in user_list and username!="":
            cursor.execute(f"select password from tlogin where username='{username}'")
            for j in cursor:
                if password == j[0]:
                    screen_manager.current = "tDash"
                    screen_manager.transition.direction = "left"
                    
                elif password == "":
                    self.callback("Login","Please enter the password")

                else:
                    self.callback("Login","Invalid Password")

        elif username == "":
            if password == "":
                self.callback("Login","Please enter the username and password")
            else:
                self.callback("Login","Please enter the username")

        else:
            if password == "":
                self.callback("Login","Please enter the password")
            else:
                self.callback("Login","Invalid username")  

    #admin login verification
    def verify_adata(self,username,password):

        #Get Data
        connection=get_sql_connection()
        cursor=connection.cursor()
        cursor.execute("select * from adlogin")
        user_list = []

        #Get Specific column like email or password
        for i in cursor.fetchall():
            user_list.append(i[0])

        #Verify username And Password
        if username in user_list and username!="":
            cursor.execute(f"select password from adlogin where username='{username}'")
            for j in cursor:
                if password == j[0]:
                    screen_manager.current = "AdDash"
                    screen_manager.transition.direction = "left"
                    
                elif password == "":
                    self.callback("Login","Please enter the password")

                else:
                    self.callback("Login","Invalid Password")

        elif username == "":
            if password == "":
                self.callback("Login","Please enter the username and password")
            else:
                self.callback("Login","Please enter the username")

        else:
            if password == "":
                self.callback("Login","Please enter the password")
            else:
                self.callback("Login","Invalid username")  

    #Take Attendance
    #upload image
    def upload(self,process_status):
        process_status.text=""
        res=capture1()
        self.callback("Status",res)

    #record attendance  
    def record_att(self,process_status,class1,Course,grade):
        classes=["class1","class2","class3","class4","class5","class6","class7","class8","class9","class10"]
        courses=[]
        curhr=get_cur_hr()
        dat=date.today()
        query='''select courses from schoolattendance.classes where classes.class=%s'''
        connection=get_sql_connection()
        cursor=connection.cursor()
        cursor.execute(query,(class1.text,))
        courses=cursor.fetchall()
        text1=""
        if (Course.text.upper(),) not in courses or class1.text not in classes:
            self.callback("Status","The details entered are invalid")
            process_status.text=""

        else:
            process_status.text=""
            text1=record(class1.text,Course.text,grade.text)
            self.callback("Status",text1)

       
        
    def mark_absent(self,class1,Course,grade):

    #mark absent students
        curhr=get_cur_hr()
        dat=date.today()
        studentsList=[]
        attendedStudentList=[]
        absentList=[]
            
        
        query='''select student.studentID from schoolattendance.student where student.class=%s and student.grades=%s'''
        data=(class1.text,grade.text)
        connection=get_sql_connection()
        cursor=connection.cursor()
        cursor.execute(query,data)
        studentsList=cursor.fetchall()

        query='''select student.studentID from schoolattendance.studentatt,schoolattendance.student where student.class=%s and student.grades=%s and studentatt.studentID=student.studentID and hour(studentatt.datetime)=%s and date(studentatt.datetime)=%s'''
        data=(class1.text,grade.text,curhr,dat)
        cursor.execute(query,data)
        attendedStudentList=cursor.fetchall()

        for x in studentsList:
            if x not in attendedStudentList:
                absentList.append(x[0])
            emailList=[]
            if absentList!=[]:
                for x in absentList:
                    query='''select student.email from student where student.studentID=%s'''
                    cursor.execute(query,(x,))
                    y=cursor.fetchall()
                    emailList.append(y[0])
                print(emailList)
                for x in emailList:
                    sendM(x[0])
            print(studentsList)
            print(absentList)
            print(attendedStudentList)

    #Add Teacher
    def addT(self,username,password):
        connection=get_sql_connection()
        cursor=connection.cursor()
        cursor.execute("select * from tlogin")
        user_list = []
        for i in cursor.fetchall():
            user_list.append(i[0])
            
        if username in user_list:
            self.callback("Add Teacher","The Username is already taken")
            
        else:
            if username == "" and password == "":
                self.callback("Add Teacher","Username and Password fields are empty")

            elif password == "":
                self.callback("Add Teacher","Enter the password")

            elif username == "":
                self.callback("Add Teacher","Enter the username")

            else:
                query = ("INSERT INTO schoolattendance.tlogin "
                    "(username, password)"
                    "VALUES (%s, %s)")
                data = (username,password)
                cursor.execute(query, data)
                connection.commit()
                self.callback("Add Teacher","Details are added Successfully")

    #Add Student
    #add student details
    def addS(self,name,rollno,class1,grade,email):
            
        if name =="" and rollno == "" and class1 =="":
            self.callback("Add Student","Fill out the details")
        elif name == "":
            self.callback("Add Student","Enter the name")
        elif rollno == "":
            self.callback("Add Student","Enter the roll number")
        elif class1 == "":
            self.callback("Add Student","Enter the class")
        elif grade == "":
            self.callback("Add Student","Enter the grade")
        elif email == "":
            self.callback("Add Student","Enter the email")
        else:
            query = ("INSERT INTO schoolattendance.student "
                "(studentID, studentName,class,grades,email)"
                "VALUES (%s, %s, %s,%s,%s)")
            data = (rollno,name,class1,grade,email)
            connection=get_sql_connection()
            cursor=connection.cursor()
            cursor.execute(query, data)
            connection.commit()
            self.callback("Add Student","Details are added Successfully")

    #upload student image
    def supload(self,process_status,name,rollno):
        process_status.text=""
        res=capture(name,rollno)
        self.callback("Status",res)

    #View Attendance
    def addDataTable(self,Class,course,date,manager):
        global layout
        if(Class.text != "Class" and course.text != "Course" and date.text != "Select Date"):
            if(layout):
                self.attendance_2.ids.attendance_box.remove_widget(layout) 
            connection=get_sql_connection()
            cursor=connection.cursor()
            
            query='''select attendance.studentID,attendance.studentName,attendance.grade,time(attendance.datetime) from schoolattendance.attendance where date(attendance.datetime)=%s and attendance.class=%s and attendance.course=%s '''
            cursor.execute(query,(date.text,Class.text,course.text.lower()))
            row_data=[]
            layout = AnchorLayout()
            data_table = MDDataTable(
                size_hint=(0.9,1),
                column_data=[
                    ("[color=#088FF7]Id[/color]", dp(20)),
                    ("[color=#088FF7]Name[/color]", dp(30)),
                    ("[color=#088FF7]Grade[/color]", dp(30)),
                    ("[color=#088FF7]Time[/color]", dp(30)),
                ],
                row_data=cursor.fetchall()
            )
            layout.add_widget(data_table)
            self.attendance_2.ids.attendance_box.add_widget(layout) 
            manager.transition.direction = "left"
            manager.current = "attendance_2"
        else:
            Snackbar(
                text="[color=#F62727]Please Fill Up All The Fields ![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                    Window.width - (dp(10) * 2)
                ) / Window.width
            ).open()    

    def on_save(self, instance, value, date_range):
        self.attendance_1.ids.datePicketBtn.text = str(value)

    def show_date_picker(self):
        currentDateTime = datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        date_dialog = MDDatePicker(min_year=year, max_year=year)
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()   

    #view report
    def addGraph(self,id,field,manager):
        global graph

        if(id.text and field.text != "Month"):
            if(graph):
                self.view_report_1.ids.box.remove_widget(graph)

            # Add the SQL query here and change these arrays  

            x = np.array(["A", "B", "C", "D", "E", "F", "G", "H","I"])
            y = np.array([10,20,90,22,34,56,78,82,100])

            plt.xlabel("No. of classes attended (%)")
            plt.bar(x,y,width=0.5,color="#088FF7")
            graph = FigureCanvasKivyAgg(plt.gcf())
            self.view_report_1.ids.box.add_widget(graph) 
            manager.transition.direction = "left"
            manager.current = "view_report_1"
        else:
            Snackbar(
                text="[color=#F62727]Please Fill Up All The Fields ![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                    Window.width - (dp(10) * 2)
                ) / Window.width
            ).open()     

    def addGraph_2(self,id,field,manager):
        global graph

        if(id.text and field.text != "Month"):
            if(graph):
                self.view_report_1.ids.box.remove_widget(graph)

            # Add the SQL query here and change these arrays

            x = np.array(["A", "B", "C", "D", "E", "F", "G", "H","I"])
            y = np.array([10,20,90,22,34,56,78,82,100])

            plt.xlabel("Avg. No. of students (%)")
            plt.bar(x,y,width=0.5,color="#088FF7")
            graph = FigureCanvasKivyAgg(plt.gcf())
            self.view_report_2.ids.box.add_widget(graph) 
            manager.transition.direction = "left"
            manager.current = "view_report_2"
        else:
            Snackbar(
                text="[color=#F62727]Please Fill Up All The Fields ![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                    Window.width - (dp(10) * 2)
                ) / Window.width
            ).open()              


    def callback(self,title,text) :
        # create dialog
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="Ok", text_color=self.theme_cls.primary_color,
                    on_press=self.close
                ),
            ],
        )
        # open and display dialog
        self.dialog.open()
     
                    
    def close(self, instance):
        # close dialog
        self.dialog.dismiss()

    def on_start(self):
        Clock.schedule_once(self.login,4)

    def login(self,*args):
        screen_manager.current = "login"

if __name__ == "__main__":
    LoginPage().run()


