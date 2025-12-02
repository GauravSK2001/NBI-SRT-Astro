#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Interferometry
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PPFB_10tap import PPFB_10tap  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import osmosdr
import time
import sip



class Interferometry(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Interferometry", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Interferometry")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Interferometry")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.prefix_phase_int_time = prefix_phase_int_time = "/home/john/dspira_2021/interferometer_data/test_files/phase/"
        self.prefix_phase_1_sec = prefix_phase_1_sec = "/home/john/dspira_2021/interferometer_data/test_files/phase/"
        self.prefix_mag_int_time = prefix_mag_int_time = "/home/john/dspira_2021/interferometer_data/test_files/magnitude/"
        self.prefix_mag_1_sec = prefix_mag_1_sec = "/home/john/dspira_2021/interferometer_data/test_files/magnitude/"
        self.prefix_hornB_int_time = prefix_hornB_int_time = "/home/john/dspira_2021/interferometer_data/test_files/hornB/"
        self.prefix_hornB_1_sec = prefix_hornB_1_sec = "/home/john/dspira_2021/interferometer_data/test_files/hornB/"
        self.prefix_hornA_int_time = prefix_hornA_int_time = "/home/john/dspira_2021/interferometer_data/test_files/hornA/"
        self.prefix_hornA_1_sec = prefix_hornA_1_sec = "/home/john/dspira_2021/interferometer_data/test_files/hornA/"
        self.one_sec_display_integration = one_sec_display_integration = 1
        self.int_time = int_time = 30
        self.Vector_length = Vector_length = 2**13
        self.HI21 = HI21 = 1420.405751768e6
        self.Bandwidth = Bandwidth = samp_rate

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_vector_sink_f_0_1_0 = qtgui.vector_sink_f(
            Vector_length,
            ((HI21 - samp_rate/2)/1e6),
            ((samp_rate/Vector_length)/1e6),
            "Frequency",
            "Signal",
            "Horn B",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_0.set_y_axis(0, 2000)
        self.qtgui_vector_sink_f_0_1_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_1_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_1_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1_0.set_ref_level(0)


        labels = ["Magnitude", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_0_win)
        self.qtgui_vector_sink_f_0_1 = qtgui.vector_sink_f(
            Vector_length,
            ((HI21 - samp_rate/2)/1e6),
            ((samp_rate/Vector_length)/1e6),
            "Frequency",
            "Signal",
            "Horn A",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1.set_y_axis(0, 2000)
        self.qtgui_vector_sink_f_0_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1.enable_grid(True)
        self.qtgui_vector_sink_f_0_1.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_ref_level(0)


        labels = ["Magnitude", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_win)
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            Vector_length,
            ((HI21 - samp_rate/2)/1e6),
            ((samp_rate/Vector_length)/1e6),
            "Frequency",
            "Phase",
            "Correlation Phase",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis((-1), 4)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(0)


        labels = ["Phase", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            Vector_length,
            ((HI21 - samp_rate/2)/1e6),
            ((samp_rate/Vector_length)/1e6),
            "Frequency",
            "Magnitude",
            "Correlation Magnitude",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 250)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ["Magnitude", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.osmosdr_source_1_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'airspy=0x14212000,bias=0,pack=0'
        )
        self.osmosdr_source_1_0.set_clock_source('external', 0)
        self.osmosdr_source_1_0.set_time_source('external', 0)
        self.osmosdr_source_1_0.set_sample_rate(samp_rate)
        self.osmosdr_source_1_0.set_center_freq(HI21, 0)
        self.osmosdr_source_1_0.set_freq_corr(0, 0)
        self.osmosdr_source_1_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1_0.set_gain_mode(False, 0)
        self.osmosdr_source_1_0.set_gain(0, 0)
        self.osmosdr_source_1_0.set_if_gain(12, 0)
        self.osmosdr_source_1_0.set_bb_gain(12, 0)
        self.osmosdr_source_1_0.set_antenna('', 0)
        self.osmosdr_source_1_0.set_bandwidth(0, 0)
        self.osmosdr_source_1 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'airspy=0x14214000,bias=0,pack=0'
        )
        self.osmosdr_source_1.set_clock_source('external', 0)
        self.osmosdr_source_1.set_time_source('external', 0)
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(HI21, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(False, 0)
        self.osmosdr_source_1.set_gain(0, 0)
        self.osmosdr_source_1.set_if_gain(12, 0)
        self.osmosdr_source_1.set_bb_gain(12, 0)
        self.osmosdr_source_1.set_antenna('', 0)
        self.osmosdr_source_1.set_bandwidth(0, 0)
        self.fft_vxx_0_0 = fft.fft_vcc(Vector_length, True, window.hanning(Vector_length), True, 2)
        self.fft_vxx_0 = fft.fft_vcc(Vector_length, True, window.hanning(Vector_length), True, 2)
        self.blocks_multiply_conjugate_cc_0_0_0 = blocks.multiply_conjugate_cc(Vector_length)
        self.blocks_multiply_conjugate_cc_0_0 = blocks.multiply_conjugate_cc(Vector_length)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(Vector_length)
        self.blocks_integrate_xx_0_0_1 = blocks.integrate_cc((int(one_sec_display_integration*samp_rate/Vector_length)), Vector_length)
        self.blocks_integrate_xx_0_0_0 = blocks.integrate_cc((int(one_sec_display_integration*samp_rate/Vector_length)), Vector_length)
        self.blocks_integrate_xx_0_0 = blocks.integrate_cc((int(one_sec_display_integration*samp_rate/Vector_length)), Vector_length)
        self.blocks_complex_to_real_1_1 = blocks.complex_to_real(Vector_length)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(Vector_length)
        self.blocks_complex_to_magphase_0_0 = blocks.complex_to_magphase(Vector_length)
        self.PPFB_10tap_0_0 = PPFB_10tap(
            Vector_length=Vector_length,
        )
        self.PPFB_10tap_0 = PPFB_10tap(
            Vector_length=Vector_length,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.PPFB_10tap_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.PPFB_10tap_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_0, 1), (self.qtgui_vector_sink_f_0_0_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.qtgui_vector_sink_f_0_1, 0))
        self.connect((self.blocks_complex_to_real_1_1, 0), (self.qtgui_vector_sink_f_0_1_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_complex_to_magphase_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.blocks_integrate_xx_0_0_1, 0), (self.blocks_complex_to_real_1_1, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_0, 0), (self.blocks_integrate_xx_0_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_0_0, 0), (self.blocks_integrate_xx_0_0_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 1))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0_0, 1))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0_0, 0))
        self.connect((self.osmosdr_source_1, 0), (self.PPFB_10tap_0, 0))
        self.connect((self.osmosdr_source_1_0, 0), (self.PPFB_10tap_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Interferometry")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_Bandwidth(self.samp_rate)
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)
        self.osmosdr_source_1_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_1_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))

    def get_prefix_phase_int_time(self):
        return self.prefix_phase_int_time

    def set_prefix_phase_int_time(self, prefix_phase_int_time):
        self.prefix_phase_int_time = prefix_phase_int_time

    def get_prefix_phase_1_sec(self):
        return self.prefix_phase_1_sec

    def set_prefix_phase_1_sec(self, prefix_phase_1_sec):
        self.prefix_phase_1_sec = prefix_phase_1_sec

    def get_prefix_mag_int_time(self):
        return self.prefix_mag_int_time

    def set_prefix_mag_int_time(self, prefix_mag_int_time):
        self.prefix_mag_int_time = prefix_mag_int_time

    def get_prefix_mag_1_sec(self):
        return self.prefix_mag_1_sec

    def set_prefix_mag_1_sec(self, prefix_mag_1_sec):
        self.prefix_mag_1_sec = prefix_mag_1_sec

    def get_prefix_hornB_int_time(self):
        return self.prefix_hornB_int_time

    def set_prefix_hornB_int_time(self, prefix_hornB_int_time):
        self.prefix_hornB_int_time = prefix_hornB_int_time

    def get_prefix_hornB_1_sec(self):
        return self.prefix_hornB_1_sec

    def set_prefix_hornB_1_sec(self, prefix_hornB_1_sec):
        self.prefix_hornB_1_sec = prefix_hornB_1_sec

    def get_prefix_hornA_int_time(self):
        return self.prefix_hornA_int_time

    def set_prefix_hornA_int_time(self, prefix_hornA_int_time):
        self.prefix_hornA_int_time = prefix_hornA_int_time

    def get_prefix_hornA_1_sec(self):
        return self.prefix_hornA_1_sec

    def set_prefix_hornA_1_sec(self, prefix_hornA_1_sec):
        self.prefix_hornA_1_sec = prefix_hornA_1_sec

    def get_one_sec_display_integration(self):
        return self.one_sec_display_integration

    def set_one_sec_display_integration(self, one_sec_display_integration):
        self.one_sec_display_integration = one_sec_display_integration

    def get_int_time(self):
        return self.int_time

    def set_int_time(self, int_time):
        self.int_time = int_time

    def get_Vector_length(self):
        return self.Vector_length

    def set_Vector_length(self, Vector_length):
        self.Vector_length = Vector_length
        self.PPFB_10tap_0.set_Vector_length(self.Vector_length)
        self.PPFB_10tap_0_0.set_Vector_length(self.Vector_length)
        self.qtgui_vector_sink_f_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_1_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))

    def get_HI21(self):
        return self.HI21

    def set_HI21(self, HI21):
        self.HI21 = HI21
        self.osmosdr_source_1.set_center_freq(self.HI21, 0)
        self.osmosdr_source_1_0.set_center_freq(self.HI21, 0)
        self.qtgui_vector_sink_f_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))
        self.qtgui_vector_sink_f_0_1_0.set_x_axis(((self.HI21 - self.samp_rate/2)/1e6), ((self.samp_rate/self.Vector_length)/1e6))

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth




def main(top_block_cls=Interferometry, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
