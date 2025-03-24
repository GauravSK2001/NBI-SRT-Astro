import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import numpy as np

import time

from threading import Thread


class IntegrationDisplay(tk.Frame):


    def __init__(self, master, detector):
        super().__init__(master)
        self.grid()


        
        self.central_freq = 1420.405751768e6
        self.n_bins = int(2**13)
        self.Bandwidth = 6e6
        self.frequency_spacing=self.Bandwidth/self.n_bins
        self.freq = (np.linspace((self.central_freq-self.Bandwidth/2), self.central_freq + self.Bandwidth/2 , self.n_bins)/1e6)


        #Create and configure plot 
        self.fig = Figure(figsize=(6, 2.74), dpi=100, layout="constrained")

        self.fig.suptitle("One-second Signal Integration")

        self.axes = self.fig.add_subplot(111)

        self.axes.set_xlabel("Frequency [MHz]")
        self.axes.set_xlim(np.min(self.freq), np.max(self.freq))


        self.axes.set_ylabel("Amplitude [SDR Counts]")

        #Create and arrange canvas Tk element
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.canvas.get_tk_widget().grid(column=0, row=0, pady=2, padx=4, sticky="nw")

        i = 0
        while i < 150:
            print(i)
            self.update_plot()
            time.sleep(1)



    def clear_plotted_objects(self):
        #Remove all objects from self.axes

        for artist in self.axes.ArtistList(self.axes, prop_name="issue"):
            artist.remove()


    def update_plot(self):
        #Update one second integration plot from current cached binary file
        self.clear_plotted_objects()

        onesec_int = np.fromfile(open("../cached_spectra/onesec_test"), dtype=np.float32)

        self.axes.plot(self.freq, onesec_int, "b-")


root = tk.Tk()

root.title("Test one second integration")
root.geometry("550x550")


observatory_interface = IntegrationDisplay(root)
observatory_interface.mainloop()