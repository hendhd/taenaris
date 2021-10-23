#!/usr/bin/python


import pickle
import os
import sys

import numpy as np
import pyvo


from astropy import coordinates
from astropy import units as u
from astropy import table


from astropy.io import votable

from matplotlib import pyplot as plt




def make_sed(votable, ap_row):
    phots=[]
    
    ucd_to_wl_old = {
    # SDS colors
    "phot.mag;em.opt.u": 3.5e-7,
    "phot.mag;em.opt.b": 4.5e-7,
    "phot.mag;em.opt.r": 6.75e-7,
    "phot.mag;em.opt.i": 8.75e-7,
    # 2MASS 
    "phot.mag;em.ir.j": 1.25e-6,
    "phot.mag;em.ir.h": 1.75e-6,
    "phot.mag;em.ir.k": 2.2e-6,
    # WISE
    "phot.mag;em.ir.3-4um": 3.5e-6,
    "phot.mag;em.ir.4-8um": 6e-6,
    "phot.mag;em.ir.8-15um": 11.5e-6,
    "phot.mag;em.ir.15-30um": 22.5e-6,
}

    # Mapping UCD to wavelength

    ucd_to_wl = {
  "phot.mag;em.opt.u": 3.5e-7,
  "phot.mag;em.opt.b": 4.5e-7,
  "phot.mag;em.opt.r": 6.75e-7,
  "phot.mag;em.opt.i": 8.75e-7,
}

    for ucd in ucd_to_wl: 

        colname=get_colname_from_ucd(votable.fields,ucd)[0]

        mag=ap_row[colname]

        phots.append((ucd_to_wl[ucd], mag))
        
    return phots


def get_colname_from_ucd(fields, ucdpattern):
    """
    Searches through the fields of an astropy votable object and returns
    the list of matche
    """

    matches=[]

    for field in fields:
        if field.ucd:
            ucd=field.ucd.lower()
            if ucd.find(ucdpattern.lower())!=-1:
                matches.append(field.name)
    return matches


class SedPlot():

    def get_to_plot(self, phots):
        self.to_plot=np.array(phots)

    def draw_plot(self, to_plot):
        self.fig.ion()
        self.fig.show()
        self.fig.semilogx(to_plot[:,0], to_plot[:,1], '-')
        self.fig.ylim([min(to_plot[:,1]), max(to_plot[:,1])])
        self.fig.ylabel(ylabel="Mag", fontsize=15)
        self.fig.xlabel(xlabel="Wavelength", fontsize=15)
        self.fig.show()
        self.fig.pause(1)

        
    def get_new_data(self, new_phots):
        self.phots=new_phots
        self.new_data=True

    def update_plot(self):
        self.new_data=False
        self.get_to_plot(self.phots)
        self.fig.clf()
        self.draw_plot(self.to_plot)

    def __init__(self):
        self.fig=plt
        self.new_data=False
        self.phots = [(0,0)]



def plot(sed):

    plt.cla()
    
    to_plot = np.array(sed)
    print(to_plot)
    plt.semilogx(to_plot[:,0], to_plot[:,1], '-')
    plt.ylim([min(to_plot[:,1]), max(to_plot[:,1])])
    plt.ylabel(ylabel="Mag", fontsize=15)
    plt.xlabel(xlabel="Wavelength", fontsize=15)
    plt.show(block=False)


def main():
    pass

    
if __name__=="__main__":
  main()

