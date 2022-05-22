import smtplib
from datetime import datetime
now=datetime.now()
def sendM(receiver_mail):
    print(receiver_mail)
    print(type(receiver_mail))
    server = smtplib.SMTP('smtp.gmail.com', port=25)
    server.starttls()
    server.login('bs1030614@gmail.com','shrusou@123')
    dat=now.strftime("%Y-%m-%d %H:%M:%S")
    st='you have not attended class on 29-03-2022 '
    server.sendmail('bs1030614@gmail.com',receiver_mail,st)
    print('Mail sent')

#sendM('2GI19CS150@students.git.edu')