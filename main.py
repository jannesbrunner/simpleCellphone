from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class CellphoneApp(App):
    def build(self):
        return Cellphone()


class Cellphone(Widget):
    pass

if __name__ == '__main__':
    CellphoneApp().run()
