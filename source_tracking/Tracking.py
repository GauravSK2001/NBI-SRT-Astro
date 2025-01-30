import time
from astropy.coordinates import (
    EarthLocation,
    SkyCoord,
    AltAz
)

from astropy.time import Time
from astropy import units as u

class source_tracking:
    """
    High-level source tracking class. Handles coordinate transformations
    (Galactic -> Equatorial -> Horizontal) and provides logic to manage
    the telescope pointing. Uses `Rot2Prog` for actual hardware moves.
    """
    def __init__(self, control=None):
        # Observing location & atmospheric conditions
        self.LONGITUDE = 12.556680
        self.LATITUDE = 55.701227
        self.HEIGHT = 100

        # Optional refraction correction parameters
        self.PRESSURE = None
        self.TEMPERATURE = None
        self.HUMIDITY = None
        self.WAVELENGTH = 21.106  # cm for 1.4 GHz (21-cm line)

        # Track current coordinates
        self.current_azel = None   # A SkyCoord in AltAz
        self.current_lb = None     # A SkyCoord in Galactic
        self.telescope_pointing = None

        # Allowed elevation range
        self.min_el = 0
        self.max_el = 90

        # For managing azimuth wrap-around
        self.offset = 0

        # Reference to the hardware controller (Rot2Prog)
        # If None, we only print moves instead of sending them.
        self.control = control
        

    def boundary_adjustments(self, next_az, current_az):
        """
        Adjust azimuth values for wrapping across 0-360 degrees.
        e.g. if we jump from Az=359 to Az=1, we want to handle that
        gracefully to avoid large backward rotations.
        """
        diff = next_az - current_az
        if diff > 359:
            self.offset -= 360
        elif diff < -359:
            self.offset += 360
        return next_az + self.offset

    def check_if_allowed_el(self, el):
        """
        Return True if the elevation is within the acceptable range; else False.
        """
        if el < self.min_el or el > self.max_el:
            print(
                f"Elevation is {round(el)}°, "
                f"but must be in [{self.min_el}, {self.max_el}]°."
            )
            return False
        return True

    def set_pointing(self, A, E):
        """
        Move the telescope to Az=A, El=E (in degrees),
        with boundary checks and offset adjustments.
        Raises ValueError if elevation is out-of-bounds.
        """
        # 1) Check elevation boundaries
        if not self.check_if_allowed_el(E):

            raise ValueError("Elevation out of bounds!")

        # 2) Correct for az wrap
        current_az = 0 if self.telescope_pointing is None else self.telescope_pointing.az.deg
        corrected_az = round(self.boundary_adjustments(round(A), current_az))

        # 3) Move the hardware if available
        if self.control is not None:
            self.control.point(corrected_az, E)
        else:
            print(f" ==> Telescope pointed to Az={round(corrected_az)}°, El={round(E)}°")

    def tracking_galactic_coordinates(self, L, B):
        """
        Convert galactic (L, B) to horizontal coordinates (Az, El)
        at the current time. Returns (current_time_iso, az_deg, el_deg).
        """
        current_time = Time.now()+1*u.hour

        # 1) Build galactic coord
        galactic_coord = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
        # 2) Convert galactic -> equatorial (ICRS)
        equatorial_coord = galactic_coord.icrs
        # 3) Observing location
        obs_loc = EarthLocation(
            lat=self.LATITUDE * u.deg,
            lon=self.LONGITUDE * u.deg,
            height=self.HEIGHT * u.m
        )
        # 4) AltAz frame
        altaz_frame = AltAz(
            obstime=current_time,
            location=obs_loc,
            pressure=self.PRESSURE,
            temperature=self.TEMPERATURE,
            relative_humidity=self.HUMIDITY,
            obswl=self.WAVELENGTH * u.cm
        )
        # 5) Transform Equatorial -> Horizontal
        horizontal_coord = equatorial_coord.transform_to(altaz_frame)
        az = horizontal_coord.az.degree
        el = horizontal_coord.alt.degree

        return current_time.iso, az, el

    def updating_pointing(self, L, B,update_time):
        """
        Check if the new (Az, El) differs from the last commanded pointing
        by >= ~1 deg. If so, send a new move command.
        """
        current_time, az, el = self.tracking_galactic_coordinates(L, B)
    
        # Build new AltAz SkyCoord for separation check
        new_azel = SkyCoord(alt=el * u.deg, az=az * u.deg, frame='altaz')
        new_lb = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')

        if self.current_azel is None:
            # First time setting pointing
            self.current_azel = new_azel
            self.current_lb = new_lb
            self.telescope_pointing = SkyCoord(
                alt=round(el)*u.deg, az=round(az)*u.deg, frame='altaz'
            )
            try:
                self.set_pointing(A=round(az), E=round(el))
            except ValueError as e:
                raise ValueError(f"{e}")
            print(f"Starting {update_time}-second monitoring cycle.\n"
            "(Ctrl+C to stop the monitoring cycle.)")    
            print(
                f"\n[{current_time}] Setting initial pointing "
                f"to Az={round(az)}°, El={round(el)}°"
            )
            
        else:

            # Compare the new pointing with the old pointing
            sep = self.telescope_pointing.separation(new_azel)
            if sep >= 0.99 * u.deg:
                self.current_azel = new_azel
                self.current_lb = new_lb
                self.telescope_pointing = SkyCoord(
                    alt=round(el)*u.deg, az=round(az)*u.deg, frame='altaz'
                )
                try:
                    self.set_pointing(A=round(az), E=round(el))
                except ValueError as e:
                    raise ValueError(f"{e}")
                    
                print(
                    f"\n[{current_time}] Updating pointing "
                    f"to Az={round(az)}°, El={round(el)}°"
                )



    def _monitor_pointing(self, update_time=5):

        switch = True
        try:
            while switch:
                if self.current_lb is not None:
                    Lval = self.current_lb.l.degree
                    Bval = self.current_lb.b.degree

                    try:
                        self.updating_pointing(Lval, Bval,update_time)

                    except ValueError as e:
                        print(f"\nError in Tracking: {e}")
                        self.current_lb=None
                        self.current_azel=None
                        self.telescope_pointing=None
                        switch = False
                        break
                        # exit the while loop
                time.sleep(update_time)
        except KeyboardInterrupt:
            print("\n\nMonitoring interrupted by user. Returning to home terminal.")
