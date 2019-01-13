import serial
import time

class PhoneManager():

    def __init__(self, **kwargs):
        self._port = "tty0"
        self._baud = 9600
        self.logger = []
        self.gps = False
        self.gps_uart = False

    def get_log(self):
        log_to_return = self.logger
        self.logger = []
        return log_to_return
    
    def service_check(self):
        check = self._at_send("AT")
        
        if(len(check) == 0):
            error = "SIM Modul not reachable. (Is it on?)"
            self.logger.append(str(error))
            return error
        elif ("OK" not in check):
            error = "Unknown SIM Modul Error"
            self.logger.append(str(error))
            return error
        elif ("READY" not in self._at_send("AT+CPIN?", 5)):
            error = "SIM Error. (Require PIN?)"
            self.logger.append(str(error))
            return error
        else:
            self.logger.append("Phone Module check was succesful")
            return True
    
    def call(self, number):
        return self._at_handle("ATD" + number + ";")

    def hang_up(self):
        return self._at_handle("ATH")
        

    def answer(self):
        answer = self._at_handle("ATA")
        return answer

    def _at_handle(self, command):
        at_answer = self._at_send(command)
        if "OK" not in at_answer:
            return at_answer
        return True

    def enable_clip(self):
        return self._at_handle("AT+CLIP=1")
        

    def toggle_gps(self):
        gps = self._at_handle("AT+CGNSPWR=1") if self.gps == False else self._at_handle("AT+CGNSPWR=0")
        if isinstance(gps, bool):
            self.gps = not self.gps
            return True
        else:
            return gps
    
    def toggle_gps_uart(self):
        if not self.gps:
            return "Please activate GPS!"
        else:
            gps_uart = self._at_handle("AT+CGNSTST=1") if self.gps_uart == False else self._at_handle("AT+CGNSTST=0")
            if isinstance(gps_uart, bool):
                self.gps_uart = not self.gps_uart
                return True
            else:
                return gps_uart
       
    
    def get_gps_status(self):
        return self._at_send("AT+CGPSSTATUS")      
    
    def get_gps_baudrate(self):
        return self._at_send("AT+CGNSIPR?")

    def get_gps_gnss_info(self):
        return self._at_send("AT+CGNSINF")

    def set_gps_baudrate(self, rate):
        return self._at_handle("AT+CGNSIPR=" + str(rate))

    def readGPS(self):
        ser = serial.Serial(self._port, self._baud)
        ser.flushInput()      #clear the input buffer
        ser.flushOutput()     #clear the output buffer
        ser.timeout = 5       #set the timeout on the serial port to 5 seconds
        answer = ser.readline() # will always be "AT" autoreply for some reasons
        # print("Answer: " + answer.decode('utf-8')) #print the response from the SIM868 chip, it will echo at first
        time.sleep(00000.1) # wait
        answer = ser.readline()  #read a line of data from the serial port
        print("GPS: " + answer.decode())
        return answer.decode()



    def _at_send(self, command, timeout = 0.0001):
        ser = serial.Serial(self._port, self._baud)
        ser.flushInput()      #clear the input buffer
        ser.flushOutput()     #clear the output buffer
        ser.timeout = 5       #set the timeout on the serial port to 5 seconds
        print("AT send: " + command)
        self.logger.append(str("AT send: " + command))
        command = str.encode(command + '\r\n')  # Need to perform carriage return an new line, encode as bytes
        type(command)
        ser.write(command)   #send the AT command, we expect "OK" as answer
        answer = ser.readline() # will always be "AT" autoreply for some reasons
        # print("Answer: " + answer.decode('utf-8')) #print the response from the SIM868 chip, it will echo at first
        time.sleep(timeout) # wait 1 second, maybe more
        answer = ser.readline()  #read a line of data from the serial port
        self.logger.append(str("Got: " + answer.decode()))
        print("Got: " + answer.decode())
        return answer.decode()

    def is_ringing(self):
        at_answer = self._at_send("ATA")
        print("Check if someone is calling us...")
        if "OK" in at_answer:
            print("Incoming call!")
            return True
        print("No incoming call")
        return False
