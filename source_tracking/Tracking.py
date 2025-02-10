import time
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
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
        self.min_el = 5   # Prevent pointing too close to the horizon
        self.max_el = 85  # Avoid tracking too close to the zenith

        # For managing azimuth wrap-around
        self.offset = 0

        # Reference to the hardware controller (Rot2Prog)
        self.control = control

    def boundary_adjustments(self, next_az, current_az):
        """
        Adjust azimuth values to prevent unnecessary long rotations
        (avoid crossing 0/360 unnecessarily).
        """
        diff = next_az - current_az
        if diff > 180:
            self.offset -= 360
        elif diff < -180:
            self.offset += 360
        return next_az + self.offset

    def check_if_allowed_el(self, el):
        """
        Check if the elevation is within acceptable limits.
        """
        if el < self.min_el or el > self.max_el:
            print(f"Elevation {round(el)}° out of range ({self.min_el}° - {self.max_el}°).")
            return False
        return True

    def set_pointing(self, A, E):
        """
        Move the telescope to Az=A, El=E after verifying limits.
        """
        if not self.check_if_allowed_el(E):
            raise ValueError("Elevation out of bounds!")

        # Adjust azimuth wrap
        if self.telescope_pointing is None:
            current_az = 0
        else:
            current_az = self.telescope_pointing.az.deg

        corrected_az = round(self.boundary_adjustments(round(A), current_az))

        if self.control:
            self.control.point(corrected_az, E)
        else:
            print(f" ==> Telescope pointed to Az={round(corrected_az)}°, El={round(E)}°")

    def tracking_galactic_coordinates(self, L, B):
        """
        Convert Galactic (L, B) to Horizontal (Az, El) coordinates at current time.
        """
        current_time = Time.now()  # Ensure UTC time
        galactic_coord = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')

        # Convert to equatorial (ICRS) -> horizontal (AltAz)
        equatorial_coord = galactic_coord.icrs
        obs_loc = EarthLocation(
            lat=self.LATITUDE * u.deg,
            lon=self.LONGITUDE * u.deg,
            height=self.HEIGHT * u.m
        )
        altaz_frame = AltAz(
            obstime=current_time,
            location=obs_loc,
            pressure=self.PRESSURE,
            temperature=self.TEMPERATURE,
            relative_humidity=self.HUMIDITY,
            obswl=self.WAVELENGTH * u.cm
        )
        horizontal_coord = equatorial_coord.transform_to(altaz_frame)
        az = horizontal_coord.az.degree
        el = horizontal_coord.alt.degree

        return current_time.iso, az, el

    def updating_pointing(self, L, B, update_time):
        """
        Update telescope pointing if position changed significantly (>1 deg).
        """
        current_time, az, el = self.tracking_galactic_coordinates(L, B)

        new_azel = SkyCoord(alt=el * u.deg, az=az * u.deg, frame='altaz')
        new_lb = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')

        # If new position differs by at least 1 deg in horizontal coords, move
        if (self.current_azel is None) or (self.telescope_pointing.separation(new_azel) >= 1 * u.deg):
            self.current_azel = new_azel
            self.current_lb = new_lb
            self.telescope_pointing = SkyCoord(alt=round(el)*u.deg, az=round(az)*u.deg, frame='altaz')

            try:
                self.set_pointing(A=round(az), E=round(el))
            except ValueError as e:
                print(f"Error setting pointing: {e}")
                return

            print(f"\n[{current_time}] Updated pointing to Az={round(az)}°, El={round(el)}°")

    def _monitor_pointing(self, update_time=5):
        """
        Continuously monitor the tracking position every `update_time` seconds.
        User can stop with Ctrl+C.
        """
        try:
            while True:
                if self.current_lb:
                    Lval = self.current_lb.l.degree
                    Bval = self.current_lb.b.degree

                    try:
                        self.updating_pointing(Lval, Bval, update_time)
                    except ValueError as e:
                        print(f"\nTracking Error: {e}")
                        break

                time.sleep(update_time)
        except KeyboardInterrupt:
            print("\n\nTracking stopped by user.")
            if self.control:
                az, el = self.control.stop()
                print(f"\nStopped at Az={round(az)}°, El={round(el)}°.\n")
                
            print("Returning to terminal.")
