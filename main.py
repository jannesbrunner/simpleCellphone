from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import (StringProperty, 
    NumericProperty, ObjectProperty)

import serial

from phonemanager import PhoneManager
from popups import (DialPopup, ErrorPopup, IncomingPopup)

class Storage():
    number = "325"

class CellphoneApp(App):
    def build(self):
        return Cellphone()


            

class Cellphone(Widget):

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
    
    # Misc
    phone = PhoneManager()
    

    def __init__(self, **kwargs):
        super(Cellphone, self).__init__(**kwargs)
        # self.phone.enable_clip()
        # Clock.schedule_interval(self.check_ring, 4) # Buggy!



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
            test = IncomingPopup(self.phone)
            test.open()
            
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
            

        elif button_str == "log":
            new_log = self.phone.get_log()
            log_text = ""
            for x in new_log:
                log_text += x + "\n"
            self.log_text += log_text
            

if __name__ == '__main__':
    CellphoneApp().run()
