import tkinter as tk

from sie.data.data_manager import DataManager
from sie.gui.utils.list_util import *
from sie.gui.utils.canvas_util import *

class MidFrame:
    """
    Middle frame : middle side canvases
    """
    def __init__(self, root):
        # variable define
        self.__src_canvas = None
        self.__out_canvas = None

        # middle canvases frame
        mid_frm = tk.Frame(root)
        self.__root = mid_frm
        mid_frm.pack(padx=2, pady=2, fill='both', expand=True)

        self.__src_canvas = CustomImageCanvas(mid_frm)
        self.__src_canvas.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        self.__out_canvas = CustomImageCanvas(mid_frm)
        self.__out_canvas.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)

        src_file = DataManager().get_work_file().to_string()
        out_file = DataManager().get_output_file()

        self.__src_canvas.set_image(src_file)
        self.__out_canvas.set_image(out_file)

        # Added by Q&A from stackoverflow
        # https://stackoverflow.com/questions/72713209/how-to-keep-two-textboxes-the-same-size-when-resizing-window-with-python-tkinter
        mid_frm.columnconfigure((0,1), weight=1)
        mid_frm.rowconfigure(0, weight=1)
