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
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import pdu
import math
import satellites.components.deframers
import satellites.components.demodulators
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
        self.TX_GS_PORT = TX_GS_PORT = 2000
        self.RX_GS_PORT = RX_GS_PORT = 2001
        self.OBC_TX_PORT = OBC_TX_PORT = 2002
        self.OBC_RX_PORT = OBC_RX_PORT = 2003

        ##################################################
        # Blocks
        ##################################################

        self.satellites_fsk_demodulator_0_0 = satellites.components.demodulators.fsk_demodulator(baudrate = baud_rate, samp_rate = baud_rate*2, iq = True, subaudio = False, options="--deviation 2400 --use_agc")
        self.satellites_fsk_demodulator_0 = satellites.components.demodulators.fsk_demodulator(baudrate = baud_rate, samp_rate = baud_rate*2, iq = True, subaudio = False, options="--deviation 2400 --use_agc")
        self.satellites_endurosat_deframer_0_0 = satellites.components.deframers.endurosat_deframer(syncword_threshold=0, options="")
        self.satellites_endurosat_deframer_0 = satellites.components.deframers.endurosat_deframer(syncword_threshold=0, options="")
        self.qtgui_waterfall_sink_x_2_0 = qtgui.waterfall_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            435e6, #fc
            samp_rate, #bw
            "FINAL", #name
            0, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_2_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_2_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_2_0.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_2_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_2_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_2_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_2_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_2_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_2_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_2_0_win)
        self.qtgui_waterfall_sink_x_2 = qtgui.waterfall_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            435e6, #fc
            samp_rate, #bw
            "FINAL", #name
            0, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_2.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_2.enable_grid(False)
        self.qtgui_waterfall_sink_x_2.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_2.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_2.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_2.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_2.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_2_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_2.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_2_win)
        self.qtgui_waterfall_sink_x_0_1 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_1.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_1_win)
        self.qtgui_waterfall_sink_x_0_0_1 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            435e6, #fc
            samp_rate, #bw
            "RAW RF INPUT", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_1.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_1_win)
        self.qtgui_waterfall_sink_x_0_0_0_0 = qtgui.waterfall_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            435e6, #fc
            samp_rate, #bw
            "Demod", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_0_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_win)
        self.qtgui_waterfall_sink_x_0_0_0 = qtgui.waterfall_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            435e6, #fc
            samp_rate, #bw
            "Demod", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_0_win)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            435e6, #fc
            samp_rate, #bw
            "RAW RF INPUT", #name
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
        self.pdu_pdu_to_stream_x_0_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_BALK, 64)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_BALK, 64)
        self.network_socket_pdu_1 = network.socket_pdu('UDP_CLIENT', "127.0.0.2", '2001', 10000, False)
        self.network_socket_pdu_0_1 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '2003', 10000, False)
        self.network_socket_pdu_0_0_0 = network.socket_pdu('UDP_SERVER', '127.0.0.1', '2002', 1200, False)
        self.network_socket_pdu_0 = network.socket_pdu('UDP_SERVER', "127.0.0.2", '2000', 10000, False)
        self.digital_symbol_sync_xx_0_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            (samp_rate/baud_rate),
            0.045,
            1.0,
            1.0,
            1.5,
            2,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            (samp_rate/baud_rate),
            0.045,
            1.0,
            1.0,
            1.5,
            2,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
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
        self.channels_channel_model_0_0 = channels.channel_model(
            noise_voltage=0.1,
            frequency_offset=0,
            epsilon=1.0005,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.1,
            frequency_offset=0,
            epsilon=1.0005,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
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
        self.msg_connect((self.satellites_endurosat_deframer_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_endurosat_deframer_0, 'out'), (self.network_socket_pdu_0_1, 'pdus'))
        self.msg_connect((self.satellites_endurosat_deframer_0, 'out'), (self.qtgui_waterfall_sink_x_2, 'in'))
        self.msg_connect((self.satellites_endurosat_deframer_0_0, 'out'), (self.blocks_message_debug_0_0_0, 'print_pdu'))
        self.msg_connect((self.satellites_endurosat_deframer_0_0, 'out'), (self.network_socket_pdu_1, 'pdus'))
        self.msg_connect((self.satellites_endurosat_deframer_0_0, 'out'), (self.qtgui_waterfall_sink_x_2_0, 'in'))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.digital_symbol_sync_xx_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.qtgui_waterfall_sink_x_0_0_1, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.digital_gfsk_mod_0_0, 0), (self.channels_channel_model_0_0, 0))
        self.connect((self.digital_gfsk_mod_0_0, 0), (self.qtgui_waterfall_sink_x_0_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.satellites_fsk_demodulator_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0, 0), (self.satellites_fsk_demodulator_0_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0_0, 0), (self.digital_gfsk_mod_0_0, 0))
        self.connect((self.satellites_fsk_demodulator_0, 0), (self.qtgui_waterfall_sink_x_0_0_0, 0))
        self.connect((self.satellites_fsk_demodulator_0, 0), (self.satellites_endurosat_deframer_0, 0))
        self.connect((self.satellites_fsk_demodulator_0_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0, 0))
        self.connect((self.satellites_fsk_demodulator_0_0, 0), (self.satellites_endurosat_deframer_0_0, 0))


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
        self.digital_symbol_sync_xx_0.set_sps((self.samp_rate/self.baud_rate))
        self.digital_symbol_sync_xx_0_0.set_sps((self.samp_rate/self.baud_rate))

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
        self.digital_symbol_sync_xx_0.set_sps((self.samp_rate/self.baud_rate))
        self.digital_symbol_sync_xx_0_0.set_sps((self.samp_rate/self.baud_rate))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(435e6, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(435e6, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(435e6, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0_1.set_frequency_range(435e6, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_2.set_frequency_range(435e6, self.samp_rate)
        self.qtgui_waterfall_sink_x_2_0.set_frequency_range(435e6, self.samp_rate)

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
