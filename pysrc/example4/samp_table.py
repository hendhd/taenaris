#! /usr/bin/ python
# -*- coding=utf-8 -*- 

# This is a demonstration of the usage of advanced SAMP. 
#
# Make sure you have Topcat installed and open before starting the
# script. 


import pyvo
import warnings
import sys



from astropy.io import votable


def magic_table(params):

    # Let's see what we get
    print (params)

    # This could be some elaborated Python code here!
    print("\nYour Python table magic here")


def magic_coords():
    # Exercise: Add some python Magic so this function will print (ra,dec) for
    # coordinates received via SAMP. 
    print ("\nYour Python Coord magic here")

 

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
    
    def receive_call_table(
            private_key, 
            sender_id, 
            msg_id, 
            mtype, 
            params, 
            extra):

        client.reply(msg_id, 
                   {"samp.status": "samp.ok", 
                    "samp.result": {} })
        # Define the function that actually contains our magic. It's
        # recommended to define it outside the main loop to keep it
        # tidy. 
        magic_table(params)
        return "OK"

    def receive_call_coord():
        # This function will be part of an exercise.
        return "OK"

    # Define client name and description. Don't be too long with the
    # name since it will appear in other Client software and may look
    # badly there. 

    client_name="PyVO: Simple SAMP"
    description = """
        A very simple Python SAMP handler based on PyVO
        Right now, it only accepts to handle tables."""


    # Make the client object
    client = pyvo.samp.SAMPIntegratedClient(

        name=client_name,
        description=description,

        # Let's explicitly listen at the right place. 
        addr="127.0.0.1")
        
    # Eventually connect our client to the hub
    client.connect()
     
    # Bind the function receive_call_table() to a SAMP mtype. 
    # This function will be executed and can contain python magic. 
    client.bind_receive_call (
        "table.load.votable",
        # configure which function shall be called when a message with
        # above mtype is received. Note: this function has to take
        # exactly 6 arguments (see in above definition). 
        receive_call_table)

    # Exercise: bind a function to receive Coordinates via SAMP. Take
    # above lines as example for this, but also have a look into the
    # pyvo documentation and the SAMP standard. 

    # Get some input so we have a bit of control over the script.       
    while stop_script != "s":
            stop_script=input ("To stop script enter s : ")


    # On command end the script
    quit()

if __name__=="__main__":
    main()
