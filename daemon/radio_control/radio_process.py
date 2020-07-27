#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: radio_process
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
import pmt
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import xmlrpc.server
import threading
from . import add_clock_tags
import math
import numpy as np
import osmosdr
import time


class radio_process(gr.top_block):

    def __init__(self, num_bins=4096, num_integrations=1000):
        gr.top_block.__init__(self, "radio_process")

        ##################################################
        # Parameters
        ##################################################
        self.num_bins = num_bins
        self.num_integrations = num_integrations

        ##################################################
        # Variables
        ##################################################
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/num_bins)
        self.fft_window = fft_window = window.blackmanharris(num_bins)
        self.window_power = window_power = sum([x*x for x in fft_window])
        self.sinc_samples = sinc_samples = np.sinc(sinc_sample_locations/np.pi)
        self.ref_scale = ref_scale = 2
        self.samp_rate = samp_rate = 2400000
        self.nlog_k = nlog_k = -20*math.log10(num_bins) -10*math.log10(float(window_power) / num_bins)-20*math.log10(float(ref_scale) / 2)
        self.motor_el = motor_el = np.nan
        self.motor_az = motor_az = np.nan
        self.is_running = is_running = False
        self.freq = freq = 1420000000
        self.custom_window = custom_window = sinc_samples*np.hamming(4*num_bins)

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_1_0 = zeromq.pub_sink(gr.sizeof_float, num_bins, 'tcp://127.0.0.1:5560', 100, False, -1)
        self.zeromq_pub_sink_1 = zeromq.pub_sink(gr.sizeof_float, num_bins, 'tcp://127.0.0.1:5561', 100, True, -1)
        self.zeromq_pub_sink_0_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5559', 100, False, -1)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5558', 100, True, -1)
        self.xmlrpc_server_0 = xmlrpc.server.SimpleXMLRPCServer(('localhost', 5557), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(1.0, num_bins)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + "soapy=0"
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.fft_vxx_0 = fft.fft_vcc(num_bins, True, fft_window, True, 3)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(num_bins, True)
        self.blocks_tags_strobe_0_0 = blocks.tags_strobe(gr.sizeof_gr_complex*1, pmt.to_pmt({"num_bins": num_bins, "samp_rate": samp_rate, "num_integrations": num_integrations, "motor_az": motor_az, "motor_el": motor_el, "freq": freq}), num_bins*4, pmt.intern("metadata"))
        self.blocks_tags_strobe_0 = blocks.tags_strobe(gr.sizeof_gr_complex*1, pmt.to_pmt(float(freq)), num_bins*4, pmt.intern("rx_freq"))
        self.blocks_stream_to_vector_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_bins)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_bins)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_bins)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_bins)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, num_bins, nlog_k)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff(1.0/float(num_integrations), num_bins)
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_vcc(custom_window[0:num_bins])
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vcc(custom_window[num_bins:2*num_bins])
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc(custom_window[2*num_bins:3*num_bins])
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc(custom_window[-num_bins:])
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.to_pmt(is_running), 100)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(num_integrations, num_bins)
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_gr_complex*1, num_bins)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, num_bins*2)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, num_bins*3)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(num_bins)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(num_bins)
        self.add_clock_tags = add_clock_tags.clk(nsamps=num_bins*4)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_selector_0, 'en'))
        self.connect((self.add_clock_tags, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_to_vector_0_2, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.zeromq_pub_sink_1, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.zeromq_pub_sink_1_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.zeromq_pub_sink_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_2, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.blocks_tags_strobe_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_tags_strobe_0_0, 0), (self.blocks_add_xx_0_0, 2))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_delay_0_1, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.add_clock_tags, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_integrate_xx_0, 0))


    def get_num_bins(self):
        return self.num_bins

    def set_num_bins(self, num_bins):
        self.num_bins = num_bins
        self.set_custom_window(self.sinc_samples*np.hamming(4*self.num_bins))
        self.set_fft_window(window.blackmanharris(self.num_bins))
        self.set_nlog_k(-20*math.log10(self.num_bins) -10*math.log10(float(self.window_power) / self.num_bins)-20*math.log10(float(self.ref_scale) / 2) )
        self.set_sinc_sample_locations(np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.num_bins))
        self.add_clock_tags.nsamps = self.num_bins*4
        self.blocks_delay_0.set_dly(self.num_bins*3)
        self.blocks_delay_0_0.set_dly(self.num_bins*2)
        self.blocks_delay_0_1.set_dly(self.num_bins)
        self.blocks_multiply_const_vxx_0.set_k(self.custom_window[-self.num_bins:])
        self.blocks_multiply_const_vxx_0_0.set_k(self.custom_window[2*self.num_bins:3*self.num_bins])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.custom_window[self.num_bins:2*self.num_bins])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.custom_window[0:self.num_bins])
        self.blocks_tags_strobe_0.set_nsamps(self.num_bins*4)
        self.blocks_tags_strobe_0_0.set_value(pmt.to_pmt({"num_bins": self.num_bins, "samp_rate": self.samp_rate, "num_integrations": self.num_integrations, "motor_az": self.motor_az, "motor_el": self.motor_el, "freq": self.freq}))
        self.blocks_tags_strobe_0_0.set_nsamps(self.num_bins*4)

    def get_num_integrations(self):
        return self.num_integrations

    def set_num_integrations(self, num_integrations):
        self.num_integrations = num_integrations
        self.blocks_multiply_const_xx_0.set_k(1.0/float(self.num_integrations))
        self.blocks_tags_strobe_0_0.set_value(pmt.to_pmt({"num_bins": self.num_bins, "samp_rate": self.samp_rate, "num_integrations": self.num_integrations, "motor_az": self.motor_az, "motor_el": self.motor_el, "freq": self.freq}))

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc_samples(np.sinc(self.sinc_sample_locations/np.pi))

    def get_fft_window(self):
        return self.fft_window

    def set_fft_window(self, fft_window):
        self.fft_window = fft_window
        self.set_window_power(sum([x*x for x in self.fft_window]))

    def get_window_power(self):
        return self.window_power

    def set_window_power(self, window_power):
        self.window_power = window_power
        self.set_nlog_k(-20*math.log10(self.num_bins) -10*math.log10(float(self.window_power) / self.num_bins)-20*math.log10(float(self.ref_scale) / 2) )

    def get_sinc_samples(self):
        return self.sinc_samples

    def set_sinc_samples(self, sinc_samples):
        self.sinc_samples = sinc_samples
        self.set_custom_window(self.sinc_samples*np.hamming(4*self.num_bins))

    def get_ref_scale(self):
        return self.ref_scale

    def set_ref_scale(self, ref_scale):
        self.ref_scale = ref_scale
        self.set_nlog_k(-20*math.log10(self.num_bins) -10*math.log10(float(self.window_power) / self.num_bins)-20*math.log10(float(self.ref_scale) / 2) )

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_tags_strobe_0_0.set_value(pmt.to_pmt({"num_bins": self.num_bins, "samp_rate": self.samp_rate, "num_integrations": self.num_integrations, "motor_az": self.motor_az, "motor_el": self.motor_el, "freq": self.freq}))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_nlog_k(self):
        return self.nlog_k

    def set_nlog_k(self, nlog_k):
        self.nlog_k = nlog_k

    def get_motor_el(self):
        return self.motor_el

    def set_motor_el(self, motor_el):
        self.motor_el = motor_el
        self.blocks_tags_strobe_0_0.set_value(pmt.to_pmt({"num_bins": self.num_bins, "samp_rate": self.samp_rate, "num_integrations": self.num_integrations, "motor_az": self.motor_az, "motor_el": self.motor_el, "freq": self.freq}))

    def get_motor_az(self):
        return self.motor_az

    def set_motor_az(self, motor_az):
        self.motor_az = motor_az
        self.blocks_tags_strobe_0_0.set_value(pmt.to_pmt({"num_bins": self.num_bins, "samp_rate": self.samp_rate, "num_integrations": self.num_integrations, "motor_az": self.motor_az, "motor_el": self.motor_el, "freq": self.freq}))

    def get_is_running(self):
        return self.is_running

    def set_is_running(self, is_running):
        self.is_running = is_running
        self.blocks_message_strobe_0.set_msg(pmt.to_pmt(self.is_running))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.blocks_tags_strobe_0.set_value(pmt.to_pmt(float(self.freq)))
        self.blocks_tags_strobe_0_0.set_value(pmt.to_pmt({"num_bins": self.num_bins, "samp_rate": self.samp_rate, "num_integrations": self.num_integrations, "motor_az": self.motor_az, "motor_el": self.motor_el, "freq": self.freq}))
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window
        self.blocks_multiply_const_vxx_0.set_k(self.custom_window[-self.num_bins:])
        self.blocks_multiply_const_vxx_0_0.set_k(self.custom_window[2*self.num_bins:3*self.num_bins])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.custom_window[self.num_bins:2*self.num_bins])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.custom_window[0:self.num_bins])




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--num-bins", dest="num_bins", type=intx, default=4096,
        help="Set num_bins [default=%(default)r]")
    parser.add_argument(
        "--num-integrations", dest="num_integrations", type=intx, default=1000,
        help="Set num_integrations [default=%(default)r]")
    return parser


def main(top_block_cls=radio_process, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(num_bins=options.num_bins, num_integrations=options.num_integrations)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()