import tkinter as tk
from time import strftime

class DigitalClock:
    def __init__(self, container, width, height, bg_color, fg_color, font_size):
        self.container = container
        self.frame = tk.Frame(self.container, width=width, height=height, bg=bg_color)
        self.frame.pack_propagate(False)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, font=('calibri', font_size, 'bold'), background=bg_color, foreground=fg_color)
        self.label.pack(expand=True)

    def update_time(self):
        string = strftime('%H:%M:%S %p')
        self.label.config(text=string)
        self.label.after(1000, self.update_time)

    def create_clock(self, width, height, bg_color, fg_color, font_size):
        self.frame = tk.Frame(self.container, width=width, height=height, bg=bg_color)
        self.frame.pack_propagate(False)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, font=('calibri', font_size, 'bold'), background=bg_color, foreground=fg_color)
        self.label.pack(expand=True)

    def start(self):
        self.update_time()
