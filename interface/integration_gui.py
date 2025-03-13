import tkinter as tk
from tkinter import ttk

import time

from threading import *



class IntegrationFrame(tk.Frame):
    #Frame containing controls for detector integration

    def __init__(self, master, rotor, detector, bd, width, height):
        super().__init__(master, bd=bd, width=width, height=height)
        self.grid()

        #Initialize rotor and detector control objects
        self.rotor = rotor
        self.detector = detector

        #Variables for spectrum save file name
        self.savefilename_var = tk.StringVar()

        self.saved_fname_var = tk.StringVar()
        
        #Variables for messages and integration time input
        self.int_time_var = tk.StringVar()

        self.int_time_elapsed = tk.IntVar()

        self.int_message_var = tk.StringVar()

        #Create labels for integration controls

        self.savefilename_label = tk.Label(self, text="File Name:")

        self.file_saved_label = tk.Label(self, textvariable=self.saved_fname_var)

        self.int_control_label = tk.Label(self, text="Integration Controls", justify="center")

        self.int_time_label = tk.Label(self, text="Integration Time (s):")

        self.int_time_status_label = tk.Label(self, text="Integration Status:")

        self.int_message_label = tk.Label(self, textvariable=self.int_message_var, justify="left", anchor="w")

        #Create labels for observatory conditions

        self.temperature_label = tk.Label(self, text=r"Air Temperature [$^\circ$ C]:")

        self.pressure_label = tk.Label(self, text="Air Pressure [kPa]:")

        self.humidity_label = tk.Label(self, text="Absolute Humidity:")

        self.cloud_label = tk.Label(self, text="Cloud cover [decimal]:")

        #Create entry and buttons for integration and file saving

        self.savefilename_entry = tk.Entry(self, textvariable=self.savefilename_var)

        self.int_time_entry = tk.Entry(self, textvariable=self.int_time_var)

        self.integrate_button = tk.Button(self, text="Integrate", width=13, command=self.integrate, state="disabled")

        self.stop_int_button = tk.Button(self, text="Stop integration", width=13, command=self.stop_integration)

        #Create integration progress bar

        self.int_progress_bar = ttk.Progressbar(self, orient="horizontal", variable=self.int_time_elapsed, length=450)

        #Arrange integration objects

        self.int_control_label.grid(column=0, row=0, columnspan=8, pady=2)

        self.savefilename_label.grid(column=0, row=1, pady=2, sticky="w")

        self.savefilename_entry.grid(column=1, row=1, columnspan=2, pady=2, sticky="w")

        self.file_saved_label.grid(column=4, row=1, columnspan=3, pady=2, sticky="w")

        self.int_time_label.grid(column=0, row=2, pady=2, sticky="w")

        self.int_time_entry.grid(column=1, row=2, columnspan=2, pady=2, sticky="w")

        self.integrate_button.grid(column=4, row=2, padx=4, pady=2, sticky="w")


        self.stop_int_button.grid(column=6, row=2, padx=4, pady=2, sticky="w")

        self.int_time_status_label.grid(column=0, row=3, pady=2, sticky="w")

        self.int_message_label.grid(column=1, row=3, columnspan=7, pady=2, sticky="w")

        self.int_progress_bar.grid(column=0, row=4, columnspan=8, padx=4, pady=2, sticky="w")

    def integrate(self, t=None):
        #Take input integration time and integrate.

        #Set file name to datetime string if no file name is given
        if self.savefilename_var.get() == "" or self.savefilename_var.get().startswith("nbi_"):
            self.savefilename_var.set(time.strftime("nbi_%d-%m-%Y_%H-%M-%S", time.gmtime()))

        #Reset file name message
        self.saved_fname_var.set("")

        #Take integration time input if not given already
        if t is None: 
            try:
                t = int(self.int_time_var.get())

            except ValueError:
                message = "Invalid numeric values for integration time"
                
                self.set_int_message(message, is_error=True)

        print(f"Interface: Integrating for {t} seconds")

        self.int_progress_bar.config(maximum=int(t))

        if self.detector is None:
            #If no detector is present, count down an integration and show progress bar.
            time_elapsed = 0


            while time_elapsed <= t:
                self.int_time_elapsed.set(time_elapsed)

                message = f"Integrating: {t - time_elapsed} s remaining"
                self.set_int_message(message)

                time.sleep(1)
                time_elapsed += 1

            message = "Complete"
            self.set_int_message(message)


        else:
            #detector.integrate(t)
            print("Interface: Integrating with detector.")

            self.detector.status = "active"

            integrate_thread = Thread(target=self.detector.integrate, daemon=True, args=[t, self.savefilename_var.get()])
            integrate_thread.start()




    def update_progressbar(self, t, time_elapsed):
        message = f"Integrating for {t} s: {t - time_elapsed} s remaining"
        self.set_int_message(message)

        self.int_time_elapsed.set(time_elapsed)

    
    def stop_integration(self):
        #Stop detector integration

        self.detector.stop_integration()

        message = f"Integration Stopped"
        self.set_int_message(message)
        


    def set_int_message(self, message, is_error=False):
        #Change text in pointing message label - change color to red if the message is an error
        print("Interface: Setting integration message to: ", message)
        if is_error:
            self.int_message_label.config(fg="red")
        else:
            self.int_message_label.config(fg="black")
        
        self.int_message_var.set(message)
        self.update()

    def show_saved_fname(self, fname):
        #Show new save file name
        print(f"Interface: Saved to: {fname}.fits")
        self.saved_fname_var.set(f"Saved to: {fname}.fits")
        self.update()

    def config_button(self, state):
        #Enable or disable Integrate button

        if state:
            self.integrate_button.config(state="active")
        else:
            self.integrate_button.config(state="disabled")

        

