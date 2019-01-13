from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import (TabbedPanel, TabbedPanelItem)
from kivy.clock import Clock
from kivy.properties import (StringProperty, 
    NumericProperty, ObjectProperty)

import time
import serial

from phonemanager import PhoneManager
from popups import (DialPopup, ErrorPopup, IncomingPopup)

class Storage():
    number = "325"

class CellphoneApp(App):
    def build(self):
        return Cellphone()


            

class Cellphone(Widget):
    info = '''Simple Cellphone v1. (2019-01-14) \n Made with Python 3 and the Kivy Framework.
             \n Hochschule fuer Technik und Wirtschaft (HTW Berlin) [university of applied sciences] \n
                Program: Computer Science \n 
                Module: B55.1 MA Ausgewählte Kapitel mobiler Anwendungen \n
                Course Instructor: Prof. Dr. Huhn \n
                Project Work, developed by Jannes Brunner (https://www.github.com/jannesbrunner)'''
    return_callback = ObjectProperty(None, allownone=True)
    units = StringProperty(None, allownone=True)
    
    # Telephone
    display_text = StringProperty("Enter Tel Number")
    display_value = NumericProperty(0)
    init_value = NumericProperty(100)
    maximum_value = NumericProperty(None, allownone=True)
    minimum_value = NumericProperty(None, allownone=True)

    # Log Screen
    log_text = StringProperty("")
    
    # GPS Screen
    gps_power = StringProperty("Turn GPS ON")
    gps_baudrate = StringProperty("")
    gps_status = StringProperty("")
    gps_gnss = StringProperty("")
    gps_data = StringProperty("")

    
    # Misc
    phone = PhoneManager()
    

    def __init__(self, **kwargs):
        super(Cellphone, self).__init__(**kwargs)
        # self.phone.enable_clip()
        # Clock.schedule_interval(self.check_ring, 4) # Buggy!

    ## GPS Function
    def toggle_gps(self):
        gps = self.phone.toggle_gps()
        if isinstance(gps, bool):
            gps_switch = "OFF" if self.phone.gps == True else "ON" 
            self.gps_power = "Turn GPS " + gps_switch
            self.log_text += "Turn GPS " + gps_switch + "\n"
            if self.phone.gps == True:
                time.sleep(1)
                print("Display GPS Info...")
                self.log_text += "Display GPS Info...\n"
                self.show_gps()
            else:
                print("GPS Clean Up")
                self.log_text += "GPS Clean UP...\n"
                self.gps_baudrate = ""
                self.gps_gnss = ""
                self.gps_status = ""
        else:
            error = ErrorPopup("GPS Toggle Error. Please Check the GPS Module (is it on?)")
            self.log_text += "GPS Toggle Error. Please Check the GPS Module (is it on?) \n"
            error.open()
    
    def show_gps(self):
       gps_baud = self.phone.get_gps_baudrate()
       gps_baud = gps_baud[9:]
       self.gps_baudrate = gps_baud

       time.sleep(0.5)
       self.gps_status = self.phone.get_gps_status()
       time.sleep(0.5)
       gps_gnss = self.phone.get_gps_gnss_info()
       gps_gnss = gps_gnss[9:]

       self.gps_gnss = gps_gnss
    
    def toggle_gps_read(self):
        gps2uart = self.phone.toggle_gps_uart()
        if gps2uart == True:
           Clock.schedule_once(Clock.schedule_interval(self.toggle_gps_read, 1), 2)
        else:
            error = ErrorPopup(gps2uart)
            error.open()
            if self.phone.gps == True:
                time.sleep(0.01)
                self.read_gps()

    def update_gps(self):
        gps2uart = self.phone.toggle_gps_uart()
        if gps2uart == True:
            time.sleep(0.5)
            self.gps_data += self.phone.readGPS() + "\n"
            time.sleep(0.5)
            gps2uart = self.phone.toggle_gps_uart()
        else:
            error = ErrorPopup(gps2uart)
            error.open()


    ## Telephone Function    
    
    def after_incoming_call(self):
        # Let's wait 10 seconds before we listening for incoming calls again
        Clock.schedule_once(Clock.schedule_interval(self.check_ring, 4), 10)


    def check_ring(self, dt):
        if self.phone.is_ringing() == True:
            # auto_dismiss=False
            print("The Phone is ringing!")

            call = IncomingPopup(self.phone)
            call.bind(on_dismiss=self.after_incoming_call)
            call.open()

            # Cancle listening for incoming calls
            return False
        else:
            pass

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
            # test = IncomingPopup(self.phone)
            # test.open()
            

            
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
                            
        elif button_str == 'answer':
            if self.phone.is_ringing():
                print("The Phone is ringing!")
                answer = self.phone.answer()
                if isinstance(answer, bool):
                    call_popup = DialPopup("with incoming calling partner")
                    call_popup.bind(on_dismiss=self.end_call)
                    call_popup.open()
                else:
                    error = ErrorPopup(answer)
                    error.open()
            else:
                error = ErrorPopup("No Incoming Call")
                error.open()

    def handle_tab_switch(self):
        last_tab = self.ids.tpanel.current_tab.text
        if "GPS" not in last_tab and self.phone.gps == True:
            self.toggle_gps()
        new_log = self.phone.get_log()
        log_text = ""
        for x in new_log:
            log_text += x + "\n"
        self.log_text += log_text


            

if __name__ == '__main__':
    CellphoneApp().run()
