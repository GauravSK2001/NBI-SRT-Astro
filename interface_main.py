import tkinter as tk


from source_tracking.Controls import Rot2Prog
from source_tracking.Tracking import SourceTracking

from interface.interface_frame import Interface


root = tk.Tk()

root.title("NBI SRT Interface")
root.geometry("650x254")

#control = Rot2Prog() #Comment this line if not using physical rotor
control=None #Comment this line if using physical rotor
rotor = SourceTracking(control=control)


#observatory_interface = pointing_frame(root, rotor=rotor)
observatory_interface = Interface(root, rotor=rotor, detector=None)

observatory_interface.mainloop()





