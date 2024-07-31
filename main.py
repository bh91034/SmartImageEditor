from tkinter import Tk

from sie.gui.gui_manager import GuiManager
from sie.data.data_manager import DataManager

# 메인 애플리케이션 클래스
class SmartImageEditor:
    def __init__(self):
        self.__data_manager = DataManager()
        self.__gui_manager = GuiManager()
    
    def get_root(self):
        return self.__gui_manager.get_root()

if __name__ == "__main__":
    app = SmartImageEditor()
    app.get_root().mainloop()