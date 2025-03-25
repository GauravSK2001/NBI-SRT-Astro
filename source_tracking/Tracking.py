import time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u


class SourceTracking:
    VALID_STATES = {"idle", "tracking", "slewing", "stowed", "home", "stopped"}

    def __init__(self, control=None):
        # Observatory location parameters 
        self.LONGITUDE = 12.556672
        self.LATITUDE = 55.701223
        self.HEIGHT = 0  # in meters

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
        self.current_source_azel = None      # Latest computed AltAz of the source
        self.current_source_lb = None        # Latest Galactic coordinates of the source
        self.current_telescope_azel = None   # Last commanded (rounded) AltAz of the telescope

        # Allowed elevation range
        self.min_el = 0
        self.max_el = 90

        # Hardware control interface
        self.control = control

        #Software GUI frames - set to None initially, but added if GUI is used.
        self.gui_control_frame = None
        self.gui_tracking_display_frame = None
        self.gui_integration_frame = None  # Included to disable integration button while not tracking a source

        # Single state attribute – only one state is active at any time.
        self.state = "idle"

        
        # Offset to be added to computed azimuth values (to manage wrap-around)
        self.offset = 0

    #GUI update methods - If no GUI is present, the method does nothing.

    def set_gui_control_frame(self, gui_control_frame):
        #Take interface pointing control frame
        self.gui_control_frame = gui_control_frame
        print("Rotor: Added interface pointing controls")

    def set_gui_integration_frame(self, gui_integration_frame):
        #Take interface pointing display frame
        self.gui_integration_frame = gui_integration_frame
        print("Rotor: Added interface integration controls")

    def set_gui_display_frame(self, gui_display_frame):
        #Take interface pointing display frame
        self.gui_tracking_display_frame = gui_display_frame

        self.update_tracking_plot()


        print("Rotor: Added interface pointing display")

    def update_gui_message(self, message, is_error=False):
        #Update GUI status label, if GUI is present

        if self.gui_control_frame is not None:
            print("Rotor: Updating pointing message to: ", message)
            self.gui_control_frame.set_pointing_message(message, is_error)

    def update_gui_azel_coordinates(self, az, el):
        #Update GUI azimuth and elevation entries during tracking, if GUI is present

        if self.gui_control_frame is not None:
            print(f"Rotor: Updating GUI azel to az {az}, el {el}")
            self.gui_control_frame.set_azel_entries(az, el)

        

    def update_tracking_plot(self):
        #Update GUI tracking plot with current azimuth and elevation
        if self.gui_tracking_display_frame is not None:
            if self.control is not None:

                rotor_az, rotor_el = self.control.status()
                rotor_az = round(rotor_az)
                rotor_el = round(rotor_el)
                self.gui_tracking_display_frame.update_pointing_plot(az=rotor_az, el=rotor_el)
                print(f"Rotor: Updating tracking plot to az {rotor_az}, el {rotor_el}")



    def enable_pointing_gui_buttons(self):
        #Re-enable GUI buttons after slew completes or tracking is stopped, if GUI is present

        if self.gui_control_frame is not None:
            print(self.gui_control_frame.selector_state.get())
            if self.gui_control_frame.selector_state.get():
                buttons = None
            else:
                buttons = [0, 2, 3, 4, 5]

            self.gui_control_frame.enable_pointing_buttons(buttons)

    def reset_pointing_gui_inputs(self, reset_lb, reset_azel, home):

        self.gui_control_frame.reset_inputs(reset_lb, reset_azel)
        if home:
            self.gui_control_frame.set_azel_entries(0, 0)


    def set_integration_button_state(self):
        #Enable or disable integration buttons based on tracking status
        return None
        #if self.gui_integration_frame is not None:

        #    print("Rotor: Enabling Integrate button")
        #    if self.state == "tracking":
        #        self.gui_integration_frame.config_button(True)
        #    else:
        #        self.gui_integration_frame.config_button(False)
        





    #Rotor methods

    def set_state(self, new_state):
        """Set the new state after verifying it's valid."""
        if new_state not in self.VALID_STATES:
            raise ValueError(f"Invalid state: {new_state}")
        self.state = new_state

    def check_if_allowed_el(self, el):
        """Ensure elevation is within acceptable limits."""
        if not (self.min_el <= el <= self.max_el):
            print(f"Elevation {round(el)}° is out of range of allowed values ({self.min_el}° - {self.max_el}°).\n")
            return False
        return True

    def check_if_reached_target(self, target_az, target_el, poll_interval=3):
        """Wait until the telescope reaches the target azimuth and elevation."""
        print("\nWait for 'Target Reached' confirmation...")
        while self.state == "slewing":
            if self.control:
                current_az, current_el = self.control.status()
                self.update_tracking_plot()
                # Use round to avoid small floating differences
                if round(current_az) == round(target_az) and round(current_el) == round(target_el):
                    print("\nTarget Reached.")
                    self.update_gui_azel_coordinates(current_az, current_el)
                    self.update_tracking_plot()
                    break
                time.sleep(poll_interval)  # Pause between checks
            else:
                # If no hardware, just break
                print("\nTarget Reached.")
                break
            

    def boundary_adjustment(self, next_azimuth, current_azimuth):
        """
        Adjust the azimuth value to handle wrap-around cases.
        
        Args:
            next_azimuth (float): The computed source azimuth.
            current_azimuth (int): The current telescope azimuth.
            
        Returns:
            float: The adjusted azimuth.
        """
        diff = next_azimuth - current_azimuth
        print('\nTracking is Updated:')
        print(f"Telescope Pointing: {current_azimuth:.0f}")
        print(f"diff: {diff}")
        print(f"offset: {self.offset}")
        print(f"with offset: {next_azimuth + self.offset}")
        print(f"Source Azimuth: {next_azimuth}\n")
        
        if self.offset==0 and diff > 350: # going from 0 to -10
            self.offset = -360
        elif self.offset==-360 and diff < -350: # going from -10 to 0
            self.offset = 0
        elif self.offset==360 and diff > 350: # going from 361 to 360?
            self.offset = 0
        elif self.offset==0 and diff < -350: # going from 360 to 361
            self.offset = 360
        else:
            pass
        return next_azimuth + self.offset

    def set_pointing(self, az, el, override=False):
        """
        Command the telescope to move to Az=az, El=el after verifying limits.
        The commanded azimuth is adjusted by the current offset.
        """
        if not override:
            if not self.check_if_allowed_el(el):
                raise ValueError("\nElevation out of bounds!")

        if self.control:
            self.control.point(az, el)
        else:
            print(f"\nSimulated pointing to Az={az}° , El={el}°.\n")

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

    def get_current_telescope_az_el(self):
        """
        Retrieve the current telescope azimuth and elevation.
        
        Returns:
            current_az (float): Current azimuth.
            current_el (float): Current elevation.
        """
        if self.current_telescope_azel is None:
            if self.control:
                current_az, current_el = self.control.status()
            else:
                current_az, current_el = 0, 0
        else:
            current_az = self.current_telescope_azel.az.deg
            current_el = self.current_telescope_azel.alt.deg
        return current_az, current_el

    def compute_effective_azimuth(self, raw_az, current_az):        
        adjusted_az = self.boundary_adjustment(raw_az, current_az)
        return round(adjusted_az)

    def update_stored_positions(self,az,el, effective_az, L=None, B=None):
        self.current_source_azel = SkyCoord(az=az * u.deg, alt=el * u.deg, frame='altaz')
        if L is not None and B is not None:
            self.current_source_lb = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
        
        self.current_telescope_azel = SkyCoord(az=effective_az * u.deg, alt=round(el) * u.deg, frame='altaz')
    
    def PPPorint(self,next_azimuth, current_azimuth):
        diff = next_azimuth - current_azimuth
        print(f"Telescope Pointing: {current_azimuth:.0f}")
        print(f"diff: {diff}")
        print(f"offset: {self.offset}")
        print(f"with offset: {next_azimuth + self.offset}")
        print(f"Source Azimuth: {next_azimuth}")
        
        
    def update_pointing(self, L, B):
        """
        Update telescope pointing if the change in position exceeds 1°.
        Adjusts the commanded azimuth using boundary adjustments.
        """
        # Retrieve current telescope azimuth.
        current_telescope_az, current_telescope_el = self.get_current_telescope_az_el()
        # Get current time and computed horizontal coordinates.
        current_time_iso, source_az, source_el = self.tracking_galactic_coordinates(L, B)
        # Round the raw computed azimuth/elevation.
        az_round = round(source_az)
        el_round = round(source_el)


        self.PPPorint(source_az, current_telescope_az)
        # Create a new horizontal coordinate for separation check.
        new_azel = SkyCoord(az=source_az * u.deg, alt=source_el * u.deg, frame='altaz')
        if self.current_telescope_azel is not None:
            separation = self.current_telescope_azel.separation(new_azel).degree
            print('Separation:', separation,'\n')
        
        # Update pointing if the change exceeds 1°.
        if self.current_telescope_azel is None or self.current_telescope_azel.separation(new_azel) >= 1 * u.deg or self.state == "idle":
            
            try:
                # Get current time and computed horizontal coordinates.
                current_time_iso, source_az, source_el = self.tracking_galactic_coordinates(L, B)
                # Round the raw computed azimuth/elevation.
                az_round = round(source_az)
                el_round = round(source_el)
                effective_telescope_az = self.compute_effective_azimuth(source_az, current_telescope_az)
                print(f"[{current_time_iso}] Updated pointing to Az={az_round}°, El={el_round}°")
                # Command the telescope (set_pointing adds the offset).
                self.set_pointing(effective_telescope_az, el_round, override=False)
                # Update stored positions.
                self.update_stored_positions(source_az, source_el, effective_telescope_az, L, B)

                self.update_gui_azel_coordinates(az_round, el_round)
                
            
            except ValueError as e:
                self.stop()
                raise ValueError(e)

    def _update_if_source_available(self):
        """
        Check if a current source is set and update telescope pointing.
        """
        if self.current_source_lb:
            self.update_pointing(self.current_source_lb.l.degree, self.current_source_lb.b.degree)

    def _monitor_pointing(self, update_time=1):
        """
        Continuously update the telescope pointing every `update_time` seconds.
        """
        try:
            while self.state == "tracking":
                self._update_if_source_available()
                self.update_tracking_plot()
                time.sleep(update_time)
        except KeyboardInterrupt:
            self._handle_keyboard_interrupt()

    def _handle_keyboard_interrupt(self):
        """
        Handle a keyboard interrupt (Ctrl+C).
        """
        print("\nTracking stopped by user (Ctrl+C).")
        self.stop()
        print("Returning to terminal...")

    
    def track_target(self, L, B, update_time=5):
        """
        Start continuous tracking of target Galactic coordinates (L, B).
        """
        self.current_source_lb = SkyCoord(l=L * u.deg, b=B * u.deg, frame='galactic')
        print(f"\nTarget galactic coordinates set to: L={L:.2f}°, B={B:.2f}°.")

        __, az, el = self.tracking_galactic_coordinates(L, B)

        self.slew(az, el, override=False)
        self.set_state("tracking")

        self.update_gui_message(f"Tracking l:{L:.2f}, b:{B:.2f}")
        self.set_integration_button_state()

        self._monitor_pointing(update_time=update_time)
    
    def get_current_telescope_az_el(self):
        """
        Retrieve the current telescope azimuth and elevation.
        
        Returns:
            current_az (float): Current azimuth.
            current_el (float): Current elevation.
        """
        if self.current_telescope_azel is None:
            if self.control:
                current_az, current_el = self.control.status()
            else:
                current_az, current_el = 0, 0
        else:
            current_az = self.current_telescope_azel.az.deg
            current_el = self.current_telescope_azel.alt.deg
        return current_az, current_el

    def slew(self, az, el, override=False, home=False, stow=False):
        """
        Slew the telescope to the specified Azimuth and Elevation.
        Blocks until the target is reached or the user interrupts with Ctrl+C.
        """
        try:
            self.set_state("slewing")
            az_cmd, el_cmd = round(az), round(el)
            
            # Retrieve current telescope position.
            current_az, _ = self.get_current_telescope_az_el()
            # Compute effective azimuth with boundary adjustments.
            effective_az = self.compute_effective_azimuth(az, current_az)
            
            # Command the telescope to point at the effective coordinates.
            self.set_pointing(effective_az, el_cmd, override=override)
            
            # Update stored positions.
            self.update_stored_positions(az_cmd, el_cmd, effective_az)
            
            print(f"Slewing to Az={az_cmd}°, El={el_cmd}°...")
            self.check_if_reached_target(az_cmd, el_cmd)

            if home:
                self.set_state("home")

                self.update_gui_message(f"Homed")
                self.reset_pointing_gui_inputs(True, False, True)
                self.enable_pointing_gui_buttons()
            elif stow:
                self.set_state("stowed")

                self.update_gui_message(f"Stowed")
                self.reset_pointing_gui_inputs(True, True, False)
                self.enable_pointing_gui_buttons()
            else:

                self.set_state("idle")

                self.enable_pointing_gui_buttons()

                self.update_gui_message("Holding")
        
        except ValueError as e:
            print(f"Error setting pointing: {e}")
            self.set_state("idle")
        
        except KeyboardInterrupt:
            print("\nSlew interrupted by user (Ctrl+C).")
            self.stop()
            print("Returning to terminal...")

    #Deprecated methods - remaining temporarily in case they turn out useful
    """
    def home(self):
        """
        #Return the telescope to the home position (Az=0°, El=0°).
    """
                
        self.set_state("home")

        self.update_gui_message(f"Homed")
        self.reset_pointing_gui_inputs(True, False, True)

    def stow(self):
        """
        #Stow the telescope to a safe position (Az=0°, El=-15°).
    """
        self.set_state("slewing")
        self.slew(0, -15, override=True)
        self.set_state("stowed")

        self.update_gui_message(f"Stowed")
        self.reset_pointing_gui_inputs(True, True, False)
    """

    def stop(self):
        """
        Stop the telescope and reset relevant tracking variables.
        """
        if self.control:
            az_stop, el_stop = self.control.stop()
            self.set_state("stopped")
            self.current_source_lb = None
            self.offset = 0 if self.offset != -360 else -360
            print(f"Stopped at Az={round(az_stop)}°, El={round(el_stop)}°.")
            self.update_tracking_plot()
            #time.sleep(2)
            self.set_state("idle")

            self.update_gui_message(f"Stopped at Az={round(az_stop)}°, El={round(el_stop)}°.", is_error=True)
            self.set_integration_button_state()

            self.enable_pointing_gui_buttons()
            


            return az_stop, el_stop
        else:
            self.set_state("stopped")
            self.current_source_lb = None
            self.offset = 0 if self.offset != -360 else -360
            time.sleep(2)
            self.set_state("idle")
