#!/usr/bin/python3
import sys
import os
import logging
import datetime
from PIL import Image
from utility import configure_logging

libdir = "./lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

configure_logging()

# Dear future me: consider converting this to a WAVESHARE_VERSION variable instead if you ever intend to support more screen sizes.

from waveshare_epd import epd5in83b_V2 # Modified Waveshare verison to use my 5.83in display.

try:
    epd = epd5in83b_V2.EPD()
    logging.debug("Initialize screen")
    epd.init()

    # Full screen refresh at 2 AM
    if datetime.datetime.now().minute == 0 and datetime.datetime.now().hour == 2:
        logging.debug("Clear screen")
        epd.Clear()

    filename = sys.argv[1]

    logging.debug("Read image file: " + filename)
    Himage = Image.open(filename)
    logging.info("Display image file on screen")

    epd.display(epd.getbuffer(Himage))
    epd.sleep()

except IOError as e:
    logging.exception(e)

except KeyboardInterrupt:
    logging.debug("Keyboard Interrupt - Exit")
    epd5in83b_V2.epdconfig.module_exit()
    exit()
