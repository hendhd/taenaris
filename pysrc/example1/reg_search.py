#! /usr/bin/ python
# -*- coding=utf-8 -*- 

import pyvo

def main():

    # Query the registry to find tap service with data in the radio
    # band

    services=pyvo.registry.search(
        servicetype="tap",
        waveband="radio")

    print (services)
  
            
if __name__=="__main__":
    main()
