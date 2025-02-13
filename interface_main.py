import tkinter as tk


#from source_tracking.Controls import Rot2Prog
from source_tracking.Tracking import source_tracking

from interface.pointing_gui import pointing_frame


root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("550x150")

#control = Rot2Prog()
#rotor = source_tracking(control=control)
rotor = source_tracking()


observatory_interface = pointing_frame(root, rotor=rotor)
observatory_interface.mainloop()




