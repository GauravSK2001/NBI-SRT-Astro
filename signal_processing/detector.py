import time

from threading import *

import numpy as np

from astropy.io import fits
from astropy.coordinates import SkyCoord

from signal_processing.single_track_PPFB import single_track_PPFB as PPFB

import os


class Detector():

    cache_fpath = "/Users/gauravsenthilkumar/repositories/NBI-SRT-Astro/.cached_spectra/"
    spectra_fpath = "/Users/gauravsenthilkumar/repositories/NBI-SRT-Astro/spectra/"

    def __init__(self, rotor):
        
        # Initialize rotor object
        self.rotor = rotor

        self.dsp = None

        #Set up spectrum parameters
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

        if self.dsp is not None:

            self.dsp.stop()
            self.dsp.wait()
        

    def save_spectrum(self, fname, data, int_time, rotor_params):
        print("Detector: Saving spectrum to ", fname)

        hdu = fits.PrimaryHDU()

        #binary_data = np.fromfile(open(Detector.cache_fpath + fname), dtype=np.float32)

        hdu.data = data

        crbin = len(data)//2

        hdu.header = self.make_header(int_time, rotor_params, crbin)

        hdu.writeto(Detector.spectra_fpath + fname + ".fits")

        self.interface_frame.show_saved_fname(fname)

    def make_header(self, int_time, rotor_params, crbin):
        hdr = fits.open("/Users/gauravsenthilkumar/repositories/NBI-SRT-Astro/signal_processing/header_template.fits")[0].header

        print(rotor_params)

        hdr["EXPTIME"] = int_time

        hdr["CRBIN1"] = crbin

        hdr["HIERARCH OBS START"] = time.strftime("%d-%m-%YT%H:%M:%S", rotor_params[0])


        if rotor_params[1] is None:
            hdr["HIERARCH GAL LONG"] = -999
            hdr["HIERARCH GAL LAT"] = -999
        else:
            hdr["HIERARCH GAL LONG"] = rotor_params[1].l.deg
            hdr["HIERARCH GAL LAT"] = rotor_params[1].b.deg

        if rotor_params[2] is None:
            hdr["HIERARCH AZ START"] = -999
            hdr["HIERARCH EL START"] = -999
        else:
            print(rotor_params[2])
            hdr["HIERARCH AZ START"] = rotor_params[2].az.deg
            hdr["HIERARCH EL START"] = rotor_params[2].alt.deg

        if rotor_params[3] is None:
            hdr["HIERARCH AZ END"] = -999
            hdr["HIERARCH EL END"] = -999
        else:
            hdr["HIERARCH AZ END"] = rotor_params[3].az.deg
            hdr["HIERARCH EL END"] = rotor_params[3].alt.deg

        return hdr
        
        


    def integrate(self, int_time, fname, rotor_params):
        #Main loop for the object

        self.value = 0
        self.maximum = int_time

        self.status = "active"


        print("Detector: Integrating with DSP")

        
            

        self.dsp = PPFB(int_time)
        self.interface_frame.set_int_message("Integrating")
        onesec_display_thread = Thread(target=self.integration_display_frame.update_loop, daemon=True)
        onesec_display_thread.start()

        self.dsp.start()

        f_int = None
        
        while True:

            file = open(Detector.cache_fpath + "onesec_int")
            onesec_cache = np.fromfile(file, dtype=np.float32)
            file.close()
            onesec_cache_length = len(onesec_cache)

            if int(onesec_cache_length/self.n_bins) >= int_time or self.status == "idle":

                if int(onesec_cache_length/self.n_bins) == int_time:
                    f_chunks = np.reshape(onesec_cache, (int_time,self.n_bins))
                    f_int = np.sum(f_chunks, axis=0)

                break
            else:
                time.sleep(1)

        self.dsp = None
        self.status = "idle"
        self.interface_frame.set_int_message("Integration Complete")
            

        if self.rotor is not None:
            rotor_params.append(self.rotor.current_source_azel)
        else:
            rotor_params.append(None)

        self.delete_onesec_int_cache()

        if f_int is not None:
            print("Saving Spectrum")
            self.save_spectrum(self.interface_frame.savefilename_var.get(), f_int / int_time, int_time, rotor_params)
        else:
            print("No spectrum to save")

    def delete_onesec_int_cache(self):
        #Delete cached one-second spectra
        os.remove(Detector.cache_fpath + "onesec_int")