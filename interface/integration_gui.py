import tkinter as tk
from tkinter import ttk

import time

from threading import *



class IntegrationFrame(tk.Frame):
    #Frame containing controls for detector integration

    def __init__(self, master, detector, bd, width, height):
        super().__init__(master, bd=bd, width=width, height=height)
        self.grid()

        #Initialize detector (waveguide)
        self.detector = detector

        #Variable for spectrum save file name
        self.savefilename_var = tk.StringVar()
        
        #Variables for messages and integration time input
        self.int_time_var = tk.StringVar()

        self.int_time_elapsed = tk.IntVar()

        self.int_message_var = tk.StringVar()

        #Create labels for integration controls

        self.savefilename_label = tk.Label(self, text="File Name:")

        self.int_control_label = tk.Label(self, text="Integration Controls", justify="center")

        self.int_time_label = tk.Label(self, text="Integration Time (s):")

        self.int_time_status_label = tk.Label(self, text="Integration Status:")

        self.int_message_label = tk.Label(self, textvariable=self.int_message_var, justify="left", anchor="w")

        #Create entry and buttons for integration and file saving

        self.savefilename_entry = tk.Entry(self, textvariable=self.savefilename_var)

        self.int_time_entry = tk.Entry(self, textvariable=self.int_time_var)

        self.integrate_button = tk.Button(self, text="Integrate", width=13, command=self.integrate)

        self.onesec_int_button = tk.Button(self, text="1 second integration", command=lambda: self.integrate(1))

        self.stop_int_button = tk.Button(self, text="Stop integration", width=13, command=self.stop_integration)

        #Create integration progress bar

        self.int_progress_bar = ttk.Progressbar(self, orient="horizontal", variable=self.int_time_elapsed, length=450)

        #Arrange integration objects

        self.int_control_label.grid(column=0, row=0, columnspan=8, pady=2)

        self.savefilename_label.grid(column=2, row=1, pady=2, sticky="w")

        self.savefilename_entry.grid(column=3, row=1, columnspan=2, pady=2, sticky="w")

        self.int_time_label.grid(column=0, row=2, pady=2, sticky="w")

        self.int_time_entry.grid(column=1, row=2, columnspan=2, pady=2, sticky="w")

        self.integrate_button.grid(column=4, row=2, padx=4, pady=2, sticky="w")

        self.onesec_int_button.grid(column=5, row=2, padx=4, pady=2, sticky="w")

        self.stop_int_button.grid(column=6, row=2, padx=4, pady=2, sticky="w")

        self.int_time_status_label.grid(column=0, row=3, pady=2, sticky="w")

        self.int_message_label.grid(column=1, row=3, columnspan=7, pady=2, sticky="w")

        self.int_progress_bar.grid(column=0, row=4, columnspan=8, padx=4, pady=2, sticky="w")

    def integrate(self, t=None):
        #Take input integration time and integrate.

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

            self.detector.save_spectrum(self.savefilename_var.get())

        else:
            #detector.integrate(t)
            print("Interface: Integrating with detector.")

            integrate_thread = Thread(target=self.detector.integrate, daemon=True, args=[t])
            integrate_thread.start()




    def update_progressbar(self, t, time_elapsed):
        message = f"Integrating for {t} s: {t - time_elapsed} s remaining"
        self.set_int_message(message)

        self.int_time_elapsed.set(time_elapsed)

    
    def stop_integration(self):
        #Stop detector integration

        self.detector.stop()

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

        

