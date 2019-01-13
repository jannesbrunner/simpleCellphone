from kivy.properties import (StringProperty, 
    NumericProperty, ObjectProperty)
from kivy.uix.popup import Popup
from kivy.clock import Clock

class DialPopup(Popup):
    display_text = StringProperty("0")
    call_duration = StringProperty("00:00")
    duration = 0   
    
    def __init__(self, number, **kwargs): # note the `abc`
        super(DialPopup, self).__init__()
        self.display_text = number
        Clock.schedule_interval(self.count_time, 1)

    def count_time(self, dt):
        self.duration += 1
        seconds = self.duration % 60
        minutes = int(self.duration / 60) 
        if seconds < 10:
            seconds = "0" + str(seconds)
        if minutes < 10:
            minutes = "0" + str(minutes)
        self.call_duration = str(minutes) + ":" + str(seconds)


class ErrorPopup(Popup):
    display_text = StringProperty("Error")
    
    def __init__(self, error, **kwargs): 
        super(ErrorPopup, self).__init__()
        self.display_text = error
        
class IncomingPopup(Popup):
    
    
    def __init__(self, phone, **kwargs): 
        super(IncomingPopup, self).__init__()
        self.phone = phone

    def end_call(self):
        end = self.phone.hang_up()
        if isinstance(end, bool):
            self.dismiss()
        else:    
            error = ErrorPopup(end)
            error.open(end)
            self.dismiss()

    def reaction(self, choice):
        if choice == "accept":
            answer = self.phone.answer()
            if isinstance(answer, bool):
                call_popup = DialPopup("with incoming calling partner")
                call_popup.bind(on_dismiss=self.end_call)
                call_popup.open()
            else:
                error = ErrorPopup(answer)
                error.open()
                self.dismiss()
        if choice == "refuse":
            self.dismiss()
