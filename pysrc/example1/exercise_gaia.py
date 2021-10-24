#!/usr/bin/env python3
# -*- coding=utf-8 -*- 

import pyvo

def main():

    # Query the registry to find tap service with data in the radio
    # band

    services=pyvo.registry.search(
        servicetype="tap",
        keywords="gaia")

    print (services)
  
            
if __name__=="__main__":
    main()
