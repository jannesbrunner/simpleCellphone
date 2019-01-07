# This little script just test the connection and comminicuation with the SIM868 chip

import serial
import time

ser = serial.Serial("COM6",9600) #ttyS0 is the port on the Pi3, it may be ttyAMA0 on the older Pi's. 
# Set it to COMX (e.g. COM6) on a Windows machine
ser.flushInput()      #clear the input buffer
ser.flushOutput()     #clear the output buffer
ser.timeout = 5       #set the timeout on the serial port to 5 seconds
command = b'AT\r\n'  # Need to perform carriage return an new line, encode as bytes
ser.write(command)   #send the AT command, we expect "OK" as answer
answer = ser.readline()  #read a line of data from the serial port
# print("Answer: " + answer.decode('utf-8')) #print the response from the SIM868 chip, it will echo at first
time.sleep(1) # wait 1 second, maybe more
answer = ser.readline()  #read a line of data from the serial port
print("Answer: " + answer.decode('utf-8'))            #print the response from the SIM868 chip

