from tkinter import Tk

from sie.gui.gui_manager import GuiManager
from sie.data.data_manager import DataManager

# 메인 애플리케이션 클래스
class SmartImageEditor:
    def __init__(self, root):
        self.root = root
        root.geometry('1200x600+20+20')
        root.title('Smart Image Editor')

        self.data_manager = DataManager()
        self.gui_manager = GuiManager(root)

if __name__ == "__main__":
    root = Tk()
    app = SmartImageEditor(root)
    root.mainloop()