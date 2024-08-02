from tkinter import Tk
from sie.gui.frames.top_frame import TopFrame
from sie.gui.frames.mid_frame import MidFrame
from sie.gui.frames.low_frame import LowFrame

class GuiManager:
    """
    A singleton class for managing the GUI of the Smart Image Editor application.

    This class is designed to follow the Singleton pattern to ensure that only one instance of 
    the GUI manager exists throughout the application. It initializes the main application window
    and manages the layout by creating and accessing different GUI frames.

    Attributes:
        __root (Tk): The main Tkinter window.
        __top_frame (TopFrame): The top frame of the GUI.
        __mid_frame (MidFrame): The middle frame of the GUI.
        __low_frame (LowFrame): The low frame of the GUI.
    """
    
    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of GuiManager is created.

        Args:
            cls (type): The class type.

        Returns:
            GuiManager: The singleton instance of GuiManager.
        """
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the GuiManager instance by setting up the GUI frames. 

        This method is only executed once during the lifetime of the singleton instance.
        """
        cls = type(self)
        if not hasattr(cls, "_init"):  # Ensure initialization is only done once
            cls._init = True
            self.__init_gui_frames()
    
    def __init_gui_frames(self):
        """
        Initializes the main GUI components including the root window and frames.

        Creates the main Tkinter window and sets its size, title, and layout frames.
        """
        self.__root = Tk()
        self.__root.geometry('1200x600+20+20')
        self.__root.title('Smart Image Editor')

        self.__top_frame = TopFrame(self.__root)
        self.__mid_frame = MidFrame(self.__root)
        self.__low_frame = LowFrame(self.__root)
    
    def get_root(self):
        """
        Returns the main Tkinter window.

        Returns:
            Tk: The root Tkinter window.
        """
        return self.__root
    
    def get_top_frame(self):
        """
        Returns the top frame of the GUI.

        Returns:
            TopFrame: The instance of the TopFrame class.
        """
        return self.__top_frame

    def get_mid_frame(self):
        """
        Returns the middle frame of the GUI.

        Returns:
            MidFrame: The instance of the MidFrame class.
        """
        return self.__mid_frame
    
    def get_low_frame(self):
        """
        Returns the low frame of the GUI.

        Returns:
            LowFrame: The instance of the LowFrame class.
        """
        return self.__low_frame
