import tkinter as tk
from tkinter import filedialog
import os


class InterfaceLauncher(tk.Frame):
    #Frame for arranging control sub-frames.

    def __init__(self, master):

        super().__init__(master)
        self.grid()

        self.selector_state = tk.IntVar(self, value=0)

        self.save_directory = tk.StringVar(self, value=os.getcwd() + "/spectra/")

        self.config_filename = "dish1.json"

        #Create labels
        self.launcher_label = tk.Label(self,text="NBITT Launcher")
        self.selector_label = tk.Label(self,text="Select configuration:")
        self.save_directory_label = tk.Label(self, text="Save Directory:")

        #Create config selector buttons
        self.dish1_selector = tk.Radiobutton(self, text="Dish 1", value=0, variable=self.selector_state, command=self.select_mode)
        self.dish2_selector = tk.Radiobutton(self, text="Dish 2", value=1, variable=self.selector_state, command=self.select_mode)
        self.inter_selector = tk.Radiobutton(self, text="Interferometer", value=2, variable=self.selector_state, command=self.select_mode)

        #Create entry for save file directory
        self.save_directory_entry = tk.Entry(self, textvariable=self.save_directory, width=30)

        #Buttons
        self.browse_button = tk.Button(self, text="Browse", command = self.browse)
        self.launch_button = tk.Button(self, text="Launch", command=self.launch)

        #Arrange elements

        self.launcher_label.grid(row=0, column=0, columnspan=4, pady=2)

        self.selector_label.grid(row=1, column=0,  pady=2)
        self.dish1_selector.grid(row=1, column=1,  pady=2)
        self.dish2_selector.grid(row=1, column=2,  pady=2)
        self.inter_selector.grid(row=1, column=3,  pady=2)

        self.save_directory_label.grid(row=2, column=0, pady=2)
        self.save_directory_entry.grid(row=2, column=1, columnspan=2, pady=2)
        self.browse_button.grid(row=2, column=3,  pady=2)

        self.launch_button.grid(row=3, column=1, columnspan=2,  pady=2)







    def select_mode(self):
        #Select configuration file from button selection

        state = self.selector_state.get()

        if state == 0:
            self.config_filename = "dish1.json"
        elif state == 1:
            self.config_filename = "dish2.json"
        elif state == 2:
            self.config_filename = "interferometer.json"

    def browse(self):
        fpath = filedialog.askdirectory()
        self.save_directory.set(fpath)

        self.update()


    

    def launch(self):
        #Launch observatory interface

        

        return None

