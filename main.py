from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (StringProperty, 
    NumericProperty, ObjectProperty)

class CellphoneApp(App):
    def build(self):
        return Cellphone()


class Cellphone(Widget):
    display_text = StringProperty("0")
    display_value = NumericProperty(0)
    init_value = NumericProperty(100)
    maximum_value = NumericProperty(None, allownone=True)
    minimum_value = NumericProperty(None, allownone=True)
    return_callback = ObjectProperty(None, allownone=True)
    units = StringProperty(None, allownone=True)
    

    def __init__(self, **kwargs):
        super(Cellphone, self).__init__(**kwargs)
       
       



    def button_callback(self, button_str):
        if button_str in [str(x) for x in range(10)]:
            if self.display_text == '0':
                self.display_text = button_str 
            else:
                self.display_text = self.display_text + button_str
            # maximum_value = self.maximum_value
            # if maximum_value != None:
            #    if self.display_value > maximum_value: 
            #        self.display_value = maximum_value
        elif button_str == 'del':
            self.display_text = self.display_text[:-1]
        elif button_str == 'dial':
            pass
        elif button_str == 'end':
            pass

    

if __name__ == '__main__':
    CellphoneApp().run()
