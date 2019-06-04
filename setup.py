from setuptools import setup, find_packages
setup(
        name="otpwidget",
        version="1.3",
        packages = find_packages(),
        description="Display TOTP code, same as Google Authenticator",
        entry_points = {
            "gui_scripts": "otpwidget = otpwidget:__main__",
            "console_scripts": "otpwidgetd = otpwidget:__main__"
        }
)
