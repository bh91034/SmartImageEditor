from tkinter import Tk

from sie.gui.frames.top_frame import TopFrame
from sie.gui.frames.mid_frame import MidFrame
from sie.gui.frames.low_frame import LowFrame

class GuiManager:
    """
    This class is designed as 'Singleton pattern'.
    Reference: https://wikidocs.net/69361
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):             # 클래스 객체에 _init 속성이 없다면
            # 최초로 생성된 instance 에 의해서만 한번 불림
            cls._init = True
            self.__init_gui_frames()
        # 일반적인 생성자에서 처리할 부분을 여기에 처리(중복해서 불리는 부분임)
    
    def __init_gui_frames(self):
        self.__root = Tk()
        self.__root.geometry('1200x600+20+20')
        self.__root.title('Smart Image Editor')

        self.__top_frame = TopFrame(self.__root)
        self.__mid_frame = MidFrame(self.__root)
        self.__low_frame = LowFrame(self.__root)
    
    def get_root(self):
        return self.__root
    
    def get_top_frame(self):
        return self.__top_frame

    def get_mid_frame(self):
        return self.__mid_frame
    
    def get_low_frame(self):
        return self.__low_frame