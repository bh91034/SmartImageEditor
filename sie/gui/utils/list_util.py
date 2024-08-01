import tkinter as tk

from abc import *
from enum import Enum, auto

class ScrollableListListener(metaclass=ABCMeta):
    @abstractmethod
    def on_list_selected(index, text):
        pass

class ScrollableUtil:
    def decode_text(encoded_text):
        if not '|' in encoded_text:
            return
        parts = encoded_text.split('|')
        number = int(parts[0])
        text = parts[1]
        return number, text

    def encode_text(idx, text):
        return str(idx) + '|' + text


# Enum to specify the type of list to create
class ScrollableListType(Enum):
    CHECK_BUTTON = auto()
    RADIO_BUTTON = auto()


class ScrollableList(tk.Frame):
    def __init__(self, parent, listener, items, list_type: ScrollableListType):
        super().__init__(parent)

        # instance variables
        self.__list_type = list_type
        self.__listener = listener
        self.__items = items
        
        # Common variables
        self.__scrollable_frame = None
        self.__radio_var = None
        self.__check_vars = {}  # Used only for CHECK_BUTTON type
        self.__buttons = []  # To hold references to checkbuttons or radiobuttons

        # Setup canvas and scrollbar
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.__scrollable_frame = tk.Frame(canvas)
        
        self.__scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=self.__scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if items is not None and len(items) > 0:
            self.update_items(items)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def __on_checkbox_change(self, index, item):
        if self.__listener is not None:
            self.__listener.on_list_selected(index, item)
    
    def __on_radio_change(self, *args):
        selected_item = self.__radio_var.get()
        print(f'###>>> selected_item={selected_item}')
        if selected_item is None or '|' not in selected_item:
            return
        index, text = ScrollableUtil.decode_text(selected_item)

        if self.__listener is not None:
            self.__listener.on_list_selected(index, text)

    def get_type(self):
        return self.__list_type
    
    def update_items(self, items):
        # Clear existing buttons
        for btn in self.__buttons:
            btn.destroy()
        self.__buttons.clear()
        
        if self.__list_type == ScrollableListType.RADIO_BUTTON:
            self.__radio_var = tk.StringVar()  # Create radio variable
            self.__radio_var.trace_add('write', self.__on_radio_change)  # Trace radio var changes
            
            if items:
                self.__radio_var.set(items[0])  # Select the first item initially
            else:
                self.__radio_var.set("")  # Clear selection if no items
            
            # Create new radio buttons
            for index, item in enumerate(items):
                rb = tk.Radiobutton(self.__scrollable_frame, text=item, variable=self.__radio_var, value=ScrollableUtil.encode_text(index, item))
                rb.pack(anchor="w")
                self.__buttons.append(rb)
        
        elif self.__list_type == ScrollableListType.CHECK_BUTTON:
            # Create new check buttons
            for index, item in enumerate(items):
                var = tk.IntVar()  # Create a variable for each checkbox
                var.trace_add('write', lambda *args, index=index, item=item: self.__on_checkbox_change(index, item))
                cb = tk.Checkbutton(self.__scrollable_frame, text=item, variable=var)
                cb.pack(anchor="w")
                self.__buttons.append(cb)
                self.__check_vars[item] = var

    def get_radio_var(self):
        return self.__radio_var
        
    def get_check_vars(self):
        if self.__list_type == ScrollableListType.CHECK_BUTTON:
            return self.__check_vars
        elif self.__list_type == ScrollableListType.RADIO_BUTTON:
            return self.__radio_var
        else:
            raise ValueError("get_check_vars is only available for CHECK_BUTTON type.")