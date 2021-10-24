#! /usr/bin/ python
# -*- coding=utf-8 -*- 


import pyvo
import warnings
import sys


def main():

    # Keep the output of this example "sane".
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    # Query the registry to obtain obscore services which offer data in
    # the radio realm

    services=pyvo.registry.search(
        servicetype="tap",
        datamodel="obscore",
        waveband="radio")
    
    # Iterate over the list of obtained services to figure out if they
    # obtain data of a specific position. Note the s_region column we
    # use for this query. It contains a REGIONAL geometry (in this case
    # an array defining a POLYGON) which we can compare with our given
    # position. 

    for svc in services:

        query="""
           SELECT TOP 15 * FROM ivoa.obscore 
           WHERE 1=CONTAINS (
                POINT('',  240.0, 47.0), 
			    s_region )
 			   """

        # Make the service object 
        obscore_svc=pyvo.dal.TAPService(svc.access_url)

        # Run the query in synchronous mode 
        result=obscore_svc.run_sync(query)
       
        # Send the resulting table to topcat for further investigation.
        # Note our first usage of SAMP. 
        result.broadcast_samp("topcat")
            
if __name__=="__main__":
    main()
