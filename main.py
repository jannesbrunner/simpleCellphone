from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import (StringProperty, 
    NumericProperty, ObjectProperty)
import serial
import time

class Storage():
    number = "325"

class CellphoneApp(App):
    def build(self):
        return Cellphone()

class DialPopup(Popup):
    display_text = StringProperty("0")
    
    def __init__(self, number, **kwargs): # note the `abc`
        super(DialPopup, self).__init__()
        self.display_text = number

class ErrorPopup(Popup):
    display_text = StringProperty("Error")
    
    def __init__(self, error, **kwargs): # note the `abc`
        super(ErrorPopup, self).__init__()
        self.display_text = error


class PhoneManager():

    def __init__(self, **kwargs):
        self.__port = "COM6"
        self._baud = 9600
        self.logger = []

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
        call = self._at_handle("ATD" + number + ";")
        return call

    def hang_up(self):
        end = self._at_handle("ATH")
        return end

    def answer(self):
        answer = self._at_handle("ATA")
        return answer

    def _at_handle(self, command):
        at_answer = self._at_send(command)
        if "OK" not in at_answer:
            return at_answer
        return True

    def _at_send(self, command, timeout = 0.0001):
        ser = serial.Serial(self.__port, self._baud)
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

    
    

   

class Cellphone(Widget):
    
    display_text = StringProperty("Enter Tel Number")
    log_text = StringProperty("Log\n")
    display_value = NumericProperty(0)
    init_value = NumericProperty(100)
    maximum_value = NumericProperty(None, allownone=True)
    minimum_value = NumericProperty(None, allownone=True)
    return_callback = ObjectProperty(None, allownone=True)
    units = StringProperty(None, allownone=True)
    phone = PhoneManager()
    

    def __init__(self, **kwargs):
        super(Cellphone, self).__init__(**kwargs)
        
       
    def start_call(self, instance):
        call = self.phone.call(self.display_text)
        if isinstance(call, bool):
            self.log_text += "Started Call \n"
            print("Started Call")
        else:
            error = ErrorPopup(call)
            error.open()
        


    def end_call(self, instance):
        end = self.phone.hang_up()
        if isinstance(end, bool):
            self.log_text += "Call ended \n"
            print("Call ended")
        else:
            error = ErrorPopup(end)
            error.open()


    def button_callback(self, button_str):
        valid_chars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "#", "*"]

        if button_str in [str(x) for x in valid_chars]:
            if self.display_text == 'Enter Tel Number':
                self.display_text = button_str 
            else:
                self.display_text = self.display_text + button_str
              
            # maximum_value = self.maximum_value
            # if maximum_value != None:
            #    if self.display_value > maximum_value: 
            #        self.display_value = maximum_value
            
        elif button_str == 'del':
            if len(self.display_text) == 1:
                self.display_text = "Enter Tel Number"
            elif self.display_text != "Enter Tel Number":
                self.display_text = self.display_text[:-1]
        elif button_str == 'dial':
            try:
                if "Enter Tel" in self.display_text:
                    error = ErrorPopup("Please Enter a valid telephone number!")
                    self.log_text += "Error: Please Enter a valid telephone number!\n"
                    error.open()
                else:
                    check = self.phone.service_check()
                    if isinstance(check, bool):
                        print("Phone ready!")
                        self.log_text += "Phone ready!\n"
                        dial_popup = DialPopup(self.display_text)
                        dial_popup.bind(on_open=self.start_call)
                        dial_popup.bind(on_dismiss=self.end_call)
                        dial_popup.open()
                    else:
                        error = ErrorPopup(check)
                        error.open()
            except serial.SerialException:
                error = ErrorPopup("No connection to the SIM Module could be established")
                self.log_text += "No connection to the SIM Module could be established!\n"
                error.open()
                            
        
        elif button_str == "log":
            new_log = self.phone.get_log()
            log_text = ""
            for x in new_log:
                log_text += x + "\n"
            self.log_text += log_text
            
    
   


    

if __name__ == '__main__':
    CellphoneApp().run()
