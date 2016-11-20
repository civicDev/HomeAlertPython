import time
import serial
from datetime import datetime
import MySQLdb
import sys
import RPi.GPIO as GPIO
from time import gmtime, strftime


sensors = serial.Serial(
   port='/dev/ttyACM1',
   baudrate = 115200,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=0.5
)

con = MySQLdb.connect(host="192.168.1.101",user="root",passwd="motocicleta",db="proiect_isu")

while 1:
      #readSms  =  sms.readline()
      #print readSms
      #sms.write("OR/0758576470/TEXT")
      readSensors = sensors.readline()
      data = readSensors
      date_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
      #print data
      if len(data) > 1 :
        #print data 
        validData = data.split("/")
        #print validData
        if len(validData) > 6 :
        
          token = validData[0]
          humidity = float(validData[1])
          temp = float(validData[2])
          butan_gas = float(validData[3])
          air = float(validData[4])
          motion = float(validData[5])
          co2 = float(validData[6])
        
          #print "INSERT INTO data(date_time,token,humidity,temp,butan_gas,atm_quality,motion,co) VALUES('" + date_time + "','" + token + "','" + str(humidity) + "','" + str(temp) + "','" + str(butan_gas) + "','" + str(air) + "','" + str(motion) + "','" + str(co2) + "')"
          print "Token",token," Humidity : ",humidity,", Temperature : ",temp,", Butan Gas : ",butan_gas,", Air Quality : ",air,", Motion : ",motion,", CO2 : ",co2
          
          try:
              cursor1 = con.cursor()
              #cursor1.execute("INSERT INTO data(date_time,token,humidity,temp,butan_gas,atm_quality,motion,co) VALUES('" + date_time + "','" + token + "','" + str(humidity) + "','" + str(temp) + "','" + str(butan_gas) + "','" + str(air) + "','" + str(motion) + "','" + str(co2) + "')")  
              sql = "INSERT INTO data(date_time,token,humidity,temp,butan_gas,atm_quality,motion,co) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(date_time,token,str(humidity),str(temp),str(butan_gas),str(air),str(motion),str(co2))
              print sql
              if(cursor1.execute(sql)):
                print "baga"
              else: 
                print "nu baga"
          except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)      