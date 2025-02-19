import tkinter as tk


from source_tracking.Controls import Rot2Prog
from source_tracking.Tracking import SourceTracking

from interface.interface_frame import Interface


root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("478x254")

control = Rot2Prog()
rotor = SourceTracking(control=control)


#observatory_interface = pointing_frame(root, rotor=rotor)
observatory_interface = Interface(root, rotor=rotor, detector=None)
print("Created Observatory")
observatory_interface.mainloop()
print("Ran mainloop")




