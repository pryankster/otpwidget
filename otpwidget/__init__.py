from __future__ import print_function
try:
    from tkinter import *
    import tkinter.ttk as ttk
    import tkinter.messagebox as messagebox
except ImportError:
    from Tkinter import *
    import ttk
    import tkMessageBox as messagebox

import pyperclip
from threading import Thread
import pyotp
import time, datetime

bgColor = "#444444"
textColors = [ "#CC2222", "#CCCC00", "#CCCCCC" ]
hiColors = [ "#CC4444", "#EEEE00", "#EEEEEE" ]
barColor = "#CCCCCC"

class OTPWidget(Frame):

    def copy_otp(self):
        s = self.text.get()
        print("Copy %s" % (s,))
        pyperclip.copy(s)

    def quit(self,e):
        self.copy_otp()
        sys.exit(0)

    def update(self):
        mod = int(30-(time.mktime(datetime.datetime.now().timetuple()) % 30));
        if mod == 30 or self.code is None:
            otp = pyotp.TOTP(self.key)
            self.code = "%6.6s" % otp.now()
            print("update code: %s" % (self.code,))
            self.text.set(self.code)
        if mod < 5:
            self.otp["style"] = "alarm.TButton"
        elif mod < 10:
            self.otp["style"] = "warn.TButton"
        else:
            self.otp["style"] = "flat.TButton"

        self.bar["value"] = mod
        print("Set to %s (%d)" % (self.code, mod))
        self.bar.after(1000,self.update)

    def createWidgets(self):
        self.text = StringVar();

        self.otp = ttk.Button(self, 
                        textvar = self.text,
                        command = self.copy_otp,
                        style = "flat.TButton" )

        self.bar = ttk.Progressbar(self,orient="horizontal",
                        length=30,
                        maximum=30,
                        value=15,
                        style="Horizontal.TProgressbar",
                        mode="determinate")

        self.otp.pack( side = TOP )
        self.bar.pack( side = BOTTOM, fill =X ) 


    def __init__(self, master=None, key = None):
        self.count = 0
        Frame.__init__(self, master)
        self.code = None
        self.pack()
        self.createWidgets()
        self.key = key
        self.update()

def __main__():
    import os

    root = Tk()
    root.resizable(0,0)

    s = ttk.Style()
    s.theme_use('classic')
    s.configure('flat.TButton',
                font = ("courier", "28", "bold"),
                background = bgColor,
                foreground = textColors[2],
                highlightcolor = hiColors[2],
                highlightthickness = 0,
                shiftrelief = 0,
                bordercolor = bgColor,
                relief = "flat",
                padding = ( 0, 0, 0, 0 )
                );
    s.map('flat.TButton', foreground = [ 
        ('pressed', bgColor), ('active', hiColors[2]),
    ], background = [ ('pressed', textColors[2]) ] )

    s.configure('warn.TButton',
                font = ("courier", "28", "bold"),
                background = bgColor,
                foreground = textColors[1],
                highlightcolor = hiColors[1],
                highlightthickness = 0,
                shiftrelief = 0,
                bordercolor = bgColor,
                relief = "flat",
                padding = ( 0, 0, 0, 0 )
                )
    s.map('warn.TButton', foreground = [ 
        ('pressed', bgColor), ('active', hiColors[1]),
    ], background = [ ('pressed', textColors[1]) ] )

    s.configure('alarm.TButton',
                font = ("courier", "28", "bold"),
                background = bgColor,
                foreground = textColors[0],
                highlightcolor = hiColors[0],
                highlightthickness = 0,
                shiftrelief = 0,
                bordercolor = bgColor,
                relief = "flat",
                padding = ( 0, 0, 0, 0 )
                )
    s.map('alarm.TButton', foreground = [ 
        ('pressed', bgColor), ('active', hiColors[0]),
    ], background = [ ('pressed', textColors[0]) ] )

    s.configure("Horizontal.TProgressbar", 
                    troughcolor=bgColor,
                    thickness=10,
                    borderwidth=0,
                    troughrelief="flat",
                    relief="flat",
                    background=barColor,
                    );

    authfile = os.path.expanduser("~/.google_authenticator")
    
    try:
        key = open(authfile,"r").readline().strip()
    except IOError as e:
        root.withdraw();
        messagebox.showerror( "Error", "Failed to open %s:\n%s" % (authfile, str(e)))
        sys.exit(1)

    app = OTPWidget(master=root, key=key)
    root.bind_all("q", app.quit)
    root.bind_all("<Escape>", lambda x: sys.exit(0))
    try:
        app.mainloop()
    except KeyboardInterrupt as e:
        print("^C")

    try:
        root.destroy()
    except TclError as e:
        s = str(e)
        if not "has been destroyed" in s:
            print(s)
