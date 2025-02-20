import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


import time


from astropy.coordinates import SkyCoord
from astropy import units as u

class tracking_map(tk.Frame):
    #Frame containing controls for detector integration

    def __init__(self, master, rotor, bd, width, height):
        super().__init__(master, bd=bd, width=width, height=height)
        self.grid()

        #Create variables for time display and time format
        self.time_format_string = "%d/%m/%Y %H:%M:%S"

        self.timevar = tk.StringVar(self, value=time.strftime(self.time_format_string, time.gmtime()))

        #Create labels for the current time display
        self.time_disp_label = tk.Label(self, text="Current Time (UTC):")
        self.clock_label = tk.Label(self, textvariable=self.timevar)

        #Create Figure and canvas with polar projection
        self.fig = Figure(figsize=(4, 4), dpi=100)

        self.axes = self.f.add_subplot(111, polar=True)

        self.canvas = FigureCanvasTkAgg(self.fig, self)

        #Arrange elements







