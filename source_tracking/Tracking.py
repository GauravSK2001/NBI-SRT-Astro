import time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u

class SourceTracking:
    """
    High-level source tracking class.

    Handles coordinate transformations (Galactic → Equatorial → Horizontal)
    and manages telescope pointing using a hardware controller (or simulation).
    """
    
    VALID_STATES = {"idle", "tracking", "slewing", "stowed", "home", "stopped"}

    def __init__(self, control=None):
        # Observatory location parameters
        self.LONGITUDE = 12.556680
        self.LATITUDE = 55.701227
        self.HEIGHT = 100  # in meters

        # Optional refraction correction parameters
        self.PRESSURE = None
        self.TEMPERATURE = None
        self.HUMIDITY = None
        self.WAVELENGTH = 21.106  # cm for 1.4 GHz (21-cm line)

        # Precompute the observer location
        self.obs_loc = EarthLocation(
            lat=self.LATITUDE * u.deg,
            lon=self.LONGITUDE * u.deg,
            height=self.HEIGHT * u.m
        )

        # Tracking state variables
        self.current_azel = None      # Latest computed AltAz (not rounded)
        self.current_lb = None        # Latest Galactic coordinates
        self.telescope_pointing = None  # Last commanded (rounded) AltAz

        # Allowed elevation range
        self.min_el = 0
        self.max_el = 90

        # Hardware control interface
        self.control = control

        # Single state attribute – only one state is active at any time.
        self.state = "idle"
        
        # Offset to be added to computed azimuth values (to manage wrap-around)
        self.offset = 0

    def set_state(self, new_state):
        """Set the new state after verifying it's valid."""
        if new_state not in self.VALID_STATES:
            raise ValueError(f"Invalid state: {new_state}")
        self.state = new_state

    def check_if_allowed_el(self, el):
        """Ensure elevation is within acceptable limits."""
        if not (self.min_el <= el <= self.max_el):
            print(f"Elevation {round(el)}° out of range ({self.min_el}° - {self.max_el}°).")
            return False
        return True

    def check_if_reached_target(self, target_az, target_el, poll_interval=1):
        """
        Poll the hardware's current position until it matches the target,
        or until user stops the program.
        """
        print("\nWait for 'Target Reached' confirmation...")
        while True:
            if self.control:
                current_az, current_el = self.control.status()
                # Use round to avoid small floating differences
                if round(current_az) == round(target_az) and round(current_el) == round(target_el):
                    print("\nTarget Reached.")
                    break
            else:
                # If no hardware, just break
                break
            time.sleep(poll_interval)

    def boundary_adjustments(self, next_az, current_az):
        """
        Adjust azimuth to avoid unnecessary 0/360° crossing.
        Updates self.offset and returns the effective azimuth.
        """
        diff = next_az - current_az
        if diff > 358:
            self.offset -= 360
        elif diff < -358:
            self.offset += 360
        return next_az + self.offset

    def set_pointing(self, az, el, override=False):
        """
        Command the telescope to move to Az=az, El=el after verifying limits.
        The commanded azimuth is adjusted by the current offset.
        """
        if not self.check_if_allowed_el(el) and not override:
            raise ValueError("Elevation out of bounds!")
        effective_az = az + self.offset
        if self.control:
            self.control.point(effective_az, el)
        else:
            print(f"Simulated pointing to Az={effective_az}° (raw: {az}°, offset: {self.offset}°), El={el}°.")

    def check_if_reached_target(self, target_az, target_el, poll_interval=1):
        """
        Poll the hardware (or simulate) until the target position is reached.
        Expects target_az to be the effective azimuth (including offset).
        """
        print("Waiting for target to be reached...")
        while True:
            if self.control:
                current_az, current_el = self.control.status()
                if round(current_az) == round(target_az) and round(current_el) == round(target_el):
                    print("Target reached.")
                    break
            else:
                # In simulation mode, assume immediate completion
                break
            time.sleep(poll_interval)

    def tracking_galactic_coordinates(self, L, B):
        """
        Convert Galactic (L, B) coordinates to horizontal (Az, El) coordinates.
        
        Returns:
            current_time_iso (str): Current time in ISO format.
            az (float): Calculated azimuth (in degrees, before offset).
            el (float): Calculated elevation (in degrees).
        """
        current_time = Time.now()
        galactic_coord = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
        equatorial_coord = galactic_coord.icrs

        altaz_frame = AltAz(
            obstime=current_time,
            location=self.obs_loc,
            pressure=self.PRESSURE,
            temperature=self.TEMPERATURE,
            relative_humidity=self.HUMIDITY,
            obswl=self.WAVELENGTH * u.cm
        )
        horizontal_coord = equatorial_coord.transform_to(altaz_frame)
        return current_time.iso, horizontal_coord.az.degree, horizontal_coord.alt.degree

    def update_pointing(self, L, B):
        """
        Update telescope pointing if the change in position exceeds 1°.
        Adjusts the commanded azimuth using boundary adjustments.
        """
        current_time_iso, az, el = self.tracking_galactic_coordinates(L, B)
        # Round the raw computed azimuth/elevation.
        az_cmd = round(az)
        el_cmd = round(el)
        
        # Determine the current effective azimuth.
        if self.telescope_pointing is None:
            current_effective_az = az_cmd + self.offset
        else:
            current_effective_az = self.telescope_pointing.az.degree
        
        # Adjust azimuth to avoid unnecessary wrap-around.
        effective_az = self.boundary_adjustments(az_cmd, current_effective_az)

        # If no previous pointing exists or the change is >= 1°.
        new_azel = SkyCoord(az=az_cmd * u.deg, alt=el_cmd * u.deg, frame='altaz')
        
        if (self.telescope_pointing is None or 
            self.telescope_pointing.separation(new_azel) >= 1 * u.deg):
            try:
                # Command the telescope (set_pointing adds the offset).
                self.set_pointing(az_cmd, el_cmd, override=False)
                
                # Update stored positions using the effective azimuth.
                self.current_azel = SkyCoord(az=az_cmd * u.deg, alt=el_cmd * u.deg, frame='altaz')
                self.current_lb = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
                self.telescope_pointing = SkyCoord(az=effective_az * u.deg, alt=el_cmd * u.deg, frame='altaz')
                
                print(f"[{current_time_iso}] Updated pointing to Az={az_cmd}°, El={el_cmd}°")
                
                if self.state != "tracking":
                    self.check_if_reached_target(effective_az, el_cmd)
                    self.set_state("tracking")
            
            except ValueError as e:
                print(f"Error setting pointing: {e}")
                self.set_state("idle")

    def _monitor_pointing(self, update_time=5):
        """
        Continuously update the telescope pointing every `update_time` seconds.
        """
        try:
            while True:
                if self.current_lb:
                    self.update_pointing(self.current_lb.l.degree, self.current_lb.b.degree)
                time.sleep(update_time)
        except KeyboardInterrupt:
            print("\nTracking stopped by user (Ctrl+C).")
            if self.control:
                az_stop, el_stop = self.control.stop()
                print(f"Stopped at Az={round(az_stop)}°, El={round(el_stop)}°.")
                self.set_state("stopped")
                time.sleep(3)
                self.set_state("idle")
            else:
                self.set_state("idle")
            print("Returning to terminal...")

    """
    Telescope Actions
    """

    def track_target(self, L, B, update_time=5):
        """
        Start continuous tracking of target Galactic coordinates (L, B).
        """
        self.current_lb = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
        print(f"\nTarget galactic coordinates set to: L={L:.2f}°, B={B:.2f}°.")
        self._monitor_pointing(update_time=update_time)

    def slew(self, az, el, override=False):
            """
            Slew the telescope to the specified Azimuth and Elevation.
            Blocks until the target is reached or the user interrupts with Ctrl+C.
            """
            try:
                self.set_state("slewing")
                az_cmd, el_cmd = round(az), round(el)
                self.set_pointing(az_cmd, el_cmd, override=override)
                self.current_azel = SkyCoord(az=az_cmd * u.deg, alt=el_cmd * u.deg, frame='altaz')
                self.telescope_pointing = self.current_azel
                print(f"Slewing to Az={az_cmd}°, El={el_cmd}°...")
                self.check_if_reached_target(az_cmd, el_cmd)

                self.set_state("idle")
            
            except ValueError as e:
                print(f"Error setting pointing: {e}")
                self.set_state("idle")
            
            except KeyboardInterrupt:
                print("\nSlew interrupted by user (Ctrl+C).")
                if self.control:
                    az_stop, el_stop = self.control.stop()
                    print(f"Stopped at Az={round(az_stop)}°, El={round(el_stop)}°.")
                    self.set_state("stopped")
                else:
                    self.set_state("idle")
                print("Returning to terminal...")
        

    def home(self):
        """
        Return the telescope to the home position (Az=0°, El=0°).
        """
        self.slew(0, 0, override=True)
        self.set_state("home")

    def stow(self):
        """
        Stow the telescope to a safe position (Az=0°, El=-5°).
        """
        self.slew(0, -5, override=True)
        self.set_state("stowed")
