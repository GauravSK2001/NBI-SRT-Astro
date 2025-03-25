import time

from threading import *

import numpy as np

from astropy.io import fits
from astropy.coordinates import SkyCoord

import os


class Detector():

    cache_fpath = "../.cached_spectra/"
    spectra_fpath = "../spectra/"

    def __init__(self, dsp, rotor):
        
        # Initialize signal processing object
        self.signal_proc = dsp
        self.rotor = rotor


        #If signal processing is present, use its spectrum settings, or default values otherwise
        if self.signal_proc is not None:
            self.central_freq = self.signal_proc.HI21
            self.n_bins = self.signal_proc.Vector_length
            self.Bandwidth = self.signal_proc.Bandwidth
            self.frequency_spacing=self.Bandwidth/self.n_bins
            self.freq = np.arange(0,self.n_bins)*self.frequency_spacing/1e6-self.Bandwidth/1e6/2

        else:
            self.central_freq = 1420.405751768e6
            self.n_bins = int(2**13)
            self.Bandwidth = 6e6
            self.frequency_spacing=self.Bandwidth/self.n_bins
            self.freq = np.arange(0,self.n_bins)*self.frequency_spacing/1e6-self.Bandwidth/1e6/2
            

        self.interface_frame = None

        self.integration_display_frame = None

        self.value = 0

        self.status = "idle"

        self.maximum = 1

    def set_interface_frame(self, interface_frame):
        #Take interface frame
        self.interface_frame = interface_frame
        print("Detector: Added interface")

    def set_interface_display_frame(self, display_frame):
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

    def save_spectrum(self, fname, int_time, rotor_params):
        print("Detector: Saving spectrum to ", fname)

        hdu = fits.PrimaryHDU()

        binary_data = np.fromfile(open(Detector.cache_fpath + fname), dtype=np.float32)
        hdu.data = binary_data

        hdu.header = self.make_header(int_time, rotor_params)

        hdu.writeto(Detector.spectra_fpath + fname + ".fits")

        self.interface_frame.show_saved_fname(fname)

    def make_header(int_time, rotor_params):
        hdr = fits.open("../signal_processing/header_template.fits")[0].header

        hdr["EXPTIME"] = int_time

        hdr["HIERARCH OBS START"] = time.strftime("%d-%m-%YT%H:%M:%S", rotor_params[0])

        hdr["HIERARCH GAL LONG"] = rotor_params[1].l.deg
        hdr["HIERARCH GAL LAT"] = rotor_params[1].b.deg

        hdr["HIERARCH AZ START"] = rotor_params[2].az.deg
        hdr["HIERARCH EL START"] = rotor_params[2].el.deg

        hdr["HIERARCH AZ END"] = rotor_params[3].az.deg
        hdr["HIERARCH EL END"] = rotor_params[3].el.deg

        return hdr
        
        


    def integrate(self, int_time, fname, rotor_params):
        #Main loop for the object

        self.value = 0
        self.maximum = int_time

        self.status = "active"


        if self.signal_proc is not None:
            print("Detector: Integrating with DSP")
            
            self.signal_proc.integrate(int_time, fname)

        
        self.status = "idle"
        self.interface_frame.set_int_message("Integration Complete")
            

        if self.rotor is not None:
            rotor_params.append(self.rotor.current_source_azel)
        else:
            rotor_params.append(None)

        self.delete_onesec_int_cache()

        self.save_spectrum(self.interface_frame.savefilename_var.get(), int_time, rotor_params)

    def delete_onesec_int_cache(self):
        #Delete cached one-second spectra
        os.remove(Detector.cache_fpath + "onesec_int")