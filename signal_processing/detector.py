import time

from threading import *

import numpy as np


class Detector():

    def __init__(self, dsp):
        
        # Initialize signal processing object
        self.signal_proc = dsp


        #If signal processing is present, use its spectrum settings, or default values otherwise
        if self.signal_proc is not None:
            self.central_freq = self.signal_proc.HI21
            self.n_bins = self.signal_proc.Vector_length
            self.Bandwidth = self.signal_proc.Bandwidth
            self.frequency_spacing=self.Bandwidth/self.n_bins
            self.freq = (np.linspace((self.central_freq-self.Bandwidth/2), self.central_freq + self.Bandwidth/2 , self.n_bins)/1e6)

        else:
            self.central_freq = 1420.405751768e6
            self.n_bins = int(2**13)
            self.Bandwidth = 6e6
            self.frequency_spacing=self.Bandwidth/self.n_bins
            self.freq = (np.linspace((self.central_freq-self.Bandwidth/2), self.central_freq + self.Bandwidth/2 , self.n_bins)/1e6)
            

        self.interface_frame = None

        self.integration_display_frame = None

        self.value = 0

        self.status = "idle"

        self.maximum = 1

    def set_interface_frame(self, interface_frame):
        #Take interface frame
        self.interface_frame = interface_frame
        print("Detector: Added interface")

    def set_interface_frame(self, display_frame):
        #Take interface frame
        self.integration_display_frame = display_frame
        print("Detector: Added integration display frame")

    def start(self, int_time):
        #Updates status to "active"

        print(f"Detector: Starting for {int_time} s")
        self.value=0
        self.maximum = int_time
        
        self.status = "active"


    def stop(self):
        #Updates status to "idle"

        print("Detector: Stopping")
        
        self.status = "idle"

        if self.signal_proc is not None:

            self.signal_proc.stop()
            self.signal_proc.wait()

    def save_spectrum(self, fname):
        print("Detector: Saving spectrum to ", fname)

        self.interface_frame.show_saved_fname(fname)
        


    def integrate(self, int_time, fname):
        #Main loop for the object, polls self.status every second.

        self.value = 0
        self.maximum = int_time

        self.status = "active"

        fpath = "../cached_spectra/"

        signal_thread = None

        if self.signal_proc is not None:
            print("Detector: Integrating with DSP")
            signal_thread = Thread(target=self.signal_proc.integrate, daemon=True, args=[int_time, fname])
            signal_thread.start()

        

        while self.status == "active":
            print(f"Detector: Integrating {self.value}/{self.maximum}")
            


            self.interface_frame.update_progressbar(self.maximum, self.value)


            if self.value >= self.maximum:
                self.status = "idle"
                self.interface_frame.update_progressbar(self.maximum, self.value)
                self.interface_frame.set_int_message("Integration Complete")
                

            time.sleep(1)
            self.value += 1

        if signal_thread is not None:
            signal_thread.join()
            self.save_spectrum(self.interface_frame.savefilename_var.get())