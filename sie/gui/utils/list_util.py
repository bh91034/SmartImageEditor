import tkinter as tk
from enum import Enum, auto
from abc import *


class ScrollableListListener(metaclass=ABCMeta):
    @abstractmethod
    def on_state_changed(index, text, state, selected_items):
        pass


class ScrollableListType(Enum):
    CHECK_BUTTON = auto()
    RADIO_BUTTON = auto()


class ScrollableList(tk.Frame):
    def __init__(self, parent, type:ScrollableListType, listener:ScrollableListListener = None, items = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.__type = type
        self.__listener = None
        self.__listbuttons = []
        self.__vars = []
        self.__items = None
        self.__text = tk.Text(self, cursor="arrow", state="disabled")
        
        vsb = tk.Scrollbar(self, command=self.__text.yview)
        self.__text.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.__text.pack(side="left", fill="both", expand=True)

        if items is not None:
            self.update_items(items)
        
        if listener is not None:
            self.__listener = listener

    def __add_widget(self, widget):
        self.__text.configure(state="normal")
        self.__text.window_create("end", window=widget)
        self.__text.insert("end", "\n")
        self.__text.configure(state="disabled")

    def __on_state_changed(self, index, state, text, *args):
        if self.__listener is not None:
            self.__listener.on_state_changed(index, text, state, self.get_selected_items())

    def __allocate_var(self):
        if self.__type == ScrollableListType.CHECK_BUTTON:
            var = tk.IntVar(value=0)
            self.__vars.append(var)
            return var
        if self.__type == ScrollableListType.RADIO_BUTTON:
            if len(self.__vars) == 0:
                self.__vars.append(tk.IntVar(value=-1))
            return self.__vars[0]
        return 

    def __create_list_control(self, index, item, var):
        if self.__type == ScrollableListType.CHECK_BUTTON:
            item_control = tk.Checkbutton(self.__text, text=item, variable=var, onvalue=1, offvalue=0,
                                command=lambda i=index, v=var, t=item: self.__on_state_changed(i, v.get(), t))
        if self.__type == ScrollableListType.RADIO_BUTTON:
            item_control = tk.Radiobutton(self.__text, text=item, variable=var, value=index,
                                command=lambda i=index, t=item: self.__on_state_changed(i, var.get(), t))
        return item_control
    
    def get_selected_items(self):
        if len(self.__vars) == 0:
            return None
        
        items = []
        if self.__type == ScrollableListType.RADIO_BUTTON:
            selected_index = self.__vars[0].get()
            items.append({"index":selected_index, "text":self.__items[selected_index]})
        if self.__type == ScrollableListType.CHECK_BUTTON:
            for idx, var in enumerate(self.__vars):
                if var.get() == 1:
                    items.append({"index":idx, "text":self.__items[idx]})
        return items
    
    def update_items(self, items):
        self.__listbuttons = []
        self.__vars = []
        self.__items = items
        
        self.__text.configure(state="normal")
        self.__text.delete("1.0", "end")

        for index, item in enumerate(items):
            var = self.__allocate_var()
            item_control = self.__create_list_control(index, item, var)
            self.__add_widget(item_control)
            self.__listbuttons.append(item_control)
        self.__text.configure(state="disabled")
