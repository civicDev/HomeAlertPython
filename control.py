import time
import serial
from datetime import datetime
import MySQLdb
import sys
import RPi.GPIO as GPIO
from time import gmtime, strftime
from urllib import urlopen



# The script as below using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)

rel_curent = 25
rel_gaz = 9
rel_stingator = 8
rel_ventilatie = 7
rel_alarma = 11

led_r = 2
led_v = 3

alarm = 0

a_gaz = 0
a_foc = 0
a_cutremur = 0


# Set relay pins as output
GPIO.setup(rel_curent, GPIO.OUT)
GPIO.setup(rel_gaz, GPIO.OUT)
GPIO.setup(rel_stingator, GPIO.OUT)
GPIO.setup(rel_ventilatie, GPIO.OUT)
GPIO.setup(rel_alarma, GPIO.OUT)

GPIO.setup(led_r, GPIO.OUT)
GPIO.setup(led_v, GPIO.OUT)

GPIO.output(led_r, GPIO.LOW)
GPIO.output(led_v, GPIO.LOW)

con = MySQLdb.connect(host="localhost",user="root",passwd="motocicleta",db="proiect_isu")

cursor1 = con.cursor()
cursor2 = con.cursor()
cursor3 = con.cursor()
cursor4 = con.cursor()
cursor5 = con.cursor()

def get_alarm(token): 
   mess = urlopen("http://192.168.1.100/api.php?id=%s&phone=%s&lat=%s&lon=%s&msg=%s"%(1,1,1,1,1))
   print mess

while True:
    
    with con:
        cursor2.execute("SELECT * FROM `data` ORDER BY `Id` DESC LIMIT 1")
        real_value = cursor2.fetchone()
        
        token = real_value[2]
        real_humidity = float(real_value[3])
        real_temp = float(real_value[4])
        real_gas = float(real_value[5]) 
        real_air = float(real_value[6])
        real_motion = float(real_value[7])
        real_co2 = float(real_value[8])
    
        cursor1.execute("SELECT * FROM `default_values` WHERE `Id`='1'")
        default_values = cursor1.fetchone()
        
     
        default_humidity = float(default_values[1])
        default_temp = float(default_values[2])
        default_butan_gas = float(default_values[3])
        default_air = float(default_values[4])
        default_motion = float(default_values[5])
        default_co2 = float(default_values[6])
        
        
        print "\n"
        print " DEFAULT------>  Humidity : ",default_humidity,", Temperature : ",default_temp,", Butan Gas : ",default_butan_gas,", Air Quality : ",default_air,", Motion : ",default_motion,", CO2 : ",default_co2
        print " REAL------>  Humidity : ",real_humidity,", Temperature : ",real_temp,", Butan Gas : ",real_gas,", Air Quality : ",real_air,", Motion : ",real_motion,", CO2 : ",real_co2
        print "\n"
        
        
        #-----------------------------------------------------------GAZ---------------------------------------------------------------------------------------
        
        #real_gas = 250
        
        #scapari de gaze 
        if(real_gas > default_butan_gas):
          
          #led_debug
          alarm = 1;
          a_gaz = 1
          
          print("Gaz Oprit")
          cursor3.execute("UPDATE `alarm` SET `al_gaz` = '1' WHERE `Id` = '1'")
          with con:
              #print "SELECT * FROM `log_alert` WHERE `token` = %s"%(token) 
              cursor4.execute("SELECT * FROM `log_alert` WHERE `token` = '%s'"%(token))
              num_row = cursor4.rowcount
              
              print num_row
              
              if(num_row == 0):
                msg_text = "Buna ziua, alerta de scapare de gaze in locuinta dumneavastra! Sa activat automat protectia si este alertat 112!"
                msg_email = 'Buna ziua, alerta de scapare de gaze in locuinta dumneavastra! Sa activat automat protectia si este alertat 112!'
                #print "INSERT INTO log_alert(token,m_sms,m_email,sent) VALUES('" + token + "','" + '" + msg_text +"' + "','" + 'Mesaje Email.' + "','" + '0' + "')"
                cursor5.execute("INSERT INTO log_alert(token,m_sms,m_email,sent) VALUES('%s','%s','%s','%s')"%(token,msg_text,msg_email,0))
                print "Se face scrierea"
          
        else:
          
          #led_debug
          alarm = 0;
          a_gaz = 0
          
          print("Gaz Pornit")
          cursor1.execute("UPDATE `alarm` SET `al_gaz` = '0' WHERE `Id` = '1'")
          
          
          #-----------------------------------------------------------GAZ---------------------------------------------------------------------------------------
          
        
        
        #-----------------------------------------------------------INCENDIU---------------------------------------------------------------------------------------
        
        #real_co2 = 300
        #incendiu
        if(real_co2 > default_co2):
          
          #led_debug
          alarm = 1;
          a_foc = 1
          
          print("Stingator pornit curent oprit")
          cursor3.execute("UPDATE `alarm` SET `al_foc` = '1' WHERE `Id` = '1'")
          
          with con:
              #print "SELECT * FROM `log_alert` WHERE `token` = %s"%(token)
              cursor4.execute("SELECT * FROM `log_alert` WHERE `token` = '%s'"%(token))
              num_row = cursor4.rowcount
              
              print num_row
              if(num_row == 0):
                msg_text = "Buna ziua, alerta de incendiu in locuinta dumneavastra! Sa activat automat protectia si este alertat 112!"
                msg_email = 'Buna ziua, alerta de incendiu de gaze in locuinta dumneavastra! Sa activat automat protectia si este alertat 112!'
                #print "INSERT INTO log_alert(token,m_sms,m_email,sent) VALUES('" + token + "','" + '" + msg_text +"' + "','" + 'Mesaje Email.' + "','" + '0' + "')"
                cursor5.execute("INSERT INTO log_alert(token,m_sms,m_email,sent) VALUES('%s','%s','%s','%s')"%(token,msg_text,msg_email,0))
                print "Se face scrierea"
            
        else:
          
          #led_debug
          alarm = 0;
          a_foc = 0
          
          print("Stingator oprit curent pornit")
          cursor3.execute("UPDATE `alarm` SET `al_foc` = '0' WHERE `Id` = '1'")
          
        #-----------------------------------------------------------INCENDIU---------------------------------------------------------------------------------------
        
        
        #-----------------------------------------------------------CUTREMUR---------------------------------------------------------------------------------------
        
        #cutremur  
        if(real_motion > default_motion):
          
          print("curent oprit gaz oprit")
         #led_debug
          alarm = 1;
          a_cutremur = 1
          
          print("Curent oprit gaz oprit")
          cursor3.execute("UPDATE `alarm` SET `al_foc` = '1' WHERE `Id` = '1'")
          
          with con:
              cursor4.execute("SELECT * FROM `log_alert` WHERE `token` = '%s'"%(token))
              num_row = cursor4.rowcount
              
              if(num_row == 0):
                msg_text = "Buna ziua, cutremur in locuinta dumneavastra! Sa activat automat protectia si este alertat 112!"
                msg_email = 'Buna ziua, cutremur in locuinta dumneavastra! Sa activat automat protectia si este alertat 112!'
                #print "INSERT INTO log_alert(token,m_sms,m_email,sent) VALUES('" + token + "','" + '" + msg_text +"' + "','" + 'Mesaje Email.' + "','" + '0' + "')"
                cursor5.execute("INSERT INTO log_alert(token,m_sms,m_email,sent) VALUES('%s','%s','%s','%s')"%(token,msg_text,msg_email,0))
                print "Se face scrierea"
            
        else:
          alarm = 0;
          a_cutremur = 0
          
          
          print("Curent pornit gaz pornit") 
          cursor3.execute("UPDATE `alarm` SET `al_cutremur` = '0' WHERE `Id` = '1'")
          
        if(alarm == 1):
          GPIO.output(led_r, GPIO.HIGH)
          GPIO.output(led_v, GPIO.LOW)
        else:
          GPIO.output(led_r, GPIO.LOW)
          GPIO.output(led_v, GPIO.HIGH)
          
        
        if(a_foc == 1 or a_cutremur == 1 or a_gaz == 1):
           print "-------> Actiune cutremur si foc"
           GPIO.output(rel_gaz, GPIO.LOW)
           GPIO.output(rel_stingator, GPIO.HIGH)
           GPIO.output(rel_curent, GPIO.LOW)
           GPIO.output(rel_alarma, GPIO.HIGH)
           GPIO.output(rel_ventilatie, GPIO.HIGH)
           get_alarm(token)
        else:
           GPIO.output(rel_gaz, GPIO.HIGH)
           GPIO.output(rel_stingator, GPIO.LOW)
           GPIO.output(rel_curent, GPIO.HIGH)
           GPIO.output(rel_alarma, GPIO.LOW)
           GPIO.output(rel_ventilatie, GPIO.HIGH)
           
     
          
        
        print "\n"
        #-----------------------------------------------------------CUTREMUR---------------------------------------------------------------------------------------
        
        time.sleep(0.5)
        
        
        