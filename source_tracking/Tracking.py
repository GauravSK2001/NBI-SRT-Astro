import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time, TimeDelta
from astropy import units as u
from datetime import datetime


class Telescope:
        def __init__(self,parameter_file):
        self.params = {} 

        file_obj=open(parameter_file)
        for line in file_obj:
                key_value=(line.strip()).split('=')
                if len(key_value)==2:
                        self.params[key_value[0].strip()] = float(key_value[1])

class Tracking:
        def __init__(self, parameter_file):
        pass

        def boundary_adjustments(self, values):
        offset = 0
        adjusted = [values[0]]
        for i in range(1, len(values)):
            diff = values[i] - values[i - 1]
            if diff > 300:
                offset -= 360
            elif diff < -300:
                offset += 360
            adjusted.append(values[i] + offset)
        return adjusted
        def calculate_sky_path(self, duration, time_step):
            """Calculate azimuth, elevation, and time for the observation period."""
            azimuths, elevations, times = [], [], []
            for i in range(0, duration, time_step):
                current_time = START_TIME + TimeDelta(i, format='sec')
                galactic_coord = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
                equatorial_coord = galactic_coord.icrs
                altaz_frame = AltAz(obstime=current_time, location=OBSERVING_LOCATION,pressure=pressure, temperature=temperature, relative_humidity=relative_humidity,obswl=obswl)
                horizontal_coord = equatorial_coord.transform_to(altaz_frame)
                azimuths.append(horizontal_coord.az.degree)
                elevations.append(horizontal_coord.alt.degree)
                times.append(current_time.iso)
                return azimuths, elevations, times
            
                

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
        
