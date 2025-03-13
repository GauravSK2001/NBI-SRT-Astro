import tkinter as tk


from source_tracking.Controls import Rot2Prog
from source_tracking.Tracking import SourceTracking

from interface.interface_frame import Interface

#from signal_processing.progressbar_counter import ProgressBarCounter

from signal_processing.detector import Detector
#from signal_processing.mod_PPFB import PPFB

from threading import *


root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("1150x550")

#control = Rot2Prog()                    #Comment this line if not using physical rotor
control=None                             #Comment this line if using physical rotor
rotor = SourceTracking(control=control)

#dsp = PPFB()                            #Comment this line if not using detector hardware
dsp = None                               #Comment this line if using physical rotor
detector = Detector(dsp=dsp)


observatory_interface = Interface(root, rotor=rotor, detector=detector)



observatory_interface.mainloop()




