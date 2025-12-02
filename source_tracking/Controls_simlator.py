import time

class Simulator_Rot2Prog:
    """
    Manages low-level communications with the rotor.
    Sends command packets and receives status packets from the device.
    """
    def __init__(self):

        # Device-specific properties.
        self.pulses_per_degree = 10  # Conversion factor: pulses per degree.
        self.az_min = 0
        self.az_max = 360
        self.el_min = 0
        self.el_max = 360

        self.movespeed = 1  # Simulated speed of movement in degrees per second.
        self.last_azel = (0, 0)  # Store last known (Az, El) position.
        self.target_azel = (0, 0)  # Store next target (Az, El) position.
        self.last_move_time = time.time()  # Timestamp of the last movement command.

        print("Simulator Rot2Prog initialized.")

    def _deg_to_ticks(self, deg, offset):
        """
        Convert degrees to ticks based on the pulses_per_degree and given offset.
        """
        return int(self.pulses_per_degree * (deg + offset))

    def status(self):
        """
        Request the current rotor status and return the Azimuth and Elevation.
        """
        # Simulate movement towards the next target position.
        current_time = time.time()
        time_elapsed = current_time - self.last_move_time
        az_current, el_current = self.last_azel
        az_target, el_target = self.target_azel

        # Calculate the maximum movement possible in the elapsed time.
        max_move = self.movespeed * time_elapsed

        # Update Azimuth
        az_diff = az_target - az_current
        if abs(az_diff) <= max_move:
            az_current = az_target
        else:
            az_current += max_move if az_diff > 0 else -max_move

        # Update Elevation
        el_diff = el_target - el_current
        if abs(el_diff) <= max_move:
            el_current = el_target
        else:
            el_current += max_move if el_diff > 0 else -max_move

        # Update last known position and timestamp.
        self.last_azel = (az_current, el_current)
        self.last_move_time = current_time

        print(f"Simulator status: Az={az_current:.2f}, El={el_current:.2f}. Time: {time.time():.2f}")

        return az_current, el_current
    
    def point(self, az, el):
        """
        Slew the rotor to the specified Azimuth and Elevation (in degrees).
        Converts given absolute values to relative ones and sends the point command.
        """
        self.status()  # Update current position before moving.
        self.target_azel = (az, el)
        self.last_move_time = time.time()

    def stop(self):
        """
        Send a stop command to the rotor and return the current position.
        """
        self.status()  # Update current position before stopping.
        self.target_azel = self.last_azel  # Set target to current position to stop movement.
        self.last_move_time = time.time()
        return self.last_azel

    def Restart(self):
        """
        Send a custom restart packet to the rotor.
        """
        # For simulation, just reset positions.
        self.last_azel = (0, 0)
        self.target_azel = (0, 0)
        self.last_move_time = time.time()
