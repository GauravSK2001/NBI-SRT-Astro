
import numpy as np

import serial

from serial import Serial

import time





class Rot2Prog:

    def __init__(self):

        self.port = "/dev/ttyUSB0"

        self.baudrate = 115200

        self.ser = Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity="N",
            stopbits=serial.STOPBITS_ONE,
            timeout=None)

        self.pulses_per_degree = 10

        self.az_min = 0

        self.az_max = 360

        self.el_min = 0.0

        self.el_max = 90

        

    def send_pkt(self, cmd, az=None, el=None):

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

        self.serial.write(cmd_bytes)

        time.sleep(1)



    def receive_rot2_pkt(self):

        received_vals = self.ser.serial.read(12)

        az = (

            (received_vals[1] * 100)

            + (received_vals[2] * 10)

            + received_vals[3]

            + (received_vals[4] / 10.0)

            - self.az_max

            + self.az_min

        )

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

        cmd = 0x2F 

        az_relative = az - self.az_min

        el_relative = el - self.el_min

        self.send_pkt(cmd, az=az_relative, el=el_relative)

        

    def stop(self):

        cmd= 0x0f

        self.send_pkt(cmd)

        

    def status(self):

        cmd = 0x1F 

        self.send_pkt(cmd)

        az_relative, el_relative = self.receive_rot2_pkt()

        time.sleep(2)

        return az_relative + self.az_min, el_relative + self.el_min

    

    def Restart(self):

        cmd=[0x57,0xef,0xbe,0xad,0xde,0x00,0x00,0x00,0x00,0x00,0x00,0xee,0x20]

        packet=bytes(cmd)

        self.serial.write(packet)

        self.serial.flush()

        print('Restarting in 5 sec')

        for i in range(5, 0, -1):

            print('.')

            time.sleep(1)  # Wait for 1 second

        print("...Restarting...")

        time.sleep(2)

        print("...Restarted...")

