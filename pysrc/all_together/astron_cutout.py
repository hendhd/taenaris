#! /usr/bin/ python
# -*- coding=utf-8 -*- 

# A demo program for PyVO
# 1. 
# 2. 
# 3. Use the datalink and SODA to make a cutout on this image around the
# galaxies we are interested in. 
#
# Make sure to have Aladin open and connected to the SAMP hub before
# starting the script.
#
# Markus Demleitner and Hendrik Heinl
# heinl@g-vo.org
#

import pyvo

import tempfile
import contextlib
import os
import warnings
import sys

from astropy import units as u
from astropy.table import Table
from astropy.io import votable


# Keep the output of this example "sane".

if not sys.warnoptions:
    warnings.simplefilter("ignore")

        

def get_single_radiosrc(ra,dec):
    """ Get radio sources with TAP-Query"""
    
    # Make the TAP service object
    service = pyvo.dal.TAPService ("https://vo.astron.nl/tap")

    # The ADQL query:
    query= """
        SELECT 
        lolss.source, lolss.ra, lolss.dec, lolss.maj_axis 
        FROM lolss.source_catalog AS lolss
        WHERE DISTANCE (
                POINT ('', lolss.ra, lolss.dec),
                POINT ('', {pos_ra}, {pos_dec})) < 100./3600. 
          """.format(pos_ra=ra, pos_dec=dec)

    # Run Search ASTRON table to obtain mosaic data
    result = service.run_sync(
                query=query,)

    return result


# PyVO won't let us send FITS image via samp, so here is the workaround
# to make it do so!
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


def recipe(ra,dec):

    # get data about radio sources from ASTRON services
    radiosource=get_single_radiosrc(ra,dec)

    # make the service object of the ASTRON TAP service
    svc = pyvo.dal.TAPService("https://vo.astron.nl/tap")
    
	# get the data of the lolss mosaic
    result = svc.run_sync("SELECT pubdid FROM lolss.mosaic")

    # We only have one result; get the datalink object for it.
    dl = next(result.iter_datalinks())
    
    # Get "the" processing service in there 
    soda_svc = dl.get_first_proc()

    # And now do the cutouts:
    for (oid, ra, dec, maj_axis) in radiosource.to_table():
        a=soda_svc.process(
            circle=[
                ra*u.deg, dec*u.deg, 
                maj_axis/3600*u.deg]).read()
 
        # Send the cutout to Aladin 
        with accessible_binary(a) as img_url:
            with pyvo.samp.connection() as conn:

                pyvo.samp.send_image_to(
                    conn=conn, 
                    url=img_url, 
                    client_name="Aladin")

    return "OK"


def main():
    receipe (240.484, 46.768)


if __name__=="__main__":
    main()

