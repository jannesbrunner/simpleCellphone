from kivy.app import App
from kivy.uix.button import Button

class CellPhone(App):
    def build(self):
        return Button(text='Simple Cellphone')

CellPhone().run()
