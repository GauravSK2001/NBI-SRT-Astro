import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import numpy as np


import time
from astropy.time import Time

from threading import Thread


from astropy.coordinates import SkyCoord, AltAz, Longitude
from astropy import units as u
from astropy.time import Time

class TrackingMap(tk.Frame):
    #Frame containing controls for detector integration

    

    def __init__(self, master, rotor, bd, width, height):
        super().__init__(master, bd=bd, width=width, height=height)
        self.grid()

        #Initialize tracking object
        self.rotor = rotor


        #Create variables for time display and time format
        self.time_format_string = "%d/%m/%Y %H:%M:%S"

        #self.timevar = tk.StringVar(self, value=time.strftime(self.time_format_string, time.gmtime()))

        #Create pointing display label
        #self.pointing_disp_label = tk.Label(self, text="Pointing and Time Display")

        #Create labels for the current time display
        #self.time_disp_label = tk.Label(self, text="Current Time (UTC):")
        #self.clock_label = tk.Label(self, textvariable=self.timevar)

        #Create Figure and canvas with polar projection
        self.fig = Figure(figsize=(5.5, 5.5), dpi=100)

        self.fig.suptitle("Telescope Pointing")

        self.axes = self.fig.add_subplot(111, polar=True)

        self.axes.set_theta_zero_location("N")

        self.axes.set_ylim(90, -16)
        self.axes.set_yticks([-15, 0, 30, 60, 75])
        self.axes.set_yticklabels(["", r"0$\degree$", r"30$\degree$", r"60$\degree$", r"75$\degree$"])
        

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.update_pointing_plot()

        #Arrange elements

        #self.time_disp_label.grid(column=0, row=0, padx=4, pady=2, sticky="w")
        #self.clock_label.grid(column=1, row=0, padx=4, pady=2, sticky="w")

        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, pady=2, padx=4, sticky="nw")

        #Begin update cycles
        #self.clock_thread = Thread(target=self.update_clock_display, daemon=True)
        #self.clock_thread.start()

        self.pointing_disp_thread = Thread(target=self.update_pointing_display, daemon=True)
        self.pointing_disp_thread.start()


    def update_clock_display(self):
        #Update the clock every second, including clock and pointing plot

        self.update_clock_label()

        time.sleep(0.5) #Including some allowance for update times
        self.update_clock_display()


    def update_pointing_display(self):
        #Update the pointing plot every 0.5 seconds


        self.update_pointing_plot()

        time.sleep(0.5)
        self.update_pointing_display()

    def update_clock_label(self):
        #Update the clock variable with the current UTC time

        self.timevar.set(time.strftime(self.time_format_string, time.gmtime()))
        self.clock_label.update()
        

    def update_pointing_plot(self):
        #Update pointing plot with current rotor coordinates and galactic plane location

        self.clear_plotted_objects()


        if self.rotor.control is not None:
            #print("Interface: found rotor control")
            rotor_az, rotor_el = self.rotor.control.status()

            #print(f"Interface: Pointing display: Az:{rotor_az}, El:{rotor_el}")

            self.axes.plot((rotor_az* u.degree).to(u.radian).value, rotor_el, "r+", label="Telescope")
        else:
            self.axes.plot(0, -15, "r+", label="Telescope")

        
        GALACTIC_PLANE_LONGITUDES = np.arange(0, 361, 1)

        galactic_azs = []
        galactic_els = []
        
        __, az, el = self.rotor.tracking_galactic_coordinates(L=GALACTIC_PLANE_LONGITUDES, B=0)
    

        galactic_azs = (np.array(az) * u.degree).to(u.radian).value
        galactic_els = np.array(el)

        visible_galactic_plane_azs = galactic_azs[np.where(galactic_els >=0)]
        visible_galactic_plane_els = galactic_els[np.where(galactic_els >=0)]
    

        self.axes.plot(visible_galactic_plane_azs, visible_galactic_plane_els, "b-", label="Galactic plane:")

        self.fig.legend(loc="outside lower left")

        self.canvas.draw()


    def clear_plotted_objects(self):
        #Remove all objects from self.axes

        for artist in self.axes.ArtistList(self.axes, prop_name="issue"):
            artist.remove()

    

        




        










"""
root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("550x550")

rotor = SourceTracking(control=None)


observatory_interface = tracking_map(root, rotor=rotor, bd=0, width=550, height=150)
observatory_interface.mainloop()
"""





