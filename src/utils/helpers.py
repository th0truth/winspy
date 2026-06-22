from typing import Dict
import logging
import json


logging.basicConfig(
  level=logging.DEBUG,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_data(filename: str, target: str) -> dict:
  data = {}
  try:
    with open(filename, "r",
              encoding="utf-8") as file:
      data: dict = json.loads(file)
    return data.get(target, {})
  except FileNotFoundError:
    logger.error("The specified file could not be found.")
  except PermissionError:
    logger.error("You do not have permission to read this file.")
  except OSError as error:
    logger.error(f"A system error occured: {error}")

  return data