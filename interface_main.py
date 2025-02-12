import tkinter as tk

import sys

#from source_tracking.Controls import Rot2Prog
from source_tracking.Tracking import source_tracking

from interface.pointing_gui import Interface

import numpy as np

from astropy.coordinates import SkyCoord
from astropy import units as u



root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("550x150")

#control = Rot2Prog()
#rotor = source_tracking(control=control)
rotor = source_tracking()


observatory_interface = Interface(root, tracker=rotor)
observatory_interface.mainloop()




