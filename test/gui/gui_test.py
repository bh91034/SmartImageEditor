#import sys
import os
import tkinter as tk
from tkinter import filedialog

import sys
sys.path.append('.')
from sie.gui.common import CustomImageCanvas

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("1200x600")

        # Initialize attributes
        self.image_list = []
        self.current_image_index = 0
        self.current_image = None

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Create frame for buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        # Folder button
        self.folder_button = tk.Button(self.frame, text="Change Folder", command=self.change_folder)
        self.folder_button.pack(side=tk.LEFT)

        # Previous image button
        self.prev_button = tk.Button(self.frame, text="Previous Image", command=self.show_prev_image)
        self.prev_button.pack(side=tk.LEFT)

        # Next image button
        self.next_button = tk.Button(self.frame, text="Next Image", command=self.show_next_image)
        self.next_button.pack(side=tk.LEFT)

        # Canvas to display images
        self.canvas = CustomImageCanvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Folder change
        self.change_folder()

        # set the 1st image to be shown in canvas
        self.canvas.set_image(self.image_list[self.current_image_index])

    def change_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            self.current_image_index = 0
            self.canvas.set_image(self.image_list[self.current_image_index])

    def show_next_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.canvas.set_image(self.image_list[self.current_image_index])

    def show_prev_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
            self.canvas.set_image(self.image_list[self.current_image_index])

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()

