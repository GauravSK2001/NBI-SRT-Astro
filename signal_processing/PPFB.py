#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import numpy as np
import osmosdr
import time
import sip



class PPFB(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "PPFB")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.Vector_length = Vector_length = 2**13
        self.Taps = Taps = 10
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*Taps/2.0, np.pi*Taps/2.0, np.pi/Vector_length)
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.samp_rate = samp_rate = 6e6
        self.one_sec_display_integration = one_sec_display_integration = 1
        self.int_time = int_time = (60*5)
        self.Window = Window = sinc
        self.PFB_bandwidth_vector_length = PFB_bandwidth_vector_length = 7e3
        self.HI21 = HI21 = 1420.405751768e6
        self.Frequency_Step_Size = Frequency_Step_Size = samp_rate/Vector_length
        self.Bandwidth = Bandwidth = samp_rate

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_tab_widget = Qt.QTabWidget()
        self.qtgui_tab_widget_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_widget_0)
        self.qtgui_tab_widget_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_layout_0.addLayout(self.qtgui_tab_widget_grid_layout_0)
        self.qtgui_tab_widget.addTab(self.qtgui_tab_widget_widget_0, 'Spectrum')
        self.top_layout.addWidget(self.qtgui_tab_widget)
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
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            Vector_length,
            ((HI21-samp_rate/2)/1e6),
            ((Frequency_Step_Size)/1e6),
            "Frequency [MHz]",
            "Power",
            "Power Spectrum",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis(0, 10)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(0)


        labels = ['ztomag2', 'Multiply conjugate', 'just mag', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
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
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            Vector_length,
            ((HI21-samp_rate/2)/1e6),
            ((Frequency_Step_Size)/1e6),
            "Frequency [MHz]",
            "Power log",
            "Power Spectrum",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis(0, 10)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


        labels = ['ztomag2', 'Multiply conjugate', 'just mag', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            Vector_length, #size
            window.WIN_FLATTOP, #wintype
            HI21, #fc
            samp_rate, #bw
            "Direct", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
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
        self.fft_vxx_0 = fft.fft_vcc(Vector_length, True, window.hanning(Vector_length), True, 6)
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
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff((int(one_sec_display_integration*samp_rate/Vector_length)), Vector_length)
        self.blocks_integrate_xx_0 = blocks.integrate_ff((int(int_time*samp_rate/Vector_length)), Vector_length)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*Vector_length, '/Users/gauravsenthilkumar/Desktop/Radio_tests/m1', False)
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
        self.blocks_complex_to_mag_squared_1 = blocks.complex_to_mag_squared(Vector_length)
        self.blocks_add_xx_0 = blocks.add_vcc(Vector_length)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.blocks_integrate_xx_0_0, 0))
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
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.qtgui_vector_sink_f_0_0_0, 0))
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
        self.connect((self.blocks_nlog10_ff_1_0, 0), (self.qtgui_vector_sink_f_0_0, 0))
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
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_1, 0))
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
        self.connect((self.osmosdr_source_1, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "PPFB")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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
        self.qtgui_freq_sink_x_0.set_frequency_range(self.HI21, self.samp_rate)
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.HI21-self.samp_rate/2)/1e6), ((self.Frequency_Step_Size)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.HI21-self.samp_rate/2)/1e6), ((self.Frequency_Step_Size)/1e6))

    def get_one_sec_display_integration(self):
        return self.one_sec_display_integration

    def set_one_sec_display_integration(self, one_sec_display_integration):
        self.one_sec_display_integration = one_sec_display_integration

    def get_int_time(self):
        return self.int_time

    def set_int_time(self, int_time):
        self.int_time = int_time
        Qt.QMetaObject.invokeMethod(self._int_time_line_edit, "setText", Qt.Q_ARG("QString", str(self.int_time)))

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
        self.qtgui_freq_sink_x_0.set_frequency_range(self.HI21, self.samp_rate)
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.HI21-self.samp_rate/2)/1e6), ((self.Frequency_Step_Size)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.HI21-self.samp_rate/2)/1e6), ((self.Frequency_Step_Size)/1e6))

    def get_Frequency_Step_Size(self):
        return self.Frequency_Step_Size

    def set_Frequency_Step_Size(self, Frequency_Step_Size):
        self.Frequency_Step_Size = Frequency_Step_Size
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.HI21-self.samp_rate/2)/1e6), ((self.Frequency_Step_Size)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.HI21-self.samp_rate/2)/1e6), ((self.Frequency_Step_Size)/1e6))

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth




def main(top_block_cls=PPFB, options=None):

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
