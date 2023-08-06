import logging
import os
from ..constants import *

def setup_logging():
    if not os.path.exists(OPENI_FOLDER):
        os.mkdir(OPENI_FOLDER)
    LOG_FORMAT = "%(asctime)s [%(levelname)s] - %(filename)s %(funcName)s() %(lineno)d: %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    logging.basicConfig(filename=os.path.join(OPENI_FOLDER, "openi.log"), level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)