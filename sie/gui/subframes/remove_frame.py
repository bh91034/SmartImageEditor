from tkinter import ttk

from sie.gui.utils.list_util import *

class RemoveTextListHandler(ScrollableListListener):
    def on_list_selected(self, index, text):
        print(f'RemoveTextListHandler.on_list_selected() : index={index}, text={text}')


#------------------------------------------------------------------------------
# Low frame - remove tab : low frame remove tab controls
#------------------------------------------------------------------------------
class RemoveFrame:
    remove_tab_text_list = None

    def __init__(self, root):
        self.frame_btn = ttk.Frame(root)
        self.frame_btn.pack(padx=2, pady=2, fill='x')
        
        btn_search_text = ttk.Button(self.frame_btn, text='텍스트 찾기')
        btn_remove_text = ttk.Button(self.frame_btn, text='텍스트 지우기')
        btn_revoke_image = ttk.Button(self.frame_btn, text='원상태 복원')

        btn_search_text.pack(side='left')
        btn_remove_text.pack(side='left')
        btn_revoke_image.pack(side='left')

        remove_tab_down_frm = ttk.Frame(root)
        RemoveFrame.__set_remove_tab_text_list(remove_tab_down_frm)

    @classmethod
    def __set_remove_tab_text_list(cls, remove_tab_down_frm):
        remove_tab_down_frm.pack(padx=2, pady=2, fill='both', expand=True)
        test_list = None
        #test_list = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL"]
        #cls.remove_tab_text_list = ScrollableRadiobuttonList(remove_tab_down_frm, RemoveTextListHandler(), test_list)
        cls.remove_tab_text_list = ScrollableCheckboxList(remove_tab_down_frm, RemoveTextListHandler(), test_list)
        cls.remove_tab_text_list.pack(side="top", fill="x", expand=True)
