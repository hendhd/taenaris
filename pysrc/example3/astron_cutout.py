#! /usr/bin/ python
# -*- coding=utf-8 -*- 

# A demo program for PyVO
# Use the datalink and SODA to make a cutout of an image on the Astron
# service. 
#
# Make sure to have Aladin open and connected to the SAMP hub before
# starting the script.

import pyvo

import tempfile
import contextlib
import os
import warnings
import sys

from astropy import units as u
from astropy.table import Table
from astropy.io import votable
        


# PyVO won't let us send FITS image via samp, so here is the workaround
# to make it do so.
@contextlib.contextmanager
def accessible_binary(bytes, suffix=".fits"):
        """
        a context manager making some bytes (typically: an image)
        available with a URL for local SAMP clients.
        """
        handle, f_name = tempfile.mkstemp(suffix=suffix)
        with open(handle, "wb") as f:
                f.write(bytes)
        try:
                yield "file://" + f_name
        finally:
                os.unlink(f_name)


def main ():
    # Keep the output of this example "sane".
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    # define ra,dec:
    ra = 240.484 
    dec = 46.768
    radius = 100/3600

    # make the service object of the ASTRON TAP service
    tap_svc = pyvo.dal.TAPService("https://vo.astron.nl/tap")
    
	# get the data of the lolss mosaic
    result = tap_svc.run_sync("SELECT pubdid FROM lolss.mosaic")

    # We only have one result; get the datalink object for it.
    dl = next(result.iter_datalinks())
    
    # Get "the" processing service in there 
    soda_svc = dl.get_first_proc()

    # And now do the cutout:
    a=soda_svc.process(
            circle=[
                ra*u.deg, dec*u.deg, 
                radius*u.deg]).read()

    # Send the cutout to Aladin 
    with accessible_binary(a) as img_url:
        with pyvo.samp.connection() as conn:

            pyvo.samp.send_image_to(
                conn=conn, 
                url=img_url, 
                client_name="Aladin")

    return "OK"


if __name__=="__main__":
    main()

