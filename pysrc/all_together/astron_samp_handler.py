#! /usr/bin/ python
# -*- coding=utf-8 -*- 

# This is a demonstration of the usage of advanced SAMP. 
#
# Make sure you have Topcat and Aladin installed and open before starting the
# script. 



import pyvo
import astron_cutout as astron

from astropy.table import Table  
from astropy.io import votable

def magic_table(params):

    # This could be some elaborated Python code here!
    print("\nYour Python magic here")

    print (params)

    # table = Table.read(params['url'], format='votable')
    table=votable.parse_single_table(params['url'])

    # table=Table.read("test.vot", format='votable')

    print (table)

    # a=astron.get_radiosrcs_upload(table)
    # fornax.main()
    print (a)


def magic_coords(params):
    ra,dec = params['ra'], params['dec']
    result=astron.recipe(ra,dec)




# We use a contextmanager to avoid "collecting" dead clients in the SAMP
# hub. 

@pyvo.samp.contextlib.contextmanager
def SAMP_conn ():

    client_name="PSH"
    description = """A simple Python SAMP handler based on PyVO"""


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

def ask_continuence():

    x=input ("To stop, enter (s): ")
    if x != "s":
        return False
    else: 
        return True
    

def main():
    stop_script=False

    # Due to name spaces, binding limits and to avoid using global
    # variables, we have to define the receiver function within the main
    # function to access the client. 
    
    def receive_call_table(
            private_key, sender_id, msg_id, 
            mtype, params, extra):
        conn.reply(msg_id, 
                   {"samp.status": "samp.ok", 
                    "samp.result": {} })
        magic_table(params)
        return "OK"

    def receive_call_coord(
            private_key, sender_id, msg_id, 
            mtype, params, extra):
        conn.reply(msg_id, 
                   {"samp.status": "samp.ok", 
                    "samp.result": {} })
        magic_coords(params)
        return "OK"

    # Use the pyvo contextmanager for the sake of the SAMP hub's sanity
    with SAMP_conn() as conn:
     
        # Bind the function receive_call() to a SAMP mtype. 
        # This function will be executed and can contain python magic. 
        conn.bind_receive_call (
            "table.load.votable",
            receive_call_table)
            
        conn.bind_receive_call (
            "coord.pointAt.sky",
            receive_call_coord)

        # Get some input so we have a bit of control over the script.       
        while stop_script != True:
            stop_script=ask_continuence()
        
        # On command end the script
        quit()

if __name__=="__main__":
    main()
