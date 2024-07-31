#from msilib.schema import Control
from tkinter import ttk

from sie.gui.subframes.remove_frame import RemoveFrame

#------------------------------------------------------------------------------
# Low frame : low side tabbed pane (tools)
#------------------------------------------------------------------------------
class LowFrame:

    def __init__(self, root):
        # create a notebook
        low_frm = ttk.Notebook(root)
        LowFrame.notebook = low_frm
        low_frm.bind("<<NotebookTabChanged>>", self.__tab_changed)

        low_frm.pack(pady=10, fill='both')
        low_frm.config(height=220)

        # create frames
        remove_tab = ttk.Frame(low_frm, height=50)
        write_tab = ttk.Frame(low_frm, height=50)
        edit_tab = ttk.Frame(low_frm, height=50)
        mosaic_tab = ttk.Frame(low_frm, height=50)

        remove_tab.pack(fill='both', expand=True)
        write_tab.pack(fill='both', expand=True)
        edit_tab.pack(fill='both', expand=True)
        mosaic_tab.pack(fill='both', expand=True)

        # add frames to notebook
        low_frm.add(remove_tab, text='텍스트지우기')
        low_frm.add(write_tab, text='텍스트쓰기')
        low_frm.add(edit_tab, text='이미지편집')
        low_frm.add(mosaic_tab, text='초상권보호')

        # init remove tab
        self.remove_frame = RemoveFrame(remove_tab)

    def __tab_changed(self, event):
        print ('[LowFrame] __tabChanged() called...')
