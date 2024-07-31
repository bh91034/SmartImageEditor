import tkinter as tk

from abc import *


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


class ScrollableRadiobuttonList(tk.Frame):
    def __init__(self, parent, listener:ScrollableListListener, items):
        super().__init__(parent)

        # instance variables
        self.__radio_var = tk.StringVar()  # Variable shared among all radio buttons
        self.__radio_buttons = []  # List to hold references to radio buttons
        self.__scrollable_frame = None
        self.__listener = listener

        # 
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
        
        self.__radio_var.trace_add('write', self.__on_radio_change)  # Add a trace to call on_radio_change when radio_var changes
        
        if items is not None and len(items) > 0:
            self.update_items(items)  # Initialize with initial items
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def __on_radio_change(self, *args):
        selected_item = self.__radio_var.get()
        print(f'###>>> selected_item={selected_item}')
        if selected_item is None or '|' not in selected_item:
            return
        index, text = ScrollableUtil.decode_text(selected_item)

        if self.__listener is not None:
            self.__listener.on_list_selected(index, text)

    def update_items(self, items):
        # Clear existing radio buttons
        for rb in self.__radio_buttons:
            rb.destroy()
        self.__radio_buttons.clear()
        
        # Update the radio_var with the first item
        if items:
            self.__radio_var.set(items[0])  # Set to the first item to select it
        else:
            self.__radio_var.set("")  # Clear the selection if no items
        
        # Create new radio buttons
        for index, item in enumerate(items):
            rb = tk.Radiobutton(self.__scrollable_frame, text=item, variable=self.__radio_var, value=ScrollableUtil.encode_text(index, item))
            rb.pack(anchor="w")
            self.__radio_buttons.append(rb)


class ScrollableCheckboxList(tk.Frame):
    def __init__(self, parent, listener, items):
        super().__init__(parent)
        
        # instance variables
        self.__check_vars = {}  # Dictionary to hold the IntVar for each checkbox
        self.__check_buttons = []  # List to hold references to checkbuttons
        self.__scrollable_frame = None
        self.__listener = listener

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
            self.update_items(items)  # Initialize with initial items
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def __on_checkbox_change(self, index, item):
        if self.__listener is not None:
            self.__listener.on_list_selected(index, item)

    def update_items(self, items):
        # Clear existing checkbuttons
        for cb in self.__check_buttons:
            cb.destroy()
        self.__check_buttons.clear()
        
        self.__check_vars.clear()  # Clear the variable dictionary
        
        # Create new checkbuttons
        for index, item in enumerate(items):
            var = tk.IntVar()  # Create a variable for each checkbox
            var.trace_add('write', lambda *args, index=index, item=item: self.__on_checkbox_change(index, item))
            cb = tk.Checkbutton(self.__scrollable_frame, text=item, variable=var)
            cb.pack(anchor="w")
            self.__check_buttons.append(cb)
            self.__check_vars[item] = var
