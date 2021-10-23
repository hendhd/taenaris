#!/usr/bin/python

import os
import sys
import pyvo


from astropy import coordinates
from astropy import table

from astropy.io import votable
import sed


from sed import SedPlot


def magic_table(params):

    # Read the table from local URL
    table=votable.parse_single_table(params['url'])
    return params['table-id'],table


def magic_table_row(params, tables):
    # Get the table id. It's possible to handle more than one table at
    # once, so keeping track of which row of which table is received is
    # a crucial task. 
    tab_id=params['table-id']

    # Get the row index
    row_ind=int(params['row'])

    # Select the right table
    votable=tables[tab_id]

    # convert the votable to an astropy table to select the right row
    table=votable.to_table()
    
    # Select the row from row index
    row=table[row_ind]
    
    # Sent the VOtable and the row to get the photometry. The votable is
    # necessary because of the included metadata, espcially the ucds. 
    phot=sed.make_sed(votable,row)
    return (phot)
    

# We use a contextmanager to avoid "collecting" dead clients in the SAMP
# hub. 

@pyvo.samp.contextlib.contextmanager
def SAMP_conn ():

    client_name="PyVO:SED"
    description = """A Python SAMP Handler based on Pyvo
                     to handle table row message"""


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
    tables={}
    sedplt=SedPlot()

    # Due to name spaces, binding limits and to avoid using global
    # variables, we have to define the receiver function within the main
    # function to access the client. 
    
    def receive_call_table(
            private_key, sender_id, msg_id, 
            mtype, params, extra):
        conn.reply(msg_id, 
                   {"samp.status": "samp.ok", 
                    "samp.result": {} })
        table_id, table = magic_table(params)
        tables[table_id]=table

        return "OK"

    def receive_highlight_row( 
            private_key, sender_id, msg_id, 
            mtype, params, extra):
        conn.reply(msg_id, 
                   {"samp.status": "samp.ok", 
                    "samp.result": {} })
        phot=magic_table_row(params, tables)
        sedplt.get_new_data(phot)
        return "OK"

    # Use the pyvo contextmanager for the sake of the SAMP hub's sanity
    with SAMP_conn() as conn:
     
        # Bind the function receive_call() to a SAMP mtype. 
        # This function will be executed and can contain python magic. 
        conn.bind_receive_call (
            "table.load.votable",
            receive_call_table)

        conn.bind_receive_message (
            "table.highlight.row",
            receive_highlight_row)

        # Get some input so we have a bit of control over the script. 
        
        
        while True:
            if sedplt.new_data==True:
                sedplt.update_plot()

if __name__=="__main__":
  main()

