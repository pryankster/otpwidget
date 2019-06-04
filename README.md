# otpwidget

This is a simple python/tkinter widget to display a google authenticator
code in a window.  Clicking on the window will copy the code to the 
clipboard.

## Requirements

This package uses the pyperclip and pyotp pacakges.  There is a 
requirements.txt file for setup.

## Installation

    % pip install -r requirements.txt
    % pip install .

## Running

You must have the google authenticator token as the first line in a file 
called `.google_authenticator` in your home directory.

The executable is installed as 'otpwidget', and will launch a tkinter window.
