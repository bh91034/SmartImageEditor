import tkinter as tk
from tkinter import ttk

class TopFrame:
    """
    Top frame : top side buttons layout and command handlers
    """
    root = None
    label_curr_file_name = None

    def __init__(self, root):
        top_frm = tk.Frame(root)
        top_frm.pack(padx=2, pady=2, fill='both', side='top')

        # top buttons : '이전 이미지', '다음 이미지', '폴더 변경', '결과 저장'
        btn_prev_image = ttk.Button(top_frm, text='이전 이미지')
        btn_next_image = ttk.Button(top_frm, text='다음 이미지')
        
        btn_change_folder = ttk.Button(top_frm, text='폴더 변경')

        btn_save_image = ttk.Button(top_frm, text='결과 저장')

        label_curr_file_title = ttk.Label(top_frm, text='작업 파일:')
        
        TopFrame.label_curr_file_name = ttk.Label(top_frm, text='testing...')

        btn_prev_image.pack(side='left')
        btn_next_image.pack(side='left')
        btn_change_folder.pack(side='left')
        btn_save_image.pack(side='right')
        label_curr_file_title.pack(side='left')
        TopFrame.label_curr_file_name.pack(side='left')
