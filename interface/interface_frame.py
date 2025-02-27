import tkinter as tk

from interface.pointing_gui import PointingFrame

from interface.integration_gui import IntegrationFrame

from interface.tracking_plot_frame import TrackingMap


class Interface(tk.Frame):
    #Frame for arranging control sub-frames.

    def __init__(self, master, rotor, detector):
        super().__init__(master)
        self.grid()

        self.left_panes = tk.PanedWindow(self, orient="vertical", bg="#BFBFBF", border=1, borderwidth=3)
        self.right_panes = tk.PanedWindow(self, orient="vertical")

        #self.add(self.left_panes)
        #self.add(self.right_panes)
        #Create pointing control frame
        self.pointing_controls = PointingFrame(self, rotor=rotor, bd=0, width=550, height=125)
        rotor.set_gui_control_frame(self.pointing_controls)

        #Create integration control frame
        self.integration_controls = IntegrationFrame(self, detector=detector, bd=0, width=500, height=125)
        detector.set_interface_frame(self.integration_controls)

        #Create calibration control frame

        #Create savefile control frame

        #Create pointing display frame
        self.pointing_display = TrackingMap(self, rotor=rotor,  bd=0, width=500, height=125)

        #Create 1-second integration spectrum frame

        #Arrange objects

        self.left_panes.add(self.pointing_controls)
        self.left_panes.add(self.integration_controls)

        self.right_panes.add(self.pointing_display)

        self.left_panes.grid(column=0, row=0)

        self.right_panes.grid(column=1, row=0, sticky="w")
