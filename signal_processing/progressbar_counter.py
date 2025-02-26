import time

from interface.interface_frame import Interface


class ProgressBarCounter():

    def __init__(self):

        self.interface_frame = None

        self.value = 0

        self.status = "idle"

        self.maximum = 1

    def set_interface_frame(self, interface_frame):
        #Take interface frame
        self.interface_frame = interface_frame
        print("Detector: Added interface")

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

    def save_spectrum(self, fname):
        print("Detector: Simulating saving spectrum to ", fname)

        self.interface_frame.show_saved_fname(fname)
        


    def integrate(self, int_time):
        #Main loop for the object, polls self.status every second.

        self.value = 0
        self.maximum = int_time

        self.status = "active"

        while self.status == "active":
            print(f"Detector: Integrating {self.value}/{self.maximum}")
            


            self.interface_frame.update_progressbar(self.maximum, self.value)

            if self.value >= self.maximum:
                self.status = "idle"
                self.interface_frame.update_progressbar(self.maximum, self.value)
                self.interface_frame.set_int_message("Integration Complete")
                self.save_spectrum(self.interface_frame.savefilename_var.get())

            time.sleep(1)
            self.value += 1

        


