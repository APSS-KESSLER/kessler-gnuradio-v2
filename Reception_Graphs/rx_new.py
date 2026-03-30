#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import soapy
import satellites.components.deframers
import sip
import threading



class rx_new(gr.top_block, Qt.QWidget):

    def __init__(self, baud_rate=9600):
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "rx_new")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Parameters
        ##################################################
        self.baud_rate = baud_rate

        ##################################################
        # Variables
        ##################################################
        self.mod_index = mod_index = 0.5
        self.variable_qtgui_range_1 = variable_qtgui_range_1 = 50
        self.samp_rate = samp_rate = 2e6
        self.rx_offset = rx_offset = 1000
        self.frequency_correction = frequency_correction = 10
        self.freq_deviation = freq_deviation = (mod_index * baud_rate) / 2
        self.Decimation = Decimation = 5

        ##################################################
        # Blocks
        ##################################################

        self._frequency_correction_range = qtgui.Range(0, 100, 1, 10, 200)
        self._frequency_correction_win = qtgui.RangeWidget(self._frequency_correction_range, self.set_frequency_correction, "frequency correction", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._frequency_correction_win)
        self._variable_qtgui_range_1_range = qtgui.Range(0, 100, 1, 50, 200)
        self._variable_qtgui_range_1_win = qtgui.RangeWidget(self._variable_qtgui_range_1_range, self.set_variable_qtgui_range_1, "'variable_qtgui_range_1'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._variable_qtgui_range_1_win)
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = 'bufflen=16384'
        tune_args = ['']
        settings = ['']

        def _set_soapy_rtlsdr_source_0_gain_mode(channel, agc):
            self.soapy_rtlsdr_source_0.set_gain_mode(channel, agc)
            if not agc:
                  self.soapy_rtlsdr_source_0.set_gain(channel, self._soapy_rtlsdr_source_0_gain_value)
        self.set_soapy_rtlsdr_source_0_gain_mode = _set_soapy_rtlsdr_source_0_gain_mode

        def _set_soapy_rtlsdr_source_0_gain(channel, name, gain):
            self._soapy_rtlsdr_source_0_gain_value = gain
            if not self.soapy_rtlsdr_source_0.get_gain_mode(channel):
                self.soapy_rtlsdr_source_0.set_gain(channel, gain)
        self.set_soapy_rtlsdr_source_0_gain = _set_soapy_rtlsdr_source_0_gain

        def _set_soapy_rtlsdr_source_0_bias(bias):
            if 'biastee' in self._soapy_rtlsdr_source_0_setting_keys:
                self.soapy_rtlsdr_source_0.write_setting('biastee', bias)
        self.set_soapy_rtlsdr_source_0_bias = _set_soapy_rtlsdr_source_0_bias

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)

        self._soapy_rtlsdr_source_0_setting_keys = [a.key for a in self.soapy_rtlsdr_source_0.get_setting_info()]

        self.soapy_rtlsdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_rtlsdr_source_0.set_frequency(0, 435e6)
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, frequency_correction)
        self.set_soapy_rtlsdr_source_0_bias(bool(False))
        self._soapy_rtlsdr_source_0_gain_value = 20
        self.set_soapy_rtlsdr_source_0_gain_mode(0, bool(False))
        self.set_soapy_rtlsdr_source_0_gain(0, 'TUNER', 20)
        self.satellites_endurosat_deframer_1_0 = satellites.components.deframers.endurosat_deframer(syncword_threshold=0, options="")
        self.qtgui_waterfall_sink_x_0_1_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Noise and stuff", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_1_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_1_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_1_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_1_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_1_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_1_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_1_0_win)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Low Pass output", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "X-Lating FIR output", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_2_1_0_1 = qtgui.time_sink_f(
            1024, #size
            baud_rate, #samp_rate
            "Symbol Sync Output", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_1_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_2_1_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2_1_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_1_0_1.enable_tags(True)
        self.qtgui_time_sink_x_2_1_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_1_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_2_1_0_1.enable_grid(False)
        self.qtgui_time_sink_x_2_1_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_1_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_2_1_0_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_1_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_1_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_1_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_1_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_1_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_1_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_1_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_1_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_2_1_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_1_0_1_win)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "FSK Demod Output", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(True)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.network_socket_pdu_0_1 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '2003', 10000, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(Decimation, firdes.low_pass(1,samp_rate,samp_rate/(2*Decimation), 1000), rx_offset, samp_rate)
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(1, firdes.low_pass(1, (samp_rate // Decimation), (freq_deviation*5), 1e3, window.WIN_RECTANGULAR, 6.76), 1)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_EARLY_LATE,
            (((samp_rate // Decimation) // baud_rate)),
            0.1,
            1.0,
            0.1,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.blocks_message_debug_0_0 = blocks.message_debug(True, gr.log_levels.info)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(((samp_rate//Decimation)/(2*math.pi*freq_deviation)))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_endurosat_deframer_1_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_endurosat_deframer_1_0, 'out'), (self.network_socket_pdu_0_1, 'pdus'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_time_sink_x_2_1_0_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.satellites_endurosat_deframer_1_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "rx_new")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_freq_deviation((self.mod_index * self.baud_rate) / 2)
        self.digital_symbol_sync_xx_0.set_sps((((self.samp_rate // self.Decimation) // self.baud_rate)))
        self.qtgui_time_sink_x_2_1_0_1.set_samp_rate(self.baud_rate)

    def get_mod_index(self):
        return self.mod_index

    def set_mod_index(self, mod_index):
        self.mod_index = mod_index
        self.set_freq_deviation((self.mod_index * self.baud_rate) / 2)

    def get_variable_qtgui_range_1(self):
        return self.variable_qtgui_range_1

    def set_variable_qtgui_range_1(self, variable_qtgui_range_1):
        self.variable_qtgui_range_1 = variable_qtgui_range_1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_quadrature_demod_cf_0.set_gain(((self.samp_rate//self.Decimation)/(2*math.pi*self.freq_deviation)))
        self.digital_symbol_sync_xx_0.set_sps((((self.samp_rate // self.Decimation) // self.baud_rate)))
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate // self.Decimation), (self.freq_deviation*5), 1e3, window.WIN_RECTANGULAR, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.Decimation), 1000))
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_1_0.set_frequency_range(0, self.samp_rate)
        self.soapy_rtlsdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_rx_offset(self):
        return self.rx_offset

    def set_rx_offset(self, rx_offset):
        self.rx_offset = rx_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.rx_offset)

    def get_frequency_correction(self):
        return self.frequency_correction

    def set_frequency_correction(self, frequency_correction):
        self.frequency_correction = frequency_correction
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, self.frequency_correction)

    def get_freq_deviation(self):
        return self.freq_deviation

    def set_freq_deviation(self, freq_deviation):
        self.freq_deviation = freq_deviation
        self.analog_quadrature_demod_cf_0.set_gain(((self.samp_rate//self.Decimation)/(2*math.pi*self.freq_deviation)))
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate // self.Decimation), (self.freq_deviation*5), 1e3, window.WIN_RECTANGULAR, 6.76))

    def get_Decimation(self):
        return self.Decimation

    def set_Decimation(self, Decimation):
        self.Decimation = Decimation
        self.analog_quadrature_demod_cf_0.set_gain(((self.samp_rate//self.Decimation)/(2*math.pi*self.freq_deviation)))
        self.digital_symbol_sync_xx_0.set_sps((((self.samp_rate // self.Decimation) // self.baud_rate)))
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate // self.Decimation), (self.freq_deviation*5), 1e3, window.WIN_RECTANGULAR, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.Decimation), 1000))



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--baud-rate", dest="baud_rate", type=eng_float, default=eng_notation.num_to_str(float(9600)),
        help="Set baud_rate [default=%(default)r]")
    return parser


def main(top_block_cls=rx_new, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(baud_rate=options.baud_rate)

    tb.start()
    tb.flowgraph_started.set()

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
