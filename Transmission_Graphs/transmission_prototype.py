#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: Lenovo
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import pdu
from gnuradio import soapy
import math
import sip
import threading



class transmission_prototype(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "transmission_prototype")

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
        self.samp_rate = samp_rate = 2e6
        self.freq_deviation = freq_deviation = (mod_index * baud_rate) / 2
        self.sensitivity = sensitivity = (2 * math.pi * freq_deviation) / samp_rate
        self.num_preamble_aa = num_preamble_aa = 5

        ##################################################
        # Blocks
        ##################################################

        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, 435e6)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(30, 0.0), 47.0))
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
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
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_BALK, 64)
        self.network_socket_pdu_0_0 = network.socket_pdu('UDP_SERVER', '127.0.0.1', '2000', 1200, False)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=(int(samp_rate // baud_rate)),
            sensitivity=sensitivity,
            bt=0.35,
            verbose=False,
            log=False,
            do_unpack=True)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.network_socket_pdu_0_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.network_socket_pdu_0_0, 'pdus'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.connect((self.digital_gfsk_mod_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.digital_gfsk_mod_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "transmission_prototype")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_freq_deviation((self.mod_index * self.baud_rate) / 2)

    def get_mod_index(self):
        return self.mod_index

    def set_mod_index(self, mod_index):
        self.mod_index = mod_index
        self.set_freq_deviation((self.mod_index * self.baud_rate) / 2)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sensitivity((2 * math.pi * self.freq_deviation) / self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate)

    def get_freq_deviation(self):
        return self.freq_deviation

    def set_freq_deviation(self, freq_deviation):
        self.freq_deviation = freq_deviation
        self.set_sensitivity((2 * math.pi * self.freq_deviation) / self.samp_rate)

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def get_num_preamble_aa(self):
        return self.num_preamble_aa

    def set_num_preamble_aa(self, num_preamble_aa):
        self.num_preamble_aa = num_preamble_aa



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--baud-rate", dest="baud_rate", type=eng_float, default=eng_notation.num_to_str(float(9600)),
        help="Set baud_rate [default=%(default)r]")
    return parser


def main(top_block_cls=transmission_prototype, options=None):
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
