import time
import serial
from serial import Serial

class Rot2Prog:
    """
    Class managing hardware-level communications with the rotor.
    Sends commands and receives status from the device.
    """
    def __init__(self):
        # Update port to match your device
        self.port = "/dev/ttyUSB1"
        self.baudrate = 115200

        # Initialize serial connection
        self.ser = Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity="N",
            stopbits=serial.STOPBITS_ONE,
            timeout=None
        )

        # User-defined properties
        self.pulses_per_degree = 10
        self.az_min = 0
        self.az_max = 360
        self.el_min = 0
        self.el_max = 360

    def send_pkt(self, cmd, az=None, el=None):
        """
        Low-level method to build and send a command packet to the rotator.
        """
        if az is not None and el is not None:
            azimuth = int(self.pulses_per_degree * (az + self.az_max))
            elevation = int(self.pulses_per_degree * (el + self.el_max))
        else:
            azimuth = 0
            elevation = 0

        azimuth_ticks = self.pulses_per_degree
        elevation_ticks = self.pulses_per_degree

        cmd_string = "W%04d%c%04d%c%c " % (
            azimuth,
            azimuth_ticks,
            elevation,
            elevation_ticks,
            cmd,
        )
        cmd_bytes = cmd_string.encode("ascii")
        self.ser.write(cmd_bytes)
        time.sleep(1)

    def receive_rot2_pkt(self):
        """
        Low-level method to read a status packet from the rotator.
        Expecting 12 bytes of data.
        """
        received_vals = self.ser.read(12)
        if len(received_vals) < 12:
            raise IOError("Incomplete packet read from rotator.")

        # Decode az
        az = (
            (received_vals[1] * 100)
            + (received_vals[2] * 10)
            + received_vals[3]
            + (received_vals[4] / 10.0)
            - self.az_max
            + self.az_min
        )
        # Decode el
        el = (
            (received_vals[6] * 100)
            + (received_vals[7] * 10)
            + received_vals[8]
            + (received_vals[9] / 10.0)
            - self.el_max
            + self.el_min
        )
        return az, el

    def point(self, az, el):
        """
        Slew the rotor to the specified Az,El (in degrees).
        """
        cmd = 0x2F
        az_relative = az - self.az_min
        el_relative = el - self.el_min
        self.send_pkt(cmd, az=az_relative, el=el_relative)

    def stop(self):
        """
        Send a stop command to the rotator.
        """
        cmd = 0x0F
        self.send_pkt(cmd)
        az_relative, el_relative = self.receive_rot2_pkt()
        time.sleep(1)
        return az_relative + self.az_min, el_relative + self.el_min

    def status(self):
        """
        Send a status command and parse the returning packet.
        """
        cmd = 0x1F
        self.send_pkt(cmd)
        az_relative, el_relative = self.receive_rot2_pkt()
        time.sleep(1)
        return az_relative + self.az_min, el_relative + self.el_min

    def Restart(self):
        """
        Send a custom restart packet to the rotator.
        """
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
