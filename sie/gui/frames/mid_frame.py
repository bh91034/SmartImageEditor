import tkinter as tk

from sie.data.data_manager import DataManager
from sie.gui.common import CanvasWorker

class MidFrame:
    """
    Middle frame : middle side canvases
    """
    def __init__(self, root):
        # middle canvases frame
        mid_frm = tk.Frame(root)
        self.__root = mid_frm
        mid_frm.pack(padx=2, pady=2, fill='both', expand=True)

        left_canvas = tk.Canvas(mid_frm, bg='lightgray')
        left_canvas.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        right_canvas = tk.Canvas(mid_frm, bg='lightgray')
        right_canvas.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)

        src_file = DataManager().get_work_file().to_string()
        out_file = DataManager().get_output_file()

        left_canvas.bind('<Configure>', self.__resizer)
        # Added by Q&A from stackoverflow
        # https://stackoverflow.com/questions/72713209/how-to-keep-two-textboxes-the-same-size-when-resizing-window-with-python-tkinter
        mid_frm.columnconfigure((0,1), weight=1)
        mid_frm.rowconfigure(0, weight=1)

        self.__src_canvas_worker = CanvasWorker(src_file, left_canvas)
        self.__out_canvas_worker = CanvasWorker(out_file, right_canvas)

    # Reference :
    # - https://www.youtube.com/watch?v=xiGQD2J47nA
    # - https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/image_bg_resize.py
    # - https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/
    def __resizer(self, e):
        self.__redraw_canvas_images()

    def __redraw_canvas_images(self):
        self.__src_canvas_worker.draw_image()
        self.__out_canvas_worker.draw_image()
