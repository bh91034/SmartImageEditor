import tkinter as tk
from tkinter import ttk


class TopFrame:
    """
    Top frame : top side buttons layout and command handlers
    """
    def __init__(self, root):
        top_frm = tk.Frame(root)
        top_frm.pack(padx=2, pady=2, fill='both', side='top')

        # top layer components: left aligned
        self.__set_alignment(ttk.Button(top_frm, text='이전 이미지'), 'left')
        self.__set_alignment(ttk.Button(top_frm, text='다음 이미지'), 'left')
        self.__set_alignment(ttk.Button(top_frm, text='폴더 변경'), 'left')
        self.__set_alignment(ttk.Label(top_frm, text='작업 파일:'), 'left')
        self.__set_alignment(ttk.Label(top_frm, text='testing...'), 'left')

        # top layer components: right aligned
        self.__set_alignment(ttk.Button(top_frm, text='결과 저장'), 'right')

    def __set_alignment(self, component, align:str):
        component.pack(side=align)
        return component
