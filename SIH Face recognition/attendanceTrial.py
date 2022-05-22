import face_recognition 
import cv2 
import numpy as np
import os
from datetime import datetime
import mysql.connector
from datetime import date

from sql_connection import get_sql_connection


now=datetime.now()
attendanceNames=[]
attend=[]

def get_cur_hr():
    hr=now.strftime("%H")
    print(hr)
    return hr

def get_cur_time():
    time=now.strftime("%H:%M:%S")
    print(time)
    return time
get_cur_hr()
get_cur_time()

def take_attendance():

    path='loginPage/images'
    images = []
    personNames = []
    myList = os.listdir(path)
    print(myList)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])
    print(personNames)

    def faceEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = faceEncodings(images)


    testpath='loginPage/test'
    
    myTestList=os.listdir(testpath)
    todayImages=[]
    for cu_img in myTestList:
        todayImages.append(os.path.splitext(cu_img)[0])
    print(todayImages)
    for img in todayImages:
        img1=img
        val=img1.split('_')
        dat=now.strftime("%Y-%m-%d")
        if val[0]==dat:
            tm=val[1].split('-')
            hr=tm[0]
            curhr=now.strftime("%H")
            if hr==curhr:
                attend.append(img)
    print(attend)
    testList=[]
    for x in attend:
        x=x+'.png'
        testList.append(x)

    print(testList)

    for test_img in testList:
        imgtest=face_recognition.load_image_file(f'{testpath}/{test_img}')

        facesCurrentFrame = face_recognition.face_locations(imgtest)
        encodesCurrentFrame = face_recognition.face_encodings(imgtest, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace,tolerance=0.55)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
                print(name)
                attendanceNames.append(name)

    return attendanceNames

def record(class_val,course_val,grade_val):
    dat=now.strftime("%Y-%m-%d")
    curhr=now.strftime("%H")
    checkList1=[]
    checkforcourse=(class_val,course_val,grade_val)
    connection=get_sql_connection()
    cursor=connection.cursor()

    #check whether two courses are taken in same hour for same class and grade
    query='''select courseatt.class, courseatt.course,courseatt.grades from schoolattendance.courseatt where hour(courseatt.datetime)=%s and date(courseatt.datetime)=%s'''
    cursor.execute(query,(curhr,dat))
    checkList1=cursor.fetchall()
    if (class_val,course_val,grade_val)  in checkList1:
            return "Two courses cannot be taken in same hour of the class"    
    
    studentId=[]
    studentName=[]
    markId=[]
    markName=[]
    y=[]
    namesList=take_attendance()  
    for x in namesList:
        y=x.split('_')
        studentId.append(y[0])
        studentName.append(y[1])
    print(studentId)
    print(studentName)
    
    #select only the photos of students taken in same hour
    query = '''SELECT studentatt.studentID FROM schoolattendance.studentatt where hour(studentatt.datetime)=%s and date(studentatt.datetime)=%s'''
    data = (curhr,dat)
    cursor.execute(query,data)
    rows=cursor.fetchall()
    
    ids=[]
    print(rows)
    
    for row in rows:
        ids.append(row[0])
    print(ids)
    
    #did not upload photo/Photo taken twice 
    for x in studentId:
        if int(x) not in ids:
           markId.append(x)
           markName.append(studentName[studentId.index(x)])
           ids.append(int(x))
    print(markId)
    print(markName)
    if len(markId)==0:
        return "did not upload photo/Photo taken twice  "
    

    else:

        #check whether all students belong to selected class
        studclass=[]
        markclass=[]
        markgrade=[]
        for x in markId:
            query='''select student.class from schoolattendance.student where student.studentID=%s '''
            cursor.execute(query,(x,))
            studclass=cursor.fetchall()

        print(studclass)
        
        print(grade_val)

        for x in studclass:
            markclass.append(x[0])
            

        for x in markId:
            query='''select student.grades from schoolattendance.student where student.studentID=%s '''
            cursor.execute(query,(x,))
            studclass=cursor.fetchall()

        print(studclass)
        
        print(grade_val)

        for x in studclass:
            markgrade.append(x[0])
            

        print(markclass)
        print(markgrade)
        if markclass.count(markclass[0]) !=len(markclass) or markgrade.count(markgrade[0])!=len(markgrade):
            return "all student doesnot belong to same class/section"
        elif class_val!=markclass[0] or grade_val!=markgrade[0]:
            print(markclass[0],class_val)
            print(markgrade[0],grade_val)
            return "The students in the photo donot belong to the mentioned class"
        
        else:
            #insert into courseatt
            query='''insert into schoolattendance.courseatt(class,course,date,datetime,grades) values(%s,%s,%s,%s,%s)'''
            course_data=(class_val,course_val,date.today(),datetime.now(),grade_val)
            cursor.execute(query,course_data)
            connection.commit()
            #insert into studentatt

            for i in range(len(markId)):
                query = ("INSERT INTO schoolattendance.studentatt "
                    "(studentID, studentName, datetime)"
                    "VALUES (%s, %s,%s)")
                data = (markId[i], markName[i], datetime.now())
                cursor.execute(query, data)
                connection.commit()
            
            #insert into attendance
            
            #query='''#SELECT studentatt.studentID,studentatt.studentName,courseatt.course,courseatt.class,courseatt.grade from schoolattendance.studentatt,schoolattendance.courseatt where hour(studentatt.datetime)= hour(courseatt.datetime) and date(studentatt.datetime)= date(courseatt.datetime) and hour(courseatt.datetime)=%s and date(courseatt.datetime)=%s  '''
            #cursor.execute(query,(curhr,dat))
            '''
            row1=[]
            row1=cursor.fetchall()
            print(row1)
            print()
            rows=[]
            for i in row1:
                if i not in rows:
                    rows.append(i)
            print(rows)
            '''
            
            
            for i in range(len(markId)):
                query = ("INSERT INTO schoolattendance.attendance "
                    "(studentID, studentName, class,course,datetime,grade)"
                    "VALUES (%s, %s,%s,%s,%s,%s)")
                data = (markId[i],markName[i],class_val,course_val,datetime.now(),grade_val)
                cursor.execute(query, data)
                connection.commit()
            return "Attendance taken successfully"
        
