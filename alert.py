import time
import serial
from datetime import datetime
import MySQLdb
import sys
import RPi.GPIO as GPIO
from time import gmtime, strftime

con = MySQLdb.connect(host="localhost",user="root",passwd="motocicleta",db="proiect_isu")
cursor = con.cursor()
cursor1 = con.cursor()
cursor2 = con.cursor()



def send_email(recipient, subject, body):
    import smtplib

    gmail_user = "isu.romania@gmail.com"
    gmail_pwd = "motocicleta123"
    FROM = "isu.romania@gmail.com"
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


def send_sms(msg_serial):
    sms = serial.Serial(
           port='/dev/ttyACM0',
           baudrate = 9600,
           parity=serial.PARITY_NONE,
           stopbits=serial.STOPBITS_ONE,
           bytesize=serial.EIGHTBITS,
           timeout=1
        )
    time.sleep(15)
    sms.write(msg_serial)
    
    

#send_sms("OK;0758576470;1233322erererere")


while 1:
 with con:
      cursor.execute("SELECT * FROM `log_alert` WHERE `sent`='0'")
      num = cursor.rowcount
      alert = cursor.fetchone()
      
      print alert
      
      if(num > 0):
          id_alert = alert[0]
          token = alert[1]
          m_sms = alert[2]
          m_email = alert[3]
          
          cursor1.execute("SELECT * FROM `user` WHERE `token`= %s",(token))
          user = cursor1.fetchall()
          
          for d_user in user:
            #print user
            email = d_user[2]
            number = d_user[4]
            
            sms_message = "OK;%s;%s"%(number,m_sms)
            send_sms(sms_message)
            send_email(email, "HOME ALERT IMPORTANT", m_email)
            time.sleep(10)
            
          print "UPDATE `log_alert` SET `sent` = '1' WHERE `Id` = %s"%(id_alert)
          cursor2.execute("UPDATE `log_alert` SET `sent` = '1' WHERE `Id` = %s"%(id_alert)) 
          
      time.sleep(0.5)  
      
  
  
  
  
  
  
  
  
        
