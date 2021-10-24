#!/usr/bin/env python3
# -*- coding=utf-8 -*- 

# Make sure topcat is running and connected to a SAMP hub before running
# this script. 

import pyvo
import warnings
import sys


def main():

    # Keep the output of this example "sane".
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    # define the access URL of the obscore service
    access_url="http://dc.zah.uni-heidelberg.de/tap"

    # define the ADQL query
    adql_query="""

           SELECT TOP 3 * FROM ivoa.obscore  
           
 	           """


    # Make the service object 
    obscore_svc=pyvo.dal.TAPService(access_url)

    # Run the query in synchronous mode 
    result=obscore_svc.run_sync(adql_query)
       
    # Send the resulting table to topcat for further investigation.
    # Note: our first usage of SAMP today. 
    result.broadcast_samp("topcat")
            
if __name__=="__main__":
    main()
