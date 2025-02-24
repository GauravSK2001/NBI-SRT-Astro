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
        self.value=0
        self.maximum = 1
        
        self.status = "idle"




    def int_loop(self):
        #Main loop for the object, polls self.status every second.

        while True:

            if self.interface_frame is None:
                continue
            print(self.status)
            if self.status == "active":
                print(f"Detector: Integrating {self.value}/{self.maximum}")
                self.value += 1


                self.interface_frame.set_time_elapsed(self.maximum, self.value)

                if self.value == self.maximum:
                    self.status = "idle"
                    self.interface_frame.set_time_elapsed(self.value)

                time.sleep(1)


