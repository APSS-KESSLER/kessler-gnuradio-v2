#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tx
# Author: Orb Ops APSS
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
from gnuradio import pdu
import math
import satellites.hier
import sip
import threading



class transmission_prototype(gr.top_block, Qt.QWidget):

    def __init__(self, baud_rate=9600):
        gr.top_block.__init__(self, "Tx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tx")
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
        self.loop_bandwidth = loop_bandwidth = 0.045
        self.TX_GS_PORT = TX_GS_PORT = 2000
        self.RX_GS_PORT = RX_GS_PORT = 2001
        self.OBC_TX_PORT = OBC_TX_PORT = 2002
        self.OBC_RX_PORT = OBC_RX_PORT = 2003

        ##################################################
        # Blocks
        ##################################################

        self.satellites_sync_to_pdu_packed_0 = satellites.hier.sync_to_pdu_packed(
            packlen=43,
            sync="1010101001111110",
            threshold=0,
        )
        self.qtgui_time_sink_x_0_1_1_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "After Correlation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_1_0.enable_tags(True)
        self.qtgui_time_sink_x_0_1_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_1_0.enable_grid(False)
        self.qtgui_time_sink_x_0_1_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_1_0.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0_1_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_1_1_0_win)
        self.qtgui_time_sink_x_0_1_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "After Demod", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_1.enable_tags(True)
        self.qtgui_time_sink_x_0_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_1.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_1_1_win)
        self.pdu_tagged_stream_to_pdu_0_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_stream_x_0_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_BALK, 64)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_BALK, 64)
        self.network_socket_pdu_1 = network.socket_pdu('UDP_CLIENT', "127.0.0.2", '2001', 10000, False)
        self.network_socket_pdu_0_1 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '2003', 10000, False)
        self.network_socket_pdu_0_0_0 = network.socket_pdu('UDP_SERVER', '127.0.0.1', '2002', 1200, False)
        self.network_socket_pdu_0 = network.socket_pdu('UDP_SERVER', "127.0.0.2", '2000', 10000, False)
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _loop_bandwidth_dial_control = qtgui.GrDialControl('Loop Bandwidth', self, 0,0.1,0.045,"default",self.set_loop_bandwidth,isFloat, scaleFactor, 100, False, "'value'")
        self.loop_bandwidth = _loop_bandwidth_dial_control

        self.top_layout.addWidget(_loop_bandwidth_dial_control)
        self.digital_gfsk_mod_0_0 = digital.gfsk_mod(
            samples_per_symbol=(int(samp_rate // baud_rate)),
            sensitivity=sensitivity,
            bt=0.35,
            verbose=False,
            log=False,
            do_unpack=True)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=(int(samp_rate // baud_rate)),
            sensitivity=sensitivity,
            bt=0.35,
            verbose=False,
            log=False,
            do_unpack=True)
        self.digital_gfsk_demod_0_1_0 = digital.gfsk_demod(
            samples_per_symbol=2,
            sensitivity=1.0,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,
            log=False)
        self.digital_gfsk_demod_0_1 = digital.gfsk_demod(
            samples_per_symbol=208,
            sensitivity=sensitivity,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,
            log=True)
        self.digital_correlate_access_code_tag_xx_0 = digital.correlate_access_code_tag_bb('1010101001111110', 0, 'preamble + syncword')
        self.channels_channel_model_0_0 = channels.channel_model(
            noise_voltage=0.1,
            frequency_offset=0,
            epsilon=1.0005,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.blocks_uchar_to_float_0_1_0_1_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0_1_0_1 = blocks.uchar_to_float()
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_message_debug_0_1 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_0_0_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_0_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.network_socket_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.network_socket_pdu_0, 'pdus'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.msg_connect((self.network_socket_pdu_0_0_0, 'pdus'), (self.blocks_message_debug_0_1, 'print_pdu'))
        self.msg_connect((self.network_socket_pdu_0_0_0, 'pdus'), (self.pdu_pdu_to_stream_x_0_0, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0_0, 'pdus'), (self.blocks_message_debug_0_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_sync_to_pdu_packed_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_sync_to_pdu_packed_0, 'out'), (self.network_socket_pdu_0_1, 'pdus'))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_gfsk_demod_0_1, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.digital_gfsk_demod_0_1_0, 0))
        self.connect((self.blocks_uchar_to_float_0_1_0_1, 0), (self.qtgui_time_sink_x_0_1_1, 0))
        self.connect((self.blocks_uchar_to_float_0_1_0_1_0, 0), (self.qtgui_time_sink_x_0_1_1_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.blocks_uchar_to_float_0_1_0_1_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.satellites_sync_to_pdu_packed_0, 0))
        self.connect((self.digital_gfsk_demod_0_1, 0), (self.blocks_uchar_to_float_0_1_0_1, 0))
        self.connect((self.digital_gfsk_demod_0_1, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.digital_gfsk_demod_0_1_0, 0), (self.pdu_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.digital_gfsk_mod_0_0, 0), (self.channels_channel_model_0_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0_0, 0), (self.digital_gfsk_mod_0_0, 0))


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
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1_1_0.set_samp_rate(self.samp_rate)

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

    def get_loop_bandwidth(self):
        return self.loop_bandwidth

    def set_loop_bandwidth(self, loop_bandwidth):
        self.loop_bandwidth = loop_bandwidth

    def get_TX_GS_PORT(self):
        return self.TX_GS_PORT

    def set_TX_GS_PORT(self, TX_GS_PORT):
        self.TX_GS_PORT = TX_GS_PORT

    def get_RX_GS_PORT(self):
        return self.RX_GS_PORT

    def set_RX_GS_PORT(self, RX_GS_PORT):
        self.RX_GS_PORT = RX_GS_PORT

    def get_OBC_TX_PORT(self):
        return self.OBC_TX_PORT

    def set_OBC_TX_PORT(self, OBC_TX_PORT):
        self.OBC_TX_PORT = OBC_TX_PORT

    def get_OBC_RX_PORT(self):
        return self.OBC_RX_PORT

    def set_OBC_RX_PORT(self, OBC_RX_PORT):
        self.OBC_RX_PORT = OBC_RX_PORT



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
