import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import numpy as np

import time

from threading import Thread, active_count


class IntegrationDisplay(tk.Frame):


    def __init__(self, master, detector):
        super().__init__(master)
        self.grid()

        #Initialize detector object
        self.detector = detector

        #If detector is present, use its spectrum settings, or default values otherwise
        if detector is not None:
            self.central_freq = detector.central_freq
            self.n_bins = int(2**13)
            self.Bandwidth = 6e6
            self.frequency_spacing=self.Bandwidth/self.n_bins
            self.freq = np.arange(0,self.n_bins)*self.frequency_spacing-self.Bandwidth/2
        else:

            self.central_freq = 1420.405751768e6
            self.n_bins = int(2**13)
            self.Bandwidth = 6e6
            self.frequency_spacing=self.Bandwidth/self.n_bins
            self.freq = np.arange(0,self.n_bins)*self.frequency_spacing-self.Bandwidth/2


        #Create and configure plot 
        self.fig = Figure(figsize=(6, 2.74), dpi=100, layout="constrained")

        self.fig.suptitle("One-second Signal Integration")

        self.axes = self.fig.add_subplot(111)

        self.axes.set_xlabel("Frequency [MHz]")
        self.axes.set_xlim(np.min(self.freq)/1e6, np.max(self.freq)/1e6)


        self.axes.set_ylabel("Amplitude [SDR Counts]")

        #Create and arrange canvas Tk element
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.canvas.get_tk_widget().grid(column=0, row=0, pady=2, padx=4, sticky="nw")



    def clear_plotted_objects(self):
        #Remove all objects from self.axes

        for artist in self.axes.ArtistList(self.axes, prop_name="issue"):
            artist.remove()


    def update_plot(self):
        #Update one second integration plot from current cached binary file
        self.clear_plotted_objects()

        onesec_int = np.fromfile(open("/Users/gauravsenthilkumar/repositories/NBI-SRT-Astro/.cached_spectra/onesec_int"), dtype=np.float32)

        length=len(self.freq)

        if len(onesec_int) == 0:
            return None

        self.axes.step(self.freq/1e6, onesec_int[-length:], "b-", where="mid")
        self.canvas.draw()

    def update_loop(self):
        #Repeat updates while detector is integrating

        time.sleep(1)

        while self.detector.status =="active":
            self.update_plot()
            print(f"Interface: Number of threads active: {active_count()}")
            time.sleep(0.75)

    

