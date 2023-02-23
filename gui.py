import multiprocessing

import speech
from press import *
import customtkinter
import tkinter
from speech import *
from multiprocessing import Process
is_on = True

win = customtkinter.CTk
# global active
# active = False
class App(customtkinter.CTk):
    global active
    active = False
    def __init__(self):
        super().__init__()

        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")
        def switch():
            print(self.switch.get())
            if self.switch.get() == 1:
                global active
                active = True
            if self.switch.get() == 0:

                active = False
        self.frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)

        self.switch = customtkinter.CTkSwitch(self.frame, text="Switch", command=switch)
        self.switch.place(x=10, y=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()



