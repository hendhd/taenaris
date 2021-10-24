#!/usr/bin/env python3
# -*- coding=utf-8 -*- 


def main ():
    proceed="n"
    
    solutions={
    "column names":"source, ra, dec, maj_axis",
    "adql" : """
                                SELECT 
                                lolss.source, lolss.ra, 
                                lolss.dec, lolss.maj_axis 
                                FROM lolss.source_catalog AS lolss
                                WHERE DISTANCE (
                                        POINT ('', lolss.ra, lolss.dec),
                                        POINT ('', 240.0, 47.0)
                                                ) < 100./3600. 
              """

    }

    # Iterating over execise and solutions

    for exercise in solutions:
        print (

        # That's how string interpolation looks like in python3.x

        """ 
        Exercise: {exercise} -- Solution: {solution} 
        """.format(
            exercise=exercise, 
            solution=solutions[exercise]
                  ) 
              )

        # Ask for user action to pause the script:      
        while proceed != "y":
            proceed=input ("Proceed to next exercise ? ")


if __name__=="__main__":
    main()

