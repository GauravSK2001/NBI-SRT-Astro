import tkinter as tk


class Interface(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        self.grid()

        self.gal_long_label = tk.Label(self, text="l:").grid(column=0, row=0)
        self.gal_lat_label = tk.Label(self, text="b:").grid(column=0, row=1)

        self.gal_long_field = tk.Entry().grid(column=1, row=0)
        self.gal_lat_field = tk.Entry().grid(column=1, row=1)

        #self.Label(frame, text="Az:").grid(column=2, row=0)
        #self.Label(frame, text="El:").grid(column=2, row=1)

        self.print_button = tk.Button(self, text="Print l, b", command=self.print_info).grid(column=2, row=0)

    def print_info():
        print()


root = tk.Tk()

observatory_interface = Interface(root)
observatory_interface.mainloop()




