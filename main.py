from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import (StringProperty, 
    NumericProperty, ObjectProperty)

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

   

class Cellphone(Widget):
    
    display_text = StringProperty("Enter Tel Number")
    display_value = NumericProperty(0)
    init_value = NumericProperty(100)
    maximum_value = NumericProperty(None, allownone=True)
    minimum_value = NumericProperty(None, allownone=True)
    return_callback = ObjectProperty(None, allownone=True)
    units = StringProperty(None, allownone=True)
    

    def __init__(self, **kwargs):
        super(Cellphone, self).__init__(**kwargs)
       
    def start_call(self, instance):
        Storage.number = self.display_text
        print("Call Started")
        


    def end_call(self, instance):
        print("Call endet")
        return False


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
            
            dial_popup = DialPopup(self.display_text)
            dial_popup.bind(on_open=self.start_call)
            dial_popup.bind(on_dismiss=self.end_call)
            dial_popup.open()
    
   


    

if __name__ == '__main__':
    CellphoneApp().run()
