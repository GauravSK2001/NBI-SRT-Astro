#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.5.1

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import osmosdr
import time




class PPFB(gr.top_block):

    def __init__(self, int_time = 300, filename="radio_integration"):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.Vector_length = Vector_length = 2**13
        self.Taps = Taps = 10
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*Taps/2.0, np.pi*Taps/2.0, np.pi/Vector_length)
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.samp_rate = samp_rate = 6e6
        self.variable_0 = variable_0 = 0
        self.one_sec_display_integration = one_sec_display_integration = 1
        self.int_time = int_time
        self.filename = filename
        self.Window = Window = sinc
        self.PFB_bandwidth_vector_length = PFB_bandwidth_vector_length = 7e3
        self.HI21 = HI21 = 1420.405751768e6
        self.Frequency_Step_Size = Frequency_Step_Size = samp_rate/Vector_length
        self.Bandwidth = Bandwidth = samp_rate

        ##################################################
        # Blocks
        ##################################################

        self.osmosdr_source_1 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'airspy=1'
        )
        self.osmosdr_source_1.set_time_source('gpsdo', 0)
        self.osmosdr_source_1.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(HI21, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(False, 0)
        self.osmosdr_source_1.set_gain(20, 0)
        self.osmosdr_source_1.set_if_gain(0, 0)
        self.osmosdr_source_1.set_bb_gain(20, 0)
        self.osmosdr_source_1.set_antenna('', 0)
        self.osmosdr_source_1.set_bandwidth(0, 0)
        self._int_time_tool_bar = Qt.QToolBar(self)
        self._int_time_tool_bar.addWidget(Qt.QLabel("Integration Time " + ": "))
        self._int_time_line_edit = Qt.QLineEdit(str(self.int_time))
        self._int_time_tool_bar.addWidget(self._int_time_line_edit)
        self._int_time_line_edit.editingFinished.connect(
            lambda: self.set_int_time(int(str(self._int_time_line_edit.text()))))
        self.qtgui_tab_widget_grid_layout_0.addWidget(self._int_time_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.qtgui_tab_widget_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.qtgui_tab_widget_grid_layout_0.setColumnStretch(c, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(Vector_length, True, window.hanning(Vector_length), True, 6)
        self.fft_vxx_0 = fft.fft_vcc(Vector_length, True, window.hanning(Vector_length), True, 6)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0_0_0_2_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0_0_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0_0_0_1_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0_0_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_nlog10_ff_1_0 = blocks.nlog10_ff(1, Vector_length, 0)
        self.blocks_nlog10_ff_1 = blocks.nlog10_ff(1, Vector_length, 0)
        self.blocks_multiply_const_vxx_0_0_0_0_0_2_0 = blocks.multiply_const_vcc(Window[9*Vector_length:10*Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_2 = blocks.multiply_const_vcc(Window[7*Vector_length:8*Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_1_0 = blocks.multiply_const_vcc(Window[8*Vector_length:9*Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_1 = blocks.multiply_const_vcc(Window[6*Vector_length:7*Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_0 = blocks.multiply_const_vcc(Window[5*Vector_length:6*Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0 = blocks.multiply_const_vcc(Window[4*Vector_length:5*Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_vcc(Window[3*Vector_length:4*Vector_length])
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vcc(Window[2*Vector_length:3*Vector_length])
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc(Window[Vector_length:2*Vector_length])
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc(Window[:Vector_length])
        self.blocks_integrate_xx_0_0_0 = blocks.integrate_ff((int(one_sec_display_integration*samp_rate/Vector_length)), Vector_length)
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff((int(one_sec_display_integration*samp_rate/Vector_length)), Vector_length)
        self.blocks_integrate_xx_0 = blocks.integrate_ff((int(int_time*samp_rate/Vector_length)), Vector_length)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_float*Vector_length, '1sec_int', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*Vector_length, 'filename', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0_0_0_0_2_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (0*Vector_length))
        self.blocks_delay_0_0_0_0_2_0 = blocks.delay(gr.sizeof_gr_complex*1, (7*Vector_length))
        self.blocks_delay_0_0_0_0_2 = blocks.delay(gr.sizeof_gr_complex*1, (7*Vector_length))
        self.blocks_delay_0_0_0_0_1_0 = blocks.delay(gr.sizeof_gr_complex*1, (8*Vector_length))
        self.blocks_delay_0_0_0_0_1 = blocks.delay(gr.sizeof_gr_complex*1, (6*Vector_length))
        self.blocks_delay_0_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (5*Vector_length))
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (4*Vector_length))
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (3*Vector_length))
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (2*Vector_length))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, Vector_length)
        self.blocks_complex_to_mag_squared_1_0 = blocks.complex_to_mag_squared(Vector_length)
        self.blocks_complex_to_mag_squared_1 = blocks.complex_to_mag_squared(Vector_length)
        self.blocks_add_xx_0 = blocks.add_vcc(Vector_length)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_1_0, 0), (self.blocks_integrate_xx_0_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_stream_to_vector_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.blocks_stream_to_vector_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_stream_to_vector_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_1, 0), (self.blocks_stream_to_vector_0_0_0_0_0_1, 0))
        self.connect((self.blocks_delay_0_0_0_0_1_0, 0), (self.blocks_stream_to_vector_0_0_0_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_2, 0), (self.blocks_stream_to_vector_0_0_0_0_0_2, 0))
        self.connect((self.blocks_delay_0_0_0_0_2_0, 0), (self.blocks_stream_to_vector_0_0_0_0_0_2_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_2_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_nlog10_ff_1, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_nlog10_ff_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0, 0), (self.blocks_add_xx_0, 4))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_0, 0), (self.blocks_add_xx_0, 5))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_1, 0), (self.blocks_add_xx_0, 6))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_1_0, 0), (self.blocks_add_xx_0, 8))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_2, 0), (self.blocks_add_xx_0, 7))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0_0_2_0, 0), (self.blocks_add_xx_0, 9))
        self.connect((self.blocks_nlog10_ff_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_nlog10_ff_1_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0_0_1, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0_0_1_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0_0_2, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0_0_2_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0_0_2_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_1, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_complex_to_mag_squared_1_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0_0_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0_0_1, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0_0_1_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0_0_2, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0_0_2_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_delay_0_0_0_0_2_0_0, 0))


    def get_Vector_length(self):
        return self.Vector_length

    def set_Vector_length(self, Vector_length):
        self.Vector_length = Vector_length
        self.set_Frequency_Step_Size(self.samp_rate/self.Vector_length)
        self.set_sinc_sample_locations(np.arange(-np.pi*self.Taps/2.0, np.pi*self.Taps/2.0, np.pi/self.Vector_length))
        self.blocks_delay_0.set_dly(int(self.Vector_length))
        self.blocks_delay_0_0.set_dly(int((2*self.Vector_length)))
        self.blocks_delay_0_0_0.set_dly(int((3*self.Vector_length)))
        self.blocks_delay_0_0_0_0.set_dly(int((4*self.Vector_length)))
        self.blocks_delay_0_0_0_0_0.set_dly(int((5*self.Vector_length)))
        self.blocks_delay_0_0_0_0_1.set_dly(int((6*self.Vector_length)))
        self.blocks_delay_0_0_0_0_1_0.set_dly(int((8*self.Vector_length)))
        self.blocks_delay_0_0_0_0_2.set_dly(int((7*self.Vector_length)))
        self.blocks_delay_0_0_0_0_2_0.set_dly(int((7*self.Vector_length)))
        self.blocks_delay_0_0_0_0_2_0_0.set_dly(int((0*self.Vector_length)))
        self.blocks_multiply_const_vxx_0.set_k(self.Window[:self.Vector_length])
        self.blocks_multiply_const_vxx_0_0.set_k(self.Window[self.Vector_length:2*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.Window[2*self.Vector_length:3*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.Window[3*self.Vector_length:4*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0.set_k(self.Window[4*self.Vector_length:5*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_0.set_k(self.Window[5*self.Vector_length:6*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_1.set_k(self.Window[6*self.Vector_length:7*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_1_0.set_k(self.Window[8*self.Vector_length:9*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_2.set_k(self.Window[7*self.Vector_length:8*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_2_0.set_k(self.Window[9*self.Vector_length:10*self.Vector_length])

    def get_Taps(self):
        return self.Taps

    def set_Taps(self, Taps):
        self.Taps = Taps
        self.set_sinc_sample_locations(np.arange(-np.pi*self.Taps/2.0, np.pi*self.Taps/2.0, np.pi/self.Vector_length))

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_Window(self.sinc)
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_Bandwidth(self.samp_rate)
        self.set_Frequency_Step_Size(self.samp_rate/self.Vector_length)
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)

    def get_variable_0(self):
        return self.variable_0

    def set_variable_0(self, variable_0):
        self.variable_0 = variable_0

    def get_one_sec_display_integration(self):
        return self.one_sec_display_integration

    def set_one_sec_display_integration(self, one_sec_display_integration):
        self.one_sec_display_integration = one_sec_display_integration

    def get_int_time(self):
        return self.int_time

    def set_int_time(self, int_time):
        self.int_time = int_time

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_Window(self):
        return self.Window

    def set_Window(self, Window):
        self.Window = Window
        self.blocks_multiply_const_vxx_0.set_k(self.Window[:self.Vector_length])
        self.blocks_multiply_const_vxx_0_0.set_k(self.Window[self.Vector_length:2*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.Window[2*self.Vector_length:3*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.Window[3*self.Vector_length:4*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0.set_k(self.Window[4*self.Vector_length:5*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_0.set_k(self.Window[5*self.Vector_length:6*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_1.set_k(self.Window[6*self.Vector_length:7*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_1_0.set_k(self.Window[8*self.Vector_length:9*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_2.set_k(self.Window[7*self.Vector_length:8*self.Vector_length])
        self.blocks_multiply_const_vxx_0_0_0_0_0_2_0.set_k(self.Window[9*self.Vector_length:10*self.Vector_length])

    def get_PFB_bandwidth_vector_length(self):
        return self.PFB_bandwidth_vector_length

    def set_PFB_bandwidth_vector_length(self, PFB_bandwidth_vector_length):
        self.PFB_bandwidth_vector_length = PFB_bandwidth_vector_length

    def get_HI21(self):
        return self.HI21

    def set_HI21(self, HI21):
        self.HI21 = HI21
        self.osmosdr_source_1.set_center_freq(self.HI21, 0)

    def get_Frequency_Step_Size(self):
        return self.Frequency_Step_Size

    def set_Frequency_Step_Size(self, Frequency_Step_Size):
        self.Frequency_Step_Size = Frequency_Step_Size

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth

    
    def run(self):

        def sig_handler(sig=None, frame=None):
            self.stop()
            self.wait()

        

        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)

        self.start()

        try:
            input('Press Enter to quit: ')
        except EOFError:
            pass
        self.stop()
        self.wait()





def main(top_block_cls=PPFB, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
