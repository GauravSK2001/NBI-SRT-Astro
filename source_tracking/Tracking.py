import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time, TimeDelta
from astropy import units as u
from datetime import datetime


class Tracking:
    def __init__(self):
        pass

class G2E: #galactic to equotorial

    def __init__(self,time='now',time_step=10, Lat='55.701227', Long='12.556680', Height=100*u.m):
        self.lat=Lat
        self.lon=Long
        self.height=Height
        if time=='now':
            self.observation_time=str(datetime.now())
        else:
            self.observation_time=time
        self.time_step=time_step
        self.Observation_location=EarthLocation(lat=self.lat,lon=self.lon,height=self.height)
        self.HIlambda=21.106*u.cm
        
    def Convert(self,L,B,t=None):
        Galactic_Coordinates=SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
        equotorial=Galactic_Coordinates.icrs
        if t==None:
            t=str(datetime.now())
        altaz_frame =AltAz(obstime=Time(t), location=self.Observation_location,obswl=self.HIlambda)
        horizontal_coord= equotorial.transform_to(altaz_frame)
        az=horizontal_coord.az.degree
        el=horizontal_coord.alt.degree
        return az, el

    def Check_if_allowed_el(self,el,min_el=10,max_el=90):
        if el<min_el or el>max_el:
            return False
        else: return True
        
