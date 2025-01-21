import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time, TimeDelta
from astropy import units as u
from datetime import datetime
import time

# class Telescope:
#         def __init__(self,parameter_file):
#         self.params = {} 

#         file_obj=open(parameter_file)
#         for line in file_obj:
#                 key_value=(line.strip()).split('=')
#                 if len(key_value)==2:
#                         self.params[key_value[0].strip()] = float(key_value[1])

class source_tracking:
    def __init__(self):
        self.START_TIME = None
        self.END_TIME = None
        self.TIME_STEP = None
        self.INTEGRATION_TIME = None
        self.PRESSURE = None
        self.TEMPERATURE = None
        self.HUMIDITY = None
        self.WAVELENGTH = 21.106
        self.LONGITUDE = 12.556680
        self.LATITUDE = 55.701227
        self.HEIGHT = 100

        self.current_azel = None  # Will hold a SkyCoord in AltAz
        self.current_lb = None    # Will hold a SkyCoord in Galactic
        self.telescope_pointing = None
        self.offset = 0
    def boundary_adjustments(self,next,current):
        """Adjust azimuth values for wrapping across 0-360 degrees."""
        
        diff = next - current
        if diff > 300:
            self.offset -= 360
        elif diff < -300:
            self.offset += 360
        return next + self.offset


    def tracking_galactic_coordinates(self, L, B):
        """
        Convert galactic (L, B) to horizontal coordinates (az, el) using the
        current time. Returns (current_time_iso, az_deg, el_deg).
        """
        current_time = Time.now()

        # 1) Galactic to Equatorial
        galactic_coord = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
        equatorial_coord = galactic_coord.icrs

        # 2) Observing location
        observing_location = EarthLocation(
            lat=self.LATITUDE * u.deg,
            lon=self.LONGITUDE * u.deg,
            height=self.HEIGHT * u.m
        )

        # 3) AltAz frame (at current time)
        altaz_frame = AltAz(
            obstime=current_time,
            location=observing_location,
            pressure=self.PRESSURE,
            temperature=self.TEMPERATURE,
            relative_humidity=self.HUMIDITY,
            obswl=self.WAVELENGTH * u.cm
        )

        # 4) Transform Equatorial -> Horizontal
        horizontal_coord = equatorial_coord.transform_to(altaz_frame)
        az = horizontal_coord.az.degree
        el = horizontal_coord.alt.degree

        return current_time.iso, az, el

    def updating_pointing(self, L, B):
        """
        Check if the new (Az, El) differs from the current pointing by >=1 deg.
        If yes, update the pointing.
        """
        current_time, az, el = self.tracking_galactic_coordinates(L, B)
        # Create a new AltAz SkyCoord for comparison
        new_azel = SkyCoord(alt=el * u.deg, az=az * u.deg, frame='altaz')

        # Also keep a galactic SkyCoord for storing L,B
        new_lb = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')

        if self.current_azel is None:
            # First time setting pointing
            self.current_azel = new_azel
            self.current_lb = new_lb
            self.telescope_pointing = SkyCoord(alt=round(el) * u.deg, az=round(az) * u.deg, frame='altaz')
            self.set_pointing(A=round(az), E=round(el))
            print(
                f"\n[{current_time}] Setting initial pointing "
                f"to Az={round(az)}°, El={round(el)}°"
            )
        else:
            # Compare the new pointing with the old pointing
            sep = self.telescope_pointing.separation(new_azel)
            if sep >= 1 * u.deg:
                self.current_azel = new_azel
                self.current_lb = new_lb
                self.telescope_pointing = SkyCoord(alt=round(el) * u.deg, az=round(az) * u.deg, frame='altaz')
                self.set_pointing(A=round(az), E=round(el))
                print(
                    f"\n[{current_time}] Updating pointing "
                    f"to Az={round(az)}°, El={round(el)}°"
                )

    def set_pointing(self, A, E):
        """
        Send command to rotor (placeholder).
        """
        if not self.check_if_allowed_el(E):# print(f"\n ==> Telescope pointed to Az={A}°, El={E}°")
            raise ValueError("Elevation out of bounds!")
        az=self.boundary_adjustments(round(A),self.telescope_pointing.az.deg)
        print(f"\n ==> Telescope pointed to Az={az}°, El={E}°")

    def check_if_allowed_el(self, el, min_el=10, max_el=90):
        """
        Simple check to see if the elevation is within [min_el, max_el].
        """
        if el < min_el or el > max_el:
            print('\n'+f"Elevation is {round(el)}°, but must be in [{round(min_el)}, {round(max_el)}]°.")
            return False
        return True

    def run(self):
        """
        Main interactive loop. Commands:
          T l b  => start/continue monitoring galactic coords (l, b).
          exit   => quit the program.
        """
        while True:
            cmd = input("Enter command: ").strip().lower()
            if cmd == "exit":
                print("Exiting...")
                break

            if cmd.startswith("t "):
                parts = cmd.split()
                if len(parts) < 3:
                    print("Error: Usage: T <l> <b> (e.g., T 10 10)")
                    continue
                try:
                    # Parse the new desired l, b
                    self.current_lb = SkyCoord(
                        l=float(parts[1]) * u.deg,
                        b=float(parts[2]) * u.deg,
                        frame='galactic'
                    )
                    print(
                        f"Set target galactic coordinates to "
                        f"l={self.current_lb.l.deg}° b={self.current_lb.b.deg}°\n"
                    )
                    # Start (or continue) updating pointing every 5s
                    self._monitor_pointing(update_time=5)
                except ValueError:
                    print("Invalid numeric values for l, b.\n")
            else:
                print("Unknown command. Use 'T <l> <b>' or 'exit'.")

    def _monitor_pointing(self, update_time=5):
        """
        Continuously check the pointing every `update_time` seconds (blocking
        loop). Press Ctrl+C to interrupt or type 'exit' in the main loop.
        """
        print(
            f"Starting {update_time}-second monitoring cycle.\n"
            "(Ctrl+C to stop the monitoring cycle.)"
        )
        try:
            while True:
                # If we have a current galactic coordinate, re-check pointing
                if self.current_lb is not None:
                    Lval = self.current_lb.l.degree
                    Bval = self.current_lb.b.degree
                    self.updating_pointing(Lval, Bval)

                time.sleep(update_time)
        except KeyboardInterrupt:
            print("\nMonitoring interrupted by user. Returning to command prompt.")


# Main Execution
# if __name__ == "__main__":
#     observation = Tracker()
#     observation.run()
              

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
        
