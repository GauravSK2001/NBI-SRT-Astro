import tkinter as tk

print('s')
from source_tracking.Controls import Rot2Prog
print('ds')
from source_tracking.Tracking import SourceTracking
print('sd')
from interface.interface_frame import Interface
print('dsd')
#from signal_processing.progressbar_counter import ProgressBarCounter

from signal_processing.detector import Detector
print('s')
from signal_processing.Final_Spectrograph_Filter import Final_Spectrograph_Filter as PPFB
print('dds')
from threading import *


root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("1188x560")

print("A")

control = Rot2Prog()                    #Comment this line if not using physical rotor
#control=None                             #Comment this line if using physical rotor
rotor = SourceTracking(control=control)
print("A")
dsp = PPFB()                            #Comment this line if not using detector hardware
#dsp = None 
#                               #Comment this line if using detector hardware
detector = Detector(dsp=dsp, rotor=rotor)

print("B")

observatory_interface = Interface(root, rotor=rotor, detector=detector)



observatory_interface.mainloop()




