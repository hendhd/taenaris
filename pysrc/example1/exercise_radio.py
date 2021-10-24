#!/usr/bin/env python3
# -*- coding=utf-8 -*- 
import pyvo
import warnings
import sys

def main():
    # Keep the output of this example "sane".
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    # Query the registry to find tap service with data in the radio
    # band

    services=pyvo.registry.search(
        # Obscore services are special TAP Services
        servicetype="tap",

        # We add the waveband argument
        waveband="radio", 

        # And the tricky part: obscore is a datamodel on a tap service
        datamodel="obscore")

    print (services)


if __name__=="__main__":
    main()
