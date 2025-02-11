import tkinter as tk

import sys

from Controls import Rot2Prog
from Tracking import source_tracking

import numpy as np

from astropy.coordinates import SkyCoord
from astropy import units as u


class Interface(tk.Frame):

          
    
    def __init__(self, master):
        super().__init__(master)
        self.grid()

        #Create variables for taking coordinate and integration time input
        self.l_var = tk.StringVar()
        self.b_var = tk.StringVar()

        self.az_var = tk.StringVar(value=0)
        self.el_var = tk.StringVar(value=0)

        self.selector_state = tk.BooleanVar(value=False)

        self.int_time_var = tk.StringVar()

        #Create objects for controlling telescope pointing
        self.gal_long_label = tk.Label(self, text="l:")
        self.gal_lat_label = tk.Label(self, text="b:")

        self.gal_long_field = tk.Entry(self, textvariable=self.l_var, state="readonly")
        self.gal_lat_field = tk.Entry(self, textvariable=self.b_var, state="readonly")


        self.az_label = tk.Label(self, text="Az:")
        self.el_label = tk.Label(self, text="El:")

        self.az_field = tk.Entry(self, textvariable=self.az_var)
        self.el_field = tk.Entry(self, textvariable=self.el_var)

        self.slew_button = tk.Button(self, text="Slew", command=self.slew, width=10)
        self.track_button = tk.Button(self, text="Print az, el", command=self.print_azel, width=10)
        
        self.selector_label = tk.Label(self, text="Coordinate selection:")

        self.gal_selector = tk.Radiobutton(self, text="l, b", value=True, variable=self.selector_state, command=self.select_coords)
        self.azel_selector = tk.Radiobutton(self, text="Az/El", value=False, variable=self.selector_state, command=self.select_coords)

        #Arrange pointing objects
        self.gal_long_label.grid(column=0, row=0)
        self.gal_lat_label.grid(column=0, row=1)

        self.gal_long_field.grid(column=1, row=0, columnspan=2)
        self.gal_lat_field.grid(column=1, row=1, columnspan=2)


        self.az_label.grid(column=3, row=0)
        self.el_label.grid(column=3, row=1)

        self.az_field.grid(column=4, row=0, columnspan=2)
        self.el_field.grid(column=4, row=1, columnspan=2)

        self.slew_button.grid(column=6, row=0)
        self.track_button.grid(column=6, row=1)
        
        self.selector_label.grid(column=0, row=2, columnspan=2)

        self.gal_selector.grid(column=2, row=2)
        self.azel_selector.grid(column=3, row=2)

        #Initialize tracking and control objects
        self.tracker = source_tracking()
   


#    def print_lb(self):
#        print("l: ", self.l_var.get(), ", b: ", self.b_var.get())

    def print_azel(self):
        print("Az: ", self.az_var.get(), ", El: ", self.el_var.get())

    def select_coords(self):
        #

        if self.selector_state.get():
            print("Selector State: ", self.selector_state.get())
            
            self.gal_long_field.config(state="normal")
            self.gal_lat_field.config(state="normal")

            self.az_field.config(state="readonly")
            self.el_field.config(state="readonly")

        else:
            print("Selector State: ", self.selector_state.get())

            self.az_field.config(state="normal")
            self.el_field.config(state="normal")


            self.gal_long_field.config(state="readonly")
            self.gal_lat_field.config(state="readonly")


         

    def slew(self):
        #Slew to given coordinates - either l, b or azel

        if self.selector_state.get():
            print("Selector State: ", self.selector_state.get())
            print("l: ", self.l_var.get(), ", b: ", self.b_var.get())

            try:
                    l = float(self.l_var.get())
                    b = float(self.b_var.get())
            except ValueError:
                    print("Invalid numeric values for l, b.")
                    

            now, az, el = self.tracker.tracking_galactic_coordinates( L=l, B=b)

            #TODO add check for valid elevation

            print("Az: ", az, ", El: ", el)

            self.az_var.set(format(az, ".2f"))
            self.el_var.set(format(el, ".2f"))


        else: 
            print("Selector State: ", self.selector_state.get())
            print("Az: ", self.az_var.get(), ", El: ", self.el_var.get())



    




root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("500x150")

observatory_interface = Interface(root)
observatory_interface.mainloop()




