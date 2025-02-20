import tkinter as tk

from interface.pointing_gui import pointing_frame

from interface.integration_gui import integration_frame


class Interface(tk.Frame):
    #Frame for arranging control sub-frames.

    def __init__(self, master, rotor, detector):
        super().__init__(master)
        self.grid()

        self.left_panes = tk.PanedWindow(self, orient="vertical", bg="#BFBFBF", border=1, borderwidth=3)
        #self.right_panes = tk.PanedWindow(self, orient="vertical")

        #self.add(self.left_panes)
        #self.add(self.right_panes)
        #Create pointing control frame
        self.pointing_controls = pointing_frame(self, rotor=rotor, bd=0, width=550, height=125)

        #Create integration control frame
        self.integration_controls = integration_frame(self, detector=detector, bd=0, width=500, height=125)

        #Create calibration control frame

        #Create savefile control frame

        #Create pointing display frame

        #Create 1-second integration spectrum frame

        #Arrange objects

        self.left_panes.add(self.pointing_controls)
        self.left_panes.add(self.integration_controls)

        self.left_panes.grid(column=0, row=0)
