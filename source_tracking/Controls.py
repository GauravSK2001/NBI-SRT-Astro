import time
import serial
from serial import Serial

class Rot2Prog:
    """
    Manages low-level communications with the rotor.
    Sends command packets and receives status packets from the device.
    """
    def __init__(self):
        # Update the port to match your device.
        self.port = "/dev/tty.usbserial-A10PDKDD"
        self.baudrate = 115200

        # Initialize the serial connection.
        self.ser = Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity="N",
            stopbits=serial.STOPBITS_ONE,
            timeout=None
        )

        # Device-specific properties.
        self.pulses_per_degree = 10  # Conversion factor: pulses per degree.
        self.az_min = 0
        self.az_max = 360
        self.el_min = 0
        self.el_max = 360

    def _deg_to_ticks(self, deg, offset):
        """
        Convert degrees to ticks based on the pulses_per_degree and given offset.
        """
        return int(self.pulses_per_degree * (deg + offset))

    def send_pkt(self, cmd, az=None, el=None):
        """
        Build and send a command packet to the rotor.
        If az and el are provided, they are converted to ticks.
        """
        if az is not None and el is not None:
            # Convert degrees to ticks using az_max/el_max as offsets.
            azimuth = self._deg_to_ticks(az, self.az_max)
            elevation = self._deg_to_ticks(el, self.el_max)
        else:
            azimuth = 0
            elevation = 0

        # For this device, the tick values are also used as tick markers.
        ticks_per_degree = self.pulses_per_degree

        # Build the command string (protocol-specific format).
        # Format: "W{azimuth:04d}{ticks_per_degree}{elevation:04d}{ticks_per_degree}{cmd} "
        cmd_string = "W%04d%c%04d%c%c " % (
            azimuth,
            ticks_per_degree,
            elevation,
            ticks_per_degree,
            cmd,
        )
        cmd_bytes = cmd_string.encode("ascii")
        self.ser.write(cmd_bytes)
        time.sleep(1)  # Allow time for the device to process the command.

    def receive_rot2_pkt(self):
        """
        Read a 12-byte status packet from the rotor and decode the azimuth and elevation.
        """
        received_vals = self.ser.read(12)
        if len(received_vals) < 12:
            raise IOError("Incomplete packet read from rotator.")

        # Decode the azimuth.
        az = (
            (received_vals[1] * 100) +
            (received_vals[2] * 10) +
            received_vals[3] +
            (received_vals[4] / 10.0) -
            self.az_max + self.az_min
        )
        # Decode the elevation.
        el = (
            (received_vals[6] * 100) +
            (received_vals[7] * 10) +
            received_vals[8] +
            (received_vals[9] / 10.0) -
            self.el_max + self.el_min
        )
        return az, el

    def point(self, az, el):
        """
        Slew the rotor to the specified Azimuth and Elevation (in degrees).
        Converts given absolute values to relative ones and sends the point command.
        """
        cmd = 0x2F  # Command code for pointing.
        # Convert absolute coordinates to relative values.
        az_relative = az - self.az_min
        el_relative = el - self.el_min
        self.send_pkt(cmd, az=az_relative, el=el_relative)

    def stop(self):
        """
        Send a stop command to the rotor and return the current position.
        """
        cmd = 0x0F  # Command code for stop.
        self.send_pkt(cmd)
        az_relative, el_relative = self.receive_rot2_pkt()
        time.sleep(1)
        return az_relative + self.az_min, el_relative + self.el_min

    def status(self):
        """
        Request the current rotor status and return the Azimuth and Elevation.
        """
        cmd = 0x1F  # Command code for status.
        self.send_pkt(cmd)
        az_relative, el_relative = self.receive_rot2_pkt()
        # time.sleep(1) # faulty delay? sleeps >3 times per 3 seconds
        return az_relative + self.az_min, el_relative + self.el_min

    def Restart(self):
        """
        Send a custom restart packet to the rotor.
        """
        # Custom restart packet (protocol-specific).
        cmd = [0x57, 0xEF, 0xBE, 0xAD, 0xDE, 0x00, 0x00, 0x00,
               0x00, 0x00, 0x00, 0xEE, 0x20]
        packet = bytes(cmd)
        self.ser.write(packet)
        self.ser.flush()
        print("Restarting in 5 sec")
        for _ in range(5, 0, -1):
            print(".")
            time.sleep(1)
        print("...Restarting...")
        time.sleep(2)
        print("...Restarted...")
