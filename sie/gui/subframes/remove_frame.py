from tkinter import ttk

from sie.gui.utils.list_util import *
from sie.control.remove_control import RemoveTextListListener, RemoveControl, RemovePostDrawHandler

#------------------------------------------------------------------------------
# Low frame - remove tab : low frame remove tab controls
#------------------------------------------------------------------------------
class RemoveFrame:
    remove_tab_text_list = None

    def __init__(self, root):
        self.__root = root
        frame_btn = ttk.Frame(root)
        frame_btn.pack(padx=2, pady=2, fill='x')
        
        self.__set_alignment(ttk.Button(frame_btn, text='텍스트 찾기', command=RemoveControl.clicked_search_text), 'left')
        self.__set_alignment(ttk.Button(frame_btn, text='텍스트 지우기'), 'left')
        self.__set_alignment(ttk.Button(frame_btn, text='원상태 복원'), 'left')

        remove_tab_down_frm = ttk.Frame(root)
        remove_tab_down_frm.pack(padx=2, pady=2, fill='both', expand=True)
        
        self.__remove_tab_text_list = ScrollableList(self.__root, listener=RemoveTextListListener(), type=ScrollableListType.CHECK_BUTTON)
        self.__remove_tab_text_list.pack(side="top", fill="x", expand=True)

        from sie.gui.gui_manager import GuiManager
        GuiManager().get_mid_frame().set_post_draw_listener(RemovePostDrawHandler())

    def __set_alignment(self, component, align:str):
        component.pack(side=align)
        return component

    def reset_text_list(self, test_list):
        self.__remove_tab_text_list.update_items(test_list)

    def get_check_list(self):
        return self.__remove_tab_text_list