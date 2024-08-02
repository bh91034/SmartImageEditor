from tkinter import Tk
from sie.gui.gui_manager import GuiManager
from sie.data.data_manager import DataManager

class SmartImageEditor:
    """
    Main application class for the Smart Image Editor.

    This class initializes the DataManager and GuiManager instances and provides access 
    to the root Tkinter window. It is responsible for starting the main event loop of the 
    Tkinter application.

    Attributes:
        __data_manager (DataManager): An instance of the DataManager class managing data-related operations.
        __gui_manager (GuiManager): An instance of the GuiManager class managing the GUI components.
    """

    def __init__(self):
        """
        Initializes the SmartImageEditor by creating instances of DataManager and GuiManager.
        
        This method sets up the data manager and GUI manager, preparing the application for 
        user interaction.
        """
        self.__data_manager = DataManager()
        self.__gui_manager = GuiManager()
    
    def get_root(self):
        """
        Returns the main Tkinter root window.

        This method provides access to the root Tkinter window managed by the GuiManager instance.

        Returns:
            Tk: The root Tkinter window for the application.
        """
        return self.__gui_manager.get_root()

if __name__ == "__main__":
    # Create an instance of the SmartImageEditor application
    app = SmartImageEditor()
    
    # Start the Tkinter event loop
    app.get_root().mainloop()
