import tkinter as tk

import sys

import time


import numpy as np

from astropy.coordinates import SkyCoord
from astropy import units as u


class pointing_frame(tk.Frame):
    #Frame containing controls for pointing the telescope including tracking
          
    
    def __init__(self, master, rotor, bd, width, height):
        super().__init__(master, bd=bd, width=width, height=height)
        self.grid()

        #Initialize tracking
        self.rotor = rotor

        num_pointing_columns = 8
        #num_pointing_rows = 5

        #Create variables for messages and taking coordinate/integration time input
        self.pointing_message_var = tk.StringVar(value="Stowed")

        self.l_var = tk.StringVar()
        self.b_var = tk.StringVar()

        self.az_var = tk.StringVar(value=0)
        self.el_var = tk.StringVar(value=0)

        self.selector_state = tk.BooleanVar(value=False)

        self.int_time_var = tk.StringVar()

        #Create labels for pointing
        self.pointing_controls_label = tk.Label(self, text="Pointing Controls", justify="center")

        self.gal_long_label = tk.Label(self, text="l:")
        self.gal_lat_label = tk.Label(self, text="b:")

        self.az_label = tk.Label(self, text="Az:")
        self.el_label = tk.Label(self, text="El:")

        self.selector_label = tk.Label(self, text="Coordinate selection:")

        self.pointing_status_label = tk.Label(self, text="Status:")
        self.pointing_message_label = tk.Label(self, textvariable=self.pointing_message_var, justify="left", anchor="w")

        #Create entries and buttons for controlling telescope pointing
        
        self.gal_long_field = tk.Entry(self, textvariable=self.l_var, state="readonly")
        self.gal_lat_field = tk.Entry(self, textvariable=self.b_var, state="readonly")

        self.az_field = tk.Entry(self, textvariable=self.az_var)
        self.el_field = tk.Entry(self, textvariable=self.el_var)

        self.slew_button = tk.Button(self, text="Slew", command=self.slew, width=6)
        self.track_button = tk.Button(self, text="Track", command=self.track, width=6, state="disabled")

        self.home_button = tk.Button(self, text="Home", command=self.home, width=6)
        self.stow_button = tk.Button(self, text="Stow", command=self.stow, width=6)
        
        self.gal_selector = tk.Radiobutton(self, text="l, b", value=True, variable=self.selector_state, command=self.select_coords)
        self.azel_selector = tk.Radiobutton(self, text="Az/El", value=False, variable=self.selector_state, command=self.select_coords)


        #Arrange pointing objects
        self.pointing_controls_label.grid(column=0, row=0, pady=2, columnspan=num_pointing_columns)

        self.gal_long_label.grid(column=0, row=1, pady=2, sticky="w")
        self.gal_lat_label.grid(column=0, row=2, pady=2, sticky="w")

        self.gal_long_field.grid(column=1, row=1, columnspan=2, pady=2, sticky="w")
        self.gal_lat_field.grid(column=1, row=2, columnspan=2, pady=2, sticky="w")


        self.az_label.grid(column=3, row=1, pady=2, sticky="w")
        self.el_label.grid(column=3, row=2, pady=2, sticky="w")

        self.az_field.grid(column=4, row=1, columnspan=2, pady=2, sticky="w")
        self.el_field.grid(column=4, row=2, columnspan=2, pady=2, sticky="w")

        self.slew_button.grid(column=6, row=1, padx=4, pady=2, sticky="w")
        self.track_button.grid(column=6, row=2, padx=4, pady=2, sticky="w")

        self.stow_button.grid(column=7, row=1, pady=2, sticky="w")
        self.home_button.grid(column=7, row=2, pady=2, sticky="w")
        
        self.selector_label.grid(column=0, row=3, columnspan=2, pady=2, sticky="w")

        self.gal_selector.grid(column=2, row=3, pady=2, sticky="w")
        self.azel_selector.grid(column=3, row=3, pady=2, sticky="w")

        self.pointing_status_label.grid(column=0, row=4, pady=2, sticky="w")
        self.pointing_message_label.grid(column=1, row=4, pady=2, columnspan=7, sticky="w")

        
   


#    def print_lb(self):
#        print("l: ", self.l_var.get(), ", b: ", self.b_var.get())

#    def print_azel(self):
#        print("Az: ", self.az_var.get(), ", El: ", self.el_var.get())

    def select_coords(self):
        #

        if self.selector_state.get():
            print("Selector State: ", self.selector_state.get())
            
            #Enable l, b inputs
            self.gal_long_field.config(state="normal")
            self.gal_lat_field.config(state="normal")

            #Enable tracking
            self.track_button.config(state="normal")

            #Disable az/el inputs
            self.az_field.config(state="readonly")
            self.el_field.config(state="readonly")

            

        else:
            print("Selector State: ", self.selector_state.get())

            #Enable az/el inputs
            self.az_field.config(state="normal")
            self.el_field.config(state="normal")

            #Disable tracking
            self.track_button.config(state="disabled")

            #Disable l, b inputs
            self.gal_long_field.config(state="readonly")
            self.gal_lat_field.config(state="readonly")

            


         

    def slew(self):
        #Take l, b or azel coordinates and slew telescope if coordinates are valid 

        message = "Slewing"

        if self.selector_state.get():
            print("Selector State: ", self.selector_state.get())
            print("Slewing to l: ", self.l_var.get(), ", b: ", self.b_var.get())

            try:
                l = float(self.l_var.get())
                b = float(self.b_var.get())

                now, az, el = self.rotor.tracking_galactic_coordinates(L=l, B=b)


                print("Az: ", az, ", El: ", el)

                self.az_var.set(round(az))
                self.el_var.set(round(el))

                #Check valid elevation
                if not self.check_valid_el(round(el)):
                    return None
                
                self.set_pointing_message(message)

                #If rotor control is present, try and slew to l, b, otherwise wait 10 seconds
                if self.rotor.control is not None:
                    try:
                        self.rotor.slew(az, el, override=False)
                        print("Issued slew command to rotor")
                
                    except Exception as e:
                        message = f"Slewing error {e}"
                        print(message)
                        self.set_pointing_message(message, is_error=True)

            

                message = "Holding"
                self.set_pointing_message(message)
                         

            except ValueError:
                message = "Invalid numeric values for l, b."
                print(message)
                self.set_pointing_message(message, is_error=True)
                    
        else: 
            print("Selector State: ", self.selector_state.get())
            print("Slewing to Az: ", self.az_var.get(), ", El: ", self.el_var.get())

            try:
                az = float(self.az_var.get())
                el = float(self.el_var.get())


                #Check valid elevation
                if not self.check_valid_el(round(el)):
                        return None
                
                self.set_pointing_message(message)

                #If rotor control is present, try and slew to l, b, otherwise wait 10 seconds
                if self.rotor.control is not None:
                    try:
                        self.rotor.slew(az, el, override=False)
                        print("Issued slew command to rotor")
                    
                    except Exception as e:
                        print(f"Slewing error {e}")

                
                message = "Holding"
                self.set_pointing_message(message)


            except ValueError:
                message = "Invalid numeric values for az, el."
                print(message)
                self.set_pointing_message(message, is_error=True)



    def track(self):
        #Take input l, b coordinates and track if coordinates are valid
        if self.rotor.state != "tracking":
            try:
                l = round(float(self.l_var.get()))
                b = round(float(self.b_var.get()))

                now, az, el = self.rotor.tracking_galactic_coordinates( L=l, B=b)


                print("Az: ", az, ", El: ", el)

                self.az_var.set(round(az))
                self.el_var.set(round(el))

                #Check valid elevation
                if not self.check_valid_el(round(el)):
                    return None
                
            

                message = f"Tracking l:{l}, b:{b}"
                print(message)

                self.set_pointing_message(message)

                self.rotor.track_target(L=l, B=b, )


                self.track_button.config(text="Stop tracking")
                self.update()

            except ValueError:
                message = "Invalid numeric values for l, b."
                print(message)
                self.set_pointing_message(message, is_error=True)

        else:
            self.track_button.config(text="Track")
            self.update()


            
            

        

    def home(self):
        #Slew to home position
        #self.rotor.set_pointing(0, 0, override=False)

        message = "Homing to Az: 0, El: 0"
        print(message)

        self.set_pointing_message(message)

        #If rotor control is present, slew to home position (az=0, el=0)
        if self.rotor.control is not None:
            try:
                self.rotor.home()

                message = "Homed"
                self.set_pointing_message(message)
                self.reset_inputs(True, False)

                self.az_var.set(0)
                self.el_var.set(0)

                    
            except Exception as e:
                print(f"Error in az/el slew: {e}")

            
        else: 
                
            message = "Holding"
            self.set_pointing_message(message)


    def stow(self):
        #Slew to stowed position

        message = "Stowing telescope"
        print(message)

        self.set_pointing_message(message)

        #If rotor is present, slew to stowed position
        if self.rotor.control is not None:
            try:
                self.rotor.stow()
                message = "Stowed"
                self.set_pointing_message(message)
                self.reset_inputs(True, True)

                    
            except Exception as e:
                print(f"Error in az/el slew: {e}")

           
        else: 
                
            message = "Stowed"
            self.set_pointing_message(message)
            self.reset_inputs(True, True)
        

    def check_valid_el(self, el):
        #Check that elevation command is within the rotor range, display an error if not.
        if not self.rotor.check_if_allowed_el(el=el):
            message = f"Input Error: Elevation {round(el)}° not in range, must be between {self.rotor.min_el}° - {self.rotor.max_el}°."
            self.set_pointing_message(message, is_error=True)
            return False
        else:
            return True


    def set_pointing_message(self, message, is_error=False):
        #Change text in pointing message label - change color to red if the message is an error
        print("Setting pointing message to: ", message)
        if is_error:
            self.pointing_message_label.config(fg="red")
        else:
            self.pointing_message_label.config(fg="black")
        
        self.pointing_message_var.set(message)
        self.update()

    def reset_inputs(self, reset_lb=False, reset_azel=False):

        if reset_lb:
            self.l_var.set("")
            self.b_var.set("")
        if reset_azel:
            self.az_var.set("")
            self.el_var.set("")

         



    



"""
root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("550x150")


observatory_interface = Interface(root)
observatory_interface.mainloop()
"""



