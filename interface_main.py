import tkinter as tk

from source_tracking.Controls import Rot2Prog
from source_tracking.Tracking import SourceTracking


from interface.launcher import InterfaceLauncher
from interface.interface_frame import Interface


from signal_processing.detector import Detector



root = tk.Tk()

root.title("NBI SRT Launcher")
# root.geometry("400x120")
root.resizable(False, False)

icon = tk.PhotoImage(file="NBI_SRT_Tandem_logo.png")
root.iconphoto(True, icon)



# observatory_launcher = InterfaceLauncher(root)

# observatory_launcher.mainloop()

#print("Opening interface")
root.geometry("1474x555")
#root.resizable(False, False)


#control = Rot2Prog()                    #Comment this line if not using physical rotor
control=None                             #Comment this line if using physical rotor
rotor = SourceTracking(control=control)


detector = Detector(rotor=rotor)



observatory_interface = Interface(root, rotor=rotor, detector=detector)



observatory_interface.mainloop()


