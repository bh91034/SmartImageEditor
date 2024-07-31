import cv2
import tkinter as tk

from PIL import ImageTk, Image
from abc import *


class PostDrawListner(metaclass=ABCMeta):
    @abstractmethod
    def do_post_draw(self, canvas, scale_ratio):
        pass


class CustomImageCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.__image_path = None
        self.__image = None
        self.__cv2_image = None
        self.__scale_ratio = 1
        self.__post_draw_listeners = []
        self.bind("<Configure>", self.__on_resize)

    def redraw_image(self):
        self.__draw_image()

    def set_image(self, image_path):
        self.__image_path = image_path
        self.__load_image()
        self.__draw_image()

    def __load_image(self):
        image = cv2.imread(self.__image_path)

        # Store the current image
        self.__image = image

    def __calculate_scale_ratio(self, w_org, h_org, w_resized, h_resized):
        return w_resized/w_org

    def __draw_image(self):
        # Check if image is available
        if self.__image is None:
            return

        # Convert the image from BGR to RGB
        self.__cv2_image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2RGB)

        # Draw cv2 image to canvas
        self.__draw_cv2_image_to_canvas()

        # callback listeners
        for listener in self.__post_draw_listeners:
            listener.do_post_draw(self, self.__scale_ratio)

    def __draw_cv2_image_to_canvas(self):
        # Convert the image to a format Tkinter can use
        image = Image.fromarray(self.__cv2_image)
        w_org, h_org = image.size

        # Resize image to fit the canvas, maintaining aspect ratio
        max_width, max_height = self.winfo_width(), self.winfo_height()
        image.thumbnail((max_width, max_height))
        w_resized, h_resized = image.size

        # Calculate scale ratio
        self.__scale_ratio = self.__calculate_scale_ratio(w_org=w_org, h_org=h_org, w_resized=w_resized, h_resized=h_resized)

        # Create photo image
        self.__photo = ImageTk.PhotoImage(image)

        # Clear the canvas and draw the new image
        self.delete("all")
        self.create_image(0, 0, image=self.__photo, anchor=tk.NW)

    def __on_resize(self, event):
        self.__draw_image()

    def set_post_draw_listener(self, listener: PostDrawListner):
        if listener not in self.__post_draw_listeners:
            self.__post_draw_listeners.append(listener)

    def draw_rect(self, position_info):
        x1 = position_info[0][0]
        y1 = position_info[0][1]
        x2 = position_info[2][0]
        y2 = position_info[2][1]
        cv2.rectangle(self.__cv2_image, (x1, y1), (x2, y2), color=(255,0,0), thickness=2)
        self.__draw_cv2_image_to_canvas()