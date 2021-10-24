#!/usr/bin/env python3
# -*- coding=utf-8 -*- 

# This is a demonstration of the usage of advanced SAMP. 
#
# Make sure you have Topcat installed and open before starting the
# script. 

import os
import pyvo
import warnings
import sys



from astropy.io import votable

import astron_smart_cutout as astron



def magic_coords(params):
    # Exercise: Add some python Magic so this function will print (ra,dec) for
    # coordinates received via SAMP. 

    ra,dec = params['ra'], params['dec']
    
    print ("\nYour Python Coord magic here")
    print (ra, dec)
    result=astron.recipe(ra,dec)




# We use a contextmanager to avoid "collecting" dead clients in the SAMP
# hub. 

@pyvo.samp.contextlib.contextmanager
def SAMP_conn ():

    client_name="PyVO: Astron Cutout"
    description = """
        A very simple Python SAMP handler based on PyVO
        """


    # Make the client object
    client = pyvo.samp.SAMPIntegratedClient(
        name=client_name,
        description=description,
        # Let's explicitly listen at the right place:
        addr="127.0.0.1")
    
    # Connect to the SAMP-hub
    client.connect()
    try:
        yield client

    finally: 
        client.disconnect()




def main():
    # Keep the output of this example "sane".
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    # We will later ask for input, so we need to define the variable
    # before. 
    stop_script=""


    # Due to name spaces, binding limits and to avoid using global
    # variables, we have to define the receiver function within the main
    # loop to access the client. 
    
    def receive_call_coord(
        # This function will be part of an exercise.
            private_key, 
            sender_id, 
            msg_id, 
            mtype, 
            params, 
            extra):

        conn.reply(msg_id, 
                   {"samp.status": "samp.ok", 
                    "samp.result": {} })
                    
        print("receive_call_coord")
        print(params)

        magic_coords(params)

        return "OK"

    # Use the pyvo contextmanager for the sake of the SAMP hub's sanity
    with SAMP_conn() as conn:
     
        # Bind the function receive_call() to a SAMP mtype. 
        # This function will be executed and can contain python magic. 
            
        conn.bind_receive_call (
            "coord.pointAt.sky",
            receive_call_coord)


        # Get some input so we have a bit of control over the script.       
        while stop_script != "s":
            stop_script=input ("To stop script enter s : ")


    # On command end the script
    quit()

if __name__=="__main__":
    main()
