import cv2
import tkinter as tk

from PIL import ImageTk, Image
from abc import *


class PostDrawListner(metaclass=ABCMeta):
    @abstractmethod
    def do_post_draw(self, canvas, image_reduced_ratio):
        pass


class CustomImageCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.__image_path = None
        self.__image = None
        self.__image_reduced_ratio = 1
        self.__post_draw_listeners = []
        self.bind("<Configure>", self.__on_resize)

    def redraw_image(self):
        self.__draw_image()

    def set_image(self, image_path):
        self.__image_path = image_path
        self.__load_image()
        self.__draw_image()

    def set_post_draw_listener(self, listener: PostDrawListner):
        if listener not in self.__post_draw_listeners:
            self.__post_draw_listeners.append(listener)

    def draw_rect(self, position_info, color='#ffff00', width=2, apply_image_reduced_ratio=True):
        reduced_ratio = 1
        if apply_image_reduced_ratio:
            reduced_ratio = self.__image_reduced_ratio
        x1 = position_info[0][0] * reduced_ratio
        y1 = position_info[0][1] * reduced_ratio
        x2 = position_info[2][0] * reduced_ratio
        y2 = position_info[2][1] * reduced_ratio
        self.create_rectangle(x1, y1, x2, y2, outline=color, width=2)
    
    def __calculate_image_reduced_ratio(self, reduced_image):
        h, w, c = self.__image.shape
        w_reduced, h_reduced = reduced_image.size
        self.__image_reduced_ratio = w_reduced / w
    
    def __load_image(self):
        image = cv2.imread(self.__image_path)
        self.__image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def __draw_image(self):
        # Convert the image to a format Tkinter can use
        image = Image.fromarray(self.__image)

        # Resize image to fit the canvas, maintaining aspect ratio
        max_width, max_height = self.winfo_width(), self.winfo_height()
        image.thumbnail((max_width, max_height))
        self.__calculate_image_reduced_ratio(image)

        # Create photo image
        self.__photo = ImageTk.PhotoImage(image)

        # Clear the canvas and draw the new image
        self.delete("all")
        self.create_image(0, 0, image=self.__photo, anchor=tk.NW)

        # callback listeners
        for listener in self.__post_draw_listeners:
            listener.do_post_draw(self, self.__image_reduced_ratio)

    def __on_resize(self, event):
        self.__draw_image()
